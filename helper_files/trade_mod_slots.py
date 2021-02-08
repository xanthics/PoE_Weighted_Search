import requests
import json
import os
from ratelimit import limits, sleep_and_retry
from helper_files.goodmod import goodmod
from helper_files.badmod import badmod
from modlist import mods
from time import sleep
from datetime import datetime


# 3:5:60
@sleep_and_retry
@limits(calls=2, period=10)
def post_api(requester, data, headers, cookies):
	print('post request')
	post_url = 'https://www.pathofexile.com/api/trade/search/Ritual'
	req = requester.post(post_url, cookies=cookies, headers=headers, json=data)
	if req.status_code == 429:
		raise ConnectionError("Post throttle error")
	if req.status_code != 200:
		raise Exception('(post) API response: {}'.format(req.status_code))
	return req.json()


# 6:4:10
@sleep_and_retry
@limits(calls=3, period=4)
def fetch_api(requester, url, headers, cookies):
	print('fetch request')
	req = requester.get(url, cookies=cookies, headers=headers)
	if req.status_code == 429:
		raise ConnectionError("fetch throttle error")
	if req.status_code != 200:
		raise Exception('(fetch) API response: {}'.format(req.status_code))
	return req.json()


# given a list of mods to check and a list of known mods, eliminate possibly bad mods
def gen_mod_map(themods, goodmods, cookies, headers):
	mod_count = 150  # number of mods to check at a time
	fetch_url = 'https://www.pathofexile.com/api/trade/fetch/{}?query={}'
	requester = requests.session()
	for base in themods:
		print(f"Gathering for: {base}")
		if base not in goodmods:
			goodmods[base] = []
		while themods[base]:
			print(f"Remaining ({base}): {len(themods[base])}")
			root_request = {"query": {"status": {"option": "any"}, "stats": [{"type": "count", "filters": [{'id': x} for x in themods[base][:mod_count]], "value": {"min": 1}}], "filters": {"type_filters": {"filters": {"category": {"option": base}, "rarity": {"option": "nonunique"}}}}}, "sort": {"price": "asc"}}
			while True:
				try:
					var = post_api(requester, root_request, headers, cookies)
					break
				except ConnectionError as e:
					sleep(66)
					print(e)
			if var['result']:
				idx = 0
				thelen = 0
				print(f"fetching: {var['id']}")
				while idx < len(var['result']) and idx < min(100, mod_count):
					while True:
						try:
							var2 = fetch_api(requester, fetch_url.format(','.join(var['result'][idx:idx + 10]), var['id']), headers, cookies)
							break
						except ConnectionError as e:
							sleep(11)
							print(e)
					idx += 10
					for res in var2['result']:
						for affix in res['item']['extended']['hashes']:
							new_mods = [x[0] for x in res['item']['extended']['hashes'][affix] if x[0] in themods[base] and x[0] not in goodmods[base]]
							if not thelen:
								thelen += len(new_mods)
							for x in new_mods:
								del themods[base][themods[base].index(x)]
							goodmods[base].extend(new_mods)
				# so we don't get stuck in a loop when the only result has fractured crafting mods that can't be explicits
				if not thelen:
					print("Fractured crafting mod that matches explicit as only result.")
					themods[base] = themods[base][mod_count:]
			else:
				print("No results", var)
				themods[base] = themods[base][mod_count:]
			with open('modmap.json', 'w') as f:
				json.dump(goodmods, f)
		with open('modmap.json', 'w') as f:
			json.dump(goodmods, f)
	requester.close()


