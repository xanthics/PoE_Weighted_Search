import requests
import json
import os
from helper_files.goodmod import goodmod
from helper_files.badmod import badmod
from datetime import datetime
from pyrate_limiter import *
from time import sleep


def post_api(requester, data, headers, cookies, league):
	print('post request')
	post_url = f'https://www.pathofexile.com/api/trade/search/{league}'
	req = requester.post(post_url, cookies=cookies, headers=headers, json=data)
	if req.status_code == 429:
		raise ConnectionError(f"Post throttle error: {req.headers['X-Rate-Limit-Account-State']},{req.headers['X-Rate-Limit-Ip-State']}")
	if req.status_code != 200:
		raise Exception('(post) API response: {}'.format(req.status_code))
	return req.json(), f"{req.headers['X-Rate-Limit-Account']},{req.headers['X-Rate-Limit-Ip']}", f"{req.headers['X-Rate-Limit-Account-State']},{req.headers['X-Rate-Limit-Ip-State']}"


def fetch_api(requester, url, headers, cookies, getheaders=False):
	print('fetch request')
	req = requester.get(url, cookies=cookies, headers=headers)
	if req.status_code == 429:
		print(f"{req.headers['X-Rate-Limit-Account']},{req.headers['X-Rate-Limit-Ip']}", f"{req.headers['X-Rate-Limit-Account-State']},{req.headers['X-Rate-Limit-Ip-State']}", sep='\n')
		raise ConnectionError(f"Fetch throttle error: {req.headers['X-Rate-Limit-Account-State']},{req.headers['X-Rate-Limit-Ip-State']}")
	if req.status_code != 200:
		raise Exception('(fetch) API response: {}'.format(req.status_code))
	if 'X-Rate-Limit-Ip-State' in req.headers and getheaders:
		return req.json(), f"{req.headers['X-Rate-Limit-Account']},{req.headers['X-Rate-Limit-Ip']}", f"{req.headers['X-Rate-Limit-Account-State']},{req.headers['X-Rate-Limit-Ip-State']}"
	else:
		return req.json()


def find_max_sleep(error):
	vals = error.split(':', maxsplit=1)[1].split(',')
	return max([int(x.split(':')[2]) for x in vals])


def check_for_zero(limit, current):
	limits = [int(x.split(':')[0]) for x in limit.split(',')]
	currents = [int(x.split(':')[0]) for x in current.split(',')]
	return any(limits[x] <= currents[x] for x in range(len(limits)))


