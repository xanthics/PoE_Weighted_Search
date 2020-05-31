import json
import os
from datetime import datetime


# Load all used mods gensearchparam
def load_mods(root_dir):
	with open(f"{root_dir}/web_files/gensearchparams.py", "r") as f:
		mymods = {}
		start = False
		for line in f:
			if start and ":" in line:
				val = line.split(':')[0].strip().strip('"\'')
				mymods[val] = []
			if "(stop)" in line:
				break
			if "(start)" in line:
				start = True
	return mymods


# load all mods in stat_translations and their ids
def parse_stats(mymods):
	with open(r'C:\git\RePoE\RePoE\data\stat_translations.json', 'r') as f:
		translation = json.load(f)
	lookups = {}

	for mod in translation:
		for entry in mod["English"]:
			line = entry["string"].format(*entry['format'])
			if "+#" in line and line not in mymods:
				line = line.replace('+#', '#')
			if line in mymods:
				if line not in lookups:
					lookups[line] = []
				if 'local' not in mod['ids'][0]:
					lookups[line].extend(mod['ids'])
	return lookups


# get all of the base/implicit combos.  return a trimmed dictionary of only bases we care about
def parsebases(allowed_bases):
	with open(r'C:\git\RePoE\RePoE\data\base_items.json', 'r') as f:
		bases = json.load(f)

	implicits = {}
	taglookups = {}
	for base in bases:
		itemclass = bases[base]['item_class']
		if itemclass in allowed_bases:
			if bases[base]['implicits']:
				for temp in bases[base]['implicits']:
					if temp not in implicits:
						implicits[temp] = []
					implicits[temp].append(itemclass)
			if itemclass not in taglookups:
				taglookups[itemclass] = []
			taglookups[itemclass].append(bases[base]['tags'])
	return implicits, taglookups


# return all the mods that can be crafted on approved slots
def craftingmods(allowed_bases):
	with open(r'C:\git\RePoE\RePoE\data\crafting_bench_options.json', 'r') as f:
		bench = json.load(f)
	crafted = {}
	for mod in bench:
		for base in mod['item_classes']:
			if base in allowed_bases:
				if mod['mod_id'] not in crafted:
					crafted[mod['mod_id']] = []
				if base not in crafted[mod['mod_id']]:
					crafted[mod['mod_id']].append(base)
	return crafted


# reverse lookup table for item_classes
def item_classes_reverse(allowed_bases):
	with open(r'C:\git\RePoE\RePoE\data\item_classes.json', 'r') as f:
		ic = json.load(f)
	ibr = {}

	for base in allowed_bases:
		for mod in ic[base]:
			if ic[base][mod] and mod != 'name':
				ibr[ic[base][mod]] = base
	return ibr


# reverse lookup table for essence mods
def essence_reverse(allowed_bases):
	with open(r'C:\git\RePoE\RePoE\data\essences.json', 'r') as f:
		essence = json.load(f)
	reverse_essence = {}

	for mod in essence:
		for base in essence[mod]['mods']:
			if base not in allowed_bases:
				continue
			temp = essence[mod]['mods'][base]
			if temp:
				if temp not in reverse_essence:
					reverse_essence[temp] = []
				reverse_essence[temp].append(base)
	return reverse_essence


def findmods(lookups, implicits):
	with open(r'C:\git\RePoE\RePoE\data\mods.json', 'r') as f:
		mods = json.load(f)
	reverse = {}
	luret = {}
	for val in mods:
		if (mods[val]['generation_type'] == 'unique' and val not in implicits) or mods[val]['domain'] in ['area', 'flask', 'atlas']:
			continue
		for stat in mods[val]['stats']:
			if stat['id'] not in reverse:
				reverse[stat['id']] = []
			reverse[stat['id']].append(val)

	for pair in lookups:
		luret[pair] = []
		for stat in lookups[pair]:
			if stat in reverse:
				for m in reverse[stat]:
					if m not in luret[pair]:
						luret[pair].append(m)

	return luret, mods