def gen_restrict_mods(goodmods, root_dir):
	# table to get the correct trade site json name
	lookup_bases = {
		'jewel': "All Jewel",
		'jewel.base': "Base Jewel",
		'jewel.abyss': "Abyss Jewel",
		'weapon': "Caster Weapon",
		'weapon.wand': "Wand (Spellslinger)",
		'accessory.amulet': "Amulet",
		'accessory.ring': "Ring",
		'accessory.belt': "Belt",
		'armour.quiver': "Quiver",
		'armour.shield': "Shield",
		'armour.gloves': "Gloves",
		'armour.helmet': "Helmet",
		'armour.chest': "Body Armour",
		'armour.boots': "Boots",
	}
	# reverse lookup to map mod hashes to human readable
	rlookup = {mods[x][idx]: x for x in mods for idx in range(len(mods[x]))}
	results = {}
	for base in goodmods:
		results[lookup_bases[base]] = {'implicit': [], 'crafted': [], 'explicit': []}
		for m in goodmods[base]:
			name = rlookup[m]
			results[lookup_bases[base]][m.split('.')[0]].append(name)
	# Add mods for specific uniques that are being considered.
	missing_mods = {
		'Ring': {
			'explicit': [
				# Precursor Emblem
				"# to # Cold Damage per Frenzy Charge",
				"#% increased Critical Strike Chance per Frenzy Charge",
				"#% increased Damage per Frenzy Charge",
				"Gain #% of Cold Damage as Extra Chaos Damage per Frenzy Charge",
				"# to # Fire Damage per Endurance Charge",
				"#% increased Attack and Cast Speed per Endurance Charge",
				"#% increased Critical Strike Chance per Endurance Charge",
				"#% increased Damage per Endurance Charge",
				"Gain #% of Fire Damage as Extra Chaos Damage per Endurance Charge",
				"# to # Lightning Damage per Power Charge",
				"#% increased Attack and Cast Speed per Power Charge",
				"#% increased Damage per Power Charge",
				"#% increased Spell Damage per Power Charge",
				"#% to Critical Strike Multiplier per Power Charge",
				"Gain #% of Lightning Damage as Extra Chaos Damage per Power Charge"
			]
		},
	}
	for slot in missing_mods:
		for gen_type in missing_mods[slot]:
			results[slot][gen_type].extend(missing_mods[slot][gen_type])

	# Add a special section for all jewel mods
	results['All Jewel'] = {'implicit': list(set(results['Base Jewel']['implicit'] + results['Abyss Jewel']['implicit'])),
							'crafted': list(set(results['Base Jewel']['crafted'] + results['Abyss Jewel']['crafted'])),
							'explicit': list(set(results['Base Jewel']['explicit'] + results['Abyss Jewel']['explicit']))}

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'r_mods = {']
	for base in sorted(results):
		buf.append(f'\t"{base}": {{')
		for section in results[base]:
			results[base][section].sort()
			if results[base][section]:
				tblstr = '",\n\t\t\t"'.join(results[base][section])
			else:
				tblstr = ''
			buf.append(f'\t\t"{section}": [\n\t\t\t"{tblstr}"\n\t\t],')
		buf.append('\t},')
	buf.append('}\n')
	with open(f"{root_dir}/restrict_mods.py", 'w') as f:
		f.write('\n'.join(buf))


# generate a mod list for every base we are tracking, copies because they will be changed later
def genmods(goodmods):
	bases = {
		'jewel.base',
		'jewel.abyss',
		'weapon',
		'weapon.wand',
		'accessory.amulet',
		'accessory.ring',
		'accessory.belt',
		'armour.quiver',
		'armour.shield',
		'armour.gloves',
		'armour.helmet',
		'armour.chest',
		'armour.boots',
	}

	mod_set = []
	for m in goodmod:
		mod_set.extend(mods[m])
	mod_list = list(mod_set)
	mod_list.sort()
	ret = {}
	for base in bases:
		ret[base] = mod_list.copy()

	for base in goodmods:
		for m in goodmods[base]:
			del ret[base][ret[base].index(m)]

	return ret


