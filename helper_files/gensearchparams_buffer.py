# Collection of mods that have been rejected

dps = 0
selections = set()

# mods that are explicitly skipped, comment with where they appear
disabled = {
	# dead explicit, only on standard
	"#% increased Melee Physical Damage while holding a Shield": dps['pphysical'] if {'Attack', 'Melee', 'Shield'}.issubset(selections) else 0,
	# Cyclopean Coil
	"#% increased Damage per 5 of your lowest Attribute": 0,
	# Pandemonius
	"Damage Penetrates #% Cold Resistance against Chilled Enemies": dps['pencold'] if {'conditionEnemyChilled'}.issubset(selections) else 0,
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
	# Local mod
	"#% increased Critical Strike Chance": dps['critchance'],

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
	"#% increased Accuracy Rating with Mace or Sceptre": ["implicit.stat_3208450870"],
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
	"#% to Critical Strike Multiplier with Mace or Sceptre": ["implicit.stat_458899422"],
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