def main():
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	allowed_bases = ['Amulet', 'Body Armour', 'Boots', 'Gloves', 'Helmet', 'Shield', 'Belt', 'AbyssJewel', 'Jewel', 'Quiver', 'Ring', 'Rune Dagger', 'Sceptre', 'Wand', 'Staff']
	implicits, taglookups = parsebases(allowed_bases)
	mymods = load_mods()
	lookups = parse_stats(mymods)
	modlist, mods = findmods(lookups, implicits)
	crafted = craftingmods(allowed_bases)
	ibr = item_classes_reverse(allowed_bases)
	essence = essence_reverse(allowed_bases)
	missing = []
	domains = {
		'abyss_jewel': ['AbyssJewel'],
		'item': ['Amulet', 'Body Armour', 'Boots', 'Gloves', 'Helmet', 'Shield', 'Belt', 'Quiver', 'Ring', 'Rune Dagger', 'Sceptre', 'Wand', 'Staff'],
		'misc': ['Jewel'],
		'delve': ['Amulet', 'Body Armour', 'Boots', 'Gloves', 'Helmet', 'Shield', 'Belt', 'AbyssJewel', 'Jewel', 'Quiver', 'Ring', 'Rune Dagger', 'Sceptre', 'Wand', 'Staff']
	}
	gen_type = {
		'suffix': 'explicit',
		'corrupted': 'implicit',
		'prefix': 'explicit'
	}
	table = {key: {'implicit': [], 'crafted': [], 'explicit': []} for key in allowed_bases}
	for mod in modlist:
		for attr in modlist[mod]:
			if (mods[attr]['domain'] == 'crafted' and attr not in crafted) or \
					(mods[attr]['generation_type'] == 'corrupted' and not any([m['weight'] for m in mods[attr]['spawn_weights']])) or \
					(mods[attr]['is_essence_only'] and attr not in essence) or \
					(attr not in implicits and
					 attr not in crafted and
					 attr not in essence and
					 (not any([m['weight'] for m in mods[attr]['spawn_weights']]))):
				# Capture non-crafted/corrupted mods that are missing spawn rules
				if mods[attr]['domain'] != 'crafted' and mods[attr]['generation_type'] != 'corrupted':
					missing.append(attr)
				continue
			if mods[attr]['is_essence_only']:
				for base in essence[attr]:
					if mod not in table[base]['explicit']:
						table[base]['explicit'].append(mod)
			elif mods[attr]['domain'] == 'crafted':
				for base in crafted[attr]:
					if mod not in table[base]['crafted']:
						table[base]['crafted'].append(mod)
			elif attr in implicits:
				for base in implicits[attr]:
					if mod not in table[base]['implicit']:
						table[base]['implicit'].append(mod)
			elif any([m['weight'] for m in mods[attr]['spawn_weights']]):
				goodbases = []
				if len(domains[mods[attr]['domain']]) == 1:
					goodbases = domains[mods[attr]['domain']]
				else:
					bases_temp = {key: taglookups[key][:] for key in domains[mods[attr]['domain']]}
					for spawn in mods[attr]['spawn_weights']:
						if spawn['weight'] and spawn['tag'] in ibr:
							goodbases.append(ibr[spawn['tag']])
							del bases_temp[ibr[spawn['tag']]]
							continue
						for base in list(bases_temp):
							idx = 0
							while idx < len(bases_temp[base]):
								if spawn['weight'] and spawn['tag'] in bases_temp[base][idx]:
									goodbases.append(base)
									del bases_temp[base]
									break
								elif spawn['tag'] in bases_temp[base][idx]:
									del bases_temp[base][idx]
									if not bases_temp[base]:
										del bases_temp[base]
										break
								else:
									idx += 1

				for base in goodbases:
					if mod not in table[base][gen_type[mods[attr]['generation_type']]]:
						table[base][gen_type[mods[attr]['generation_type']]].append(mod)
			else:
				missing.append(attr)
	table['Caster Weapon'] = {'implicit': [], 'crafted': [], 'explicit': []}
	table['Spellslinger MH'] = {'implicit': [], 'crafted': [], 'explicit': []}
	table['All Jewel'] = {'implicit': [], 'crafted': [], 'explicit': []}

	# Add special mods that are worth considering but don't reveal spawn rules, such as temple mods or specific uniques:
	missing_mods = {
		'Spellslinger MH': {
			'implicit': [
				"Adds # to # Chaos Damage (Local)",
				"Adds # to # Cold Damage (Local)",
				"Adds # to # Fire Damage (Local)",
				"Adds # to # Lightning Damage (Local)"
			],
			'explicit': [
				"Adds # to # Chaos Damage (Local)",
				"Adds # to # Cold Damage (Local)",
				"Adds # to # Fire Damage (Local)",
				"Adds # to # Lightning Damage (Local)"
			],
			'crafted': [
				"Adds # to # Cold Damage (Local)",
				"Adds # to # Fire Damage (Local)",
				"Adds # to # Lightning Damage (Local)"
			]
		},
		'Caster Weapon': {
			'explicit': [
				'#% reduced Mana Cost of Skills',  # Apep's Rage
				'Minions have #% chance to deal Double Damage',  # 'Citaqualotl's'
				'Minions have #% increased Attack Speed',  # 'of Citaqualotl'
				'Minions have #% increased Cast Speed',  # 'of Citaqualotl'
				'Minions have #% increased Cast Speed',  # 'of Citaqualotl'
				'Gain #% of Non-Chaos Damage as extra Chaos Damage',  # 'Tacati's'
				'#% increased Trap Damage',  # 'Matatl's'
				'#% increased Mine Damage',  # 'Matatl's'
			]
		},
		'Gloves': {
			'explicit': [
				'#% reduced Mana Cost of Skills',  # Voidbringer
				'# to # added Fire Damage against Burning Enemies',  # 'of Puhuarte'
				'#% increased Damage with Hits against Chilled Enemies',  # 'of Puhuarte'
				'#% increased Critical Strike Chance against Shocked Enemies',  # 'of Puhuarte'
			]
		},
		'Ring': {
			'explicit': [
				'#% increased Attack Damage if your other Ring is a Shaper Item',  # Mark of the Elder
				'#% increased Spell Damage if your other Ring is an Elder Item',  # Mark of the Shaper
			]
		},
	}

	for slot in missing_mods:
		for gen_type in missing_mods[slot]:
			table[slot][gen_type].extend(missing_mods[slot][gen_type])

	for val in ['Rune Dagger', 'Sceptre', 'Wand', 'Staff']:
		for modgroup in table[val]:
			for newbase in ['Caster Weapon', 'Spellslinger MH']:
				table[newbase][modgroup].extend(table[val][modgroup])
				table[newbase][modgroup] = list(set(table[newbase][modgroup]))
		del table[val]
	for val in ['Jewel', 'AbyssJewel']:
		for modgroup in table[val]:
			table['All Jewel'][modgroup].extend(table[val][modgroup])
			table['All Jewel'][modgroup] = list(set(table['All Jewel'][modgroup]))
	table['Spellslinger DW'] = table['Spellslinger MH']  # Shallow copy is okay as we want both lists to be the same.
	table["Base Jewel"] = table.pop("Jewel")
	table["Abyss Jewel"] = table.pop("AbyssJewel")

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'r_mods = {']
	for base in sorted(table):
		buf.append(f'\t"{base}": {{')
		for section in table[base]:
			table[base][section].sort()
			tblstr = '",\n\t\t\t"'.join(table[base][section])
			buf.append(f'\t\t"{section}": [\n\t\t\t"{tblstr}"\n\t\t],')
		buf.append('\t},')
	buf.append('}')
	with open(f"{root_dir}/web_files/restrict_mods.py", 'w') as f:
		f.write('\n'.join(buf))
	for miss in missing:
		print(miss)


if __name__ == '__main__':
	main()
