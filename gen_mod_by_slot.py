import json
from datetime import datetime

# Load all used mods gensearchparam
def load_mods():
	with open("gensearchparams.py", "r") as f:
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
	mm = {}

	for mod in translation:
		for entry in mod["English"]:
			line = entry["string"].format(*entry['format'])
			if line in mymods:
				if line not in mm:
					mm[line] = []
				if 'local' not in mod['ids'][0]:
					mm[line].extend(mod['ids'])
			elif "+#" in line:
				line = line.replace('+#', '#')
				if line in mymods:
					if line not in mm:
						mm[line] = []
					if 'local' not in mod['ids'][0]:
						mm[line].extend(mod['ids'])
	return mm


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
			for tag in bases[base]['tags']:
				if tag not in taglookups:
					taglookups[tag] = []
				taglookups[tag].append(itemclass)
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
				if ic[base][mod] not in ibr:
					ibr[ic[base][mod]] = []
				ibr[ic[base][mod]].append(base)
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
	allowed_bases = ['Amulet', 'Body Armour', 'Boots', 'Gloves', 'Helmet', 'Shield', 'Belt', 'AbyssJewel', 'Jewel', 'Quiver', 'Ring', 'Rune Dagger', 'Sceptre', 'Wand', 'Staff']
	implicits, taglookups = parsebases(allowed_bases)
	mymods = load_mods()
	lookups = parse_stats(mymods)
	modlist, mods = findmods(lookups, implicits)
	crafted = craftingmods(allowed_bases)
	ibr = item_classes_reverse(allowed_bases)
	essence = essence_reverse(allowed_bases)
	taglookups.update(ibr)
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
	for m in sorted(taglookups):
		taglookups[m] = list(set(taglookups[m]))
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
				bases = {key: -1 for key in domains[mods[attr]['domain']]}
				for spawn in mods[attr]['spawn_weights'][:-1]:
					if spawn['tag'] in taglookups:
						for base in taglookups[spawn['tag']]:
							if base in bases and bases[base] < 1:
								bases[base] = spawn['weight']
				for base in taglookups['default']:
					if base in bases and bases[base] == -1:
						bases[base] = mods[attr]['spawn_weights'][-1]['weight']
				for base in [x for x in bases if bases[x]]:
					if mod not in table[base][gen_type[mods[attr]['generation_type']]]:
						table[base][gen_type[mods[attr]['generation_type']]].append(mod)
			else:
				missing.append(attr)

	table['Caster Weapon'] = {'implicit': [], 'crafted': [], 'explicit': []}
	table['All Jewel'] = {'implicit': [], 'crafted': [], 'explicit': []}

	# Add special mods that are worth considering but don't reveal spawn rules, such as temple mods or specific uniques:
	# TODO: Temple mods
	table['Caster Weapon']['explicit'].append('#% reduced Mana Cost of Skills')  # Apep's Rage
	table['Gloves']['explicit'].append('#% reduced Mana Cost of Skills')  # Voidbringer

	for val in ['Rune Dagger', 'Sceptre', 'Wand', 'Staff']:
		for modgroup in table[val]:
			table['Caster Weapon'][modgroup].extend(table[val][modgroup])
			table['Caster Weapon'][modgroup] = list(set(table['Caster Weapon'][modgroup]))
		del table[val]
	for val in ['Jewel', 'AbyssJewel']:
		for modgroup in table[val]:
			table['All Jewel'][modgroup].extend(table[val][modgroup])
			table['All Jewel'][modgroup] = list(set(table['All Jewel'][modgroup]))

	table["Base Jewel"] = table.pop("Jewel")
	table["Abyss Jewel"] = table.pop("AbyssJewel")

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'r_mods = {']
	for base in sorted(table):
		buf.append(f'\t"{base}": {{')
		for section in table[base]:
			table[base][section].sort()
			buf.append(f'\t\t"{section}": {table[base][section]},')
		buf.append('\t},')
	buf.append('}')
	with open("restrict_mods.py", 'w') as f:
		f.write('\n'.join(buf))
	for miss in missing:
		print(miss)


if __name__ == '__main__':
	main()
