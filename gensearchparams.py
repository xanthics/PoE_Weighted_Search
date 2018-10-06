#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# Given dps values from Path of Building, generates a search url for jewels and stat sticks
from modlist import mods


def gensearchparams(dps, selections):
	modstr = {
		"#% increased Area Damage": dps['% generic'] if {'Area'}.issubset(selections) else 0,
		"#% increased Attack Speed": dps['attack speed'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Attack Speed if you've dealt a Critical Strike Recently": dps['attack speed'] if {'Attack'}.issubset(selections) and {'Totem'}.isdisjoint(selections) else 0,
		"#% increased Attack Speed while Dual Wielding": dps['attack speed'] if {'Attack', 'Duel Wielding'}.issubset(selections) else 0,
		"#% increased Attack Speed while holding a Shield": dps['attack speed'] if {'Attack', 'Shield'}.issubset(selections) else 0,
		"#% increased Attack Speed with Axes": dps['attack speed'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"#% increased Attack Speed with Bows": dps['attack speed'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"#% increased Attack Speed with Claws": dps['attack speed'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"#% increased Attack Speed with Daggers": dps['attack speed'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"#% increased Attack Speed with Maces": dps['attack speed'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"#% increased Attack Speed with One Handed Melee Weapons": dps['attack speed'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Attack Speed with Staves": dps['attack speed'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"#% increased Attack Speed with Swords": dps['attack speed'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"#% increased Attack Speed with Two Handed Melee Weapons": dps['attack speed'] if {'Attack', 'Two Handed Weapon'}.issubset(selections) else 0,
		"#% increased Attack Speed with Wands": dps['attack speed'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed": dps['attack speed'] if {'Attack'}.issubset(selections) else (dps['cast speed'] if {'Spell'}.issubset(selections) else 0),
		"#% increased Cast Speed": dps['cast speed'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Cast Speed if you've dealt a Critical Strike Recently": dps['cast speed'] if {'Spell'}.issubset(selections) and {'Totem'}.isdisjoint(selections) else 0,
		"#% increased Cast Speed while Dual Wielding": dps['cast speed'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"#% increased Cast Speed while holding a Shield": dps['cast speed'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"#% increased Cast Speed while wielding a Staff": dps['cast speed'] if {'Spell', 'Staff'}.issubset(selections) else 0,
		"#% increased Cast Speed with Cold Skills": dps['cast speed'] if {'Spell', 'Cold'}.issubset(selections) else 0,
		"#% increased Cast Speed with Fire Skills": dps['cast speed'] if {'Spell', 'Fire'}.issubset(selections) else 0,
		"#% increased Cast Speed with Lightning Skills": dps['cast speed'] if {'Spell', 'Lightning'}.issubset(selections) else 0,
		"#% increased Chaos Damage": dps['% chaos'],
		"#% increased Cold Damage": dps['% cold'],
		"#% increased Critical Strike Chance": dps['crit chance'],
		"#% increased Critical Strike Chance for Spells": dps['crit chance'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance if you haven't dealt a Critical Strike Recently": dps['crit chance'] if {'Totem', 'Mine', 'Trap'} & selections else 0,
		"#% increased Weapon Critical Strike Chance while Dual Wielding": dps['crit chance'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Cold Skills": dps['crit chance'] if {'Cold'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Fire Skills": dps['crit chance'] if {'Fire'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Lightning Skills": dps['crit chance'] if {'Lightning'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with One Handed Melee Weapons": dps['crit chance'] if {'Attack', 'Melee'}.issubset(selections) and {'Two Handed Weapon'}.isdisjoint(selections) else 0,
		"#% increased Critical Strike Chance with Two Handed Melee Weapons": dps['crit chance'] if {'Attack', 'Melee', 'Two Handed Weapon'}.issubset(selections) else 0,
		"#% increased Damage": dps['% generic'],
		"#% increased Damage if you've Killed Recently": dps['% generic'] if {'Totem', 'Mine', 'Trap'}.isdisjoint(selections) else 0,
		"#% increased Damage when on Full Life": dps['% generic'],
		"#% increased Elemental Damage": dps['% elemental'],
		"#% increased Elemental Damage with Attack Skills": dps['% elemental'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Fire Damage": dps['% fire'],
		"#% increased Global Critical Strike Chance": dps['crit chance'],
		"#% increased Lightning Damage": dps['% lightning'],
		"#% increased Melee Critical Strike Chance": dps['crit chance'] if {'Melee'}.issubset(selections) else 0,
		"#% to Melee Critical Strike Multiplier": dps['crit multi'] if {'Melee'}.issubset(selections) else 0,
		"#% increased Melee Damage": dps['% generic'] if {'Melee'}.issubset(selections) else 0,
		"#% increased Melee Physical Damage while holding a Shield": dps['% generic'] if {'Melee', 'Shield'}.issubset(selections) else 0,
		"#% increased Mine Damage": dps['% generic'] if {'Mine'}.issubset(selections) else 0,
		"#% increased Global Physical Damage": dps['% physical'],
		"#% increased Physical Damage with Axes": dps['% physical'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"#% increased Physical Damage with Bows": dps['% physical'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"#% increased Physical Damage with Claws": dps['% physical'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"#% increased Physical Damage with Daggers": dps['% physical'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"#% increased Physical Damage with Maces": dps['% physical'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"#% increased Physical Damage with One Handed Melee Weapons": dps['% physical'] if {'Attack', 'Melee'}.issubset(selections) and {'Two Handed Weapon'}.isdisjoint(selections) else 0,
		"#% increased Physical Damage with Staves": dps['% physical'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"#% increased Physical Damage with Swords": dps['% physical'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"#% increased Physical Damage with Two Handed Melee Weapons": dps['% physical'] if {'Attack', 'Two Handed Weapon', 'Melee'}.issubset(selections) else 0,
		"#% increased Physical Damage with Wands": dps['% physical'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"#% increased Physical Weapon Damage while Dual Wielding": dps['% physical'] if {'Attack', 'Dual Wielding'}.issubset(selections) else 0,
		"#% increased Projectile Damage": dps['% generic'] if {'Projectile'}.issubset(selections) else 0,
		"#% increased Spell Damage": dps['% generic'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Spell Damage while holding a Shield": dps['% generic'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"#% increased Spell Damage while wielding a Staff": dps['% generic'] if {'Spell', 'Staff'}.issubset(selections) else 0,
		"#% increased Totem Damage": dps['% generic'] if {'Totem'}.issubset(selections) else 0,
		"#% increased Trap Damage": dps['% generic'] if {'Trap'}.issubset(selections) else 0,
		"#% to Global Critical Strike Multiplier": dps['crit multi'],
		"#% increased Critical Strike Chance with Elemental Skills": dps['crit chance'] if {'Elemental'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Elemental Skills": dps['crit multi'] if {'Elemental'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier for Spells": dps['crit multi'] if {'Spell'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier if you've Killed Recently": dps['crit multi'] if {'Totem', 'Mine', 'Trap'}.isdisjoint(selections) else 0,
		"#% to Critical Strike Multiplier while Dual Wielding": dps['crit multi'] if {'Dual Wielding'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Cold Skills": dps['crit multi'] if {'Cold'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Fire Skills": dps['crit multi'] if {'Fire'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Lightning Skills": dps['crit multi'] if {'Lightning'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with One Handed Melee Weapons": dps['crit multi'] if {'Melee', 'Attack'}.issubset(selections) and {'Two Handed Weapon'}.isdisjoint(selections) else 0,
		"#% to Critical Strike Multiplier with Two Handed Melee Weapons": dps['crit multi'] if {'Melee', 'Attack', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Attacks": dps['flat chaos'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells": dps['flat chaos'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while Dual Wielding": dps['flat chaos'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while holding a Shield": dps['flat chaos'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while wielding a Two Handed Weapon": dps['flat chaos'] if {'Spell', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Attacks": dps['flat cold'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Axe Attacks": dps['flat cold'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Bow Attacks": dps['flat cold'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Claw Attacks": dps['flat cold'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Dagger Attacks": dps['flat cold'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Mace Attacks": dps['flat cold'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells": dps['flat cold'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while Dual Wielding": dps['flat cold'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while holding a Shield": dps['flat cold'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while wielding a Two Handed Weapon": dps['flat cold'] if {'Spell', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Staff Attacks": dps['flat cold'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Sword Attacks": dps['flat cold'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Wand Attacks": dps['flat cold'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Attacks": dps['flat fire'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Axe Attacks": dps['flat fire'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Bow Attacks": dps['flat fire'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Claw Attacks": dps['flat fire'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Dagger Attacks": dps['flat fire'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Mace Attacks": dps['flat fire'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells": dps['flat fire'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while Dual Wielding": dps['flat fire'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while holding a Shield": dps['flat fire'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while wielding a Two Handed Weapon": dps['flat fire'] if {'Spell', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Staff Attacks": dps['flat fire'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Sword Attacks": dps['flat fire'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Wand Attacks": dps['flat fire'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Attacks": dps['flat lightning'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Axe Attacks": dps['flat lightning'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Bow Attacks": dps['flat lightning'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Claw Attacks": dps['flat lightning'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Dagger Attacks": dps['flat lightning'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Mace Attacks": dps['flat lightning'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells": dps['flat lightning'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while Dual Wielding": dps['flat lightning'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while holding a Shield": dps['flat lightning'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while wielding a Two Handed Weapon": dps['flat lightning'] if {'Spell', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Staff Attacks": dps['flat lightning'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Sword Attacks": dps['flat lightning'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Wand Attacks": dps['flat lightning'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Attacks": dps['flat phys'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Axe Attacks": dps['flat phys'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Bow Attacks": dps['flat phys'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Claw Attacks": dps['flat phys'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Dagger Attacks": dps['flat phys'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Mace Attacks": dps['flat phys'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells": dps['flat phys'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while Dual Wielding": dps['flat phys'] if {'Spell', 'Dual Wielding'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while holding a Shield": dps['flat phys'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while wielding a Two Handed Weapon": dps['flat phys'] if {'Spell', 'Two Handed Weapon'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Staff Attacks": dps['flat phys'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Sword Attacks": dps['flat phys'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Wand Attacks": dps['flat phys'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Damage Penetrates #% Cold Resistance": dps['pen cold'],
		"Damage Penetrates #% Elemental Resistance if you haven't Killed Recently": dps['pen all'],
		"Damage Penetrates #% Elemental Resistances": dps['pen all'],
		"Damage Penetrates #% Fire Resistance": dps['pen fire'],
		"Damage Penetrates #% Lightning Resistance": dps['pen lightning'],
		"Gain #% of Elemental Damage as Extra Chaos Damage": dps['ele as chaos'],
		"Gain #% of Physical Damage as Extra Cold Damage": dps['extra cold'],
		"Gain #% of Physical Damage as Extra Damage of a random Element": dps['extra random'],
		"Gain #% of Physical Damage as Extra Fire Damage": dps['extra fire'],
		"Gain #% of Physical Damage as Extra Fire Damage if you've dealt a Critical Strike Recently": dps['extra fire'],
		"Gain #% of Physical Damage as Extra Lightning Damage": dps['extra lightning'],
		"Minions deal #% increased Damage": dps['% generic'] if {'Minion Damage'}.issubset(selections) else 0,
		"Minions have #% increased Attack Speed": dps['attack speed'] if {'Minion Attack Speed'}.issubset(selections) else 0,
		"Gain #% of Non-Chaos Damage as extra Chaos Damage": dps['extra chaos'],
		'# to Maximum Power Charges': dps['+1 power charge'] if {'Power'}.issubset(selections) else 0,
		'# to Maximum Frenzy Charges': dps['+1 frenzy charge'] if {'Frenzy'}.issubset(selections) else 0,
		'# to Maximum Endurance Charges': dps['+1 endurance charge'] if {'Endurance'}.issubset(selections) else 0
	}

	# List of mods that will go in to a 'not' filter so that certain items will never appear
	# These items have high values of damage mods with some downside that is not accounted for
	ignoredmods = [
		'#% less Critical Strike Chance',  # Marylene's Fallacy
		'Lose all Power Charges on reaching Maximum Power Charges'  # Malachai's Loop
	]

	mlist = {}
	notquery = []
	notitem = '{{"id":"{}"}}'
	for mod in mods:
		if mods[mod] in modstr:
			if modstr[mods[mod]]:
				mlist[mod] = modstr[mods[mod]]
		if mods[mod] in ignoredmods:
			notquery.append(notitem.format(mod))

	searchstring = 'https://www.pathofexile.com/api/trade/search/Delve?redirect&source={{"query":{{"filters":{{"type_filters": {{"filters": {{"category": {{"option": "jewel"}}}}}}}},"status":{{"option":"online"}},"stats":[{{"type":"weight","value":{{"min":7500}},"filters":[{}]}},{{"type":"not","filters":[{}]}}]}}}}'
	item = '{{"id":"{}","value":{{"weight":{}}}}}'
	query = []
	for i in mlist:
		query.append(item.format(i, mlist[i]))
	return searchstring.format(','.join(query), ','.join(notquery))

