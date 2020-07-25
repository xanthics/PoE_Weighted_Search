#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher

import json
import os
import urllib.request, urllib.parse
from datetime import datetime
from helper_files.gen_mod_by_slot import load_mods


# helper function to build a quick/dirty html table to manually check if various explicit values are included in pseudo values
# This list is manually updated, and values are manually checked.
def handle_pseudos(pseudos, mlist, root_dir):
	# Keyword for each pseudo.  This is also so we can spot new pseudo mods
	# Manually curated
	mod_matches = {
		"+# total to Strength": ["Strength"],
		"+# total to Dexterity": ["Dexterity"],
		"+# total to Intelligence": ["Intelligence"],
		"+# total maximum Energy Shield": ['maximum', 'Energy', 'Shield'],
		"#% total increased maximum Energy Shield": ['#%', 'increased', 'maximum', 'Energy', 'Shield'],
		"+#% total Attack Speed": ['#%', 'Attack', 'Speed'],
		"+#% total Cast Speed": ['#%', 'Cast', 'Speed'],
		"#% total increased Physical Damage": ['#%', 'increased', 'Physical', 'Damage'],
		"+#% Global Critical Strike Chance": ['Critical', 'Strike', 'Chance'],
		"+#% total Critical Strike Chance for Spells": ['Critical', 'Strike', 'Chance', 'Spells'],
		"+#% Global Critical Strike Multiplier": ['Critical', 'Strike', 'Multiplier'],
		"Adds # to # Physical Damage": ['Adds', 'Physical', 'Damage'],
		"Adds # to # Lightning Damage": ['Adds', 'Lightning', 'Damage'],
		"Adds # to # Cold Damage": ['Adds', 'Cold', 'Damage'],
		"Adds # to # Fire Damage": ['Adds', 'Fire', 'Damage'],
		"Adds # to # Chaos Damage": ['Adds', 'Chaos', 'Damage'],
		"Adds # to # Physical Damage to Attacks": ['Adds', 'Physical', 'Damage'],
		"Adds # to # Lightning Damage to Attacks": ['Adds', 'Lightning', 'Damage'],
		"Adds # to # Cold Damage to Attacks": ['Adds', 'Cold', 'Damage'],
		"Adds # to # Fire Damage to Attacks": ['Adds', 'Fire', 'Damage'],
		"Adds # to # Chaos Damage to Attacks": ['Adds', 'Chaos', 'Damage'],
		"Adds # to # Physical Damage to Spells": ['Adds', 'Physical', 'Damage'],
		"Adds # to # Lightning Damage to Spells": ['Adds', 'Lightning', 'Damage'],
		"Adds # to # Cold Damage to Spells": ['Adds', 'Cold', 'Damage'],
		"Adds # to # Fire Damage to Spells": ['Adds', 'Fire', 'Damage'],
		"Adds # to # Chaos Damage to Spells": ['Adds', 'Chaos', 'Damage'],
		"#% increased Lightning Damage": ['#%', 'increased', 'Lightning', 'Damage'],
		"#% increased Fire Damage": ['#%', 'increased', 'Fire', 'Damage'],
		"#% increased Spell Damage": ['#%', 'increased', 'Spell', 'Damage'],
		"#% increased Lightning Spell Damage": ['#%', 'increased', 'Lightning', 'Damage'],
		"#% increased Cold Spell Damage": ['#%', 'increased', 'Cold', 'Damage'],
		"#% increased Fire Spell Damage": ['#%', 'increased', 'Fire', 'Damage'],
		"#% increased Lightning Damage with Attack Skills": ['#%', 'increased', 'Lightning', 'Damage'],
		"#% increased Cold Damage with Attack Skills": ['#%', 'increased', 'Cold', 'Damage'],
		"#% increased Fire Damage with Attack Skills": ['#%', 'increased', 'Fire', 'Damage'],
	}
	# Matches that are known to be bad that occur with mod_matches
	bad_matches_mismatch = {
		'+# total maximum Life': ['#% increased Damage when on Full Life', '#% increased maximum Life'],
		'+# total maximum Mana': ['#% increased maximum Mana', '#% reduced Mana Cost of Skills'],
		'+#% Global Critical Strike Chance': ['Spells have #% to Critical Strike Chance ', 'Attacks have #% to Critical Strike Chance', '#% increased Critical Strike Chance for Spells', '#% increased Melee Critical Strike Chance'],
		'+#% Global Critical Strike Multiplier': ['#% to Melee Critical Strike Multiplier', '#% to Critical Strike Multiplier for Spells'],
		'+#% total Critical Strike Chance for Spells': ["Spells have #% to Critical Strike Chance "],
	}
	# mods that don't match with a pseudomod
	# This needs to be updated occasionally
	# check for updates by removing relevant block in BEEN_SEEN section
	bad_matches_no_match = {
		'+#% total Attack Speed': ['#% increased Attack and Cast Speed'],
		'+#% total Cast Speed': ['#% increased Attack and Cast Speed'],
		'Adds # to # Chaos Damage': ['Adds # to # Chaos Damage to Attacks', 'Adds # to # Chaos Damage to Spells'],
		'Adds # to # Lightning Damage': ['Adds # to # Lightning Damage to Attacks', 'Adds # to # Lightning Damage to Spells', "Adds # to # Lightning Damage to Spells and Attacks"],
		'Adds # to # Fire Damage': ['Adds # to # Fire Damage to Attacks', 'Adds # to # Fire Damage to Spells', "Adds # to # Fire Damage to Spells and Attacks"],
		'Adds # to # Cold Damage': ['Adds # to # Cold Damage to Attacks', 'Adds # to # Cold Damage to Spells', "Adds # to # Cold Damage to Spells and Attacks"],
		'Adds # to # Physical Damage': ['Adds # to # Physical Damage to Attacks', 'Adds # to # Physical Damage to Spells'],
		'Adds # to # Chaos Damage to Attacks': ['Adds # to # Chaos Damage to Spells'],
		'Adds # to # Chaos Damage to Spells': ['Adds # to # Chaos Damage to Attacks'],
		'Adds # to # Lightning Damage to Attacks': ['Adds # to # Lightning Damage to Spells'],
		'Adds # to # Lightning Damage to Spells': ['Adds # to # Lightning Damage to Attacks'],
		'Adds # to # Fire Damage to Attacks': ['Adds # to # Fire Damage to Spells'],
		'Adds # to # Fire Damage to Spells': ['Adds # to # Fire Damage to Attacks'],
		'Adds # to # Cold Damage to Attacks': ['Adds # to # Cold Damage to Spells'],
		'Adds # to # Cold Damage to Spells': ['Adds # to # Cold Damage to Attacks'],
		'Adds # to # Physical Damage to Attacks': ['Adds # to # Physical Damage to Spells'],
		'Adds # to # Physical Damage to Spells': ['Adds # to # Physical Damage to Attacks'],
		"+# total to Dexterity": ["# to Level of all Dexterity Skill Gems", "#% increased Damage per 15 Dexterity", "#% increased Dexterity"],
		"+# total to Intelligence": ["# to Level of all Intelligence Skill Gems", "#% increased Damage per 15 Intelligence", "#% increased Intelligence"],
		"+# total to Strength": ["# to Level of all Strength Skill Gems", "#% increased Damage per 15 Strength", "#% increased Strength"],
	}
	# qualifiers in mods that remove them from matching
	bad_words = [
		'Recently', 'Shield', 'Dual Wielding', 'Axe', 'Bow', 'Claw', 'Dagger', 'Mace', 'One Handed', 'Stave', 'Staff', 'Sword', 'Two Handed', 'Wand', 'Nearby', 'during', 'Minions', 'Skills', 'Charge', 'Bleeding', 'Poisoned', 'Ignited', 'Chilled', "Blinded", "Shocked"
	]
	# list of mods that are good matchs
	good_matches = {
		'#% increased Spell Damage': ['#% increased Spell Damage'],
		'+#% Global Critical Strike Chance': ['#% increased Global Critical Strike Chance'],
		'+#% Global Critical Strike Multiplier': ['#% to Global Critical Strike Multiplier'],
		'+#% total Cast Speed': ['#% increased Cast Speed'],
		'+#% total Critical Strike Chance for Spells': ['#% increased Critical Strike Chance for Spells'],

		'Adds # to # Chaos Damage to Attacks': ['Adds # to # Chaos Damage to Attacks', 'Adds # to # Chaos Damage'],
		'Adds # to # Lightning Damage to Attacks': ['Adds # to # Lightning Damage to Attacks', 'Adds # to # Lightning Damage', 'Adds # to # Lightning Damage to Spells and Attacks'],
		'Adds # to # Fire Damage to Attacks': ['Adds # to # Fire Damage to Attacks', 'Adds # to # Fire Damage', 'Adds # to # Fire Damage to Spells and Attacks'],
		'Adds # to # Cold Damage to Attacks': ['Adds # to # Cold Damage to Attacks', 'Adds # to # Cold Damage', 'Adds # to # Cold Damage to Spells and Attacks'],
		'Adds # to # Physical Damage to Attacks': ['Adds # to # Physical Damage to Attacks', "Adds # to # Physical Damage"],

		'Adds # to # Chaos Damage to Spells': ['Adds # to # Chaos Damage to Spells', 'Adds # to # Chaos Damage'],
		'Adds # to # Lightning Damage to Spells': ['Adds # to # Lightning Damage to Spells', 'Adds # to # Lightning Damage', 'Adds # to # Lightning Damage to Spells and Attacks'],
		'Adds # to # Fire Damage to Spells': ['Adds # to # Fire Damage to Spells', 'Adds # to # Fire Damage', 'Adds # to # Fire Damage to Spells and Attacks'],
		'Adds # to # Cold Damage to Spells': ['Adds # to # Cold Damage to Spells', 'Adds # to # Cold Damage', 'Adds # to # Cold Damage to Spells and Attacks'],
		'Adds # to # Physical Damage to Spells': ['Adds # to # Physical Damage to Spells', 'Adds # to # Physical Damage'],

		"+# total to Dexterity": ["# to Dexterity", "# to Strength and Dexterity", "# to Dexterity and Intelligence", "# to all Attributes"],
		"+# total to Intelligence": ["# to Intelligence", "# to Strength and Intelligence", "# to Dexterity and Intelligence", "# to all Attributes"],
		"+# total to Strength": ["# to Strength", "# to Strength and Intelligence", "# to Strength and Dexterity", "# to all Attributes"],

		"#% increased Cold Damage with Attack Skills": ["#% increased Cold Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],
		"#% increased Fire Damage with Attack Skills": ["#% increased Fire Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],
		"#% increased Lightning Damage with Attack Skills": ["#% increased Lightning Damage", '#% increased Elemental Damage', "#% increased Elemental Damage with Attack Skills"],

		"#% increased Cold Spell Damage": ["#% increased Cold Damage", '#% increased Elemental Damage'],
		"#% increased Fire Spell Damage": ["#% increased Fire Damage", '#% increased Elemental Damage'],
		"#% increased Lightning Spell Damage": ["#% increased Lightning Damage", '#% increased Elemental Damage'],

		# Do not match on weapons, will include local damage
		'#% total increased Physical Damage': ['#% increased Global Physical Damage'],
		'+#% total Attack Speed': ['#% increased Attack Speed'],
	}
	# First delete the pseudo values we don't care about
	for val in [
		# Mods we don't currently care about
		'+#% total to Cold Resistance', '+#% total to Fire Resistance', '+#% total to Lightning Resistance', '+#% total Elemental Resistance', '+#% total to Chaos Resistance', '+#% total Resistance', '# total Resistances', '# total Elemental Resistances', '+#% total to all Elemental Resistances',
		'#% increased Movement Speed', '#% increased Rarity of Items found', '# Life Regenerated per Second', '#% of Life Regenerated per Second', '#% of Physical Attack Damage Leeched as Life', '#% of Physical Attack Damage Leeched as Mana', '#% increased Mana Regeneration Rate',
		'+# total to Level of Socketed Gems', '+# total to Level of Socketed Elemental Gems', '+# total to Level of Socketed Fire Gems', '+# total to Level of Socketed Cold Gems', '+# total to Level of Socketed Lightning Gems', '+# total to Level of Socketed Chaos Gems', '+# total to Level of Socketed Spell Gems',
		'+# total to Level of Socketed Projectile Gems', '+# total to Level of Socketed Bow Gems', '+# total to Level of Socketed Melee Gems', '+# total to Level of Socketed Minion Gems', '+# total to Level of Socketed Strength Gems', '+# total to Level of Socketed Dexterity Gems', '+# total to Level of Socketed Intelligence Gems',
		'+# total to Level of Socketed Aura Gems', '+# total to Level of Socketed Movement Gems', '+# total to Level of Socketed Curse Gems', '+# total to Level of Socketed Vaal Gems', '+# total to Level of Socketed Support Gems', '+# total to Level of Socketed Skill Gems', '+# total to Level of Socketed Warcry Gems',
		'+# total to Level of Socketed Golem Gems', '# Implicit Modifiers', '# Prefix Modifiers', '# Suffix Modifiers', '# Modifiers', '# Crafted Prefix Modifiers', '# Crafted Suffix Modifiers', '# Crafted Modifiers', '# Empty Prefix Modifiers', '# Empty Suffix Modifiers', '# Empty Modifiers',
		'# Incubator Kills (Whispering)', '# Incubator Kills (Fine)', '# Incubator Kills (Singular)', "# Incubator Kills (Cartographer's)", '# Incubator Kills (Otherwordly)', '# Incubator Kills (Abyssal)', '# Incubator Kills (Fragmented)', '# Incubator Kills (Skittering)', '# Incubator Kills (Infused)',
		'# Incubator Kills (Fossilised)', '# Incubator Kills (Decadent)', "# Incubator Kills (Diviner's)", '# Incubator Kills (Primal)', '# Incubator Kills (Enchanted)', "# Incubator Kills (Geomancer's)", '# Incubator Kills (Ornate)', '# Incubator Kills (Time-Lost)', "# Incubator Kills (Celestial Armoursmith's)",
		"# Incubator Kills (Celestial Blacksmith's)", "# Incubator Kills (Celestial Jeweller's)", '# Incubator Kills (Eldritch)', '# Incubator Kills (Obscured)', '# Incubator Kills (Foreboding)', "# Incubator Kills (Thaumaturge's)", '# Incubator Kills (Mysterious)', "# Incubator Kills (Gemcutter's)", '# Incubator Kills (Feral)',
		'# Fractured Modifiers', '# Notable Passive Skills', '+#% Quality to Elemental Damage Modifiers', '+#% Quality to Caster Modifiers', '+#% Quality to Attack Modifiers', '+#% Quality to Defence Modifiers', '+#% Quality to Life and Mana Modifiers', '+#% Quality to Resistance Modifiers', '+#% Quality to Attribute Modifiers',
		# These mods are too specific and would provide no/minimal benefit to use
		"Adds # to # Chaos Damage", "Adds # to # Lightning Damage", "Adds # to # Fire Damage", "Adds # to # Cold Damage", "Adds # to # Physical Damage",
		# These mods are too generic for my purposes
		"Adds # to # Elemental Damage to Spells", "Adds # to # Elemental Damage", "Adds # to # Elemental Damage to Attacks", "Adds # to # Damage to Attacks", "Adds # to # Damage to Spells", "Adds # to # Damage", "+# total to all Attributes", "#% increased Elemental Damage with Attack Skills",
		"+# total maximum Life", "+# total maximum Mana",
		"#% increased Burning Damage",
		"#% increased Cold Damage", "#% increased Fire Damage", "#% increased Lightning Damage", '#% increased Elemental Damage'
	]:
		if val in pseudos:
			del pseudos[val]
	matches = {}
	for p in pseudos:
		if p not in mod_matches:
			print(f"New pseudo mod found: {p}")
		else:
			c = 0
			for val in load_mods(root_dir):
				# check if mod has BEEN_SEEN
				if not(p in good_matches and val in good_matches[p]) and \
						not(p in bad_matches_mismatch and val in bad_matches_mismatch[p]) and \
						not(p in bad_matches_no_match and val in bad_matches_no_match[p]) and \
						not(any(x in val for x in bad_words)) and \
						all([x in val for x in mod_matches[p]]):
					c += 1
					matches[f"{p}§{c}"] = {'pseudo_id': pseudos[p], 'mod_name': val, 'mod_ids': mlist[val]}

	buf = ['<!DOCTYPE html><html lang="en"><head><link href="../css/layout.css" rel="stylesheet" type="text/css" /><meta charset="UTF-8"><title>mods</title></head><body>']
	link = '{{"query":{{"status":{{"option":"online"}},"stats":[{{"type":"weight","filters":[{{"id":"{}","disabled":false,"value":{{"weight":1}}}}],"disabled":false,"value":{{"min":1}}}},{{"type":"and","filters":[{{"id":"{}","disabled":false}}],"disabled":false}}]}},"sort":{{"statgroup.0":"desc"}}}}'

	for mod in sorted(matches):
		buf.append('<table><tr><th>Link</th><th>Pseudo</th><th>Mod</th><th>pseudo_id</th><th>mod_id</th></tr>')
		for submod in matches[mod]['mod_ids']:
			f_link = urllib.parse.quote(link.format(matches[mod]["pseudo_id"], submod))
			buf.append(f'<tr><td><a href="https://www.pathofexile.com/trade/search/Standard?q={f_link}" target="_blank">link</a></td><td class="select_text">"{mod.split("§")[0]}"</td><td class="select_text">"{matches[mod]["mod_name"]}"</td><td>{matches[mod]["pseudo_id"]}</td><td>{submod}</td></tr>')
		buf.append('</table><br /><br />')

	buf.append('</body></html>')
	with open('manual_table.html', 'w') as f:
		f.write('\n'.join(buf))

	buf2 = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", '\n\n# Autogenerated function to implement pseudomods\ndef pseudo_lookup(modstr, base, reverse, selections):', '\tret = {}']
	for mod in sorted(good_matches):
		multivalcheck = ''
		# Check that we are using pseudo mods that are specific to attacks or spells on the right mods
		if any([x in mod for x in ['Spell', 'Cast']]):
			multivalcheck = ' and {"Spell"}.issubset(selections)'
		if any([x in mod for x in ['Attack']]):
			multivalcheck = ' and {"Attack"}.issubset(selections)'
		ifstr = '"] == modstr["'.join(good_matches[mod])
		multivalcheck += f' and (modstr["{ifstr}"])' if len(good_matches[mod]) > 1 else ''
		# Do not use these pseudo mods on weapons
		if mod in ['#% total increased Physical Damage', '+#% total Attack Speed']:
			multivalcheck += ' and base not in ["Caster Weapon", "Spellslinger MH", "Spellslinger DW"]'
		buf2.append('\t# Check that the value is non-zero and if necessary that it isn\'t a bad base for that mod and that all values are equal')
		buf2.append(f'\tif modstr["{good_matches[mod][0]}"]{multivalcheck}:')
		buf2.append('\t\t# Assign the value to our pseudomod')
		buf2.append(f'\t\tret["{pseudos[mod]}"] = round(modstr["{good_matches[mod][0]}"], 2)')
		ifstr = '"] = modstr["'.join(good_matches[mod])
		buf2.append('\t\t# zero out the mods being used by pseudomod.  Don\'t delete from list so that we don\'t crash if checked later')
		buf2.append(f'\t\tmodstr["{ifstr}"] = 0')
		buf2.append('\t\t# Add mod to reverse lookup in case mod gets trimmed')
		buf2.append(f'\t\treverse["{pseudos[mod]}"] = "{mod}"\n')
	buf2.append('\treturn ret\n')

	with open(f'{root_dir}/pseudo_lookup.py', 'w') as f:
		f.write('\n'.join(buf2))


def updatemods(root_dir):
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}, 'Fractured': {}}
	pseudos = {}
	modurl = "https://www.pathofexile.com/api/trade/data/stats"
	headers = {'User-Agent': '(poe discord: xanthics) poe weighted search mod gen'}
	req = urllib.request.Request(modurl, headers=headers)
	data = urllib.request.urlopen(req)
	vals = json.load(data)
	for i in vals['result']:
		if i['label'] in [
			'Explicit',
			'Implicit',
			'Crafted',
			'Fractured'
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
		mlist[label].sort()
		buf.append('\t"{}": ["{}"],'.format(label, '", "'.join(mlist[label])))
	buf.append('}')

	with open(f'{root_dir}/modlist.py', 'w') as f:
		f.write('\n'.join(buf))

	handle_pseudos(pseudos, mlist, root_dir)


def updateleagues(root_dir):
	leagueurl = "http://api.pathofexile.com/leagues?realm=pc&compact=1"
	headers = {'User-Agent': '(poe discord: xanthics) poe weighted search mod gen'}
	req = urllib.request.Request(leagueurl, headers=headers)
	data = urllib.request.urlopen(req)
	vals = json.load(data)

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
	updatemods(root_dir_g)
	updateleagues(root_dir_g)
	updatejsonmods(root_dir_g)
