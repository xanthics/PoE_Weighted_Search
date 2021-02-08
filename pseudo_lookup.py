#!/usr/bin/python
# -*- coding: utf-8 -*-
# Generated: 02/08/2021(m/d/y) 08:49:09 utc


# Autogenerated function to implement pseudomods
def pseudo_lookup(modstr, base, reverse, selections):
	ret = {}
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Global Critical Strike Chance"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_global_critical_strike_chance"] = round(modstr["#% increased Global Critical Strike Chance"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Global Critical Strike Chance"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_global_critical_strike_chance"] = "+#% Global Critical Strike Chance"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Critical Strike Chance for Spells"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_critical_strike_chance_for_spells"] = round(modstr["#% increased Critical Strike Chance for Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Critical Strike Chance for Spells"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_critical_strike_chance_for_spells"] = "+#% total Critical Strike Chance for Spells"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% to Global Critical Strike Multiplier"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_global_critical_strike_multiplier"] = round(modstr["#% to Global Critical Strike Multiplier"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% to Global Critical Strike Multiplier"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_global_critical_strike_multiplier"] = "+#% Global Critical Strike Multiplier"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Cast Speed"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_total_cast_speed"] = round(modstr["#% increased Cast Speed"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Cast Speed"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_total_cast_speed"] = "+#% total Cast Speed"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["Adds # to # Chaos Damage to Attacks"] and (modstr["Adds # to # Chaos Damage to Attacks"] == modstr["Adds # to # Chaos Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_chaos_damage_to_attacks"] = round(modstr["Adds # to # Chaos Damage to Attacks"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Chaos Damage to Attacks"] = modstr["Adds # to # Chaos Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_chaos_damage_to_attacks"] = "Adds # to # Chaos Damage to Attacks"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Chaos Damage to Spells"] and (modstr["Adds # to # Chaos Damage to Spells"] == modstr["Adds # to # Chaos Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_chaos_damage_to_spells"] = round(modstr["Adds # to # Chaos Damage to Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Chaos Damage to Spells"] = modstr["Adds # to # Chaos Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_chaos_damage_to_spells"] = "Adds # to # Chaos Damage to Spells"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Chaos Damage"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_chaos_damage"] = round(modstr["Adds # to # Chaos Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Chaos Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_chaos_damage"] = "Adds # to # Chaos Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["Adds # to # Lightning Damage to Attacks"] and (modstr["Adds # to # Lightning Damage to Attacks"] == modstr["Adds # to # Lightning Damage"] == modstr["Adds # to # Lightning Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_lightning_damage_to_attacks"] = round(modstr["Adds # to # Lightning Damage to Attacks"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Lightning Damage to Attacks"] = modstr["Adds # to # Lightning Damage"] = modstr["Adds # to # Lightning Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_lightning_damage_to_attacks"] = "Adds # to # Lightning Damage to Attacks"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Lightning Damage to Spells"] and (modstr["Adds # to # Lightning Damage to Spells"] == modstr["Adds # to # Lightning Damage"] == modstr["Adds # to # Lightning Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_lightning_damage_to_spells"] = round(modstr["Adds # to # Lightning Damage to Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Lightning Damage to Spells"] = modstr["Adds # to # Lightning Damage"] = modstr["Adds # to # Lightning Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_lightning_damage_to_spells"] = "Adds # to # Lightning Damage to Spells"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Lightning Damage"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_lightning_damage"] = round(modstr["Adds # to # Lightning Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Lightning Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_lightning_damage"] = "Adds # to # Lightning Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["Adds # to # Fire Damage to Attacks"] and (modstr["Adds # to # Fire Damage to Attacks"] == modstr["Adds # to # Fire Damage"] == modstr["Adds # to # Fire Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_fire_damage_to_attacks"] = round(modstr["Adds # to # Fire Damage to Attacks"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Fire Damage to Attacks"] = modstr["Adds # to # Fire Damage"] = modstr["Adds # to # Fire Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_fire_damage_to_attacks"] = "Adds # to # Fire Damage to Attacks"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Fire Damage to Spells"] and (modstr["Adds # to # Fire Damage to Spells"] == modstr["Adds # to # Fire Damage"] == modstr["Adds # to # Fire Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_fire_damage_to_spells"] = round(modstr["Adds # to # Fire Damage to Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Fire Damage to Spells"] = modstr["Adds # to # Fire Damage"] = modstr["Adds # to # Fire Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_fire_damage_to_spells"] = "Adds # to # Fire Damage to Spells"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Fire Damage"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_fire_damage"] = round(modstr["Adds # to # Fire Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Fire Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_fire_damage"] = "Adds # to # Fire Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["Adds # to # Cold Damage to Attacks"] and (modstr["Adds # to # Cold Damage to Attacks"] == modstr["Adds # to # Cold Damage"] == modstr["Adds # to # Cold Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_cold_damage_to_attacks"] = round(modstr["Adds # to # Cold Damage to Attacks"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Cold Damage to Attacks"] = modstr["Adds # to # Cold Damage"] = modstr["Adds # to # Cold Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_cold_damage_to_attacks"] = "Adds # to # Cold Damage to Attacks"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Cold Damage to Spells"] and (modstr["Adds # to # Cold Damage to Spells"] == modstr["Adds # to # Cold Damage"] == modstr["Adds # to # Cold Damage to Spells and Attacks"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_cold_damage_to_spells"] = round(modstr["Adds # to # Cold Damage to Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Cold Damage to Spells"] = modstr["Adds # to # Cold Damage"] = modstr["Adds # to # Cold Damage to Spells and Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_cold_damage_to_spells"] = "Adds # to # Cold Damage to Spells"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Cold Damage"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_cold_damage"] = round(modstr["Adds # to # Cold Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Cold Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_cold_damage"] = "Adds # to # Cold Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["Adds # to # Physical Damage to Attacks"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_physical_damage_to_attacks"] = round(modstr["Adds # to # Physical Damage to Attacks"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Physical Damage to Attacks"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_physical_damage_to_attacks"] = "Adds # to # Physical Damage to Attacks"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["Adds # to # Physical Damage to Spells"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_adds_physical_damage_to_spells"] = round(modstr["Adds # to # Physical Damage to Spells"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["Adds # to # Physical Damage to Spells"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_adds_physical_damage_to_spells"] = "Adds # to # Physical Damage to Spells"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Cold Damage"] and (modstr["#% increased Cold Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Elemental Damage with Attack Skills"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_cold_damage_with_attack_skills"] = round(modstr["#% increased Cold Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Cold Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Elemental Damage with Attack Skills"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_cold_damage_with_attack_skills"] = "#% increased Cold Damage with Attack Skills"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Cold Damage"] and (modstr["#% increased Cold Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Spell Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_cold_spell_damage"] = round(modstr["#% increased Cold Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Cold Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Spell Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_cold_spell_damage"] = "#% increased Cold Spell Damage"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Cold Damage"] and (modstr["#% increased Cold Damage"] == modstr["#% increased Elemental Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_cold_damage"] = round(modstr["#% increased Cold Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Cold Damage"] = modstr["#% increased Elemental Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_cold_damage"] = "#% increased Cold Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Fire Damage"] and (modstr["#% increased Fire Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Elemental Damage with Attack Skills"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_fire_damage_with_attack_skills"] = round(modstr["#% increased Fire Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Fire Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Elemental Damage with Attack Skills"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_fire_damage_with_attack_skills"] = "#% increased Fire Damage with Attack Skills"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Fire Damage"] and (modstr["#% increased Fire Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Spell Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_fire_spell_damage"] = round(modstr["#% increased Fire Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Fire Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Spell Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_fire_spell_damage"] = "#% increased Fire Spell Damage"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Fire Damage"] and (modstr["#% increased Fire Damage"] == modstr["#% increased Elemental Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_fire_damage"] = round(modstr["#% increased Fire Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Fire Damage"] = modstr["#% increased Elemental Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_fire_damage"] = "#% increased Fire Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Lightning Damage"] and (modstr["#% increased Lightning Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Elemental Damage with Attack Skills"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_lightning_damage_with_attack_skills"] = round(modstr["#% increased Lightning Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Lightning Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Elemental Damage with Attack Skills"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_lightning_damage_with_attack_skills"] = "#% increased Lightning Damage with Attack Skills"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Lightning Damage"] and (modstr["#% increased Lightning Damage"] == modstr["#% increased Elemental Damage"] == modstr["#% increased Spell Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_lightning_spell_damage"] = round(modstr["#% increased Lightning Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Lightning Damage"] = modstr["#% increased Elemental Damage"] = modstr["#% increased Spell Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_lightning_spell_damage"] = "#% increased Lightning Spell Damage"
	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	elif modstr["#% increased Lightning Damage"] and (modstr["#% increased Lightning Damage"] == modstr["#% increased Elemental Damage"]):
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_lightning_damage"] = round(modstr["#% increased Lightning Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Lightning Damage"] = modstr["#% increased Elemental Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_lightning_damage"] = "#% increased Lightning Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Global Physical Damage"] and base not in ["Caster Weapon", "Wand (Spellslinger)"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_increased_physical_damage"] = round(modstr["#% increased Global Physical Damage"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Global Physical Damage"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_increased_physical_damage"] = "#% total increased Physical Damage"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["#% increased Attack Speed"] and base not in ["Caster Weapon", "Wand (Spellslinger)"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_total_attack_speed"] = round(modstr["#% increased Attack Speed"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["#% increased Attack Speed"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_total_attack_speed"] = "+#% total Attack Speed"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["# to Dexterity"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_total_dexterity"] = round(modstr["# to Dexterity"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["# to Dexterity"] = modstr["# to Strength and Dexterity"] = modstr["# to Dexterity and Intelligence"] = modstr["# to all Attributes"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_total_dexterity"] = "+# total to Dexterity"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["# to Intelligence"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_total_intelligence"] = round(modstr["# to Intelligence"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["# to Intelligence"] = modstr["# to Strength and Intelligence"] = modstr["# to Dexterity and Intelligence"] = modstr["# to all Attributes"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_total_intelligence"] = "+# total to Intelligence"

	# Check that the value is non-zero and if necessary that it isn't a bad base for that mod and that all values are equal
	if modstr["# to Strength"]:
		# Assign the value to our pseudomod
		ret["pseudo.pseudo_total_strength"] = round(modstr["# to Strength"], 2)
		# zero out the mods being used by pseudomod.  Don't delete from list so that we don't crash if checked later
		modstr["# to Strength"] = modstr["# to Strength and Intelligence"] = modstr["# to Strength and Dexterity"] = modstr["# to all Attributes"] = 0
		# Add mod to reverse lookup in case mod gets trimmed
		reverse["pseudo.pseudo_total_strength"] = "+# total to Strength"

	return ret
