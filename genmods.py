#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher

import json
import urllib.request
from datetime import datetime


def updatemods():
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}, 'Fractured': {}}
	modurl = "https://www.pathofexile.com/api/trade/data/stats"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib.request.Request(modurl, headers=headers)
	data = urllib.request.urlopen(req)
	vals = json.load(data)
	for i in vals['result']:
		if i['label'] in ['Explicit', 'Implicit', 'Crafted', 'Fractured']:
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

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", 'mods = {\n']

	for label in sorted(mlist):
		mlist[label].sort()
		buf.append('\t"{}": ["{}"],'.format(label, '", "'.join(mlist[label])))
	buf.append('}')

	with open('modlist.py', 'w') as f:
		f.write('\n'.join(buf))


def updateleagues():
	leagueurl = "http://api.pathofexile.com/leagues?realm=pc&compact=1"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib.request.Request(leagueurl, headers=headers)
	data = urllib.request.urlopen(req)
	vals = json.load(data)

	buf = ["#!/usr/bin/python", "# -*- coding: utf-8 -*-", f"# Generated: {datetime.utcnow().strftime('%m/%d/%Y(m/d/y) %H:%M:%S')} utc", f"leagues = {[x['id'] for x in vals if not x['id'].startswith('SSF')]}"]
	with open('leaguelist.py', 'w') as f:
		f.write('\n'.join(buf))


if __name__ == "__main__":
	updatemods()
	updateleagues()
