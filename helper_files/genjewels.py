#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# This program generates all the jewels that need to be added to Path of Building
import json
import os


def gentxt(names, root_dir):
	header = '''
Rarity: Rare
{0}
Hypnotic Eye Jewel
--------
Item Level: 1
--------
{0}
	
	'''

	with open(f'{root_dir}/jewellist.txt', 'w') as fout:
		for name in names:
			fout.write(header.format(name))


# as pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly
# These should be added directly after the <SharedItems> tag
# <Shared Items> should be right after </Accounts>
def genxml(names, root_dir):
	header = '''		<Item>
			Rarity: RARE
{0}
Hypnotic Eye Jewel
Item Level: 1
Implicits: 0
{0}
		</Item>
'''

	with open(f'{root_dir}/jewellistxml.txt', 'w') as fout:
		for name in names:
			fout.write(header.format(name))


if __name__ == '__main__':
	g_root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	with open(f'{g_root_dir}/mods.json') as fin:
		g_data = json.load(fin)
		g_names = [x['desc'] for x in g_data]
	gentxt(g_names, g_root_dir)
	genxml(g_names, g_root_dir)