# given a list of mods to check and a list of known mods, eliminate possibly bad mods
def gen_mod_map(themods, goodmods, cookies, headers, post_limit, fetch_limit, league):
	mod_count = 180  # number of mods to check at a time
	fetch_url = 'https://www.pathofexile.com/api/trade/fetch/{}?query={}'
	requester = requests.session()
	limit = '1:1:1'
	current = '0:0:0'
	limit2 = '1:1:1'
	current2 = '0:0:0'
	for synth, corrupt, modset in [['false', 'false', 'normal'],
								   ['true', 'false', 'synth'],
								   ['false', 'true', 'corrupt']]:
		for base in themods:
			print(f"Gathering for: {base}")
			if base not in goodmods:
				goodmods[base] = {'normal': [], 'synth': [], 'corrupt': []}
			while themods[base][modset]:
				print(f"Remaining ({base}): {len(themods[base][modset])}")
				root_request = {"query": {"status": {"option": "any"}, "stats": [{"type": "count", "filters": [{'id': x} for x in themods[base][modset][:mod_count]], "value": {"min": 1}}],
										  "filters": {"type_filters": {"filters": {"rarity": {"option": "nonunique"}, "category": {"option": base}}, "disabled": False}, "misc_filters": {"filters": {"synthesised_item": {"option": synth}, "corrupted": {"option": corrupt}}}}}, "sort": {"price": "asc"}}
				while True:
					try:
						post_limit.try_acquire('post')
						if check_for_zero(limit, current):
							print("Desync between pyrate and header, pausing post")
							limit = '1:1:1'
							current = '0:0:0'
							while True:
								post_limit.try_acquire('post')
						var, limit, current = post_api(requester, root_request, headers, cookies, league)
						break
					except BucketFullException as err:
						print(err.meta_info)
						sleep(err.meta_info['remaining_time'] + 1)
					except ConnectionError as e:
						print(e)
						sleep(find_max_sleep(e.__str__()))
				if var['result']:
					idx = 0
					thelen = 0
					print(f"fetching: {var['id']}")
					while idx < len(var['result']) and idx < min(50, mod_count):
						while True:
							try:
								fetch_limit.try_acquire('fetch')
								if check_for_zero(limit2, current2):
									print("Desync between pyrate and header, pausing fetch")
									limit2 = '1:1:1'
									current2 = '0:0:0'
									while True:
										fetch_limit.try_acquire('fetch')
								var2, limit2, current2 = fetch_api(requester, fetch_url.format(','.join(var['result'][idx:idx + 10]), var['id']), headers, cookies, True)
								break
							except BucketFullException as err:
								print(err.meta_info)
								sleep(err.meta_info['remaining_time'] + 1)
							except ConnectionError as e:
								print(e)
								sleep(find_max_sleep(e.__str__()))
						idx += 10
						for res in var2['result']:
							for affix in res['item']['extended']['hashes']:
								new_mods = [x[0] for x in res['item']['extended']['hashes'][affix] if x[0] in themods[base][modset] and x[0] not in goodmods[base][modset]]
								if not thelen:
									thelen += len(new_mods)
								for x in new_mods:
									del themods[base][modset][themods[base][modset].index(x)]
								goodmods[base][modset].extend(new_mods)
					# so we don't get stuck in a loop when the only result has fractured crafting mods that can't be explicits
					if not thelen:
						print("Fractured crafting mod that matches explicit as only result.")
						themods[base][modset] = themods[base][modset][mod_count:]
				else:
					print("No results", var)
					themods[base][modset] = themods[base][modset][mod_count:]
				# in case there is an interuption, save every result
				with open('modmap.json', 'w') as f:
					json.dump(goodmods, f)
		# Should have all results saved by now, but make sure.
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
	from modlist import mods
	# reverse lookup to map mod hashes to human readable
	rlookup = {mods[x][idx]: x for x in mods for idx in range(len(mods[x]))}
	results = {}
	for base in goodmods:
		results[lookup_bases[base]] = {'synth_implicit': [], 'corrupt_implicit': [], 'implicit': [], 'crafted': [], 'explicit': []}
		for m in goodmods[base]['normal']:
			name = rlookup[m]
			results[lookup_bases[base]][m.split('.')[0]].append(name)
		for m in goodmods[base]['synth']:
			results[lookup_bases[base]]['synth_implicit'].append(rlookup[m])
		for m in goodmods[base]['corrupt']:
			results[lookup_bases[base]]['corrupt_implicit'].append(rlookup[m])
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
	results['All Jewel'] = {'synth_implicit': list(set(results['Base Jewel']['synth_implicit'] + results['Abyss Jewel']['synth_implicit'])),
							'corrupt_implicit': list(set(results['Base Jewel']['corrupt_implicit'] + results['Abyss Jewel']['corrupt_implicit'])),
							'implicit': list(set(results['Base Jewel']['implicit'] + results['Abyss Jewel']['implicit'])),
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
	from modlist import mods
	mod_set = []
	for m in goodmod:
		mod_set.extend(mods[m])
	mod_list = list(mod_set)
	mod_list.sort()
	imp_list = [x for x in mod_list if x.startswith('implicit')]
	ret = {}
	for base in bases:
		ret[base] = {}
		ret[base]['normal'] = mod_list.copy()
		ret[base]['synth'] = imp_list.copy()
		ret[base]['corrupt'] = imp_list.copy()

	for base in goodmods:
		for modtype in ['normal', 'synth', 'corrupt']:
			for m in goodmods[base][modtype]:
				del ret[base][modtype][ret[base][modtype].index(m)]

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
		'# Incubator Kills (Blighted)', '# Incubator Kills (Maddening)', '# Incubator Kills (Morphing)', '+#% Quality to Critical Modifiers', '+#% Quality to Speed Modifiers', 'Has # Influences', 'Has Crusader Influence', 'Has Elder Influence', 'Has Hunter Influence', 'Has Redeemer Influence',
		'Has Room: Antechamber', 'Has Room: Apex of Ascension (Tier 3)', 'Has Room: Arena of Valour (Tier 2)', "Has Room: Armourer's Workshop (Tier 1)", 'Has Room: Armoury (Tier 2)', 'Has Room: Atlas of Worlds (Tier 3)', 'Has Room: Automaton Lab (Tier 2)', 'Has Room: Banquet Hall', 'Has Room: Barracks (Tier 2)',
		'Has Room: Breach Containment Chamber (Tier 2)', 'Has Room: Catalyst of Corruption (Tier 2)', 'Has Room: Cellar', 'Has Room: Chamber of Iron (Tier 3)', 'Has Room: Chasm', 'Has Room: Cloister', 'Has Room: Conduit of Lightning (Tier 3)', 'Has Room: Corruption Chamber (Tier 1)', 'Has Room: Court of Sealed Death (Tier 3)',
		'Has Room: Crucible of Flame (Tier 3)', 'Has Room: Cultivar Chamber (Tier 2)', 'Has Room: Defense Research Lab (Tier 3)', 'Has Room: Demolition Lab (Tier 2)', 'Has Room: Department of Thaumaturgy (Tier 2)', "Has Room: Doryani's Institute (Tier 3)", 'Has Room: Engineering Department (Tier 2)', 'Has Room: Explosives Room (Tier 1)',
		'Has Room: Factory (Tier 3)', 'Has Room: Flame Workshop (Tier 1)', "Has Room: Gemcutter's Workshop (Tier 1)", 'Has Room: Glittering Halls (Tier 3)', 'Has Room: Guardhouse (Tier 1)', 'Has Room: Hall of Champions (Tier 3)', 'Has Room: Hall of Heroes (Tier 2)', 'Has Room: Hall of Legends (Tier 3)', 'Has Room: Hall of Locks (Tier 2)',
		'Has Room: Hall of Lords (Tier 2)', 'Has Room: Hall of Mettle (Tier 1)', 'Has Room: Hall of Offerings (Tier 2)', 'Has Room: Hall of War (Tier 3)', 'Has Room: Halls', 'Has Room: Hatchery (Tier 1)', 'Has Room: House of the Others (Tier 3)', 'Has Room: Hurricane Engine (Tier 2)', 'Has Room: Hybridisation Chamber (Tier 3)',
		"Has Room: Jeweller's Workshop (Tier 1)", 'Has Room: Jewellery Forge (Tier 2)', 'Has Room: Lightning Workshop (Tier 1)', 'Has Room: Locus of Corruption (Tier 3)', 'Has Room: Museum of Artefacts (Tier 3)', 'Has Room: Office of Cartography (Tier 2)', 'Has Room: Omnitect Forge (Tier 2)', 'Has Room: Omnitect Reactor Plant (Tier 2)',
		'Has Room: Passageways', 'Has Room: Pits', 'Has Room: Poison Garden (Tier 1)', 'Has Room: Pools of Restoration (Tier 1)', 'Has Room: Royal Meeting Room (Tier 1)', 'Has Room: Sacrificial Chamber (Tier 1)', "Has Room: Sadist's Den (Tier 3)", 'Has Room: Sanctum of Immortality (Tier 3)', 'Has Room: Sanctum of Unity (Tier 2)',
		'Has Room: Sanctum of Vitality (Tier 2)', 'Has Room: Shrine of Empowerment (Tier 1)', 'Has Room: Shrine of Unmaking (Tier 3)', 'Has Room: Sparring Room (Tier 1)', 'Has Room: Splinter Research Lab (Tier 1)', 'Has Room: Storage Room (Tier 1)', 'Has Room: Storm of Corruption (Tier 3)', 'Has Room: Strongbox Chamber (Tier 1)',
		"Has Room: Surveyor's Study (Tier 1)", 'Has Room: Tempest Generator (Tier 1)', 'Has Room: Temple Defense Workshop (Tier 2)', 'Has Room: Temple Nexus (Tier 3)', 'Has Room: Throne of Atziri (Tier 3)', 'Has Room: Tombs', 'Has Room: Torment Cells (Tier 1)', 'Has Room: Torture Cages (Tier 2)', 'Has Room: Toxic Grove (Tier 3)',
		'Has Room: Trap Workshop (Tier 1)', 'Has Room: Treasury (Tier 2)', 'Has Room: Tunnels', 'Has Room: Vault (Tier 1)', 'Has Room: Warehouses (Tier 2)', 'Has Room: Wealth of the Vaal (Tier 3)', 'Has Room: Workshop (Tier 1)', 'Has Shaper Influence', 'Has Warlord Influence',
		'+#% Physical and Chaos Damage Modifiers', 'Has Room: Apex of Atzoatl'
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
	print("New pseudo mods:", ', '.join([f'{repr(k)}' for k in sorted(pseudos) if k not in bad_pseudos + good_pseudos]))

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
	# Validate modes
	for key in good_matches:
		for mod in good_matches[key]:
			if mod not in goodmod:
				print(f"Outdated Mod: {mod}")

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
	# This should check for changes before generating/writing to file.  Undecided if implementing
	buf2 = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", '\n\n# Autogenerated function to implement pseudomods\ndef pseudo_lookup(modstr, base, reverse, selections):', '\tret = {}']
	for modset in good_matches_order:
		for c, mod in enumerate(modset):
			multivalcheck = ''
			# Check that we are using pseudo mods that are specific to attacks or spells on the right mods
			#			if any([x in mod for x in ['Spell', 'Cast']]):
			#				multivalcheck = ' and {"Spell"}.issubset(selections)'
			#			if any([x in mod for x in ['Attack']]):
			#				multivalcheck = ' and {"Attack"}.issubset(selections)'
			ifstr = '"][0] == modstr["'.join(good_matches[mod])
			multivalcheck += f' and (modstr["{ifstr}"][0])' if len(good_matches[mod]) > 1 else ''
			# Do not use these pseudo mods on weapons
			if mod in ['#% total increased Physical Damage', '+#% total Attack Speed']:
				multivalcheck += ' and base not in ["Caster Weapon", "Wand (Spellslinger)"]'
			buf2.append('\t# Check that the value is non-zero and if necessary that it isn\'t a bad base for that mod and that all values are equal')
			buf2.append(f'\t{"elif" if c else "if"} modstr["{good_matches[mod][0]}"][0]{multivalcheck}:')
			buf2.append('\t\t# Assign the value to our pseudomod')
			buf2.append(f'\t\tret["{pseudos[mod]}"] = [round(modstr["{good_matches[mod][0]}"][0], 2), modstr["{good_matches[mod][0]}"][1]]')
			ifstr = '"][0] = modstr["'.join(good_matches[mod])
			buf2.append('\t\t# zero out the mods being used by pseudomod.  Don\'t delete from list so that we don\'t crash if checked later')
			buf2.append(f'\t\tmodstr["{ifstr}"][0] = 0')
			buf2.append('\t\t# Add mod to reverse lookup in case mod gets trimmed')
			buf2.append(f'\t\treverse["{pseudos[mod]}"] = "{mod}"')
			del good_matches[mod]
		buf2.append('')
	for mod in good_matches_special:
		buf2.append('\t# Check that the value is non-zero and if necessary that it isn\'t a bad base for that mod and that all values are equal')
		buf2.append(f'\tif modstr["{good_matches_special[mod][0]}"][0]:')
		buf2.append('\t\t# Assign the value to our pseudomod')
		buf2.append(f'\t\tret["{pseudos[mod]}"] = [round(modstr["{good_matches_special[mod][0]}"][0], 2), modstr["{good_matches_special[mod][0]}"][1]]')
		ifstr = '"][0] = modstr["'.join(good_matches_special[mod])
		buf2.append('\t\t# zero out the mods being used by pseudomod.  Don\'t delete from list so that we don\'t crash if checked later')
		buf2.append(f'\t\tmodstr["{ifstr}"][0] = 0')
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
	newmods = []
	for label in sorted(mlist):
		if label.isascii():  # since we can't check for valid utf-8 encoding, this is all we get
			if label not in goodmod and label not in badmod:
				newmods.append(label)
			mlist[label].sort()
			buf.append('\t"{}": ["{}"],'.format(label, '", "'.join(mlist[label])))
		else:
			print(f'skipping: {label.encode("utf-8")}')
	buf.append('}')
	if newmods:
		newmods.sort()
		newstr = '",\n\t"'.join(newmods)
		print(f'New mod(s): \n\t"{newstr}"')
	removed = []
	for label in goodmod+badmod:
		if label not in mlist:
			removed.append(label)
	if removed:
		removed.sort()
		newstr = '",\n\t"'.join(removed)
		print(f'Removed mod(s): \n\t"{newstr}"')

	# This should check for changes before generating/writing but won't implement
	with open(f'{root_dir}/modlist.py', 'w') as f:
		f.write('\n'.join(buf))

	handle_pseudos(pseudos, root_dir)


def updateleagues(root_dir, headers, cookies):
	leagueurl = "http://api.pathofexile.com/leagues?realm=pc&compact=1"
	vals = fetch_api(requests, leagueurl, headers, cookies)
	from leaguelist import leagues
	if set(leagues) != set([x['id'] for x in vals if not x['id'].startswith('SSF')]):
		print("Updating League List")
		buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", f"leagues = {[x['id'] for x in vals if not x['id'].startswith('SSF')]}"]
		with open(f'{root_dir}/leaguelist.py', 'w') as f:
			f.write('\n'.join(buf))
	else:
		print("League List is unchanged")


# because converting json to a python object for every page load is slow
def updatejsonmods(root_dir):
	with open(f"{root_dir}/mods.json", 'r') as f:
		n_mjson = json.loads(f.read())
	version = n_mjson[0]['version']
	del n_mjson[0]['version']
	from modsjson import mjson
	if version not in mjson:
		mjson[version] = n_mjson
		buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'mjson = {']
		for version in sorted(mjson):
			buf.append(f"\t{version}: [")
			for mod in mjson[version]:
				buf.append(f'\t\t{{"name": "{mod["name"]}", "desc": "{mod["desc"]}", "count": {mod["count"]}}},')
			buf.append('\t],')
		buf.append('}')

		with open(f'{root_dir}/modsjson.py', 'w') as f:
			f.write('\n'.join(buf))
	else:
		print("modsjson.py is unchanged")