# Calculate mod/pseudomod dependancy trees for query optimizations
def handle_pseudos(pseudos, root_dir):
	bad_pseudos = [
		'# Crafted Modifiers', '# Crafted Prefix Modifiers', '# Crafted Suffix Modifiers', '# Empty Modifiers', '# Empty Prefix Modifiers', '# Empty Suffix Modifiers',
		'# Fractured Modifiers', '# Implicit Modifiers', '# Modifiers', '# Notable Passive Skills', '# Prefix Modifiers', '# Suffix Modifiers',
		'# Incubator Kills (Abyssal)', "# Incubator Kills (Cartographer's)", "# Incubator Kills (Celestial Armoursmith's)", "# Incubator Kills (Celestial Blacksmith's)",
		"# Incubator Kills (Celestial Jeweller's)", '# Incubator Kills (Decadent)', "# Incubator Kills (Diviner's)", '# Incubator Kills (Eldritch)',
		'# Incubator Kills (Enchanted)', '# Incubator Kills (Feral)', '# Incubator Kills (Fine)', '# Incubator Kills (Foreboding)', '# Incubator Kills (Fossilised)',
		'# Incubator Kills (Fragmented)', "# Incubator Kills (Gemcutter's)", "# Incubator Kills (Geomancer's)", '# Incubator Kills (Infused)', '# Incubator Kills (Mysterious)',
		'# Incubator Kills (Obscured)', '# Incubator Kills (Ornate)', '# Incubator Kills (Otherwordly)', '# Incubator Kills (Primal)', '# Incubator Kills (Singular)',
		'# Incubator Kills (Skittering)', "# Incubator Kills (Thaumaturge's)", '# Incubator Kills (Time-Lost)', '# Incubator Kills (Whispering)',
		'# Life Regenerated per Second', '# total Elemental Resistances', '# total Resistances', '#% increased Mana Regeneration Rate', '#% increased Movement Speed',
		'#% increased Rarity of Items found', '#% of Life Regenerated per Second', '#% of Physical Attack Damage Leeched as Life', '#% of Physical Attack Damage Leeched as Mana',
		'+# total to Level of Socketed Aura Gems', '+# total to Level of Socketed Bow Gems', '+# total to Level of Socketed Chaos Gems',
		'+# total to Level of Socketed Cold Gems', '+# total to Level of Socketed Curse Gems', '+# total to Level of Socketed Dexterity Gems',
		'+# total to Level of Socketed Elemental Gems', '+# total to Level of Socketed Fire Gems', '+# total to Level of Socketed Gems',
		'+# total to Level of Socketed Golem Gems', '+# total to Level of Socketed Intelligence Gems', '+# total to Level of Socketed Lightning Gems',
		'+# total to Level of Socketed Melee Gems', '+# total to Level of Socketed Minion Gems', '+# total to Level of Socketed Movement Gems',
		'+# total to Level of Socketed Projectile Gems', '+# total to Level of Socketed Skill Gems', '+# total to Level of Socketed Spell Gems',
		'+# total to Level of Socketed Strength Gems', '+# total to Level of Socketed Support Gems', '+# total to Level of Socketed Vaal Gems',
		'+# total to Level of Socketed Warcry Gems',
		'+#% Quality to Attack Modifiers', '+#% Quality to Attribute Modifiers', '+#% Quality to Caster Modifiers', '+#% Quality to Defence Modifiers',
		'+#% Quality to Elemental Damage Modifiers', '+#% Quality to Life and Mana Modifiers', '+#% Quality to Resistance Modifiers',
		'+#% total Elemental Resistance', '+#% total Resistance', '+#% total to Chaos Resistance', '+#% total to Cold Resistance', '+#% total to Fire Resistance',
		'+#% total to Lightning Resistance', '+#% total to all Elemental Resistances',
		# mods that seem good but aren't
		'+# total to all Attributes',  # eg 5 str, 11 dex, 14 int item will have value of 5

		'+# total maximum Energy Shield',  # includes local mods
		'#% total increased Physical Damage',  # includes local mods
		'+# total maximum Life',  # includes strength
		'+# total maximum Mana',  # includes int
		'#% increased Burning Damage',  # duplicate of (pseudo) % increased fire damage
		'#% increased Spell Damage',  # superset of all elements
		'#% increased Elemental Damage',  # superset of all elements
		'#% increased Elemental Damage with Attack Skills',  # superset of all elements
		'+#% total Critical Strike Chance for Spells',  # subset of global crit strike chance
		# too generic
		'Adds # to # Damage', 'Adds # to # Damage to Attacks', 'Adds # to # Damage to Spells',
		'Adds # to # Elemental Damage', 'Adds # to # Elemental Damage to Attacks', 'Adds # to # Elemental Damage to Spells',
		# All of these include attack and spell damage
		'#% increased Cold Damage',
		'#% increased Fire Damage',
		'#% increased Lightning Damage',
		'Adds # to # Chaos Damage',
		'Adds # to # Cold Damage',
		'Adds # to # Fire Damage',
		'Adds # to # Lightning Damage',
		'Adds # to # Physical Damage',  # only present on uniques
	]
	# list of keywords to find possible sub mods
	# All include, Any include
	good_pseudos = [
		'#% increased Cold Damage with Attack Skills', '#% increased Cold Spell Damage',
		'#% increased Fire Damage with Attack Skills', '#% increased Fire Spell Damage',
		'#% increased Lightning Damage with Attack Skills', '#% increased Lightning Spell Damage',
		'+# total to Dexterity', '+# total to Intelligence', '+# total to Strength',
		'+#% Global Critical Strike Multiplier', '+#% Global Critical Strike Chance',
		'+#% total Attack Speed', '+#% total Cast Speed',
		'Adds # to # Chaos Damage to Attacks', 'Adds # to # Chaos Damage to Spells',
		'Adds # to # Cold Damage to Attacks', 'Adds # to # Cold Damage to Spells',
		'Adds # to # Fire Damage to Attacks', 'Adds # to # Fire Damage to Spells',
		'Adds # to # Lightning Damage to Attacks', 'Adds # to # Lightning Damage to Spells',
		'Adds # to # Physical Damage to Attacks', 'Adds # to # Physical Damage to Spells',
		'#% total increased maximum Energy Shield',  # global only
	]
	print("New mods:", ', '.join([f'{repr(k)}' for k in sorted(pseudos) if k not in bad_pseudos + good_pseudos]))

	# list of mods that are good matches.
	good_matches = {
		'+#% Global Critical Strike Chance': ['#% increased Global Critical Strike Chance'],
		'+#% total Critical Strike Chance for Spells': ['#% increased Critical Strike Chance for Spells'],
		'+#% Global Critical Strike Multiplier': ['#% to Global Critical Strike Multiplier'],
		'+#% total Cast Speed': ['#% increased Cast Speed'],

		'Adds # to # Chaos Damage to Attacks': ['Adds # to # Chaos Damage to Attacks', 'Adds # to # Chaos Damage'],
		'Adds # to # Chaos Damage to Spells': ['Adds # to # Chaos Damage to Spells', 'Adds # to # Chaos Damage'],
		"Adds # to # Chaos Damage": ["Adds # to # Chaos Damage"],

		'Adds # to # Lightning Damage to Attacks': ['Adds # to # Lightning Damage to Attacks', 'Adds # to # Lightning Damage', 'Adds # to # Lightning Damage to Spells and Attacks'],
		'Adds # to # Lightning Damage to Spells': ['Adds # to # Lightning Damage to Spells', 'Adds # to # Lightning Damage', 'Adds # to # Lightning Damage to Spells and Attacks'],
		"Adds # to # Lightning Damage": ["Adds # to # Lightning Damage"],

		'Adds # to # Fire Damage to Attacks': ['Adds # to # Fire Damage to Attacks', 'Adds # to # Fire Damage', 'Adds # to # Fire Damage to Spells and Attacks'],
		'Adds # to # Fire Damage to Spells': ['Adds # to # Fire Damage to Spells', 'Adds # to # Fire Damage', 'Adds # to # Fire Damage to Spells and Attacks'],
		"Adds # to # Fire Damage": ["Adds # to # Fire Damage"],

		'Adds # to # Cold Damage to Attacks': ['Adds # to # Cold Damage to Attacks', 'Adds # to # Cold Damage', 'Adds # to # Cold Damage to Spells and Attacks'],
		'Adds # to # Cold Damage to Spells': ['Adds # to # Cold Damage to Spells', 'Adds # to # Cold Damage', 'Adds # to # Cold Damage to Spells and Attacks'],
		"Adds # to # Cold Damage": ["Adds # to # Cold Damage"],

		'Adds # to # Physical Damage to Attacks': ['Adds # to # Physical Damage to Attacks'],
		'Adds # to # Physical Damage to Spells': ['Adds # to # Physical Damage to Spells'],

		"#% increased Cold Damage with Attack Skills": ["#% increased Cold Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],
		"#% increased Cold Spell Damage": ["#% increased Cold Damage", '#% increased Elemental Damage', '#% increased Spell Damage'],
		"#% increased Cold Damage": ['#% increased Cold Damage', '#% increased Elemental Damage'],

		"#% increased Fire Damage with Attack Skills": ["#% increased Fire Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],
		"#% increased Fire Spell Damage": ["#% increased Fire Damage", '#% increased Elemental Damage', '#% increased Spell Damage'],
		"#% increased Fire Damage": ["#% increased Fire Damage", '#% increased Elemental Damage'],

		"#% increased Lightning Damage with Attack Skills": ["#% increased Lightning Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],
		"#% increased Lightning Spell Damage": ["#% increased Lightning Damage", '#% increased Elemental Damage', '#% increased Spell Damage'],
		"#% increased Lightning Damage": ["#% increased Lightning Damage", '#% increased Elemental Damage'],

		# Do not match on weapons, will include local damage
		'#% total increased Physical Damage': ['#% increased Global Physical Damage'],
		'+#% total Attack Speed': ['#% increased Attack Speed'],
	}
	# Based on the contents of good_matches, set up if/elif/elif chains
	good_matches_order = [
		['+#% Global Critical Strike Chance'],
		['+#% total Critical Strike Chance for Spells'],
		['+#% Global Critical Strike Multiplier'],
		['+#% total Cast Speed'],
		['Adds # to # Chaos Damage to Attacks', 'Adds # to # Chaos Damage to Spells', "Adds # to # Chaos Damage"],
		['Adds # to # Lightning Damage to Attacks', 'Adds # to # Lightning Damage to Spells', "Adds # to # Lightning Damage"],
		['Adds # to # Fire Damage to Attacks', 'Adds # to # Fire Damage to Spells', "Adds # to # Fire Damage"],
		['Adds # to # Cold Damage to Attacks', 'Adds # to # Cold Damage to Spells', "Adds # to # Cold Damage"],
		['Adds # to # Physical Damage to Attacks', 'Adds # to # Physical Damage to Spells'],
		["#% increased Cold Damage with Attack Skills", "#% increased Cold Spell Damage", "#% increased Cold Damage"],
		["#% increased Fire Damage with Attack Skills", "#% increased Fire Spell Damage", "#% increased Fire Damage"],
		["#% increased Lightning Damage with Attack Skills", "#% increased Lightning Spell Damage", "#% increased Lightning Damage"],
		['#% total increased Physical Damage'],
		['+#% total Attack Speed'],
	]
	# These matches get different rules, only check the first and zero out the rest
	good_matches_special = {
		"+# total to Dexterity": ["# to Dexterity", "# to Strength and Dexterity", "# to Dexterity and Intelligence", "# to all Attributes"],
		"+# total to Intelligence": ["# to Intelligence", "# to Strength and Intelligence", "# to Dexterity and Intelligence", "# to all Attributes"],
		"+# total to Strength": ["# to Strength", "# to Strength and Intelligence", "# to Strength and Dexterity", "# to all Attributes"],
	}
	buf2 = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", '\n\n# Autogenerated function to implement pseudomods\ndef pseudo_lookup(modstr, base, reverse, selections):', '\tret = {}']
	for modset in good_matches_order:
		for c, mod in enumerate(modset):
			multivalcheck = ''
			# Check that we are using pseudo mods that are specific to attacks or spells on the right mods
			#			if any([x in mod for x in ['Spell', 'Cast']]):
			#				multivalcheck = ' and {"Spell"}.issubset(selections)'
			#			if any([x in mod for x in ['Attack']]):
			#				multivalcheck = ' and {"Attack"}.issubset(selections)'
			ifstr = '"] == modstr["'.join(good_matches[mod])
			multivalcheck += f' and (modstr["{ifstr}"])' if len(good_matches[mod]) > 1 else ''
			# Do not use these pseudo mods on weapons
			if mod in ['#% total increased Physical Damage', '+#% total Attack Speed']:
				multivalcheck += ' and base not in ["Caster Weapon", "Wand (Spellslinger)"]'
			buf2.append('\t# Check that the value is non-zero and if necessary that it isn\'t a bad base for that mod and that all values are equal')
			buf2.append(f'\t{"elif" if c else "if"} modstr["{good_matches[mod][0]}"]{multivalcheck}:')
			buf2.append('\t\t# Assign the value to our pseudomod')
			buf2.append(f'\t\tret["{pseudos[mod]}"] = round(modstr["{good_matches[mod][0]}"], 2)')
			ifstr = '"] = modstr["'.join(good_matches[mod])
			buf2.append('\t\t# zero out the mods being used by pseudomod.  Don\'t delete from list so that we don\'t crash if checked later')
			buf2.append(f'\t\tmodstr["{ifstr}"] = 0')
			buf2.append('\t\t# Add mod to reverse lookup in case mod gets trimmed')
			buf2.append(f'\t\treverse["{pseudos[mod]}"] = "{mod}"')
			del good_matches[mod]
		buf2.append('')
	for mod in good_matches_special:
		buf2.append('\t# Check that the value is non-zero and if necessary that it isn\'t a bad base for that mod and that all values are equal')
		buf2.append(f'\tif modstr["{good_matches_special[mod][0]}"]:')
		buf2.append('\t\t# Assign the value to our pseudomod')
		buf2.append(f'\t\tret["{pseudos[mod]}"] = round(modstr["{good_matches_special[mod][0]}"], 2)')
		ifstr = '"] = modstr["'.join(good_matches_special[mod])
		buf2.append('\t\t# zero out the mods being used by pseudomod.  Don\'t delete from list so that we don\'t crash if checked later')
		buf2.append(f'\t\tmodstr["{ifstr}"] = 0')
		buf2.append('\t\t# Add mod to reverse lookup in case mod gets trimmed')
		buf2.append(f'\t\treverse["{pseudos[mod]}"] = "{mod}"')
		buf2.append('')

	buf2.append('\treturn ret\n')

	print(f"Mods not processed in good_matches: {good_matches.keys()}" if good_matches else "All mods handled")

	with open(f'{root_dir}/pseudo_lookup.py', 'w') as f:
		f.write('\n'.join(buf2))


def updatemods(root_dir, headers, cookies):
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}}
	pseudos = {}
	modurl = "https://www.pathofexile.com/api/trade/data/stats"
	vals = fetch_api(requests, modurl, headers, cookies)
	for i in vals['result']:
		if i['label'] in [
			'Explicit',
			'Implicit',
			'Crafted',
		]:
			results[i['label']] = {k['id']: k['text'] for k in i['entries']}
		elif i['label'] == 'Pseudo':
			pseudos = {k['text']: k['id'] for k in i['entries']}

	mlist = {}
	for label in results:
		for val in results[label]:
			cur = results[label][val].replace('\n', ' ')
			if cur not in mlist:
				mlist[cur] = [val]
			else:
				mlist[cur].append(val)

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'mods = {']

	for label in sorted(mlist):
		if label.isascii():  # since we can't check for valid utf-8 encoding, this is all we get
			if label not in goodmod and label not in badmod:
				print(f"New mod: {label}")
			mlist[label].sort()
			buf.append('\t"{}": ["{}"],'.format(label, '", "'.join(mlist[label])))
		else:
			print(f'skipping: {label.encode("utf-8")}')
	buf.append('}')

	with open(f'{root_dir}/modlist.py', 'w') as f:
		f.write('\n'.join(buf))

	handle_pseudos(pseudos, root_dir)


