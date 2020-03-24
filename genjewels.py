#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# This program generates all the jewels that need to be added to Path of Building
import json


def gentxt(names):
	header = '''
Rarity: Rare
{0}
Hypnotic Eye Jewel
--------
Item Level: 1
--------
{0}
	
	'''

	with open('jewellist.txt', 'w') as fout:
		for name in names:
			fout.write(header.format(name))


# as pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly
# These should be added directly after the <SharedItems> tag
# <Shared Items> should be right after </Accounts>
def genxml(names):
	header = '''		<Item>
			Rarity: RARE
{0}
Hypnotic Eye Jewel
Item Level: 1
Implicits: 0
{0}
		</Item>
'''

	with open('jewellistxml.txt', 'w') as fout:
		for name in names:
			fout.write(header.format(name))


if __name__ == '__main__':
	with open('mods.json') as fin:
		data = json.load(fin)
		g_names = [x['desc'] for x in data]
	gentxt(g_names)
	genxml(g_names)
