#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher

import json
import urllib.request


def main():
	results = {'Explicit': {}, 'Implicit': {}, 'Crafted': {}}
	modurl="https://www.pathofexile.com/api/trade/data/stats"
	data = urllib.request.urlopen(modurl)
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