def updateleagues(root_dir, headers, cookies):
	leagueurl = "http://api.pathofexile.com/leagues?realm=pc&compact=1"
	vals = fetch_api(requests, leagueurl, headers, cookies)

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", f"leagues = {[x['id'] for x in vals if not x['id'].startswith('SSF')]}"]
	with open(f'{root_dir}/leaguelist.py', 'w') as f:
		f.write('\n'.join(buf))


# because converting json to a python object for every page load is slow
def updatejsonmods(root_dir):
	with open(f"{root_dir}/mods.json", 'r') as f:
		mjson = json.loads(f.read())

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'mjson = [']
	for mod in mjson:
		buf.append(f'\t{{"name": "{mod["name"]}", "desc": "{mod["desc"]}", "count": {mod["count"]}}},')
	buf.append(']')

	with open(f'{root_dir}/modsjson.py', 'w') as f:
		f.write('\n'.join(buf))


if __name__ == "__main__":
	root_dir_g = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	g_cookies = {'POESESSID': ''}
	g_headers = {'User-Agent': '(poe discord: xan#7840) poe weighted search mod gen tool'}
	with open('modmap.json', 'r') as fi:
		knownmods = json.load(fi)
	mymods = genmods(knownmods)
#	gen_mod_map(mymods, knownmods, g_cookies, g_headers)
	gen_restrict_mods(knownmods, root_dir_g)
	updatemods(root_dir_g, g_headers, g_cookies)
	updateleagues(root_dir_g, g_headers, g_cookies)
	updatejsonmods(root_dir_g)
