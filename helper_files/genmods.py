#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher

import json
import os
import urllib.request
from datetime import datetime


def updatemods(root_dir):
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}, 'Fractured': {}}
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
			for ii in i['entries']:
				results[i['label']][ii['id']] = ii['text']

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
	root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	updatemods(root_dir)
	updateleagues(root_dir)
	updatejsonmods(root_dir)