def setup_limits(cookies, headers, league):
	requester = requests.session()
	post_url = f'https://www.pathofexile.com/api/trade/search/{league}'
	root_request = {"query": {"status": {"option": "any"}, "stats": [{"type": "count", "filters": [], "value": {"min": 1}}], "filters": {"type_filters": {"filters": {"category": {"option": 'weapon'}, "rarity": {"option": "nonunique"}}}}}, "sort": {"price": "asc"}}
	req = requester.post(post_url, cookies=cookies, headers=headers, json=root_request)
	arr_ip = [x.split(':') for x in req.headers['X-Rate-Limit-Ip'].split(',')]
	if 'X-Rate-Limit-Account' in req.headers:
		arr_ip = [x.split(':') for x in req.headers['X-Rate-Limit-Account'].split(',')] + arr_ip
#	arrs = [x.split(':') for x in f"{req.headers['X-Rate-Limit-Account']},{req.headers['X-Rate-Limit-Ip']}".split(',')]
#	post_limit = Limiter(*[RequestRate(int(x[0]), (int(x[1]) + 1) * Duration.SECOND) for x in arrs])
	# build new arrs
	arrs = {}
	for r, p, d in arr_ip:
		r = int(r)
		p = int(p) + 1  # Add 1 second for desync
		if p not in arrs:
			arrs[p] = r
	print(arrs)
	post_limit = Limiter(*[RequestRate(arrs[x], x * Duration.SECOND) for x in sorted(arrs)])

	fetch_url = 'https://www.pathofexile.com/api/trade/fetch/{}'
	req = requester.get(fetch_url, cookies=cookies, headers=headers)
	arr_ip = [x.split(':') for x in req.headers['X-Rate-Limit-Ip'].split(',')]
	if 'X-Rate-Limit-Account' in req.headers:
		arr_ip = [x.split(':') for x in req.headers['X-Rate-Limit-Account'].split(',')] + arr_ip
