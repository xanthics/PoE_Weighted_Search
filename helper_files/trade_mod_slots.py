import requests
import json
import os
from ratelimit import limits, sleep_and_retry
from helper_files.goodmod import goodmod
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
def gen_mod_map(themods, goodmods):
	mod_count = 150  # number of mods to check at a time
	cookies = {'POESESSID': ''}
	headers = {'User-Agent': 'poe weighted search mod gen tool', 'From': 'poe discord: xan#7840'}
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


if __name__ == "__main__":
	root_dir_g = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open('modmap.json', 'r') as fi:
		knownmods = json.load(fi)
	mymods = genmods(knownmods)
#	gen_mod_map(mymods, knownmods)
	gen_restrict_mods(knownmods, root_dir_g)

