#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.6.x or higher
import unittest
import json
from gensearchparams import gensearchparams


class TestGenSearchParams(unittest.TestCase):
	# Test function to pass all possible flags and dps values to see if anything breaks
	def test_gensearchparams(self):
		selections = {'useFrenzyCharges', 'usePowerCharges', 'useEnduranceCharges', 'Attack', 'Spell', 'Mace', 'Bow', 'Wand', 'Claw', 'Staff', 'Sword', 'Axe', 'Dagger', 'Trap', 'Mine', 'Totem', 'Melee', 'Area', 'Projectile', 'Elemental', 'Fire', 'Cold', 'Lightning',
					  'Shield', 'DualWielding', 'TwoHandedWeapon', 'conditionKilledRecently', 'conditionCritRecently', 'conditionHitRecently', 'conditionMinionsKilledRecently', 'No Recent Crit', 'conditionUsedMinionSkillRecently', 'No Recent Kill',
					  'conditionUsingFlask', 'Elder', 'conditionFullLife', 'Shaper', 'conditionEnemyBleeding', 'conditionEnemyPoisoned', 'conditionEnemyBlinded', 'conditionEnemyIgnited', 'conditionEnemyBurning', 'conditionEnemyShocked', 'conditionEnemyChilled',
					  'conditionEnemyFrozen', 'NoCraftedMods', 'NearbyRareUnique'}
		with open("mods.json", 'r') as f:
			vals = json.load(f)
		dps = {}
		for val in vals + [{'name': 'PowerCount'}, {'name': 'FrenzyCount'}, {'name': 'EnduranceCount'}, {'name': 'extrarandom'}]:
			dps[val['name']] = 10
		gensearchparams(dps, selections)


if __name__ == '__main__':
	unittest.main()
