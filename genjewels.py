#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# This program generates all the jewels that need to be added to Path of Building


def gentxt():
	header = '''
Rarity: Rare
{0}
Prismatic Jewel
--------
Item Level: 1
--------
{0}
	
	'''

	with open('mods.txt') as fin, open('jewellist.txt', 'w') as fout:
		for line in fin:
			line = line.strip('\n')
			fout.write(header.format(line))

# as pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly
# These should be added directly after the <SharedItems> tag
# <Shared Items> should be right after </Accounts>
def genxml():
	header = '''		<Item>
			Rarity: RARE
{0}
Prismatic Jewel
Item Level: 1
Implicits: 0
{0}
		</Item>
'''

	with open('mods.txt') as fin, open('jewellistxml.txt', 'w') as fout:
		for line in fin:
			line = line.strip('\n')
			fout.write(header.format(line))


if __name__ == '__main__':
	gentxt()
	genxml()
