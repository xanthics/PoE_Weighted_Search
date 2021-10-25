#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: Jeremy Parks
# Note: Requires Python 3.6.x or higher
# Given dps values from Path of Building, generates a search url
from modlist import mods
from restrict_mods import r_mods
from pseudo_lookup import pseudo_lookup


# TODO: Flag to round ele/spell % if they are close to an element
# TODO: Implement unsupported mods (end of modstr)
def gensearchparams(dps, selections, base):
	localmulti = 0.5 if 'SpellslingerDW' in selections else 0
	localmulti += sum(1 if x in selections else 0 for x in ['Spellslinger', 'BattleMage'])
	# First element is per point value, second element is "total value" for sorting.
	modstr = {
		# Attack Speed
		"#% increased Attack Speed": [dps['attackspeed'][0], dps['attackspeed'][1]],
		"#% increased Attack Speed if you've dealt a Critical Strike Recently": [dps['attackspeed'][0] if {'CritRecently'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed while Dual Wielding": [dps['attackspeed'][0] if {'DualWielding'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed while holding a Shield": [dps['attackspeed'][0] if {'Shield'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Axes": [dps['attackspeed'][0] if {'Axe'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Bows": [dps['attackspeed'][0] if {'Bow'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Claws": [dps['attackspeed'][0] if {'Claw'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Daggers": [dps['attackspeed'][0] if {'Dagger'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Maces or Sceptres": [dps['attackspeed'][0] if {'Mace'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with One Handed Melee Weapons": [dps['attackspeed'][0] if {'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Staves": [dps['attackspeed'][0] if {'Staff'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Swords": [dps['attackspeed'][0] if {'Sword'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Two Handed Melee Weapons": [dps['attackspeed'][0] if {'TwoHandedWeapon', 'Melee'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed with Wands": [dps['attackspeed'][0] if {'Wand'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Attack Speed while a Rare or Unique Enemy is Nearby": [dps['attackspeed'][0] if {'NearbyRareUnique'}.issubset(selections) else 0, dps['attackspeed'][1]],
		# Cast Speed
		"#% increased Cast Speed": [dps['castspeed'][0], dps['castspeed'][1]],
		"#% increased Cast Speed if you've dealt a Critical Strike Recently": [dps['castspeed'][0] if {'CritRecently'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed while Dual Wielding": [dps['castspeed'][0] if {'DualWielding'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed while holding a Shield": [dps['castspeed'][0] if {'Shield'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed while wielding a Staff": [dps['castspeed'][0] if {'Staff'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed with Cold Skills": [dps['castspeed'][0] if {'Cold'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed with Fire Skills": [dps['castspeed'][0] if {'Fire'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed with Lightning Skills": [dps['castspeed'][0] if {'Lightning'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Cast Speed if you've Killed Recently": [dps['castspeed'][0] if {'KilledRecently'}.issubset(selections) else 0, dps['castspeed'][1]],
		# Attack and Cast Speed
		"#% increased Attack and Cast Speed": [dps['attackspeed'][0] + dps['castspeed'][0], dps['attackspeed'][1] + dps['castspeed'][1]],
		# Damage - Physical
		"#% increased Global Physical Damage": [dps['pphysical'][0], dps['pphysical'][1]],
		"#% increased Physical Damage with Attack Skills": [dps['pphysical'][0] if {'Attack'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Spell Skills": [dps['pphysical'][0] if {'Spell'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Axes": [dps['pphysical'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Bows": [dps['pphysical'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Claws": [dps['pphysical'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Daggers": [dps['pphysical'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Maces or Sceptres": [dps['pphysical'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Staves": [dps['pphysical'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Swords": [dps['pphysical'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['pphysical'][1]],
		"#% increased Physical Damage with Wands": [dps['pphysical'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['pphysical'][1]],
		# Damage - Elemental
		"#% increased Elemental Damage": [dps['pelemental'][0], dps['pelemental'][1]],
		"#% increased Elemental Damage with Attack Skills": [dps['pelemental'][0] if {'Attack'}.issubset(selections) else 0, dps['pelemental'][1]],
		# Damage - Cold
		"#% increased Cold Damage": [dps['pcold'][0], dps['pcold'][1]],
		"#% increased Cold Damage with Attack Skills": [dps['pcold'][0] if {'Attack'}.issubset(selections) else 0, dps['pcold'][1]],
		"#% increased Cold Damage with Spell Skills": [dps['pcold'][0] if {'Spell'}.issubset(selections) else 0, dps['pcold'][1]],
		# Damage - Lightning
		"#% increased Lightning Damage": [dps['plightning'][0], dps['plightning'][1]],
		"#% increased Lightning Damage with Attack Skills": [dps['plightning'][0] if {'Attack'}.issubset(selections) else 0, dps['plightning'][1]],
		"#% increased Lightning Damage with Spell Skills": [dps['plightning'][0] if {'Spell'}.issubset(selections) else 0, dps['plightning'][1]],
		# Damage - Fire
		"#% increased Fire Damage": [dps['pfire'][0], dps['pfire'][1]],
		"#% increased Fire Damage with Attack Skills": [dps['pfire'][0] if {'Attack'}.issubset(selections) else 0, dps['pfire'][1]],
		"#% increased Fire Damage with Spell Skills": [dps['pfire'][0] if {'Spell'}.issubset(selections) else 0, dps['pfire'][1]],
		# Damage - Chaos
		"#% increased Chaos Damage": [dps['pchaos'][0], dps['pchaos'][1]],
		"#% increased Chaos Damage with Attack Skills": [dps['pchaos'][0] if {'Attack'}.issubset(selections) else 0, dps['pchaos'][1]],
		"#% increased Chaos Damage with Spell Skills": [dps['pchaos'][0] if {'Spell'}.issubset(selections) else 0, dps['pchaos'][1]],
		# Damage - Any Attack
		'#% increased Attack Damage': [dps['pattack'][0] if {'Attack'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Melee Damage": [dps['pmelee'][0] if {'Attack', 'Melee'}.issubset(selections) else 0, dps['pmelee'][1]],
		"#% increased Damage with Axes": [dps['pattack'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Bows": [dps['pattack'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Claws": [dps['pattack'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Daggers": [dps['pattack'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Maces or Sceptres": [dps['pattack'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with One Handed Weapons": [dps['pattack'][0] if {'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Staves": [dps['pattack'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Swords": [dps['pattack'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Two Handed Weapons": [dps['pattack'][0] if {'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Damage with Wands": [dps['pattack'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Attack Damage while Dual Wielding": [dps['pattack'][0] if {'Attack', 'DualWielding'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Attack Damage while holding a Shield": [dps['pattack'][0] if {'Attack', 'Shield'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Projectile Attack Damage": [dps['pgeneric'][0] if {'Projectile', "Attack"}.issubset(selections) else 0, dps['pgeneric'][1]],
		# Damage - Any Spell
		"#% increased Spell Damage": [dps['pspell'][0] if {'Spell'}.issubset(selections) else 0, dps['pspell'][1]],
		"#% increased Spell Damage while Dual Wielding": [dps['pspell'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['pspell'][1]],
		"#% increased Spell Damage while holding a Shield": [dps['pspell'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['pspell'][1]],
		"#% increased Spell Damage while wielding a Staff": [dps['pspell'][0] if {'Spell', 'Staff'}.issubset(selections) else 0, dps['pspell'][1]],
		# Damage - Any
		"#% increased Area Damage": [max(dps['pspell'][0], dps['pattack'][0], dps['pmelee'][0]) if {'Area'}.issubset(selections) else 0, max(dps['pspell'][1], dps['pattack'][1], dps['pmelee'][1])],
		"#% increased Damage": [dps['pgeneric'][0], dps['pgeneric'][1]],
		"#% increased Mine Damage": [dps['pgeneric'][0] if {'Mine'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Projectile Damage": [dps['pgeneric'][0] if {'Projectile'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Totem Damage": [dps['pgeneric'][0] if {'Totem'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Trap Damage": [dps['pgeneric'][0] if {'Trap'}.issubset(selections) else 0, dps['pgeneric'][1]],
		# Damage - Conditional
		"#% increased Damage with Vaal Skills": [dps['pgeneric'][0] if {'Vaal'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"Triggered Spells deal #% increased Spell Damage": [dps['pgeneric'][0] if {'Trigger'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"Exerted Attacks deal #% increased Damage": [dps['pgeneric'][0] if {'Exerted'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Projectile Attack Damage during any Flask Effect": [dps['pgeneric'][0] if {'Projectile', "Attack", 'UsingFlask'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Damage while Leeching": [dps['pgeneric'][0] if {'Leeching'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Damage while Leeching Life": [dps['pgeneric'][0] if {'leechLife'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Damage while Leeching Mana": [dps['pgeneric'][0] if {'leechMana'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Elemental Damage if you've dealt a Critical Strike Recently": [dps['pelemental'][0] if {'CritRecently'}.issubset(selections) else 0, dps['pelemental'][1]],
		"#% increased Damage if you've Killed Recently": [dps['pgeneric'][0] if {'KilledRecently'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Damage with Hits against Chilled Enemies": [dps['pgeneric'][0] if {'EnemyChilled'}.issubset(selections) and {'Attack', 'Spell'}.intersection(selections) else 0, dps['pgeneric'][1]],
		# *x Damage
		"Spells have a #% chance to deal Double Damage": [dps['chancedoubledamage'][0] if {'Spell'}.issubset(selections) else 0, dps['chancedoubledamage'][1]],
		"#% chance to deal Double Damage": [dps['chancedoubledamage'][0], dps['chancedoubledamage'][1]],
		"#% chance to deal Double Damage if you have Stunned an Enemy Recently": [dps['chancedoubledamage'][0] if {'Stun'}.issubset(selections) else 0, dps['chancedoubledamage'][1]],
		"#% chance to deal Triple Damage": [dps['chancetripledamage'][0], dps['chancetripledamage'][1]],
		# Base Critical Strike chance
		"#% to Spell Critical Strike Chance": [dps['basecrit'][0] if {'Spell'}.issubset(selections) else 0, dps['basecrit'][1]],  # Note that this is base crit.  Yes the space is in the main trade site
		"Attacks have #% to Critical Strike Chance": [dps['basecrit'][0] if {'Attack'}.issubset(selections) else 0, dps['basecrit'][1]],  # Note that this is base crit.
		# Critical Strike Chance
		"#% increased Vaal Skill Critical Strike Chance": [dps['critchance'][0] if {'Vaal'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance for Spells": [dps['critchance'][0] if {'Spell'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance if you haven't dealt a Critical Strike Recently": [dps['critchance'][0] if {'NoRecentCrit'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Attack Critical Strike Chance while Dual Wielding": [dps['critchance'][0] if {'Attack', 'DualWielding'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Cold Skills": [dps['critchance'][0] if {'Cold'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Fire Skills": [dps['critchance'][0] if {'Fire'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Lightning Skills": [dps['critchance'][0] if {'Lightning'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with One Handed Melee Weapons": [dps['critchance'][0] if {'Attack', 'Melee'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Two Handed Melee Weapons": [dps['critchance'][0] if {'Attack', 'Melee', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Global Critical Strike Chance": [dps['critchance'][0], dps['critchance'][1]],
		"#% increased Melee Critical Strike Chance": [dps['critchance'][0] if {'Attack', 'Melee'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Elemental Skills": [dps['critchance'][0] if {'Elemental'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance against Poisoned Enemies": [dps['critchance'][0] if {'EnemyPoisoned'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance against Shocked Enemies": [dps['critchance'][0] if {'EnemyShocked'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance for Spells while Dual Wielding": [dps['critchance'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance for Spells while holding a Shield": [dps['critchance'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance for Spells while wielding a Staff": [dps['critchance'][0] if {'Spell', 'Staff'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance if you have Killed Recently": [dps['critchance'][0] if {'KilledRecently'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance if you've been Shocked Recently": [dps['critchance'][0] if {'beShocked'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% increased Critical Strike Chance with Bows": [dps['critchance'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['critchance'][1]],
		# Critical Strike Multiplier
		"#% to Melee Critical Strike Multiplier": [dps['critmulti'][0] if {'Attack', 'Melee'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Global Critical Strike Multiplier": [dps['critmulti'][0], dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Elemental Skills": [dps['critmulti'][0] if {'Elemental'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier for Spells": [dps['critmulti'][0] if {'Spell'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier if you've Killed Recently": [dps['critmulti'][0] if {'KilledRecently'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier while Dual Wielding": [dps['critmulti'][0] if {'DualWielding'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Cold Skills": [dps['critmulti'][0] if {'Cold'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Fire Skills": [dps['critmulti'][0] if {'Fire'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Lightning Skills": [dps['critmulti'][0] if {'Lightning'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with One Handed Melee Weapons": [dps['critmulti'][0] if {'Melee', 'Attack'}.issubset(selections) and {'TwoHandedWeapon'}.isdisjoint(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Two Handed Melee Weapons": [dps['critmulti'][0] if {'Melee', 'Attack', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% Critical Strike Multiplier while a Rare or Unique Enemy is Nearby": [dps['critmulti'][0] if {'NearbyRareUnique'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier for Spells while Dual Wielding": [dps['critmulti'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier for Spells while holding a Shield": [dps['critmulti'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier for Spells while wielding a Staff": [dps['critmulti'][0] if {'Spell', 'Staff'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier if you haven't dealt a Critical Strike Recently": [dps['critmulti'][0] if {'NoRecentCrit'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier if you've Shattered an Enemy Recently": [dps['critmulti'][0] if {'Shatter'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Axes": [dps['critmulti'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Bows": [dps['critmulti'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Claws": [dps['critmulti'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Daggers": [dps['critmulti'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Maces or Sceptres": [dps['critmulti'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Staves": [dps['critmulti'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Swords": [dps['critmulti'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['critmulti'][1]],
		"#% to Critical Strike Multiplier with Wands": [dps['critmulti'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['critmulti'][1]],
		# Flat Damage - Chaos
		"# to # Added Chaos Damage with Bow Attacks": [dps['flatchaos'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"# to # Added Chaos Damage with Claw Attacks": [dps['flatchaos'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"# to # Added Chaos Damage with Dagger Attacks": [dps['flatchaos'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"Adds # to # Chaos Damage to Attacks": [dps['flatchaos'][0] if {'Attack'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"Adds # to # Chaos Damage to Spells": [dps['flatchaos'][0] if {'Spell'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"# to # Added Spell Chaos Damage while Dual Wielding": [dps['flatchaos'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"# to # Added Spell Chaos Damage while holding a Shield": [dps['flatchaos'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"# to # Added Spell Chaos Damage while wielding a Two Handed Weapon": [dps['flatchaos'][0] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['flatchaos'][1]],
		"Adds # to # Chaos Damage": [dps['flatchaos'][0], dps['flatchaos'][1]],
		"Adds # to # Chaos Damage if you've dealt a Critical Strike Recently": [dps['flatchaos'][0] if {'CritRecently'}.issubset(selections) else 0, dps['flatchaos'][1]],
		# Flat Damage - Cold
		"Adds # to # Cold Damage to Attacks": [dps['flatcold'][0] if {'Attack'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Axe Attacks": [dps['flatcold'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Bow Attacks": [dps['flatcold'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Claw Attacks": [dps['flatcold'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Dagger Attacks": [dps['flatcold'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Mace or Sceptre Attacks": [dps['flatcold'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['flatcold'][1]],
		"Adds # to # Cold Damage to Spells": [dps['flatcold'][0] if {'Spell'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Spell Cold Damage while Dual Wielding": [dps['flatcold'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Spell Cold Damage while holding a Shield": [dps['flatcold'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Spell Cold Damage while wielding a Two Handed Weapon": [dps['flatcold'][0] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Staff Attacks": [dps['flatcold'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Sword Attacks": [dps['flatcold'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['flatcold'][1]],
		"# to # Added Cold Damage with Wand Attacks": [dps['flatcold'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['flatcold'][1]],
		"Adds # to # Cold Damage": [dps['flatcold'][0], dps['flatcold'][1]],
		"Adds # to # Cold Damage to Spells and Attacks": [dps['flatcold'][0] if {'Attack', 'Spell'}.intersection(selections) else 0, dps['flatcold'][1]],
		# Flat Damage - Fire
		"Adds # to # Fire Damage to Attacks": [dps['flatfire'][0] if {'Attack'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Axe Attacks": [dps['flatfire'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Bow Attacks": [dps['flatfire'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Claw Attacks": [dps['flatfire'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Dagger Attacks": [dps['flatfire'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Mace or Sceptre Attacks": [dps['flatfire'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['flatfire'][1]],
		"Adds # to # Fire Damage to Spells": [dps['flatfire'][0] if {'Spell'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Spell Fire Damage while Dual Wielding": [dps['flatfire'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Spell Fire Damage while holding a Shield": [dps['flatfire'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Spell Fire Damage while wielding a Two Handed Weapon": [dps['flatfire'][0] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Staff Attacks": [dps['flatfire'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Sword Attacks": [dps['flatfire'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['flatfire'][1]],
		"# to # Added Fire Damage with Wand Attacks": [dps['flatfire'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['flatfire'][1]],
		"Adds # to # Fire Damage": [dps['flatfire'][0], dps['flatfire'][1]],
		"Adds # to # Fire Damage to Spells and Attacks": [dps['flatfire'][0] if {'Attack', 'Spell'}.intersection(selections) else 0, dps['flatfire'][1]],
		# Flat Damage - Lightning
		"Adds # to # Lightning Damage to Attacks": [dps['flatlightning'][0] if {'Attack'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Axe Attacks": [dps['flatlightning'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Bow Attacks": [dps['flatlightning'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Claw Attacks": [dps['flatlightning'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Dagger Attacks": [dps['flatlightning'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Mace or Sceptre Attacks": [dps['flatlightning'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"Adds # to # Lightning Damage to Spells": [dps['flatlightning'][0] if {'Spell'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Spell Lightning Damage while Dual Wielding": [dps['flatlightning'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Spell Lightning Damage while holding a Shield": [dps['flatlightning'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Spell Lightning Damage while wielding a Two Handed Weapon": [dps['flatlightning'][0] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Staff Attacks": [dps['flatlightning'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Sword Attacks": [dps['flatlightning'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"# to # Added Lightning Damage with Wand Attacks": [dps['flatlightning'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"Adds # to # Lightning Damage": [dps['flatlightning'][0], dps['flatlightning'][1]],
		"Adds # to # Lightning Damage to Spells and Attacks": [dps['flatlightning'][0] if {'Attack', 'Spell'}.intersection(selections) else 0, dps['flatlightning'][1]],
		# Flat Damage - Physical
		"Adds # to # Physical Damage for each Impale on Enemy": [dps['flatphys'][0] * dps['ImpaleStacks'][0], dps['flatphys'][1] * dps['ImpaleStacks'][1]],
		"Adds # to # Physical Damage to Attacks": [dps['flatphys'][0] if {'Attack'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Axe Attacks": [dps['flatphys'][0] if {'Attack', 'Axe'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Bow Attacks": [dps['flatphys'][0] if {'Attack', 'Bow'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Claw Attacks": [dps['flatphys'][0] if {'Attack', 'Claw'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Dagger Attacks": [dps['flatphys'][0] if {'Attack', 'Dagger'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Mace or Sceptre Attacks": [dps['flatphys'][0] if {'Attack', 'Mace'}.issubset(selections) else 0, dps['flatphys'][1]],
		"Adds # to # Physical Damage to Spells": [dps['flatphys'][0] if {'Spell'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Spell Physical Damage while Dual Wielding": [dps['flatphys'][0] if {'Spell', 'DualWielding'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Spell Physical Damage while holding a Shield": [dps['flatphys'][0] if {'Spell', 'Shield'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Spell Physical Damage while wielding a Two Handed Weapon": [dps['flatphys'][0] if {'Spell', 'TwoHandedWeapon'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Staff Attacks": [dps['flatphys'][0] if {'Attack', 'Staff'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Sword Attacks": [dps['flatphys'][0] if {'Attack', 'Sword'}.issubset(selections) else 0, dps['flatphys'][1]],
		"# to # Added Physical Damage with Wand Attacks": [dps['flatphys'][0] if {'Attack', 'Wand'}.issubset(selections) else 0, dps['flatphys'][1]],
		# Flat Damage - Conditional
		"# to # added Fire Damage against Burning Enemies": [dps['flatfire'][0] if {'EnemyBurning'}.issubset(selections) else 0, dps['flatfire'][1]],
		"Adds # to # Fire Damage against Ignited Enemies": [dps['flatfire'][0] if {'EnemyIgnited'}.issubset(selections) else 0, dps['flatfire'][1]],
		"Adds # to # Cold Damage against Chilled or Frozen Enemies": [dps['flatcold'][0] if {'EnemyChilled', 'EnemyFrozen'}.intersection(selections) else 0, dps['flatcold'][1]],
		"Adds # to # Lightning Damage against Shocked Enemies": [dps['flatlightning'][0] if {'EnemyShocked'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"Adds # to # Cold Damage if you've dealt a Critical Strike Recently": [dps['flatcold'][0] if {'CritRecently'}.issubset(selections) else 0, dps['flatcold'][1]],
		"Adds # to # Fire Damage if you've dealt a Critical Strike Recently": [dps['flatfire'][0] if {'CritRecently'}.issubset(selections) else 0, dps['flatfire'][1]],
		"Adds # to # Lightning Damage if you've dealt a Critical Strike Recently": [dps['flatlightning'][0] if {'CritRecently'}.issubset(selections) else 0, dps['flatlightning'][1]],
		"Adds # to # Physical Damage if you've dealt a Critical Strike Recently": [dps['flatphys'][0] if {'CritRecently'}.issubset(selections) else 0, dps['flatphys'][1]],
		# Damage Penetration
		"Damage Penetrates #% Cold Resistance": [dps['pencold'][0], dps['pencold'][1]],
		"Damage Penetrates #% Elemental Resistance if you haven't Killed Recently": [dps['penall'][0] if {'NoRecentKill'}.issubset(selections) else 0, dps['penall'][1]],
		"Damage Penetrates #% Elemental Resistances": [dps['penall'][0], dps['penall'][1]],
		"Damage Penetrates #% Fire Resistance": [dps['penfire'][0], dps['penfire'][1]],
		"Damage Penetrates #% Lightning Resistance": [dps['penlightning'][0], dps['penlightning'][1]],
		"Damage Penetrates #% Chaos Resistance": [dps['penchaos'][0], dps['penchaos'][1]],
		"Damage with Weapons Penetrates #% Cold Resistance": [dps['pencold'][0] if {'Attack'}.issubset(selections) else 0, dps['pencold'][1]],
		"Damage with Weapons Penetrates #% Fire Resistance": [dps['penfire'][0] if {'Attack'}.issubset(selections) else 0, dps['penfire'][1]],
		"Damage with Weapons Penetrates #% Lightning Resistance": [dps['penlightning'][0] if {'Attack'}.issubset(selections) else 0, dps['penlightning'][1]],
		"Overwhelm #% Physical Damage Reduction": [dps['opdr'][0], dps['opdr'][1]],
		# Helmet Resist Mods
		"Nearby Enemies have #% to Chaos Resistance": [dps['nerchaos'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['nerchaos'][1]],
		"Nearby Enemies have #% to Cold Resistance": [dps['nercold'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['nercold'][1]],
		"Nearby Enemies have #% to Fire Resistance": [dps['nerfire'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['nerfire'][1]],
		"Nearby Enemies have #% to Lightning Resistance": [dps['nerlightning'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['nerlightning'][1]],
		"Nearby Enemies take #% increased Elemental Damage": [dps['neiele'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['neiele'][1]],
		"Nearby Enemies take #% increased Physical Damage": [dps['neiphys'][0] if {'NearbyEnemy'}.issubset(selections) else 0, dps['neiphys'][1]],
		# Gain % of ### as extra ###
		"Gain #% of Elemental Damage as Extra Chaos Damage": [dps['eleaschaos'][0], dps['eleaschaos'][1]],
		"Gain #% of Physical Damage as Extra Cold Damage": [dps['extracold'][0], dps['extracold'][1]],
		"Gain #% of Physical Damage as Extra Damage of a random Element": [dps['extrarandom'][0], dps['extrarandom'][1]],
		"Gain #% of Physical Damage as Extra Fire Damage": [dps['extrafire'][0], dps['extrafire'][1]],
		"Gain #% of Physical Damage as Extra Fire Damage if you've dealt a Critical Strike Recently": [dps['extrafire'][0] if {'CritRecently'}.issubset(selections) else 0, dps['extrafire'][1]],
		"Gain #% of Physical Damage as Extra Lightning Damage": [dps['extralightning'][0], dps['extralightning'][1]],
		"Gain #% of Non-Chaos Damage as extra Chaos Damage": [dps['extrachaos'][0], dps['extrachaos'][1]],
		"Gain #% of Cold Damage as Extra Chaos Damage": [dps['coldasextrachaos'][0], dps['coldasextrachaos'][1]],
		"Gain #% of Fire Damage as Extra Chaos Damage": [dps['fireasextrachaos'][0], dps['fireasextrachaos'][1]],
		"Gain #% of Lightning Damage as Extra Chaos Damage": [dps['lightningasextrachaos'][0], dps['lightningasextrachaos'][1]],
		"Gain #% of Physical Damage as Extra Chaos Damage": [dps['physicalasextrachaos'][0], dps['physicalasextrachaos'][1]],
		# Related to Endurance/Frenzy/Power charges
		'# to Maximum Power Charges': [dps['1powercharge'][0] if {'usePowerCharges'}.issubset(selections) else 0, dps['1powercharge'][1]],
		'# to Maximum Frenzy Charges': [dps['1frenzycharge'][0] if {'useFrenzyCharges'}.issubset(selections) else 0, dps['1frenzycharge'][1]],
		'# to Maximum Endurance Charges': [dps['1endurancecharge'][0] if {'useEnduranceCharges'}.issubset(selections) else 0, dps['1endurancecharge'][1]],
		'# to Maximum Power Charges and Maximum Endurance Charges': [dps['1powercharge'][0] + dps['1endurancecharge'][0] if {'usePowerCharges'}.issubset(selections) or {'useEnduranceCharges'}.issubset(selections) else 0, dps['1powercharge'][1] + dps['1endurancecharge'][1]],
		# Accuracy
		'# to Accuracy Rating': [dps['flataccuracy'][0], dps['flataccuracy'][1]],
		"#% increased Accuracy Rating with Axes": [dps['paccuracy'][0] if {'Axe'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Bows": [dps['paccuracy'][0] if {'Bow'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Claws": [dps['paccuracy'][0] if {'Claw'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Daggers": [dps['paccuracy'][0] if {'Dagger'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Maces or Sceptres": [dps['paccuracy'][0] if {'Mace'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Staves": [dps['paccuracy'][0] if {'Staff'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Swords": [dps['paccuracy'][0] if {'Sword'}.issubset(selections) else 0, dps['paccuracy'][1]],
		"#% increased Accuracy Rating with Wands": [dps['paccuracy'][0] if {'Wand'}.issubset(selections) else 0, dps['paccuracy'][1]],
		'#% increased Global Accuracy Rating': [dps['paccuracy'][0], dps['paccuracy'][1]],
#		"#% increased Accuracy Rating if you haven't Killed Recently": [dps['paccuracy'][0] if {'NoRecentKill'}.issubset(selections) else 0, dps['paccuracy'][1]],
		# Attributes
		'# to Strength': [dps['20str'][0], dps['20str'][1]],
		'# to Intelligence': [dps['20int'][0], dps['20int'][1]],
		'# to Dexterity': [dps['20dex'][0], dps['20dex'][1]],
		'# to Strength and Intelligence': [dps['20str'][0] + dps['20int'][0], dps['20str'][1] + dps['20int'][1]],
		'# to Strength and Dexterity': [dps['20str'][0] + dps['20dex'][0], dps['20str'][1] + dps['20dex'][1]],
		'# to Dexterity and Intelligence': [dps['20int'][0] + dps['20dex'][0], dps['20int'][1] + dps['20dex'][1]],
		'# to all Attributes': [dps['20int'][0] + dps['20dex'][0] + dps['20str'][0], dps['20int'][1] + dps['20dex'][1] + dps['20str'][1]],
		'#% increased Damage per 15 Dexterity': [dps['damageperdex'][0], dps['damageperdex'][1]],
		'#% increased Damage per 15 Intelligence': [dps['damageperint'][0], dps['damageperint'][1]],
		'#% increased Damage per 15 Strength': [dps['damageperstr'][0], dps['damageperstr'][1]],
		"#% increased Attributes": [dps['pstr'][0] + dps['pdex'][0] + dps['pint'][0], dps['pstr'][1] + dps['pdex'][1] + dps['pint'][1]],
		"#% increased Strength": [dps['pstr'][0], dps['pstr'][1]],
		"#% increased Intelligence": [dps['pint'][0], dps['pint'][1]],
		"#% increased Dexterity": [dps['pdex'][0], dps['pdex'][1]],
		# Damage Over Time
		"#% increased Damage over Time": [dps['pdot'][0], dps['pdot'][1]],
		"#% increased Chaos Damage over Time": [dps['pchaosdot'][0], dps['pchaosdot'][1]],
		"#% increased Physical Damage over Time": [dps['pphysdot'][0], dps['pphysdot'][1]],
		"#% increased Damage over Time while Dual Wielding": [dps['pdot'][0] if {'DualWielding'}.issubset(selections) else 0, dps['pdot'][1]],
		"#% increased Damage over Time while holding a Shield": [dps['pdot'][0] if {'Shield'}.issubset(selections) else 0, dps['pdot'][1]],
		"#% increased Damage over Time while wielding a Two Handed Weapon": [dps['pdot'][0] if {'TwoHandedWeapon'}.issubset(selections) else 0, dps['pdot'][1]],
		"#% increased Damage with Ailments": [dps['pdotailment'][0], dps['pdotailment'][1]],
		"#% increased Damage with Bleeding": [dps['pbleed'][0], dps['pbleed'][1]],
		"#% increased Damage with Poison": [dps['ppoison'][0], dps['ppoison'][1]],
		"#% increased Burning Damage": [dps['pignite'][0], dps['pignite'][1]],
		# Damage Over Time Multiplier
		"#% to Fire Damage over Time Multiplier": [dps['pfiredotmulti'][0], dps['pfiredotmulti'][1]],
		"#% to Cold Damage over Time Multiplier": [dps['pcolddotmulti'][0], dps['pcolddotmulti'][1]],
		"#% to Chaos Damage over Time Multiplier": [dps['pchaosdotmulti'][0], dps['pchaosdotmulti'][1]],
		'#% to Physical Damage over Time Multiplier': [dps['physdotmulti'][0], dps['physdotmulti'][1]],
		'#% to Damage over Time Multiplier': [dps['pdotmulti'][0], dps['pdotmulti'][1]],
		"#% to Chaos Damage over Time Multiplier with Attack Skills": [dps['pchaosdotmulti'][0] if {'Attack'}.intersection(selections) else 0, dps['pchaosdotmulti'][1]],
		"#% to Damage over Time Multiplier with Attack Skills": [dps['pdotmulti'][0] if {'Attack'}.intersection(selections) else 0, dps['pdotmulti'][1]],
		"#% to Fire Damage over Time Multiplier with Attack Skills": [dps['pfiredotmulti'][0] if {'Attack'}.intersection(selections) else 0, dps['pfiredotmulti'][1]],
		"#% to Physical Damage over Time Multiplier with Attack Skills": [dps['physdotmulti'][0] if {'Attack'}.intersection(selections) else 0, dps['physdotmulti'][1]],
		# Damage Over Time Conditional
		"Enemies Maimed by you take #% increased Damage Over Time": [dps['pdotmulti'][0] if {'EnemyMaimed'}.intersection(selections) else 0, dps['pdotmulti'][1]],
		# Life, ES, and Mana
		"# to maximum Life": [dps['flatlife'][0], dps['flatlife'][1]],
		"#% increased maximum Life": [dps['plife'][0], dps['plife'][1]],
		"# to maximum Energy Shield": [dps['flates'][0], dps['flates'][1]],
		"#% increased maximum Energy Shield": [dps['pes'][0], dps['pes'][1]],
		"# to maximum Mana": [dps['flatmana'][0], dps['flatmana'][1]],
		"#% increased maximum Mana": [dps['pmana'][0], dps['pmana'][1]],
		'#% reduced Mana Cost of Skills': [dps['pmanaskillreduce'][0], dps['pmanaskillreduce'][1]],
		"#% increased Totem Life": [dps['ptotemlife'][0], dps['ptotemlife'][1]],
		# Minion % damage
		"Minions have #% chance to deal Double Damage": [dps['minionchancedoubledamage'][0], dps['minionchancedoubledamage'][1]],
		"Minions deal #% increased Damage": [dps['pminion'][0], dps['pminion'][1]],
		"Minions have #% increased Attack Speed": [dps['minionattackspeed'][0], dps['minionattackspeed'][1]],
		"Minions have #% increased Cast Speed": [dps['minioncastspeed'][0], dps['minioncastspeed'][1]],
		"Minions have #% increased Attack and Cast Speed if you or your Minions have Killed Recently": [dps['minionattackspeed'][0] + dps['minioncastspeed'][0] if {'KilledRecently', 'MinionsKilledRecently'}.intersection(selections) else 0, dps['minionattackspeed'][1] + dps['minioncastspeed'][1]],
		"Minions deal #% increased Damage if you've used a Minion Skill Recently": [dps['pminion'][0] if {'UsedMinionSkillRecently'}.issubset(selections) else 0, dps['pminion'][1]],
		# Minion Flat Damage
		"Minions deal # to # additional Physical Damage": [dps['minionflatphys'][0], dps['minionflatphys'][1]],
		"Minions deal # to # additional Lightning Damage": [dps['minionflatlightning'][0], dps['minionflatlightning'][1]],
		"Minions deal # to # additional Cold Damage": [dps['minionflatcold'][0], dps['minionflatcold'][1]],
		"Minions deal # to # additional Fire Damage": [dps['minionflatfire'][0], dps['minionflatfire'][1]],
		"Minions deal # to # additional Chaos Damage": [dps['minionflatchaos'][0], dps['minionflatchaos'][1]],
		# Minion Accuracy
		"#% increased Minion Accuracy Rating": [dps['minionpaccuracy'][0], dps['minionpaccuracy'][1]],
		"Minions have # to Accuracy Rating": [dps['minionflataccuracy'][0], dps['minionflataccuracy'][1]],
		# Gem Levels Generic
		"# to Level of all Chaos Skill Gems": [dps['achaossg'][0], dps['achaossg'][1]],
		"# to Level of all Cold Skill Gems": [dps['acoldsg'][0], dps['acoldsg'][1]],
		"# to Level of all Fire Skill Gems": [dps['afiresg'][0], dps['afiresg'][1]],
		"# to Level of all Lightning Skill Gems": [dps['alightningsg'][0], dps['alightningsg'][1]],
		"# to Level of all Physical Skill Gems": [dps['aphysicalsg'][0], dps['aphysicalsg'][1]],
		"# to Level of all Dexterity Skill Gems": [dps['adexsg'][0], dps['adexsg'][1]],
		"# to Level of all Intelligence Skill Gems": [dps['aintsg'][0], dps['aintsg'][1]],
		"# to Level of all Strength Skill Gems": [dps['astrsg'][0], dps['astrsg'][1]],
		"# to Level of all Minion Skill Gems": [dps['aminionsg'][0], dps['aminionsg'][1]],
		"# to Level of all Raise Spectre Gems": [dps['aminionsg'][0] if {'Spectre'}.issubset(selections) else 0, dps['aminionsg'][1]],
		"# to Level of all Vaal Skill Gems": [dps['avaalsg'][0], dps['avaalsg'][1]],
		# Spell Gem Levels
		"# to Level of all Chaos Spell Skill Gems": [dps['achaossg'][0] if {'Spell'}.issubset(selections) else 0, dps['achaossg'][1]],
		"# to Level of all Cold Spell Skill Gems": [dps['acoldsg'][0] if {'Spell'}.issubset(selections) else 0, dps['acoldsg'][1]],
		"# to Level of all Fire Spell Skill Gems": [dps['afiresg'][0] if {'Spell'}.issubset(selections) else 0, dps['afiresg'][1]],
		"# to Level of all Lightning Spell Skill Gems": [dps['alightningsg'][0] if {'Spell'}.issubset(selections) else 0, dps['alightningsg'][1]],
		"# to Level of all Physical Spell Skill Gems": [dps['aphysicalsg'][0] if {'Spell'}.issubset(selections) else 0, dps['aphysicalsg'][1]],
		"# to Level of all Spell Skill Gems": [dps['aspellsg'][0] if {'Spell'}.issubset(selections) else 0, dps['aspellsg'][1]],
		# Aura related mods
		"Anger has #% increased Aura Effect": [dps['iaeanger'][0], dps['iaeanger'][1]],
		"Determination has #% increased Aura Effect": [dps['iaedeterminaton'][0], dps['iaedeterminaton'][1]],
		"Discipline has #% increased Aura Effect": [dps['iaediscipline'][0], dps['iaediscipline'][1]],
		"Grace has #% increased Aura Effect": [dps['iaegrace'][0], dps['iaegrace'][1]],
		"Hatred has #% increased Aura Effect": [dps['iaehatred'][0], dps['iaehatred'][1]],
		"Malevolence has #% increased Aura Effect": [dps['iaemalevolence'][0], dps['iaemalevolence'][1]],
		"Pride has #% increased Aura Effect": [dps['iaepride'][0], dps['iaepride'][1]],
		"Wrath has #% increased Aura Effect": [dps['iaewrath'][0], dps['iaewrath'][1]],
		"Zealotry has #% increased Aura Effect": [dps['iaezealotry'][0], dps['iaezealotry'][1]],
		"#% increased Effect of Non-Curse Auras from your Skills on Enemies": [dps['iaeenemy'][0], dps['iaeenemy'][1]],
		"#% increased effect of Non-Curse Auras from your Skills": [dps['iaenc'][0], dps['iaenc'][1]],
		"Auras from your Skills grant #% increased Damage to you and Allies": [dps['pdpas'][0], dps['pdpas'][1]],
		# Flasks
		"#% increased Critical Strike Chance during any Flask Effect": [dps['critchance'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['critchance'][1]],
		"#% to Critical Strike Multiplier during any Flask Effect": [dps['critmulti'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['critmulti'][1]],
		"Damage Penetrates #% Elemental Resistances during any Flask Effect": [dps['penall'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['penall'][1]],
		"#% increased Damage during any Flask Effect": [dps['pgeneric'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Attack Speed during any Flask Effect": [dps['attackspeed'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['attackspeed'][1]],
		"#% increased Cast Speed during any Flask Effect": [dps['castspeed'][0] if {'UsingFlask'}.issubset(selections) else 0, dps['castspeed'][1]],
		"#% increased Melee Damage during any Flask Effect": [dps['pgeneric'][0] if {'UsingFlask', 'Attack', 'Melee'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Spell Damage during any Flask Effect": [dps['pgeneric'][0] if {'UsingFlask', 'Spell'}.issubset(selections) else 0, dps['pgeneric'][1]],
		"#% increased Critical Strike Chance against Blinded Enemies": [dps['critchance'][0] if {'EnemyBlinded'}.issubset(selections) else 0, dps['critchance'][1]],
		# local flat damage mods for Spellslinger and BattleMage
		"Adds # to # Chaos Damage (Local)": [dps['flatchaos'][0] * localmulti, dps['flatchaos'][1] * localmulti],
		"Adds # to # Cold Damage (Local)": [dps['flatcold'][0] * localmulti, dps['flatcold'][1] * localmulti],
		"Adds # to # Fire Damage (Local)": [dps['flatfire'][0] * localmulti, dps['flatfire'][1] * localmulti],
		"Adds # to # Lightning Damage (Local)": [dps['flatlightning'][0] * localmulti, dps['flatlightning'][1] * localmulti],
		"Adds # to # Physical Damage (Local)": [dps['flatphys'][0] * localmulti, dps['flatphys'][1] * localmulti],
		# Rare or Precursor Emblem
		"# to # Added Cold Damage per Frenzy Charge": [dps['flatcold'][0] * dps["FrenzyCount"][0] if {'useFrenzyCharges'}.issubset(selections) else 0, dps['flatcold'][1] * dps["FrenzyCount"][1]],
		"#% increased Accuracy Rating per Frenzy Charge": [dps['paccuracy'][0] * dps["FrenzyCount"][0] if {'useFrenzyCharges'}.issubset(selections) else 0, dps['paccuracy'][1] * dps["FrenzyCount"][1]],
		"#% increased Damage per Frenzy Charge": [dps['pgeneric'][0] * dps["FrenzyCount"][0] if {'useFrenzyCharges'}.issubset(selections) else 0, dps['pgeneric'][1] * dps["FrenzyCount"][1]],
		"# to # Fire Damage per Endurance Charge": [dps['flatfire'][0] * dps["EnduranceCount"][0] if {'useEnduranceCharges'}.issubset(selections) else 0, dps['flatfire'][1] * dps["EnduranceCount"][1]],
		"#% increased Damage per Endurance Charge": [dps['pgeneric'][0] * dps["EnduranceCount"][0] if {'useEnduranceCharges'}.issubset(selections) else 0, dps['pgeneric'][1] * dps["EnduranceCount"][1]],
		"# to # Lightning Damage per Power Charge": [dps['flatlightning'][0] * dps["PowerCount"][0] if {'usePowerCharges'}.issubset(selections) else 0, dps['flatlightning'][1] * dps["PowerCount"][1]],
		"#% increased Damage per Power Charge": [dps['pgeneric'][0] * dps["PowerCount"][0] if {'usePowerCharges'}.issubset(selections) else 0, dps['pgeneric'][1] * dps["PowerCount"][1]],
		"#% increased Spell Damage per Power Charge": [dps['pgeneric'][0] * dps["PowerCount"][0] if {'usePowerCharges', 'Spell'}.issubset(selections) else 0, dps['pgeneric'][1] * dps["PowerCount"][1]],
		# Precursor Emblem
		"#% increased Critical Strike Chance per Frenzy Charge": [dps['critchance'][0] * dps["FrenzyCount"][0] if {'useFrenzyCharges', 'includeDelve'}.issubset(selections) else 0, dps['critchance'][1] * dps["FrenzyCount"][1]],
		"Gain #% of Cold Damage as Extra Chaos Damage per Frenzy Charge": [dps['coldasextrachaos'][0] * dps["FrenzyCount"][0] if {'useFrenzyCharges', 'includeDelve'}.issubset(selections) else 0, dps['coldasextrachaos'][1] * dps["FrenzyCount"][1]],
		"#% increased Attack and Cast Speed per Endurance Charge": [(dps['attackspeed'][0] + dps['castspeed'][0]) * dps["EnduranceCount"][0] if {'useEnduranceCharges', 'includeDelve'}.issubset(selections) else 0, (dps['attackspeed'][1] + dps['castspeed'][1]) * dps["EnduranceCount"][1] * dps["EnduranceCount"][1]],
		"#% increased Critical Strike Chance per Endurance Charge": [dps['critchance'][0] * dps["EnduranceCount"][0] if {'useEnduranceCharges', 'includeDelve'}.issubset(selections) else 0, dps['critchance'][1] * dps["EnduranceCount"][1]],
		"Gain #% of Fire Damage as Extra Chaos Damage per Endurance Charge": [dps['fireasextrachaos'][0] * dps["EnduranceCount"][0] if {'useEnduranceCharges', 'includeDelve'}.issubset(selections) else 0, dps['fireasextrachaos'][1] * dps["EnduranceCount"][1]],
		"#% increased Attack and Cast Speed per Power Charge": [(dps['attackspeed'][0] + dps['castspeed'][0]) * dps["PowerCount"][0] if {'usePowerCharges', 'includeDelve'}.issubset(selections) else 0, (dps['attackspeed'][1] + dps['castspeed'][1]) * dps["PowerCount"][1] * dps["PowerCount"][1]],
		"#% to Critical Strike Multiplier per Power Charge": [dps['critmulti'][0] * dps["PowerCount"][0] if {'usePowerCharges', 'includeDelve'}.issubset(selections) else 0, dps['critmulti'][1] * dps["PowerCount"][1]],
		"Gain #% of Lightning Damage as Extra Chaos Damage per Power Charge": [dps['lightningasextrachaos'][0] * dps["PowerCount"][0] if {'usePowerCharges', 'includeDelve'}.issubset(selections) else 0, dps['lightningasextrachaos'][1] * dps["PowerCount"][1]],
		# Unique item mods
		"#% increased Attack Damage if your other Ring is a Shaper Item": [dps['pattack'][0] if {'Attack', 'otherringshaper'}.issubset(selections) else 0, dps['pattack'][1]],
		"#% increased Spell Damage if your other Ring is an Elder Item": [dps['pspell'][0] if {'Spell', 'otherringelder'}.issubset(selections) else 0, dps['pspell'][1]],
		# Culling Strike
		"Culling Strike": [dps['perfectcull'][0], dps['perfectcull'][1]],


		# Not yet implemented
		"#% increased Energy Shield from Body Armour": [0, 0],
		"Gain #% of Maximum Life as Extra Maximum Energy Shield": [0, 0],
		"#% increased Duration of Ailments on Enemies": [0, 0],
		"Ignites you inflict deal Damage #% faster": [0, 0],
		"Bleeding you inflict deals Damage #% faster": [0, 0],
		"Poisons you inflict deal Damage #% faster": [0, 0],
		"Damaging Ailments deal damage #% faster": [0, 0],

	}
	# table to get the correct trade site json name
	lookup_bases = {
		"All Jewel": 'jewel',
		"Base Jewel": 'jewel.base',
		"Abyss Jewel": 'jewel.abyss',
		"Caster Weapon": 'weapon',
		"Wand (Spellslinger)": 'weapon.wand',
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

	pseudos = {}
	if {'PseudoMods'}.issubset(selections):
		pseudos = pseudo_lookup(modstr, base, reverse, selections)

	for mod in modstr:
		if modstr[mod][0]:
			for val in mods[mod]:
				if ('crafted' in val and ({'NoCraftedMods'}.issubset(selections) or mod not in r_mods[base]['crafted'])) or \
				   ('implicit' in val and ({'NoImplicitMods'}.issubset(selections) or
										   mod not in r_mods[base]['synth_implicit']+r_mods[base]['corrupt_implicit']+r_mods[base]['implicit'] or
										   ({'NoSynthImplicitMods', 'NoCorruptImplicitMods'}.issubset(selections) and mod not in r_mods[base]['implicit']) or
										   ({'NoSynthImplicitMods'}.issubset(selections) and mod not in r_mods[base]['corrupt_implicit']+r_mods[base]['implicit']) or
										   ({'NoCorruptImplicitMods'}.issubset(selections) and mod not in r_mods[base]['synth_implicit']+r_mods[base]['implicit']))) or \
				   ('explicit' in val and mod not in r_mods[base]['explicit']):
					continue
				mlist[val] = (round(modstr[mod][0], 2), modstr[mod][1])
				reverse[val] = mod
	mlist.update(pseudos)
	# TODO: Load values from file that is initialized by trade_mod_slots
	maxweight = 200
	baseweight = 55
	modweight = 4
	maxmods = int((maxweight - baseweight) / modweight)
	# sort mods based on their total value assumed by some amount of said mod instead of per point value
	for c, i in enumerate({k: v[0] for k, v in sorted(mlist.items(), key=lambda value: abs(value[1][1]), reverse=True)}):
		if c < maxmods:
			query.append(item.format(i, mlist[i][0]))
		else:
			trimmed.append(f'({i.split(".")[0]}) {reverse[i]} - {mlist[i][0]}')

	return searchstring.format(lookup_bases[base], int(max(dps['pgeneric'][0], dps['pminion'][0]) * 16), ','.join(query)), len(query) + len(trimmed), trimmed
