#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.3.x or higher
# Given dps values from Path of Building, generates a search url for jewels and stat sticks
from modlist import mods


def gensearchparams(dps, selections):
	modstr = {
		"#% increased Area Damage": dps['% generic'] if {'Area'}.issubset(selections) else 0,
		"#% increased Attack Speed": dps['attack speed'],
		"#% increased Attack Speed if you've dealt a Critical Strike Recently": dps['attack speed'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Attack Speed while Dual Wielding": dps['attack speed'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Attack Speed while holding a Shield": dps['attack speed'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Attack Speed with Axes": dps['attack speed'] if {'Axe'}.issubset(selections) else 0,
		"#% increased Attack Speed with Bows": dps['attack speed'] if {'Bow'}.issubset(selections) else 0,
		"#% increased Attack Speed with Claws": dps['attack speed'] if {'Claw'}.issubset(selections) else 0,
		"#% increased Attack Speed with Daggers": dps['attack speed'] if {'Dagger'}.issubset(selections) else 0,
		"#% increased Attack Speed with Maces": dps['attack speed'] if {'Mace'}.issubset(selections) else 0,
		"#% increased Attack Speed with One Handed Melee Weapons": dps['attack speed'] if {'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Attack Speed with Staves": dps['attack speed'] if {'Staff'}.issubset(selections) else 0,
		"#% increased Attack Speed with Swords": dps['attack speed'] if {'Sword'}.issubset(selections) else 0,
		"#% increased Attack Speed with Two Handed Melee Weapons": dps['attack speed'] if {'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Attack Speed with Wands": dps['attack speed'] if {'Wand'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed": dps['attack speed'] + dps['cast speed'],
		"#% increased Cast Speed": dps['cast speed'],
		"#% increased Cast Speed if you've dealt a Critical Strike Recently": dps['cast speed'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Cast Speed while Dual Wielding": dps['cast speed'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Cast Speed while holding a Shield": dps['cast speed'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Cast Speed while wielding a Staff": dps['cast speed'] if {'Staff'}.issubset(selections) else 0,
		"#% increased Cast Speed with Cold Skills": dps['cast speed'] if {'Cold'}.issubset(selections) else 0,
		"#% increased Cast Speed with Fire Skills": dps['cast speed'] if {'Fire'}.issubset(selections) else 0,
		"#% increased Cast Speed with Lightning Skills": dps['cast speed'] if {'Lightning'}.issubset(selections) else 0,
		"#% increased Elemental Damage if you've dealt a Critical Strike Recently": dps['% elemental'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Chaos Damage": dps['% chaos'],
		"#% increased Cold Damage": dps['% cold'],
		"#% increased Critical Strike Chance": dps['crit chance'],
		"#% increased Critical Strike Chance for Spells": dps['crit chance'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance if you haven't dealt a Critical Strike Recently": dps['crit chance'] if {'No Recent Crit'}.issubset(selections) else 0,
		"#% increased Weapon Critical Strike Chance while Dual Wielding": dps['crit chance'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Cold Skills": dps['crit chance'] if {'Cold'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Fire Skills": dps['crit chance'] if {'Fire'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Lightning Skills": dps['crit chance'] if {'Lightning'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with One Handed Melee Weapons": dps['crit chance'] if {'Attack', 'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Critical Strike Chance with Two Handed Melee Weapons": dps['crit chance'] if {'Attack', 'Melee', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Damage": dps['% generic'],
		'#% increased Attack Damage': dps['% generic'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Damage if you've Killed Recently": dps['% generic'] if {'conditionKilledRecently'}.issubset(selections) else 0,
		"#% increased Damage when on Full Life": dps['% generic'] if {'conditionFullLife'}.issubset(selections) else 0,
		"#% increased Elemental Damage": dps['% elemental'],
		"#% increased Elemental Damage with Attack Skills": dps['% elemental'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Fire Damage": dps['% fire'],
		"#% increased Global Critical Strike Chance": dps['crit chance'],
		"#% increased Lightning Damage": dps['% lightning'],
		"#% increased Melee Critical Strike Chance": dps['crit chance'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% to Melee Critical Strike Multiplier": dps['crit multi'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Melee Damage": dps['% generic'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Melee Physical Damage while holding a Shield": dps['% generic'] if {'Attack', 'Melee', 'Shield'}.issubset(selections) else 0,
		"#% increased Mine Damage": dps['% generic'] if {'Mine'}.issubset(selections) else 0,
		"#% increased Global Physical Damage": dps['% physical'],
		"#% increased Physical Damage with Axes": dps['% physical'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"#% increased Physical Damage with Bows": dps['% physical'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"#% increased Physical Damage with Claws": dps['% physical'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"#% increased Physical Damage with Daggers": dps['% physical'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"#% increased Physical Damage with Maces": dps['% physical'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"#% increased Physical Damage with One Handed Melee Weapons": dps['% physical'] if {'Attack', 'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Physical Damage with Staves": dps['% physical'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"#% increased Physical Damage with Swords": dps['% physical'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"#% increased Physical Damage with Two Handed Melee Weapons": dps['% physical'] if {'Attack', 'TwoHandedWeapon', 'Melee'}.issubset(selections) else 0,
		"#% increased Physical Damage with Wands": dps['% physical'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"#% increased Physical Weapon Damage while Dual Wielding": dps['% physical'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
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
		"#% to Critical Strike Multiplier if you've Killed Recently": dps['crit multi'] if {'conditionKilledRecently'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier while Dual Wielding": dps['crit multi'] if {'DualWielding'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Cold Skills": dps['crit multi'] if {'Cold'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Fire Skills": dps['crit multi'] if {'Fire'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Lightning Skills": dps['crit multi'] if {'Lightning'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with One Handed Melee Weapons": dps['crit multi'] if {'Melee', 'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% to Critical Strike Multiplier with Two Handed Melee Weapons": dps['crit multi'] if {'Melee', 'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Attacks": dps['flat chaos'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells": dps['flat chaos'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while Dual Wielding": dps['flat chaos'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while holding a Shield": dps['flat chaos'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while wielding a Two Handed Weapon": dps['flat chaos'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage": dps['flat chaos'],
		"Adds # to # Chaos Damage if you've dealt a Critical Strike Recently": dps['flat chaos'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Attacks": dps['flat cold'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Axe Attacks": dps['flat cold'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Bow Attacks": dps['flat cold'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Claw Attacks": dps['flat cold'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Dagger Attacks": dps['flat cold'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Mace Attacks": dps['flat cold'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells": dps['flat cold'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while Dual Wielding": dps['flat cold'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while holding a Shield": dps['flat cold'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while wielding a Two Handed Weapon": dps['flat cold'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Staff Attacks": dps['flat cold'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Sword Attacks": dps['flat cold'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Wand Attacks": dps['flat cold'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Cold Damage": dps['flat cold'],
		"Adds # to # Cold Damage to Spells and Attacks": dps['flat cold'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Fire Damage to Attacks": dps['flat fire'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Axe Attacks": dps['flat fire'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Bow Attacks": dps['flat fire'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Claw Attacks": dps['flat fire'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Dagger Attacks": dps['flat fire'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Mace Attacks": dps['flat fire'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells": dps['flat fire'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while Dual Wielding": dps['flat fire'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while holding a Shield": dps['flat fire'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while wielding a Two Handed Weapon": dps['flat fire'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Staff Attacks": dps['flat fire'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Sword Attacks": dps['flat fire'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Wand Attacks": dps['flat fire'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Fire Damage": dps['flat fire'],
		"Adds # to # Fire Damage to Spells and Attacks": dps['flat fire'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Lightning Damage to Attacks": dps['flat lightning'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Axe Attacks": dps['flat lightning'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Bow Attacks": dps['flat lightning'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Claw Attacks": dps['flat lightning'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Dagger Attacks": dps['flat lightning'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Mace Attacks": dps['flat lightning'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells": dps['flat lightning'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while Dual Wielding": dps['flat lightning'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while holding a Shield": dps['flat lightning'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while wielding a Two Handed Weapon": dps['flat lightning'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Staff Attacks": dps['flat lightning'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Sword Attacks": dps['flat lightning'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Wand Attacks": dps['flat lightning'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage": dps['flat lightning'],
		"Adds # to # Lightning Damage to Spells and Attacks": dps['flat lightning'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Physical Damage to Attacks": dps['flat phys'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Axe Attacks": dps['flat phys'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Bow Attacks": dps['flat phys'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Claw Attacks": dps['flat phys'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Dagger Attacks": dps['flat phys'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Mace Attacks": dps['flat phys'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells": dps['flat phys'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while Dual Wielding": dps['flat phys'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while holding a Shield": dps['flat phys'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while wielding a Two Handed Weapon": dps['flat phys'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Staff Attacks": dps['flat phys'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Sword Attacks": dps['flat phys'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Wand Attacks": dps['flat phys'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Physical Damage": dps['flat phys'],
		"Damage Penetrates #% Cold Resistance": dps['pen cold'],
		"Damage Penetrates #% Cold Resistance against Chilled Enemies": dps['pen cold'] if {'conditionEnemyChilled'}.issubset(selections) else 0,
		"Damage Penetrates #% Elemental Resistance if you haven't Killed Recently": dps['pen all'] if {'No Recent Kill'}.issubset(selections) else 0,
		"Damage Penetrates #% Elemental Resistances": dps['pen all'],
		"Damage Penetrates #% Fire Resistance": dps['pen fire'],
		"Damage Penetrates #% Lightning Resistance": dps['pen lightning'],
		"Gain #% of Elemental Damage as Extra Chaos Damage": dps['ele as chaos'],
		"Gain #% of Physical Damage as Extra Cold Damage": dps['extra cold'],
		"Gain #% of Physical Damage as Extra Damage of a random Element": dps['extra random'],
		"Gain #% of Physical Damage as Extra Fire Damage": dps['extra fire'],
		"Gain #% of Physical Damage as Extra Fire Damage if you've dealt a Critical Strike Recently": dps['extra fire'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Gain #% of Physical Damage as Extra Lightning Damage": dps['extra lightning'],
		"Gain #% of Non-Chaos Damage as extra Chaos Damage": dps['extra chaos'],
		'# to Maximum Power Charges': dps['+1 power charge'] if {'Power'}.issubset(selections) else 0,
		'# to Maximum Frenzy Charges': dps['+1 frenzy charge'] if {'Frenzy'}.issubset(selections) else 0,
		'# to Maximum Endurance Charges': dps['+1 endurance charge'] if {'Endurance'}.issubset(selections) else 0,
		'# to Accuracy Rating': dps['flat accuracy'],
		'#% increased Global Accuracy Rating': dps['% accuracy'],
		"#% increased Accuracy Rating if you haven't Killed Recently": dps['% accuracy'] if {'No Recent Kill'}.issubset(selections) else 0,
		'# to Strength': dps['20 str'],
		'# to Intelligence': dps['20 int'],
		'# to Dexterity': dps['20 dex'],
		'# to Strength and Intelligence': dps['20 str'] + dps['20 int'],
		'# to Strength and Dexterity': dps['20 str'] + dps['20 dex'],
		'# to Dexterity and Intelligence': dps['20 int'] + dps['20 dex'],
		'# to all Attributes': dps['20 int'] + dps['20 dex'] + dps['20 str'],
		'#% increased Damage per 15 Dexterity': dps['damage per dex'],
		'#% increased Damage per 15 Intelligence': dps['damage per int'],
		'#% increased Damage per 15 Strength': dps['damage per str'],
		"#% increased Critical Strike Chance during any Flask Effect": dps['crit chance'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier during any Flask Effect": dps['crit multi'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Damage Penetrates #% Elemental Resistances during any Flask Effect": dps['pen all'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Damage during any Flask Effect": dps['% generic'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Damage Penetrates #% Lightning Resistance during Flask effect": dps['pen lightning'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells during Flask effect": dps['flat lightning'] if {'conditionUsingFlask', 'Spell'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Attacks during Flask effect": dps['flat lightning'] if {'conditionUsingFlask', 'Attack'}.issubset(selections) else 0,
		"#% increased Attack Speed during any Flask Effect": dps['attack speed'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Cast Speed during any Flask Effect": dps['cast speed'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Melee Damage during any Flask Effect": dps['% generic'] if {'conditionUsingFlask', 'Attack', 'Melee'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells and Attacks during any Flask Effect": dps['flat chaos'] if {'conditionUsingFlask'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"#% increased Spell Damage during any Flask Effect": dps['% generic'] if {'conditionUsingFlask', 'Spell'}.issubset(selections) else 0,
		"#% increased Elemental Damage with Attack Skills during any Flask Effect": dps['% elemental'] if {'conditionUsingFlask', 'Attack'}.issubset(selections) else 0,
		"Damage Penetrates #% Fire Resistance against Blinded Enemies": dps['pen fire'] if {'Blinded'}.issubset(selections) else 0,
		"#% increased Damage with Hits and Ailments against Blinded Enemies": dps['% generic'] if {'Blinded'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"#% increased Fire Damage with Hits and Ailments against Blinded Enemies": dps['% fire'] if {'Blinded'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"#% increased Critical Strike Chance against Blinded Enemies": dps['crit chance'] if {'Blinded'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed if you've Hit an Enemy Recently": dps['attack speed'] + dps['cast speed'] if {'conditionHitRecently'}.issubset(selections) else 0,
		"#% increased Damage per 5 of your lowest Attribute": dps['% lowest'],
		"#% increased Attributes": dps['% str'] + dps['% dex'] + dps['% int'],
		"#% increased Strength": dps['% str'],
		"#% increased Intelligence": dps['% int'],
		"#% increased Dexterity": dps['% dex'],
		"#% increased Attack Damage if your other Ring is a Shaper Item": dps['% generic'] if {'Shaper', 'Attack'}.issubset(selections) else 0,
		"#% increased Spell Damage if your other Ring is an Elder Item": dps['% generic'] if {'Elder', 'Spell'}.issubset(selections) else 0,
		"# to # Cold Damage per Frenzy Charge": dps['flat cold'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Accuracy Rating per Frenzy Charge": dps['% accuracy'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance per Frenzy Charge": dps['crit chance'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Damage per Frenzy Charge": dps['% generic'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"Gain #% of Cold Damage as Extra Chaos Damage per Frenzy Charge": dps['cold as extra chaos'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"# to # Fire Damage per Endurance Charge": dps['flat fire'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed per Endurance Charge": (dps['attack speed'] + dps['cast speed']) * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance per Endurance Charge": dps['crit chance'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Damage per Endurance Charge": dps['% generic'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"Gain #% of Fire Damage as Extra Chaos Damage per Endurance Charge": dps['fire as extra chaos'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"# to # Lightning Damage per Power Charge": dps['flat lightning'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed per Power Charge": (dps['attack speed'] + dps['cast speed']) * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Damage per Power Charge": dps['% generic'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Spell Damage per Power Charge": dps['% generic'] * dps["PowerCount"] if {'usePowerCharges', 'Spell'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier per Power Charge": dps['crit multi'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"Gain #% of Lightning Damage as Extra Chaos Damage per Power Charge": dps['lightning as extra chaos'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Damage over Time": dps['% dot'],
		"#% increased Damage over Time while Dual Wielding": dps['% dot'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Damage over Time while holding a Shield": dps['% dot'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Damage over Time while wielding a Two Handed Weapon": dps['% dot'] if {'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Damage with Ailments": dps['% dot'],
		"#% increased Damage with Bleeding": dps['% bleed'],
		"Adds # to # Physical Damage against Bleeding Enemies": dps['flat phys'] if {'conditionEnemyBleeding'}.issubset(selections) else 0,
		"Adds # to # Physical Damage against Poisoned Enemies": dps['flat phys'] if {'conditionEnemyPoisoned'}.issubset(selections) else 0,
		"#% increased Damage with Poison": dps['% poison'],
		"#% increased Critical Strike Chance against Poisoned Enemies": dps['crit chance'] if {'Poisoned'}.issubset(selections) else 0,
		"Adds # to # Fire Damage against Ignited Enemies": dps['flat fire'] if {'conditionEnemyIgnited'}.issubset(selections) else 0,
		"# to # added Fire Damage against Burning Enemies": dps['flat fire'] if {'conditionEnemyBurning'}.issubset(selections) else 0,
		"#% increased Burning Damage": dps['% ignite'],
		"#% increased Damage with Hits against Chilled Enemies": dps['% generic'] if {'conditionEnemyChilled'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Cold Damage against Chilled or Frozen Enemies": dps['flat cold'] if {'conditionEnemyChilled', 'conditionEnemyFrozen'}.intersection(selections) else 0,
		"#% increased Critical Strike Chance against Shocked Enemies": dps['crit chance'] if {'conditionEnemyShocked'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage against Shocked Enemies": dps['flat lightning'] if {'conditionEnemyShocked'}.issubset(selections) else 0,
		"# to maximum Life": dps['flat life'],
		"#% increased maximum Life": dps['% life'],
		"# to maximum Energy Shield": dps['flat es'],
		"#% increased maximum Energy Shield": dps['% es'],
		"Minions deal #% increased Damage": dps['% minion'],
		"Minions have #% increased Attack Speed": dps['minion attack speed'],
		"Minions have #% increased Cast Speed": dps['minion cast speed'],
		"Minions have #% increased Attack and Cast Speed if you or your Minions have Killed Recently": dps['minion attack speed'] + dps['minion cast speed'] if {'conditionKilledRecently', 'conditionMinionsKilledRecently'}.intersection(selections) else 0,
		"#% increased Minion Damage if you've used a Minion Skill Recently": dps['% minion'] if {'conditionUsedMinionSkillRecently'}.issubset(selections) else 0,
		"Minions deal # to # additional Physical Damage": dps['minion flat phys'],
		"Minions deal # to # additional Lightning Damage": dps['minion flat lightning'],
		"Minions deal # to # additional Cold Damage": dps['minion flat cold'],
		"Minions deal # to # additional Fire Damage": dps['minion flat fire'],
		"Minions deal # to # additional Chaos Damage": dps['minion flat chaos'],
		"#% to Cold Damage over Time Multiplier": dps['% colddotmulti'],
		"#% to Non-Ailment Chaos Damage over Time Multiplier": dps['% chaosdotmulti'],
	}

	# mods that are explicitly skipped, comment with where they appear
	disabled = {
		# Veruso's Battering Rams
		"#% increased Melee Damage per Endurance Charge": dps['% generic'] * dps["EnduranceCount"] if {'Endurance', 'Melee'}.issubset(selections) else 0,
		# Surgebinders
		"#% increased Elemental Damage per Frenzy Charge": dps['% elemental'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Tidebreaker and Surgebinders
		"#% increased Physical Damage per Endurance Charge": dps['% physical'] * dps["EnduranceCount"] if {'Endurance'}.issubset(selections) else 0,
		# Snakebite
		"#% increased Attack Speed per Frenzy Charge": dps['attack speed'] * dps["FrenzyCount"] if {'Frenzy', 'Attack'}.issubset(selections) else 0,
		# The Blood Dance
		"#% increased Attack and Cast Speed per Frenzy Charge": dps['attack speed'] * dps["FrenzyCount"] if {'Attack', 'Frenzy'}.issubset(selections) else (dps['cast speed'] * dps["FrenzyCount"] if {'Spell', 'Frenzy'}.issubset(selections) else 0),
		# Tulfall
		"#% increased Cold Damage per Frenzy Charge": dps['% cold'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Hyaon's Fury
		"#% increased Lightning Damage per Frenzy Charge": dps['% lightning'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Nebuloch
		"Adds # to # Physical Damage per Endurance Charge": dps['flat phys'] * dps["EnduranceCount"] if {'Endurance'}.issubset(selections) else 0,
		# Cane of Unravelling
		"#% increased Cast Speed per Power Charge": dps['cast speed'] * dps["PowerCount"] if {'Power'}.issubset(selections) else 0,
		# The Aylardex
		"#% increased Critical Strike Chance per Power Charge": dps['crit chance'] * dps["PowerCount"] if {'Power'}.issubset(selections) else 0,
		# Victario's Acuity
		"#% increased Projectile Damage per Power Charge": dps['% generic'] * dps["PowerCount"] if {'Power', 'Projectile'}.issubset(selections) else 0,
		# Shimmeron
		"Adds # to # Lightning Damage to Spells per Power Charge": dps['flat lightning'] * dps["PowerCount"] if {'Power', 'Spell'}.issubset(selections) else 0,
		# Farrul's Pounce
		"#% increased Damage with Hits and Ailments against Bleeding Enemies": 0,
		"# to Accuracy against Bleeding Enemies": 0,
		# Witchfire Brew
		"#% increased Damage Over Time during Flask Effect": 0,
		# Yoke of Suffering and Leper's Alms
		"#% increased Duration of Ailments on Enemies": 0,
		# Kondo's Pride
		"#% increased Melee Damage against Bleeding Enemies": 0,
		# Goredrill, Haemophellia, corrupted axe implicit
		"#% increased Attack Damage against Bleeding Enemies": 0,
		# Maligaro's Cruelty
		"#% increased Damage with Poison per Frenzy Charge": 0,
		"#% increased Poison Duration per Power Charge": 0,
		# Fenumus' Toxins
		"#% increased Damage with Poison per Power Charge": 0,
		# Coralito's Signature
		"#% increased Duration of Poisons you inflict during Flask effect": 0,
		# Razor of the Seventh Sun
		"#% increased Burning Damage if you've Ignited an Enemy Recently": 0,
		"#% increased Melee Physical Damage against Ignited Enemies": 0,
		# Gang's Momentum
		"#% increased Damage against Ignited Enemies": 0,
		# Dyadus
		"#% increased Damage with Ignite inflicted on Chilled Enemies": 0,
		# Brutus' Lead Sprinkler
		"Adds # to # Fire Damage to Attacks against Ignited Enemies": 0,
		# Stormfire
		"Adds # to # Lightning Damage to Hits against Ignited Enemies": 0,
		# Cospri's Malice
		"#% increased Critical Strike Chance against Chilled Enemies": 0,
		# Tasalio's Sign
		"Adds # to # Cold Damage against Chilled Enemies": 0,
		"Adds # to # Physical Damage to Attacks against Frozen Enemies": 0,
		# Spine of the First Claimant
		"#% increased Damage with Hits against Frozen Enemies": 0,
		# The Halcyon
		"#% increased Damage if you've Frozen an Enemy Recently": 0,
		# Valako's Sign
		"#% increased Damage with Hits against Shocked Enemies": 0,
		# Inpulsa's Broken Heart
		"#% increased Damage if you have Shocked an Enemy Recently": 0,
		# Singularity
		"#% increased Damage with Hits and Ailments against Hindered Enemies": 0,
		# Shaper's Touch
		"# Accuracy Rating per 2 Intelligence": 0,
		"# Life per 4 Dexterity": 0,
		"# maximum Energy Shield per 5 Strength": 0,
		# The Green Dream/Nightmare
		"Gain #% of Cold Damage as Extra Chaos Damage": 0,
		# The Red Dream/Nightmare
		"Gain #% of Fire Damage as Extra Chaos Damage": 0,
		# The Blue Dream/Nightmare
		"Gain #% of Lightning Damage as Extra Chaos Damage": 0,
		# The Grey Spire, The Dark Seer, Fencoil, Mirebough
		"#% increased Global Damage": 0,
		# Speaker's Wreath
		"#% increased Minion Attack Speed per 50 Dexterity": 0,
		# The Scourge
		"#% increased Minion Damage if you've used a Minion Skill Recently": 0,
		# Null's Inclination
		"Minions deal #% increased Damage per 10 Dexterity": 0,
		# Grip of the Council
		"Minions gain #% of Physical Damage as Extra Cold Damage": 0,
		# Clayshaper
		"Minions' Attacks deal # to # additional Physical Damage": 0,
		# Hyperboreus
		"#% increased Damage with Hits and Ailments against Chilled Enemies": 0,
		# Only appears on flasks
		"#% increased Critical Strike Chance during Flask Effect": 0,
	}

	# TODO: Determine if each mod is worth adding or specific to a static unique
	# mods that have not been processed yet
	queued = {
		"#% Critical Strike Multiplier while there is a Rare or Unique Enemy Nearby": 0,
		"#% increased Attack Speed while a Rare or Unique Enemy is Nearby": 0,

		"#% increased Bleeding Duration": 0,
		"#% increased Poison Duration": 0,
		"#% Critical Strike Chance per Power Charge": 0,  # Note that this is base crit.
		"# to Accuracy Rating while at Maximum Frenzy Charges": 0,
		"# to Maximum Life per 10 Dexterity": 0,
		"# to Maximum Life per 2 Intelligence": 0,
		"#% Global Critical Strike Multiplier while you have no Frenzy Charges": 0,
		"#% increased Attack Critical Strike Chance per 200 Accuracy Rating": 0,
		"#% increased Attack Speed if you've Killed Recently": 0,
		"#% increased Attack Speed per 10 Dexterity": 0,
		"#% increased Attack Speed per 25 Dexterity": 0,
		"#% increased Attack Speed when on Full Life": 0,
		"#% increased Attack Speed while Ignited": 0,
		"#% increased Attack Speed with Movement Skills": 0,
		"#% increased Attack and Cast Speed if you've used a Movement Skill Recently": 0,
		"#% increased Bleeding Duration per 12 Intelligence": 0,
		"#% increased Cast Speed if you've Killed Recently": 0,
		"#% increased Cast Speed while Ignited": 0,
		"#% increased Cold Damage if you have used a Fire Skill Recently": 0,
		"#% increased Cold Damage with Attack Skills": 0,
		"#% increased Critical Strike Chance against Enemies on Full Life": 0,
		"#% increased Critical Strike Chance if you have Killed Recently": 0,
		"#% increased Damage while Ignited": 0,
		"#% increased Damage while Leeching": 0,
		"#% increased Damage while Shocked": 0,
		"#% increased Damage while you have no Frenzy Charges": 0,
		"#% increased Damage with Channelling Skills": 0,
		"#% increased Damage with Movement Skills": 0,
		"#% increased Duration": 0,
		"#% increased Duration of Elemental Ailments on Enemies": 0,
		"#% increased Elemental Damage if you've used a Warcry Recently": 0,
		"#% increased Energy Shield per 10 Strength": 0,
		"#% increased Energy Shield per Power Charge": 0,
		"#% increased Fire Damage if you have been Hit Recently": 0,
		"#% increased Fire Damage if you have used a Cold Skill Recently": 0,
		"#% increased Fire Damage per 20 Strength": 0,
		"#% increased Lightning Damage per 10 Intelligence": 0,
		"#% increased Lightning Damage with Attack Skills": 0,
		"#% increased Melee Damage when on Full Life": 0,
		"#% increased Melee Physical Damage per 10 Dexterity": 0,
		"#% increased Mine Arming Speed": 0,
		"#% increased Mine Laying Speed": 0,
		"#% increased Physical Damage over time per 10 Dexterity": 0,
		"#% increased Physical Damage with Ranged Weapons": 0,
		"#% increased Physical Weapon Damage per 10 Strength": 0,
		"#% increased Projectile Attack Damage": 0,
		"#% increased Projectile Attack Damage during any Flask Effect": 0,
		"#% increased Projectile Attack Damage per 200 Accuracy Rating": 0,
		"#% increased Skill Effect Duration": 0,
		"#% increased Spell Damage if you've dealt a Critical Strike Recently": 0,
		"#% increased Spell Damage per 10 Intelligence": 0,
		"#% increased Spell Damage per 10 Strength": 0,
		"#% increased Spell Damage per 16 Dexterity": 0,
		"#% increased Spell Damage per 16 Intelligence": 0,
		"#% increased Spell Damage per 16 Strength": 0,
		"#% increased Spell Damage while Dual Wielding": 0,
		"#% increased Vaal Skill Critical Strike Chance": 0,
		"#% increased Vaal Skill Damage": 0,
		"#% increased Vaal Skill Effect Duration": 0,
		"#% of Cold Damage Converted to Fire Damage": 0,
		"#% of Fire Damage Converted to Chaos Damage": 0,
		"#% of Lightning Damage Converted to Chaos Damage": 0,
		"#% of Lightning Damage Converted to Cold Damage": 0,
		"#% of Physical Damage Converted to Chaos Damage": 0,
		"#% of Physical Damage Converted to Cold Damage": 0,
		"#% of Physical Damage Converted to Fire Damage": 0,
		"#% of Physical Damage Converted to Lightning Damage": 0,
		"#% of Physical Damage Converted to Lightning during Flask effect": 0,
		"#% to Critical Strike Multiplier if you have Blocked Recently": 0,
		"Adds # to # Cold Damage to Attacks per 10 Dexterity": 0,
		"Adds # to # Fire Damage if you've Blocked Recently": 0,
		"Adds # to # Fire Damage to Attacks per 10 Strength": 0,
		"Adds # to # Lightning Damage to Attacks per 10 Intelligence": 0,
		"Adds # to # Physical Damage to Attacks per 25 Dexterity": 0,
		"Attacks have #% to Critical Strike Chance": 0,
		"Chaos Skills have #% increased Skill Effect Duration": 0,
		"Damage Penetrates #% of Fire Resistance if you have Blocked Recently": 0,
		"Gain #% of Physical Attack Damage as Extra Fire Damage": 0,
		"Gain #% of Physical Attack Damage as Extra Lightning Damage": 0,
		"Gain #% of Physical Damage as Extra Chaos Damage": 0,
		"Gain #% of Physical Damage as Extra Chaos Damage while at maximum Power Charges": 0,
		"Projectile Attack Skills have #% increased Critical Strike Chance": 0,
		"Traps and Mines deal # to # additional Physical Damage": 0
	}
	# List of mods that will go in to a 'not' filter so that certain items will never appear
	# These items have high values of damage mods with some downside that is not accounted for
	ignoredmods = [
		'#% less Critical Strike Chance',  # Marylene's Fallacy
		'Lose all Power Charges on reaching Maximum Power Charges',  # Malachai's Loop
		'# Lightning Damage taken per second per Power Charge if your Skills have dealt a Critical Strike Recently',  # Shimmeron
		'#% less Mine Damage',  # Tremor Rod
	]

	searchstring = '{{"query":{{"filters":{{"type_filters": {{"filters": {{"category": {{"option": "jewel"}}}}}}}},"status":{{"option":"online"}},"stats":[{{"type":"weight","value":{{"min":7500}},"filters":[{}]}},{{"type":"not","filters":[{}]}}]}}}}'
	item = '{{"id":"{}","value":{{"weight":{}}}}}'
	notitem = '{{"id":"{}"}}'

	mlist = {}
	query = []
	notquery = []

	min_threshold = 0.0  # dps['% generic'] / 20
	craftmods = not {'NoCraftedMods'}.issubset(selections)
	for mod in modstr:
		if modstr[mod] > min_threshold:
			for val in mods[mod]:
				if (not craftmods) and 'crafted' in val:
					continue
				mlist[val] = round(modstr[mod], 2)

	for notmod in ignoredmods:
		for val in mods[notmod]:
			notquery.append(notitem.format(val))

	for i in sorted(mlist, key=mlist.get, reverse=True):
		query.append(item.format(i, mlist[i]))
	return searchstring.format(','.join(query), ','.join(notquery))