#	arrs = [x.split(':') for x in f"{req.headers['X-Rate-Limit-Account']},{req.headers['X-Rate-Limit-Ip']}".split(',')]
#	fetch_limit = Limiter(*[RequestRate(int(x[0]), (int(x[1])+1) * Duration.SECOND) for x in arrs])
	# build new arrs
	arrs = {}
	for r, p, d in arr_ip:
		r = int(r)
		p = int(p) + 1  # Add 1 second for desync
		if p not in arrs:
			arrs[p] = r
	print(arrs)
	fetch_limit = Limiter(*[RequestRate(arrs[x], x * Duration.SECOND) for x in sorted(arrs)])

	# try against both buckets to reflect setup request
	post_limit.try_acquire('post')
	fetch_limit.try_acquire('fetch')
	return post_limit, fetch_limit


if __name__ == "__main__":
	root_dir_g = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	g_league = 'Expedition'
	g_cookies = {'POESESSID': ''}
	g_headers = {'User-Agent': '(poe discord: xan#7840) poe weighted search mod gen tool'}
	g_post_limit, g_fetch_limit = setup_limits(g_cookies, g_headers, g_league)
	updatemods(root_dir_g, g_headers, g_cookies)
	with open('modmap.json', 'r') as fi:
		knownmods = json.load(fi)
	mymods = genmods(knownmods)
#	gen_mod_map(mymods, knownmods, g_cookies, g_headers, g_post_limit, g_fetch_limit, g_league)
	gen_restrict_mods(knownmods, root_dir_g)
	updateleagues(root_dir_g, g_headers, g_cookies)
	updatejsonmods(root_dir_g)
