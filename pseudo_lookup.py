#!/usr/bin/python
# -*- coding: utf-8 -*-
# Generated: 07/25/2020(m/d/y) 02:10:05 utc


def pseudo_lookup(modstr, base):
	ret = {}
	if modstr["#% increased Elemental Damage"]:
		ret["pseudo.pseudo_increased_elemental_damage"] = round(modstr["#% increased Elemental Damage"], 2)
		del modstr["#% increased Elemental Damage"]
	if modstr["#% increased Spell Damage"]:
		ret["pseudo.pseudo_increased_spell_damage"] = round(modstr["#% increased Spell Damage"], 2)
		del modstr["#% increased Spell Damage"]
	if modstr["#% increased Global Physical Damage"] and base not in ["Caster Weapon", "Spellslinger MH", "Spellslinger DW"]:
		ret["pseudo.pseudo_increased_physical_damage"] = round(modstr["#% increased Global Physical Damage"], 2)
		del modstr["#% increased Global Physical Damage"]
	if modstr["#% increased Global Critical Strike Chance"]:
		ret["pseudo.pseudo_global_critical_strike_chance"] = round(modstr["#% increased Global Critical Strike Chance"], 2)
		del modstr["#% increased Global Critical Strike Chance"]
	if modstr["#% to Global Critical Strike Multiplier"]:
		ret["pseudo.pseudo_global_critical_strike_multiplier"] = round(modstr["#% to Global Critical Strike Multiplier"], 2)
		del modstr["#% to Global Critical Strike Multiplier"]
	if modstr["#% increased Attack Speed"] and base not in ["Caster Weapon", "Spellslinger MH", "Spellslinger DW"]:
		ret["pseudo.pseudo_total_attack_speed"] = round(modstr["#% increased Attack Speed"], 2)
		del modstr["#% increased Attack Speed"]
	if modstr["#% increased Cast Speed"]:
		ret["pseudo.pseudo_total_cast_speed"] = round(modstr["#% increased Cast Speed"], 2)
		del modstr["#% increased Cast Speed"]
	if modstr["#% increased Critical Strike Chance for Spells"]:
		ret["pseudo.pseudo_critical_strike_chance_for_spells"] = round(modstr["#% increased Critical Strike Chance for Spells"], 2)
		del modstr["#% increased Critical Strike Chance for Spells"]
	if modstr["Adds # to # Chaos Damage to Attacks"] and (modstr["Adds # to # Chaos Damage to Attacks"] == modstr["Adds # to # Chaos Damage"]):
		ret["pseudo.pseudo_adds_chaos_damage_to_attacks"] = round(modstr["Adds # to # Chaos Damage to Attacks"], 2)
		del modstr["Adds # to # Chaos Damage to Attacks"]
		del modstr["Adds # to # Chaos Damage"]
	if modstr["Adds # to # Chaos Damage to Spells"] and (modstr["Adds # to # Chaos Damage to Spells"] == modstr["Adds # to # Chaos Damage"]):
		ret["pseudo.pseudo_adds_chaos_damage_to_spells"] = round(modstr["Adds # to # Chaos Damage to Spells"], 2)
		del modstr["Adds # to # Chaos Damage to Spells"]
		del modstr["Adds # to # Chaos Damage"]
	if modstr["Adds # to # Cold Damage to Attacks"] and (modstr["Adds # to # Cold Damage to Attacks"] == modstr["Adds # to # Cold Damage"] == modstr["Adds # to # Cold Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_cold_damage_to_attacks"] = round(modstr["Adds # to # Cold Damage to Attacks"], 2)
		del modstr["Adds # to # Cold Damage to Attacks"]
		del modstr["Adds # to # Cold Damage"]
		del modstr["Adds # to # Cold Damage to Spells and Attacks"]
	if modstr["Adds # to # Cold Damage to Spells"] and (modstr["Adds # to # Cold Damage to Spells"] == modstr["Adds # to # Cold Damage"] == modstr["Adds # to # Cold Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_cold_damage_to_spells"] = round(modstr["Adds # to # Cold Damage to Spells"], 2)
		del modstr["Adds # to # Cold Damage to Spells"]
		del modstr["Adds # to # Cold Damage"]
		del modstr["Adds # to # Cold Damage to Spells and Attacks"]
	if modstr["Adds # to # Fire Damage to Attacks"] and (modstr["Adds # to # Fire Damage to Attacks"] == modstr["Adds # to # Fire Damage"] == modstr["Adds # to # Fire Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_fire_damage_to_attacks"] = round(modstr["Adds # to # Fire Damage to Attacks"], 2)
		del modstr["Adds # to # Fire Damage to Attacks"]
		del modstr["Adds # to # Fire Damage"]
		del modstr["Adds # to # Fire Damage to Spells and Attacks"]
	if modstr["Adds # to # Fire Damage to Spells"] and (modstr["Adds # to # Fire Damage to Spells"] == modstr["Adds # to # Fire Damage"] == modstr["Adds # to # Fire Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_fire_damage_to_spells"] = round(modstr["Adds # to # Fire Damage to Spells"], 2)
		del modstr["Adds # to # Fire Damage to Spells"]
		del modstr["Adds # to # Fire Damage"]
		del modstr["Adds # to # Fire Damage to Spells and Attacks"]
	if modstr["Adds # to # Lightning Damage to Attacks"] and (modstr["Adds # to # Lightning Damage to Attacks"] == modstr["Adds # to # Lightning Damage"] == modstr["Adds # to # Lightning Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_lightning_damage_to_attacks"] = round(modstr["Adds # to # Lightning Damage to Attacks"], 2)
		del modstr["Adds # to # Lightning Damage to Attacks"]
		del modstr["Adds # to # Lightning Damage"]
		del modstr["Adds # to # Lightning Damage to Spells and Attacks"]
	if modstr["Adds # to # Lightning Damage to Spells"] and (modstr["Adds # to # Lightning Damage to Spells"] == modstr["Adds # to # Lightning Damage"] == modstr["Adds # to # Lightning Damage to Spells and Attacks"]):
		ret["pseudo.pseudo_adds_lightning_damage_to_spells"] = round(modstr["Adds # to # Lightning Damage to Spells"], 2)
		del modstr["Adds # to # Lightning Damage to Spells"]
		del modstr["Adds # to # Lightning Damage"]
		del modstr["Adds # to # Lightning Damage to Spells and Attacks"]
	if modstr["Adds # to # Physical Damage to Attacks"] and (modstr["Adds # to # Physical Damage to Attacks"] == modstr["Adds # to # Physical Damage"]):
		ret["pseudo.pseudo_adds_physical_damage_to_attacks"] = round(modstr["Adds # to # Physical Damage to Attacks"], 2)
		del modstr["Adds # to # Physical Damage to Attacks"]
		del modstr["Adds # to # Physical Damage"]
	if modstr["Adds # to # Physical Damage to Spells"] and (modstr["Adds # to # Physical Damage to Spells"] == modstr["Adds # to # Physical Damage"]):
		ret["pseudo.pseudo_adds_physical_damage_to_spells"] = round(modstr["Adds # to # Physical Damage to Spells"], 2)
		del modstr["Adds # to # Physical Damage to Spells"]
		del modstr["Adds # to # Physical Damage"]
	return ret
