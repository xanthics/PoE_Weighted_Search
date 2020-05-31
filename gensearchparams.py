#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.6.x or higher
# Given dps values from Path of Building, generates a search url
from modlist import mods
from restrict_mods import r_mods


def gensearchparams(dps, selections, base):
	modstr = {
		# (start) Automatic tool for generating mod/base pairs starts here
		# Attack Speed
		"#% increased Attack Speed": dps['attackspeed'],
		"#% increased Attack Speed if you've dealt a Critical Strike Recently": dps['attackspeed'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Attack Speed while Dual Wielding": dps['attackspeed'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Attack Speed while holding a Shield": dps['attackspeed'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Attack Speed with Axes": dps['attackspeed'] if {'Axe'}.issubset(selections) else 0,
		"#% increased Attack Speed with Bows": dps['attackspeed'] if {'Bow'}.issubset(selections) else 0,
		"#% increased Attack Speed with Claws": dps['attackspeed'] if {'Claw'}.issubset(selections) else 0,
		"#% increased Attack Speed with Daggers": dps['attackspeed'] if {'Dagger'}.issubset(selections) else 0,
		"#% increased Attack Speed with Maces or Sceptres": dps['attackspeed'] if {'Mace'}.issubset(selections) else 0,
		"#% increased Attack Speed with One Handed Melee Weapons": dps['attackspeed'] if {'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Attack Speed with Staves": dps['attackspeed'] if {'Staff'}.issubset(selections) else 0,
		"#% increased Attack Speed with Swords": dps['attackspeed'] if {'Sword'}.issubset(selections) else 0,
		"#% increased Attack Speed with Two Handed Melee Weapons": dps['attackspeed'] if {'TwoHandedWeapon', 'Melee'}.issubset(selections) else 0,
		"#% increased Attack Speed with Wands": dps['attackspeed'] if {'Wand'}.issubset(selections) else 0,
		"#% increased Attack Speed while a Rare or Unique Enemy is Nearby": dps['attackspeed'] if {'NearbyRareUnique'}.issubset(selections) else 0,
		# Cast Speed
		"#% increased Cast Speed": dps['castspeed'],
		"#% increased Cast Speed if you've dealt a Critical Strike Recently": dps['castspeed'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Cast Speed while Dual Wielding": dps['castspeed'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Cast Speed while holding a Shield": dps['castspeed'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Cast Speed while wielding a Staff": dps['castspeed'] if {'Staff'}.issubset(selections) else 0,
		"#% increased Cast Speed with Cold Skills": dps['castspeed'] if {'Cold'}.issubset(selections) else 0,
		"#% increased Cast Speed with Fire Skills": dps['castspeed'] if {'Fire'}.issubset(selections) else 0,
		"#% increased Cast Speed with Lightning Skills": dps['castspeed'] if {'Lightning'}.issubset(selections) else 0,
		# Attack and Cast Speed
		"#% increased Attack and Cast Speed": dps['attackspeed'] + dps['castspeed'],
		"#% increased Attack and Cast Speed if you've Hit an Enemy Recently": dps['attackspeed'] + dps['castspeed'] if {'conditionHitRecently'}.issubset(selections) else 0,
		# Damage - Any
		"#% increased Area Damage": max(dps['pspell'], dps['pattack'], dps['pmelee']) if {'Area'}.issubset(selections) else 0,
		"#% increased Chaos Damage": dps['pchaos'],
		"#% increased Cold Damage": dps['pcold'],
		"#% increased Damage": dps['pgeneric'],
		'#% increased Attack Damage': dps['pattack'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Elemental Damage": dps['pelemental'],
		"#% increased Elemental Damage with Attack Skills": dps['pelemental'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Fire Damage": dps['pfire'],
		"#% increased Lightning Damage": dps['plightning'],
		"#% increased Melee Damage": dps['pmelee'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Mine Damage": dps['pgeneric'] if {'Mine'}.issubset(selections) else 0,
		"#% increased Global Physical Damage": dps['pphysical'],
		"#% increased Damage with Axes": dps['pattack'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"#% increased Damage with Bows": dps['pattack'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"#% increased Damage with Claws": dps['pattack'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"#% increased Damage with Daggers": dps['pattack'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"#% increased Damage with Maces or Sceptres": dps['pattack'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"#% increased Damage with One Handed Weapons": dps['pattack'] if {'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Damage with Staves": dps['pattack'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"#% increased Damage with Swords": dps['pattack'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"#% increased Damage with Two Handed Weapons": dps['pattack'] if {'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Damage with Wands": dps['pattack'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"#% increased Attack Damage while Dual Wielding": dps['pattack'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
		"#% increased Projectile Damage": dps['pgeneric'] if {'Projectile'}.issubset(selections) else 0,
		"#% increased Spell Damage": dps['pspell'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Spell Damage while holding a Shield": dps['pspell'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"#% increased Spell Damage while wielding a Staff": dps['pspell'] if {'Spell', 'Staff'}.issubset(selections) else 0,
		"#% increased Totem Damage": dps['pgeneric'] if {'Totem'}.issubset(selections) else 0,
		"#% increased Trap Damage": dps['pgeneric'] if {'Trap'}.issubset(selections) else 0,
		# Damage - Conditional
		"#% increased Elemental Damage if you've dealt a Critical Strike Recently": dps['pelemental'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Damage if you've Killed Recently": dps['pgeneric'] if {'conditionKilledRecently'}.issubset(selections) else 0,
		"#% increased Damage when on Full Life": dps['pgeneric'] if {'conditionFullLife'}.issubset(selections) else 0,
		"#% increased Damage with Hits against Chilled Enemies": dps['pgeneric'] if {'conditionEnemyChilled'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		# Double Damage
		"Spells have a #% chance to deal Double Damage": dps['chancedoubledamage'] if {'Spell'}.issubset(selections) else 0,
		"#% chance to deal Double Damage": dps['chancedoubledamage'],
		# Base Critical Strike chance
		"Spells have #% to Critical Strike Chance ": dps['basecrit'] if {'Spell'}.issubset(selections) else 0,  # Note that this is base crit.
		"Attacks have #% to Critical Strike Chance": dps['basecrit'] if {'Attack'}.issubset(selections) else 0,  # Note that this is base crit.
		"#% Critical Strike Chance per Power Charge": dps['basecrit'] * dps["PowerCount"],  # Note that this is base crit.
		# Critical Strike Chance
		"#% increased Critical Strike Chance for Spells": dps['critchance'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance if you haven't dealt a Critical Strike Recently": dps['critchance'] if {'No Recent Crit'}.issubset(selections) else 0,
		"#% increased Attack Critical Strike Chance while Dual Wielding": dps['critchance'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Cold Skills": dps['critchance'] if {'Cold'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Fire Skills": dps['critchance'] if {'Fire'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Lightning Skills": dps['critchance'] if {'Lightning'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with One Handed Melee Weapons": dps['critchance'] if {'Attack', 'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Critical Strike Chance with Two Handed Melee Weapons": dps['critchance'] if {'Attack', 'Melee', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Global Critical Strike Chance": dps['critchance'],
		"#% increased Melee Critical Strike Chance": dps['critchance'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance with Elemental Skills": dps['critchance'] if {'Elemental'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance against Poisoned Enemies": dps['critchance'] if {'Poisoned'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance against Shocked Enemies": dps['critchance'] if {'conditionEnemyShocked'}.issubset(selections) else 0,
		# Critical Strike Multiplier
		"#% to Melee Critical Strike Multiplier": dps['critmulti'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% to Global Critical Strike Multiplier": dps['critmulti'],
		"#% to Critical Strike Multiplier with Elemental Skills": dps['critmulti'] if {'Elemental'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier for Spells": dps['critmulti'] if {'Spell'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier if you've Killed Recently": dps['critmulti'] if {'conditionKilledRecently'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier while Dual Wielding": dps['critmulti'] if {'DualWielding'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Cold Skills": dps['critmulti'] if {'Cold'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Fire Skills": dps['critmulti'] if {'Fire'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with Lightning Skills": dps['critmulti'] if {'Lightning'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier with One Handed Melee Weapons": dps['critmulti'] if {'Melee', 'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% to Critical Strike Multiplier with Two Handed Melee Weapons": dps['critmulti'] if {'Melee', 'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% Critical Strike Multiplier while a Rare or Unique Enemy is Nearby": dps['critmulti'] if {'NearbyRareUnique'}.issubset(selections) else 0,
		# Flat Damage
		"Adds # to # Chaos Damage to Attacks": dps['flatchaos'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells": dps['flatchaos'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while Dual Wielding": dps['flatchaos'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while holding a Shield": dps['flatchaos'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells while wielding a Two Handed Weapon": dps['flatchaos'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage": dps['flatchaos'],
		"Adds # to # Chaos Damage if you've dealt a Critical Strike Recently": dps['flatchaos'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Attacks": dps['flatcold'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Axe Attacks": dps['flatcold'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Bow Attacks": dps['flatcold'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Claw Attacks": dps['flatcold'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Dagger Attacks": dps['flatcold'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Mace or Sceptre Attacks": dps['flatcold'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells": dps['flatcold'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while Dual Wielding": dps['flatcold'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while holding a Shield": dps['flatcold'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Spells while wielding a Two Handed Weapon": dps['flatcold'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Staff Attacks": dps['flatcold'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Sword Attacks": dps['flatcold'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Cold Damage to Wand Attacks": dps['flatcold'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Cold Damage": dps['flatcold'],
		"Adds # to # Cold Damage to Spells and Attacks": dps['flatcold'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Fire Damage to Attacks": dps['flatfire'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Axe Attacks": dps['flatfire'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Bow Attacks": dps['flatfire'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Claw Attacks": dps['flatfire'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Dagger Attacks": dps['flatfire'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Mace or Sceptre Attacks": dps['flatfire'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells": dps['flatfire'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while Dual Wielding": dps['flatfire'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while holding a Shield": dps['flatfire'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Spells while wielding a Two Handed Weapon": dps['flatfire'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Staff Attacks": dps['flatfire'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Sword Attacks": dps['flatfire'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Fire Damage to Wand Attacks": dps['flatfire'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Fire Damage": dps['flatfire'],
		"Adds # to # Fire Damage to Spells and Attacks": dps['flatfire'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Lightning Damage to Attacks": dps['flatlightning'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Axe Attacks": dps['flatlightning'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Bow Attacks": dps['flatlightning'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Claw Attacks": dps['flatlightning'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Dagger Attacks": dps['flatlightning'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Mace or Sceptre Attacks": dps['flatlightning'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells": dps['flatlightning'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while Dual Wielding": dps['flatlightning'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while holding a Shield": dps['flatlightning'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells while wielding a Two Handed Weapon": dps['flatlightning'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Staff Attacks": dps['flatlightning'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Sword Attacks": dps['flatlightning'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Wand Attacks": dps['flatlightning'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage": dps['flatlightning'],
		"Adds # to # Lightning Damage to Spells and Attacks": dps['flatlightning'] if {'Attack', 'Spell'}.intersection(selections) else 0,
		"Adds # to # Physical Damage to Attacks": dps['flatphys'] if {'Attack'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Axe Attacks": dps['flatphys'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Bow Attacks": dps['flatphys'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Claw Attacks": dps['flatphys'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Dagger Attacks": dps['flatphys'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Mace or Sceptre Attacks": dps['flatphys'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells": dps['flatphys'] if {'Spell'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while Dual Wielding": dps['flatphys'] if {'Spell', 'DualWielding'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while holding a Shield": dps['flatphys'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Spells while wielding a Two Handed Weapon": dps['flatphys'] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Staff Attacks": dps['flatphys'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Sword Attacks": dps['flatphys'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"Adds # to # Physical Damage to Wand Attacks": dps['flatphys'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"Adds # to # Physical Damage": dps['flatphys'],
		"Adds # to # Physical Damage against Bleeding Enemies": dps['flatphys'] if {'conditionEnemyBleeding'}.issubset(selections) else 0,
		"Adds # to # Physical Damage against Poisoned Enemies": dps['flatphys'] if {'conditionEnemyPoisoned'}.issubset(selections) else 0,
		"# to # added Fire Damage against Burning Enemies": dps['flatfire'] if {'conditionEnemyBurning'}.issubset(selections) else 0,
		"Adds # to # Fire Damage against Ignited Enemies": dps['flatfire'] if {'conditionEnemyIgnited'}.issubset(selections) else 0,
		"Adds # to # Cold Damage against Chilled or Frozen Enemies": dps['flatcold'] if {'conditionEnemyChilled', 'conditionEnemyFrozen'}.intersection(selections) else 0,
		"Adds # to # Lightning Damage against Shocked Enemies": dps['flatlightning'] if {'conditionEnemyShocked'}.issubset(selections) else 0,
		"Adds # to # Cold Damage if you've dealt a Critical Strike Recently": dps['flatcold'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Adds # to # Fire Damage if you've dealt a Critical Strike Recently": dps['flatfire'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage if you've dealt a Critical Strike Recently": dps['flatlightning'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Adds # to # Physical Damage if you've dealt a Critical Strike Recently": dps['flatphys'] if {'conditionCritRecently'}.issubset(selections) else 0,
		# Damage Penetration
		"Damage Penetrates #% Cold Resistance": dps['pencold'],
		"Damage Penetrates #% Elemental Resistance if you haven't Killed Recently": dps['penall'] if {'No Recent Kill'}.issubset(selections) else 0,
		"Damage Penetrates #% Elemental Resistances": dps['penall'],
		"Damage Penetrates #% Fire Resistance": dps['penfire'],
		"Damage Penetrates #% Lightning Resistance": dps['penlightning'],
		# Gain % of ### as extra ###
		"Gain #% of Elemental Damage as Extra Chaos Damage": dps['eleaschaos'],
		"Gain #% of Physical Damage as Extra Cold Damage": dps['extracold'],
		"Gain #% of Physical Damage as Extra Damage of a random Element": dps['extrarandom'],
		"Gain #% of Physical Damage as Extra Fire Damage": dps['extrafire'],
		"Gain #% of Physical Damage as Extra Fire Damage if you've dealt a Critical Strike Recently": dps['extrafire'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"Gain #% of Physical Damage as Extra Lightning Damage": dps['extralightning'],
		"Gain #% of Non-Chaos Damage as extra Chaos Damage": dps['extrachaos'],
		"Gain #% of Cold Damage as Extra Chaos Damage": dps['coldasextrachaos'],
		"Gain #% of Fire Damage as Extra Chaos Damage": dps['fireasextrachaos'],
		"Gain #% of Lightning Damage as Extra Chaos Damage": dps['lightningasextrachaos'],
		"Gain #% of Physical Damage as Extra Chaos Damage": dps['physicalasextrachaos'],
		# Related to Endurance/Frenzy/Power charges
		'# to Maximum Power Charges': dps['1powercharge'] if {'Power'}.issubset(selections) else 0,
		'# to Maximum Frenzy Charges': dps['1frenzycharge'] if {'Frenzy'}.issubset(selections) else 0,
		'# to Maximum Endurance Charges': dps['1endurancecharge'] if {'Endurance'}.issubset(selections) else 0,
		# Accuracy
		'# to Accuracy Rating': dps['flataccuracy'],
		'#% increased Global Accuracy Rating': dps['paccuracy'],
		"#% increased Accuracy Rating if you haven't Killed Recently": dps['paccuracy'] if {'No Recent Kill'}.issubset(selections) else 0,
		# Attributes
		'# to Strength': dps['20str'],
		'# to Intelligence': dps['20int'],
		'# to Dexterity': dps['20dex'],
		'# to Strength and Intelligence': dps['20str'] + dps['20int'],
		'# to Strength and Dexterity': dps['20str'] + dps['20dex'],
		'# to Dexterity and Intelligence': dps['20int'] + dps['20dex'],
		'# to all Attributes': dps['20int'] + dps['20dex'] + dps['20str'],
		'#% increased Damage per 15 Dexterity': dps['damageperdex'],
		'#% increased Damage per 15 Intelligence': dps['damageperint'],
		'#% increased Damage per 15 Strength': dps['damageperstr'],
		"#% increased Attributes": dps['pstr'] + dps['pdex'] + dps['pint'],
		"#% increased Strength": dps['pstr'],
		"#% increased Intelligence": dps['pint'],
		"#% increased Dexterity": dps['pdex'],
		# Damage Over Time
		"#% increased Damage over Time": dps['pdot'],
		"#% increased Damage over Time while Dual Wielding": dps['pdot'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Damage over Time while holding a Shield": dps['pdot'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Damage over Time while wielding a Two Handed Weapon": dps['pdot'] if {'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Damage with Ailments": dps['pdotailment'],
		"#% increased Damage with Bleeding": dps['pbleed'],
		"#% increased Damage with Poison": dps['ppoison'],
		"#% increased Burning Damage": dps['pignite'],
		# Damage Over Time Multiplier
		"#% to Cold Damage over Time Multiplier": dps['pcolddotmulti'],
		"#% to Chaos Damage over Time Multiplier": dps['pchaosdotmulti'],
		'#% to Damage over Time Multiplier': dps['pdotmulti'],
		# Life, ES, and Mana
		"# to maximum Life": dps['flatlife'],
		"#% increased maximum Life": dps['plife'],
		"# to maximum Energy Shield": dps['flates'],
		"#% increased maximum Energy Shield": dps['pes'],
		"# to maximum Mana": dps['flatmana'],
		"#% increased maximum Mana": dps['pmana'],
		'#% reduced Mana Cost of Skills': dps['pmanaskillreduce'],
		# Minion % damage
		"Minions have #% chance to deal Double Damage": dps['pminion'],
		"Minions deal #% increased Damage": dps['pminion'],
		"Minions have #% increased Attack Speed": dps['minionattackspeed'],
		"Minions have #% increased Cast Speed": dps['minioncastspeed'],
		"Minions have #% increased Attack and Cast Speed if you or your Minions have Killed Recently": dps['minionattackspeed'] + dps['minioncastspeed'] if {'conditionKilledRecently', 'conditionMinionsKilledRecently'}.intersection(selections) else 0,
		"Minions deal #% increased Damage if you've used a Minion Skill Recently": dps['pminion'] if {'conditionUsedMinionSkillRecently'}.issubset(selections) else 0,
		# Minion Flat Damage
		"Minions deal # to # additional Physical Damage": dps['minionflatphys'],
		"Minions deal # to # additional Lightning Damage": dps['minionflatlightning'],
		"Minions deal # to # additional Cold Damage": dps['minionflatcold'],
		"Minions deal # to # additional Fire Damage": dps['minionflatfire'],
		"Minions deal # to # additional Chaos Damage": dps['minionflatchaos'],
		# Gem Levels Generic
		"# to Level of all Chaos Skill Gems": dps['achaossg'],
		"# to Level of all Cold Skill Gems": dps['acoldsg'],
		"# to Level of all Fire Skill Gems": dps['afiresg'],
		"# to Level of all Lightning Skill Gems": dps['alightningsg'],
		"# to Level of all Physical Skill Gems": dps['aphysicalsg'],
		"# to Level of all Dexterity Skill Gems": dps['adexsg'],
		"# to Level of all Intelligence Skill Gems": dps['aintsg'],
		"# to Level of all Strength Skill Gems": dps['astrsg'],
		"# to Level of all Minion Skill Gems": dps['aminionsg'],
		"# to Level of all Raise Spectre Gems": dps['aminionsg'] if {'Spectre'}.issubset(selections) else 0,
		"# to Level of all Raise Zombie Gems": dps['aminionsg'] if {'Zombie'}.issubset(selections) else 0,
		# Spell Gem Levels
		"# to Level of all Chaos Spell Skill Gems": dps['achaossg'] if {'Spell'}.issubset(selections) else 0,
		"# to Level of all Cold Spell Skill Gems": dps['acoldsg'] if {'Spell'}.issubset(selections) else 0,
		"# to Level of all Fire Spell Skill Gems": dps['afiresg'] if {'Spell'}.issubset(selections) else 0,
		"# to Level of all Lightning Spell Skill Gems": dps['alightningsg'] if {'Spell'}.issubset(selections) else 0,
		"# to Level of all Physical Spell Skill Gems": dps['aphysicalsg'] if {'Spell'}.issubset(selections) else 0,
		"# to Level of all Spell Skill Gems": dps['aspellsg'] if {'Spell'}.issubset(selections) else 0,
		# Flasks
		"#% increased Critical Strike Chance during any Flask Effect": dps['critchance'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier during any Flask Effect": dps['critmulti'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Damage Penetrates #% Elemental Resistances during any Flask Effect": dps['penall'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Damage during any Flask Effect": dps['pgeneric'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Damage Penetrates #% Lightning Resistance during Flask effect": dps['penlightning'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Spells during Flask effect": dps['flatlightning'] if {'conditionUsingFlask', 'Spell'}.issubset(selections) else 0,
		"Adds # to # Lightning Damage to Attacks during Flask effect": dps['flatlightning'] if {'conditionUsingFlask', 'Attack'}.issubset(selections) else 0,
		"#% increased Attack Speed during any Flask Effect": dps['attackspeed'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Cast Speed during any Flask Effect": dps['castspeed'] if {'conditionUsingFlask'}.issubset(selections) else 0,
		"#% increased Melee Damage during any Flask Effect": dps['pgeneric'] if {'conditionUsingFlask', 'Attack', 'Melee'}.issubset(selections) else 0,
		"Adds # to # Chaos Damage to Spells and Attacks during any Flask Effect": dps['flatchaos'] if {'conditionUsingFlask'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"#% increased Spell Damage during any Flask Effect": dps['pgeneric'] if {'conditionUsingFlask', 'Spell'}.issubset(selections) else 0,
		"#% increased Elemental Damage with Attack Skills during any Flask Effect": dps['pelemental'] if {'conditionUsingFlask', 'Attack'}.issubset(selections) else 0,
		"Damage Penetrates #% Fire Resistance against Blinded Enemies": dps['penfire'] if {'Blinded'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance against Blinded Enemies": dps['critchance'] if {'Blinded'}.issubset(selections) else 0,
		# (stop) Automatic tool for generating mod/base pairs stops here
		# local flat damage mods for Spellslinger
		"Adds # to # Chaos Damage (Local)": dps['flatchaos'] if base == 'Spellslinger MH' else dps['flatchaos']*0.5 if base == "Spellslinger DW" else 0,
		"Adds # to # Cold Damage (Local)": dps['flatcold'] if base == 'Spellslinger MH' else dps['flatcold']*0.5 if base == "Spellslinger DW" else 0,
		"Adds # to # Fire Damage (Local)": dps['flatfire'] if base == 'Spellslinger MH' else dps['flatfire']*0.5 if base == "Spellslinger DW" else 0,
		"Adds # to # Lightning Damage (Local)": dps['flatlightning'] if base == 'Spellslinger MH' else dps['flatlightning']*0.5 if base == "Spellslinger DW" else 0,
		# Shaper & Elder unique rings
		"#% increased Attack Damage if your other Ring is a Shaper Item": dps['pgeneric'] if {'Shaper', 'Attack'}.issubset(selections) else 0,
		"#% increased Spell Damage if your other Ring is an Elder Item": dps['pgeneric'] if {'Elder', 'Spell'}.issubset(selections) else 0,
		# Precursor Emblem
		"# to # Cold Damage per Frenzy Charge": dps['flatcold'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Accuracy Rating per Frenzy Charge": dps['paccuracy'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance per Frenzy Charge": dps['critchance'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"#% increased Damage per Frenzy Charge": dps['pgeneric'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"Gain #% of Cold Damage as Extra Chaos Damage per Frenzy Charge": dps['coldasextrachaos'] * dps["FrenzyCount"] if {'useFrenzyCharges'}.issubset(selections) else 0,
		"# to # Fire Damage per Endurance Charge": dps['flatfire'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed per Endurance Charge": (dps['attackspeed'] + dps['castspeed']) * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance per Endurance Charge": dps['critchance'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"#% increased Damage per Endurance Charge": dps['pgeneric'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"Gain #% of Fire Damage as Extra Chaos Damage per Endurance Charge": dps['fireasextrachaos'] * dps["EnduranceCount"] if {'useEnduranceCharges'}.issubset(selections) else 0,
		"# to # Lightning Damage per Power Charge": dps['flatlightning'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Attack and Cast Speed per Power Charge": (dps['attackspeed'] + dps['castspeed']) * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Damage per Power Charge": dps['pgeneric'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"#% increased Spell Damage per Power Charge": dps['pgeneric'] * dps["PowerCount"] if {'usePowerCharges', 'Spell'}.issubset(selections) else 0,
		"#% to Critical Strike Multiplier per Power Charge": dps['critmulti'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
		"Gain #% of Lightning Damage as Extra Chaos Damage per Power Charge": dps['lightningasextrachaos'] * dps["PowerCount"] if {'usePowerCharges'}.issubset(selections) else 0,
	}
	# table to get the correct trade site json name
	lookup_bases = {
		"All Jewel": 'jewel',
		"Base Jewel": 'jewel.base',
		"Abyss Jewel": 'jewel.abyss',
		"Caster Weapon": 'weapon',
		"Spellslinger MH": 'weapon.wand',
		"Spellslinger DW": 'weapon.wand',
		"Amulet": 'accessory.amulet',
		"Ring": 'accessory.ring',
		"Belt": 'accessory.belt',
		"Quiver": 'armour.quiver',
		"Shield": 'armour.shield',
		"Gloves": 'armour.gloves',
		"Helmet": 'armour.helmet',
		"Body Armour": 'armour.chest',
		"Boots": 'armour.boots',
	}

	searchstring = '{{"query":{{"filters":{{"type_filters":{{"filters":{{"category":{{"option":"{}"}}}}}}}},"status":{{"option":"online"}},"stats":[{{"type":"weight","value":{{"min":{}}},"filters":[{}]}}]}}}}'
	item = '{{"id":"{}","value":{{"weight":{}}}}}'

	mlist = {}
	query = []
	reverse = {}
	trimmed = []

	minthreshold = 0.01  # max(dps['pgeneric'], dps['pminion']) / 100
	for mod in modstr:
		if abs(modstr[mod]) > minthreshold:
			for val in mods[mod]:
				if ('crafted' in val and ({'NoCraftedMods'}.issubset(selections) or mod not in r_mods[base]['crafted'])) or \
				   ('implicit' in val and ({'NoImplicitMods'}.issubset(selections) or mod not in r_mods[base]['implicit'])) or \
				   ('fractured' in val and ({'NoFracturedMods'}.issubset(selections) or mod not in r_mods[base]['explicit'])) or \
				   ('explicit' in val and mod not in r_mods[base]['explicit']):
					continue
				mlist[val] = round(modstr[mod], 2)
				reverse[val] = mod

	maxmods = 29
	# from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
	for c, i in enumerate({k: v for k, v in sorted(mlist.items(), key=lambda value: abs(value[1]))}):
		if c < maxmods:
			query.append(item.format(i, mlist[i]))
		else:
			trimmed.append(f'({i.split(".")[0]}) {reverse[i]} - {mlist[i]}')

	return searchstring.format(lookup_bases[base], int(max(dps['pgeneric'], dps['pminion']) * 16), ','.join(query)), len(query) + len(trimmed), trimmed
