#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.6.x or higher
# Given dps values from Path of Building, generates a search url
from modlist import mods


def gensearchparams(dps, selections):
	modstr = {
		# Attack Speed
		"#% increased Attack Speed": dps['attackspeed'],
		"#% increased Attack Speed if you've dealt a Critical Strike Recently": dps['attackspeed'] if {'conditionCritRecently'}.issubset(selections) else 0,
		"#% increased Attack Speed while Dual Wielding": dps['attackspeed'] if {'DualWielding'}.issubset(selections) else 0,
		"#% increased Attack Speed while holding a Shield": dps['attackspeed'] if {'Shield'}.issubset(selections) else 0,
		"#% increased Attack Speed with Axes": dps['attackspeed'] if {'Axe'}.issubset(selections) else 0,
		"#% increased Attack Speed with Bows": dps['attackspeed'] if {'Bow'}.issubset(selections) else 0,
		"#% increased Attack Speed with Claws": dps['attackspeed'] if {'Claw'}.issubset(selections) else 0,
		"#% increased Attack Speed with Daggers": dps['attackspeed'] if {'Dagger'}.issubset(selections) else 0,
		"#% increased Attack Speed with Maces and Sceptres": dps['attackspeed'] if {'Mace'}.issubset(selections) else 0,
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
		"#% increased Area Damage": dps['pgeneric'] if {'Area'}.issubset(selections) else 0,
		"#% increased Chaos Damage": dps['pchaos'],
		"#% increased Cold Damage": dps['pcold'],
		"#% increased Damage": dps['pgeneric'],
		'#% increased Attack Damage': dps['pgeneric'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Elemental Damage": dps['pelemental'],
		"#% increased Elemental Damage with Attack Skills": dps['pelemental'] if {'Attack'}.issubset(selections) else 0,
		"#% increased Fire Damage": dps['pfire'],
		"#% increased Lightning Damage": dps['plightning'],
		"#% increased Melee Damage": dps['pgeneric'] if {'Attack', 'Melee'}.issubset(selections) else 0,
		"#% increased Melee Physical Damage while holding a Shield": dps['pgeneric'] if {'Attack', 'Melee', 'Shield'}.issubset(selections) else 0,
		"#% increased Mine Damage": dps['pgeneric'] if {'Mine'}.issubset(selections) else 0,
		"#% increased Global Physical Damage": dps['pphysical'],
		"#% increased Damage with Axes": dps['pgeneric'] if {'Attack', 'Axe'}.issubset(selections) else 0,
		"#% increased Damage with Bows": dps['pgeneric'] if {'Attack', 'Bow'}.issubset(selections) else 0,
		"#% increased Damage with Claws": dps['pgeneric'] if {'Attack', 'Claw'}.issubset(selections) else 0,
		"#% increased Damage with Daggers": dps['pgeneric'] if {'Attack', 'Dagger'}.issubset(selections) else 0,
		"#% increased Damage with Maces and Sceptres": dps['pgeneric'] if {'Attack', 'Mace'}.issubset(selections) else 0,
		"#% increased Damage with One Handed Weapons": dps['pgeneric'] if {'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0,
		"#% increased Damage with Staves": dps['pgeneric'] if {'Attack', 'Staff'}.issubset(selections) else 0,
		"#% increased Damage with Swords": dps['pgeneric'] if {'Attack', 'Sword'}.issubset(selections) else 0,
		"#% increased Damage with Two Handed Weapons": dps['pgeneric'] if {'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0,
		"#% increased Damage with Wands": dps['pgeneric'] if {'Attack', 'Wand'}.issubset(selections) else 0,
		"#% increased Weapon Damage while Dual Wielding": dps['pgeneric'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
		"#% increased Projectile Damage": dps['pgeneric'] if {'Projectile'}.issubset(selections) else 0,
		"#% increased Spell Damage": dps['pgeneric'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Spell Damage while holding a Shield": dps['pgeneric'] if {'Spell', 'Shield'}.issubset(selections) else 0,
		"#% increased Spell Damage while wielding a Staff": dps['pgeneric'] if {'Spell', 'Staff'}.issubset(selections) else 0,
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
		"#% increased Critical Strike Chance": dps['critchance'],
		"#% increased Critical Strike Chance for Spells": dps['critchance'] if {'Spell'}.issubset(selections) else 0,
		"#% increased Critical Strike Chance if you haven't dealt a Critical Strike Recently": dps['critchance'] if {'No Recent Crit'}.issubset(selections) else 0,
		"#% increased Weapon Critical Strike Chance while Dual Wielding": dps['critchance'] if {'Attack', 'DualWielding'}.issubset(selections) else 0,
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
		"Adds # to # Cold Damage to Mace and Sceptre Attacks": dps['flatcold'] if {'Attack', 'Mace'}.issubset(selections) else 0,
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
		"Adds # to # Fire Damage to Mace and Sceptre Attacks": dps['flatfire'] if {'Attack', 'Mace'}.issubset(selections) else 0,
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
		"Adds # to # Lightning Damage to Mace and Sceptre Attacks": dps['flatlightning'] if {'Attack', 'Mace'}.issubset(selections) else 0,
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
		"Adds # to # Physical Damage to Mace and Sceptre Attacks": dps['flatphys'] if {'Attack', 'Mace'}.issubset(selections) else 0,
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
		"Damage Penetrates #% Cold Resistance against Chilled Enemies": dps['pencold'] if {'conditionEnemyChilled'}.issubset(selections) else 0,
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
		"#% increased Damage per 5 of your lowest Attribute": dps['plowest'],
		"#% increased Attributes": dps['pstr'] + dps['pdex'] + dps['pint'],
		"#% increased Strength": dps['pstr'],
		"#% increased Intelligence": dps['pint'],
		"#% increased Dexterity": dps['pdex'],
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
		# Shaper & Elder unique rings
		"#% increased Attack Damage if your other Ring is a Shaper Item": dps['pgeneric'] if {'Shaper', 'Attack'}.issubset(selections) else 0,
		"#% increased Spell Damage if your other Ring is an Elder Item": dps['pgeneric'] if {'Elder', 'Spell'}.issubset(selections) else 0,
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
		# Life & ES
		"# to maximum Life": dps['flatlife'],
		"#% increased maximum Life": dps['plife'],
		"# to maximum Energy Shield": dps['flates'],
		"#% increased maximum Energy Shield": dps['pes'],
		# Minion % damage
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
	}

	# mods that are explicitly skipped, comment with where they appear
	disabled = {
		# Veruso's Battering Rams
		"#% increased Melee Damage per Endurance Charge": dps['pgeneric'] * dps["EnduranceCount"] if {'Endurance', 'Melee'}.issubset(selections) else 0,
		# Surgebinders
		"#% increased Elemental Damage per Frenzy Charge": dps['pelemental'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Tidebreaker and Surgebinders
		"#% increased Physical Damage per Endurance Charge": dps['pphysical'] * dps["EnduranceCount"] if {'Endurance'}.issubset(selections) else 0,
		# Snakebite
		"#% increased Attack Speed per Frenzy Charge": dps['attackspeed'] * dps["FrenzyCount"] if {'Frenzy', 'Attack'}.issubset(selections) else 0,
		# The Blood Dance
		"#% increased Attack and Cast Speed per Frenzy Charge": dps['attackspeed'] * dps["FrenzyCount"] if {'Attack', 'Frenzy'}.issubset(selections) else (dps['castspeed'] * dps["FrenzyCount"] if {'Spell', 'Frenzy'}.issubset(selections) else 0),
		# Tulfall
		"#% increased Cold Damage per Frenzy Charge": dps['pcold'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Hyaon's Fury
		"#% increased Lightning Damage per Frenzy Charge": dps['plightning'] * dps["FrenzyCount"] if {'Frenzy'}.issubset(selections) else 0,
		# Nebuloch
		"Adds # to # Physical Damage per Endurance Charge": dps['flatphys'] * dps["EnduranceCount"] if {'Endurance'}.issubset(selections) else 0,
		# Cane of Unravelling
		"#% increased Cast Speed per Power Charge": dps['castspeed'] * dps["PowerCount"] if {'Power'}.issubset(selections) else 0,
		# The Aylardex
		"#% increased Critical Strike Chance per Power Charge": dps['critchance'] * dps["PowerCount"] if {'Power'}.issubset(selections) else 0,
		# Victario's Acuity
		"#% increased Projectile Damage per Power Charge": dps['pgeneric'] * dps["PowerCount"] if {'Power', 'Projectile'}.issubset(selections) else 0,
		# Shimmeron
		"Adds # to # Lightning Damage to Spells per Power Charge": dps['flatlightning'] * dps["PowerCount"] if {'Power', 'Spell'}.issubset(selections) else 0,
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
		# Only appears on uniques
		"#% increased Damage with Hits and Ailments against Blinded Enemies": dps['pgeneric'] if {'Blinded'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
		"#% increased Fire Damage with Hits and Ailments against Blinded Enemies": dps['pfire'] if {'Blinded'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0,
	}

	# TODO: Determine if each mod is worth adding or specific to a static unique
	# mods that have not been processed yet
	queued = {
		"#% increased Weapon Damage while Dual Wielding": 0,
		# This sectioned delayed until next league(if nexus goes core)
		# Update :: Nexus is not going core, will wait for rework
		"#% increased Attack Damage per 500 Maximum Mana": 0,
		"#% increased Spell Damage per 500 Maximum Mana": 0,
		"#% increased Attack and Cast Speed during Onslaught": 0,
		"#% increased Accuracy Rating with Axes": ["implicit.stat_2538120572"],
		"#% increased Accuracy Rating with Bows": ["implicit.stat_169946467"],
		"#% increased Accuracy Rating with Claws": ["implicit.stat_1297965523"],
		"#% increased Accuracy Rating with Daggers": ["implicit.stat_2054715690"],
		"#% increased Accuracy Rating with Maces and Sceptres": ["implicit.stat_3208450870"],
		"#% increased Accuracy Rating with Staves": ["implicit.stat_1617235962"],
		"#% increased Accuracy Rating with Swords": ["implicit.stat_2090868905"],
		"#% increased Accuracy Rating with Wands": ["implicit.stat_2150183156"],
		"#% increased Cold Damage with Spell Skills": ["implicit.stat_2186994986"],
		"#% increased Critical Strike Chance for Spells while Dual Wielding": ["implicit.stat_1218939541"],
		"#% increased Critical Strike Chance for Spells while holding a Shield": ["implicit.stat_952509814"],
		"#% increased Critical Strike Chance for Spells while wielding a Staff": ["implicit.stat_140429540"],
		"#% to Critical Strike Multiplier for Spells while Dual Wielding": ["implicit.stat_2349237916"],
		"#% to Critical Strike Multiplier for Spells while holding a Shield": ["implicit.stat_2311200892"],
		"#% to Critical Strike Multiplier for Spells while wielding a Staff": ["implicit.stat_3629080637"],
		"#% increased Damage if Corrupted": ["implicit.stat_767196662"],
		"#% increased Fire Damage with Attack Skills": ["implicit.stat_2468413380"],
		"#% increased Fire Damage with Spell Skills": ["implicit.stat_361162316"],
		"#% increased Lightning Damage with Attack Skills": ["explicit.stat_4208907162", "implicit.stat_4208907162"],
		"#% increased Lightning Damage with Spell Skills": ["implicit.stat_3935031607"],
		"#% increased Minion Accuracy Rating": ["implicit.stat_1718147982"],
		"#% increased Physical Damage with Attack Skills": ["implicit.stat_2266750692"],
		"#% increased Physical Damage with Spell Skills": ["implicit.stat_1430255627"],
		"#% increased Spell Damage if Corrupted": ["implicit.stat_374116820"],
		"#% increased maximum Life if Corrupted": ["implicit.stat_3887484120"],
		"#% to Critical Strike Multiplier with Axes": ["implicit.stat_4219746989"],
		"#% to Critical Strike Multiplier with Bows": ["implicit.stat_1712221299"],
		"#% to Critical Strike Multiplier with Claws": ["implicit.stat_2811834828"],
		"#% to Critical Strike Multiplier with Daggers": ["implicit.stat_3998601568"],
		"#% to Critical Strike Multiplier with Maces and Sceptres": ["implicit.stat_458899422"],
		"#% to Critical Strike Multiplier with Staves": ["implicit.stat_1474913037"],
		"#% to Critical Strike Multiplier with Swords": ["implicit.stat_3114492047"],
		"#% to Critical Strike Multiplier with Wands": ["implicit.stat_1241396104"],
		"#% increased Attack and Cast Speed if Corrupted": ["implicit.stat_26867112"],
		"#% increased Global Critical Strike Chance if Corrupted"

		"#% increased Bleeding Duration": 0,
		"#% increased Poison Duration": 0,
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
	]

	searchstring = '{{"query":{{"filters":{{"type_filters":{{"filters":{{"category":{{"option":"jewel"}}}}}}}},"status":{{"option":"online"}},"stats":[{}{{"type":"weight","value":{{"min":{}}},"filters":[{}]}},{{"type":"not","filters":[{}]}}]}}}}'
	item = '{{"id":"{}","value":{{"weight":{}}}}}'
	notitem = '{{"id":"{}"}}'
	emptygroup = '{"type":"and","filters":[]}, '

	mlist = {}
	query = []
	notquery = []

	minthreshold = 0.0  # dps['pgeneric'] / 20
	for mod in modstr:
		if modstr[mod] > minthreshold:
			for val in mods[mod]:
				if ({'NoCraftedMods'}.issubset(selections) and 'crafted' in val) or \
				   ({'NoFracturedMods'}.issubset(selections) and 'fractured' in val) or \
				   ({'NoImplicitMods'}.issubset(selections) and 'implicit' in val):
					continue
				mlist[val] = round(modstr[mod], 2)

	for notmod in ignoredmods:
		for val in mods[notmod]:
			notquery.append(notitem.format(val))

	for i in sorted(mlist, key=mlist.get, reverse=True):
		query.append(item.format(i, mlist[i]))
	return searchstring.format(emptygroup * int(dps['emptycount']), int(max(dps['pgeneric'], dps['pminion']) * 16), ','.join(query), ','.join(notquery))
