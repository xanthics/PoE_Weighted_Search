#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# Given dps values from Path of Building, generate a search for jewels and stat sticks
# Usage
# dps: dictionary of dps values, set to 0 for unused
# miniondamage and minionattackspeet: set to true if you have specced the relevant nodes on the tree
# selections: update with a type, 0 or more class, 1 or more tags, 1 type of hands
# - This is how you control what mods are considered
from gensearchparams import gensearchparams


def main():
	dps = {
		'% fire': 0,
		'% cold': 62.2,
		'% lightning': 2.2,
		'% elemental': 64.3,
		'% chaos': 1.2,
		'% physical': 98.3,
		'% generic': 101.7,
		'crit chance': 57.6,
		'crit multi': 138.8,
		'attack speed': 0,
		'cast speed': 0,
		'pen all': 614.6,
		'pen fire': 0,
		'pen cold': 592.3,
		'pen lightning': 22.3,
		'flat phys': 66.1,
		'flat lightning': 40.4,
		'flat fire': 41.4,
		'flat cold': 41.4,
		'flat chaos': 40.9,
		'extra fire': 428.6,
		'extra cold': 433.0,
		'extra lightning': 416.6,
		'extra chaos': 904.4,
		'ele as chaos': 474.4,
		'+1 power charge': 2304.8,
		'+1 frenzy charge': 0
	}

	dps['extra random'] = (dps['extra fire'] + dps['extra cold'] + dps['extra lightning']) / 3

	# Valid selection terms are:
	# Type: Attack, Spell
	# Class: Bow, Wand, Claw, Sword, Axe, Dagger, Mace, Staff, Trap, Mine, Totem
	# Tags: Melee, Area, Projectile, Elemental, Fire, Cold, Lightning
	# Hands: Shield, Duel Wielding, Two Handed Weapon
	# Charges: Frenzy, Power
	# Minion stats: Minion Damage, Minion Attack Speed
	# Note that non-selected elements will be excluded

	selections = {'Spell', 'Mine', 'Area', 'Elemental', 'Cold', 'Shield', 'Power'}

	query = gensearchparams(dps, selections)

	print(query)
	with open('querystring.txt', 'w') as f:
		f.write(query)


if __name__ == '__main__':
	main()
