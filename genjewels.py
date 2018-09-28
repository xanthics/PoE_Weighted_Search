#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# This program generates all the jewels that need to be added to Path of Building

header = '''
Rarity: Rare
{}
Prismatic Jewel
--------
Item Level: 1
--------
'''

with open('mods.txt') as fin, open('jewellist.txt', 'w') as fout:
	for line in fin:
		line = line.strip('\n')
		fout.write(header.format(line)+line+'\n')
