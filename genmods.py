#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher

import json
import urllib.request


def main():
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}}
	modurl="https://www.pathofexile.com/api/trade/data/stats"
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
	req = urllib.request.Request(modurl, headers=headers)
	data = urllib.request.urlopen(req)
	vals = json.load(data)
	for i in vals['result']:
		if i['label'] in ['Explicit', 'Implicit', 'Crafted']:
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

	with open('modlist.py', 'w') as f:
		f.write('''#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher\n''')
		f.write('mods = {\n')
		for label in sorted(mlist):
			f.write('\t"{}": ["{}"],\n'.format(label, '", "'.join(mlist[label])))
		f.write('}\n')


if __name__ == "__main__":
	main()