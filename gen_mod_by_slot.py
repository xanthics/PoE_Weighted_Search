import json


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
				if tag != 'default':
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
	taglookup = {
		'amulet': ['Amulet'],
		'body_armour': ['Body Armour'],
		'boots': ['Boots'],
		'gloves': ['Gloves'],
		'helmet': ['Helmet'],
		'shield': ['Shield'],
		'belt': ['Belt'],
		'abyss_jewel': ['AbyssJewel'],
		"abyss_jewel_melee": ['AbyssJewel'],
		"abyss_jewel_ranged": ['AbyssJewel'],
		"abyss_jewel_summoner": ['AbyssJewel'],
		"abyss_jewel_caster": ['AbyssJewel'],
		'jewel': ['Jewel'],
		'quiver': ['Quiver'],
		'ring': ['Ring'],
		'dagger': ['Rune Dagger'],
		'sceptre': ['Sceptre'],
		'wand': ['Wand'],
		'staff': ['Staff'],
		'armour': ['Body Armour', 'Boots', 'Gloves', 'Helmet', 'Shield']
	}
	taglookup.update(ibr)
	taglookup.update(taglookups)
	missing = []
	for m in taglookup:
		taglookup[m] = list(set(taglookup[m]))
	table = {key: {'implicit': [], 'crafted': [], 'explicit': []} for key in allowed_bases}
	for mod in modlist:
		for attr in modlist[mod]:
			if (mods[attr]['domain'] == 'crafted' and attr not in crafted) or \
					(mods[attr]['generation_type'] == 'corrupted' and not any([m['weight'] for m in mods[attr]['spawn_weights']])) or \
					(mods[attr]['is_essence_only'] and attr not in essence) or \
					(attr not in implicits and
					 attr not in crafted and
					 attr not in essence and
					 ((not any([m['weight'] for m in mods[attr]['spawn_weights']])) and len(mods[attr]['spawn_weights']) < 2)):
				continue
			if mods[attr]['generation_type'] == 'corrupted':
				for m in mods[attr]['spawn_weights']:
					if m['weight'] and m['tag'] in taglookup:
						for base in taglookup[m['tag']]:
							if mod not in table[base]['implicit']:
								table[base]['implicit'].append(mod)
							if base == 'Jewel':
								if mod not in table['AbyssJewel']['implicit']:
									table['AbyssJewel']['implicit'].append(mod)
			elif mods[attr]['is_essence_only']:
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
				if len(mods[attr]['spawn_weights']) > 1:
					for spawn in mods[attr]['spawn_weights']:
						if spawn["weight"]:
							if spawn['tag'] not in taglookup:
								if spawn['tag'] not in missing:
									missing.append(spawn['tag'])
							else:
								for base in taglookup[spawn['tag']]:
									if mod not in table[base]['explicit']:
										table[base]['explicit'].append(mod)
			else:
				print(attr)
	table['Caster Weapon'] = {'implicit': [], 'crafted': [], 'explicit': []}
	table['All Jewel'] = {'implicit': [], 'crafted': [], 'explicit': []}

	for val in ['Rune Dagger', 'Sceptre', 'Wand', 'Staff']:
		for modgroup in table[val]:
			table['Caster Weapon'][modgroup].extend(table[val][modgroup])
			table['Caster Weapon'][modgroup] = list(set(table['Caster Weapon'][modgroup]))
		del table[val]
	for val in ['Jewel', 'AbyssJewel']:
		for modgroup in table[val]:
			table['All Jewel'][modgroup].extend(table[val][modgroup])
			table['All Jewel'][modgroup] = list(set(table['All Jewel'][modgroup]))

	buf = 'mods = {\n'
	for base in table:
		buf += f'\t"{base}": {{\n'
		for section in table[base]:
			table[base][section].sort()
			buf += f'\t\t"{section}": {table[base][section]},\n'
		buf += '\t},\n'
	buf += '}'
	with open("restrict_mods.py", 'w') as f:
		f.write(buf)
	print(missing)


if __name__ == '__main__':
	main()
