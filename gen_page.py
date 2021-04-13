from browser import document as doc
from browser.html import TABLE, TR, TH, TD, BUTTON, DIV, STRONG, INPUT, LABEL, P, BR, H1, H3, UL, LI, A, SELECT, OPTION, SECTION
from browser import bind
from browser.local_storage import storage

from gensearchparams import gensearchparams
from leaguelist import leagues
from baselist import bases
from modsjson import mjson

# checkboxes that have their state saved
saved_states = ["NoCraftedMods", "NoImplicitMods", "includeDelve", "PseudoMods"]

storage_key = "poe_weighted_search"

current_version = max(mjson)


# Setter storage so that we can differentiate values on this site from others at the same domain
def set_storage(key, val):
	storage["{}-{}".format(storage_key, key)] = val


# Getting for storage so that we can differentiate values on this site from others at the same domain
def get_storage(key):
	return storage["{}-{}".format(storage_key, key)]


# Check if a value exists in storage
def check_storage(key):
	return "{}-{}".format(storage_key, key) in storage


# Gathers the weights and flags on the page to generate a query for the main trade site
def generate_query(ev):
	league = leagues[doc['league'].selectedIndex]
	set_storage('league', league)
	base = bases[doc['base'].selectedIndex]
	set_storage('base', base)
	for _f in saved_states:
		if doc[_f].checked:
			set_storage(_f, "T")
		else:
			set_storage(_f, "")
	url_api = f'https://www.pathofexile.com/trade/search/{league}?q='
	dps = {}
	for elt in doc.get(selector='input[type="number"].dps_val'):
		dps[elt.id] = [float(elt.value)/float(elt.getAttribute("data-normal")), float(elt.value)]
	dps['extrarandom'] = [(dps['extrafire'][0] + dps['extracold'][0] + dps['extralightning'][0]) / 3, (dps['extrafire'][1] + dps['extracold'][1] + dps['extralightning'][1]) / 3]
	selections = set()
	for elt in doc.get(selector='input[type="checkbox"]'):
		if elt.checked:
			selections.add(elt.id)
	mjson_max = max(mjson)
	if mjson_max != current_version:
		for mod in mjson[mjson_max]:
			if mod['name'] not in dps:
				dps[mod['name']] = [0, 0]
	querystring, count, culled = gensearchparams(dps, selections, base)
	doc['culled'].text = ''
	if culled:
		mystr = ''
		for _x in [BR() + x for x in culled]:
			mystr += _x
		doc['culled'] <= BR() + f'{len(culled)} mods were culled from query.' + BR() + mystr
	doc["query"].href = url_api + querystring
	doc["modcount"].text = count
	doc["414bypass"].value = querystring
	doc["query"].style.display = "inline"
	doc["notice"].style.display = "inline"
	doc["414by"].style.display = "inline"


# If there is a query string, processes it to fill in values
def process_querystring():
	global current_version
	if len(str(doc.query)):
		if 'vals' in doc.query:
			n_arr = doc.query['vals'].split(',')
			version = int(n_arr[0])
			if version in mjson:
				if version != current_version:
					doc['specialnotice'] <= H1("You are using an outdated version of mods.json, this should automatically update when you start PoB-Item-Tester" + BR() + f"Current version is {current_version}, you are using {version}.")
					doc['specialnotice'].style.display = 'block'
					current_version = version
				init_weight(current_version)
				for c, val in enumerate(n_arr[1:]):
					if val:
						doc[mjson[version][c]['name']].value = float(val)
			else:
				doc['specialnotice'] <= H1("You are using an unsupported version of mods.json" + BR() + f"Current version is {current_version}, you are using {version}.")
				doc['specialnotice'].style.display = 'block'
				init_weight(current_version)
			# Handle mods that aren't weights or flags
			for key in doc.query:
				if key not in ['Flags', 'vals']:
					try:
						doc[key].value = doc.query[key]
					except KeyError:
						print(f"Key '{key}' recieved but not currently supported")

		else:
			init_weight(0)
#			doc['specialnotice'] <= H1("You are using an outdated version of PoB-Item-Tester" + BR() + f"Update from " + A("VolatilePulse's Github Repository", href="https://github.com/VolatilePulse/PoB-Item-Tester", target="_blank"))
			doc['specialnotice'] <= P(f"Several mods have been given support on this site ahead of changes to PoB-Item-Tester.  If you would like to see the updated Weights list, add &vals={current_version} to the end of the url (and hit enter)" + BR() + f"Current version is {current_version}.")
			doc['specialnotice'].style.display = 'block'
			current_version = 0
			for key in doc.query:
				if key not in ['Flags']:
					try:
						doc[key].value = doc.query[key]
					except KeyError:
						print(f"Key '{key}' recieved but not currently supported")

		try:
			flags = doc.query["Flags"].strip(',').split(',')
			for f in flags:
				if f.startswith('condition'):
					f = f[9:]
				try:
					doc[f].checked = True
				except KeyError:
					print("Flag '{}' recieved but not currently supported.".format(f))
			if 'CritRecently' not in flags:
				doc["NoRecentCrit"].checked = True
			if 'KilledRecently' not in flags:
				doc["NoRecentKill"].checked = True
		except KeyError:
			print("No Flags parameter passed in query string")

		for val in ['Skill', 'Character']:
			try:
				if doc.query[val]:
					doc[val] <= doc.query[val]
			except KeyError:
				doc[val].style.display = "none"
	else:
		init_weight(current_version)
		print("No query string found")

	# Set default states
	doc["PseudoMods"].checked = True
	for _f in saved_states:
		if check_storage(_f):
			doc[_f].checked = bool(get_storage(_f))


# Populate the league dropdown with values
def create_league_list():
	sel = SELECT(size=1, multiple=False, id="league")
	for league in leagues:
		sel <= OPTION(league)
	doc['leaguelist'] <= sel
	if check_storage('league') and get_storage('league') in leagues:
		doc['league'].value = get_storage('league')


# Populate the bases dropdown with values
def create_base_list():
	sel = SELECT(size=1, multiple=False, id="base")
	for base in bases:
		sel <= OPTION(base)
	doc['baselist'] <= sel
	if check_storage('base') and get_storage('base') in bases:
		doc['base'].value = get_storage('base')


# Initialize all ui elements for the home page
def init_page():
	create_league_list()
	create_base_list()
	pages = ['Main', 'Weights', 'Flags', 'About', 'Changelog']
	for c, page in enumerate(pages):
		doc['buttons'] <= BUTTON(page, data_id=page, Class=f'page{" current_tab" if not c else ""}', Id=f'b_{page}')
		doc['pages'] <= SECTION(Id=page)
		if c:
			doc[page].style.display = 'none'

	data = [('includeDelve', 'Include Precursor Emblem mods'), ('NoCraftedMods', 'Ignore Crafted Mods'), ('NoImplicitMods', 'Ignore Implicit Mods'), ('PseudoMods', 'Use PseudoMods in Search')]
	t = make_table(data, 1, 'ignore')
	doc['searchflags'] <= STRONG('Options:') + ' choices that affect type of returned mods' + BR() + 'PseudoMods is experimental. Please report any issues.' + t + BR()

	init_about()
	init_flags()
	init_change()

	doc["query"].style.display = "none"
	doc["notice"].style.display = "none"
	doc["414by"].style.display = "none"
	b_generate = BUTTON("Generate Query")
	b_generate.bind("click", generate_query)
	doc["generate"] <= b_generate
	process_querystring()
	init_main()
	doc["loading"].style.display = "none"

	# Make it so navigation buttons work
	@bind('.page', 'click')
	def change_page(ev):
		val = ev.target['data-id']
		if val == 'Main':
			init_main()
		doc[val].style.display = 'block'
		doc[f'b_{val}'].attrs['class'] = 'current_tab page'
		idx = pages.index(val)
		for i in pages[:idx] + pages[idx+1:]:
			doc[i].style.display = 'none'
			doc[f'b_{i}'].attrs['class'] = 'page'


# Fill in the "about" page
def init_about():
	t = doc['About']
	t <= H1('Usage Hint')
	t <= P('This tool is for finding additions to your current gear set.  So if you are replacing an item, you should unequip it in PoB first and save, before doing a search.')
	t <= H1('Design Choices')
	t <= P("This page is designed for finding rares for any slot based on how they affect your damage.  Attack weapons are not supported due to them not being modelable with weights.  Additionally almost all unique only mods are ignored.")
	t <= P("A summary of mods/items that aren't supported (yet?).  Some list items will be revisited after PoB 2.0 update.")
	t <= UL(
		LI('Flasks') +
		LI('All uniques except delve rings and Shaper/Elder rings') +
		LI('effect of non-damaging ailments') +
		LI('cooldown reduction') +
		LI('while focused') +
		LI('with this weapon') +
		LI('bleed & ignite duration') +
		LI('chance to bleed/poison/ignite') +
		LI('local weapon mods except flat phys & element, for spellslinger and battlemage.  phys can\'t account for % mods or weapon base stats') +
		LI('Heist weapon only implicits for mods that depend on the base weapon stats also.  EG #% to Damage over Time Multiplier for Bleeding (Sundering Axe)') +
		LI('Increases and Reductions to Damage of Vaal Skills also apply to Non-Vaal Skills') +
		LI('+ minimum charges') +
		LI('onslaught') +
		LI('Mods such as # to # Added Attack Lightning Damage per 200 Accuracy Rating + 25% less accuracy') +
		LI('attack mods that can only appear on weapons') +
		LI('mh/oh specific mods') +
		LI('annoints') +
		LI('Flasks applied to you have #% increased Effect') +
		LI('#% to Quality (any type)') +
		LI('# to Level of Socketed Gems and other mods that require your skill to be socketed in that item.')
	)
	t <= P("Here are all the " + A('Good Mods', href="https://github.com/xanthics/PoE_Weighted_Search/blob/master/helper_files/goodmod.py", target="_blank") + " that are implemented and " + A('Where they appear', href="https://github.com/xanthics/PoE_Weighted_Search/blob/master/restrict_mods.py", target="_blank") + "  Here are all the " + A('Bad Mods', href="https://github.com/xanthics/PoE_Weighted_Search/blob/master/helper_files/badmod.py", target="_blank") + ' which are skipped.')
	t <= H1('Using this page.')
	t <= P('There are 2 primary ways to use this page. A script created by VolatilePulse and coldino, or manually adding the jewels with the necessary mods to PoB and copying the values over by hand.')
	t <= H3('Using VolatilePulse and coldino\'s script')
	t <= UL(
		LI("Go to" + A(" PoB Fork releases page ", href="https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases", target="_blank") + "and download Path Of Building(Community Fork).") +
		LI("Install or extract files") +
		LI("Create and save a build. Leave PoB running") +
		LI("Navigate to" + A(" VolatilePulse's Github Repository", href="https://github.com/VolatilePulse/PoB-Item-Tester", target="_blank")) +
		LI("Clone or download, unzip, and enter directory") +
		LI("Run TestItem.ahk, select the build you want from the list.") +
		LI("Ctrl+Windows+d and it should automatically open this page with values filled out.") +
		LI("Ctrl+Alt+Windows+d will prompt you to choose build and then automatically open this page.") +
		LI("Double check all of the flags to make sure they match what you are trying to do. EG if you are molten strike you probably don't care about the melee flag as the projectile part is more important")
	)
	t <= STRONG("Troubleshooting:")
	t <= P('After the first time you run TestItem.ahk it will generate TestItem.ini. You may need to modify "PathToPoB"')
	t <= H3("Manually copy from PoB")
	t <= P("This is what the Item Tester is automating for you.  It is generally not recommended to use this method as it is more time consuming.")
	t <= P("You need to add jewels to Path of Building, if you have not yet done so.  Note these will always be the latest verions.")
	t <= A("Text file to add jewels by hand", href="jewellist.txt", target="_blank")
	t <= P(A("xml file to add jewels direction to Path of Building Settings (at your own risk). ", href="jewellistxml.txt", target="_blank") + "As pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly. The lines from jewellistxml.txt should be added directly after the <SharedItems> tag. <Shared Items> should be right after </Accounts>. If you only have <SharedItems/> in that file, you will need to replace it with <SharedItems></SharedItems>")
	t <= P("You then need to spec an empty jewel node on your tree, or modify an item to have an empty socket, in PoB and mouse over each added jewel for the values to add in this table. After filling in the table and selection the relevant mods, click \"Generate Query\" and a query string will be created for you.")


# Fill in the "weights" page
def init_weight(version):
	t = TABLE()
	th = TR()
	th <= TH("Damage")
	th <= TH("Jewel Mod")
	t <= th
	for m in mjson[version]:
		t <= TR(TD(f'<input type="number" id="{m["name"]}" value="0" data-normal="{m["count"]}" step="0.1" class="dps_val">') + TD(m['desc']))
	doc['Weights'] <= t


# Given an array of values, create a w width table of checkboxes
def make_table(data, w, section):
	t = TABLE()
	tr = TR()
	for c, d in enumerate(data, 1):
		if isinstance(d, str):
			tr <= TD(LABEL(INPUT(type='checkbox', Id=d, Class='flag_val', data_id=d, data_type=section) + d))
		else:
			tr <= TD(LABEL(INPUT(type='checkbox', Id=d[0], Class='flag_val', data_id=d[1], data_type=section) + d[1]))
		if not c % w:
			t <= tr
			tr = TR()
	if c % w:
		t <= tr
	return t


# Initialize the "flags" page
def init_flags():
	data = [('useFrenzyCharges', 'Frenzy'), ('usePowerCharges', 'Power'), ('useEnduranceCharges', 'Endurance')]
	t = make_table(data, 3, 'Charges')
	doc['Flags'] <= STRONG('Charges:') + ' Do you sustain charges?' + t + BR()

	t = TABLE()
	t <= TR(TD(INPUT(type="number", Id="PowerCount", value="0", data_normal="1", style={"width": "3em"}, Class="dps_val")) + TD('Power'))
	t <= TR(TD(INPUT(type="number", Id="FrenzyCount", value="0", data_normal="1", style={"width": "3em"}, Class="dps_val")) + TD('Frenzy'))
	t <= TR(TD(INPUT(type="number", Id="EnduranceCount", value="0", data_normal="1", style={"width": "3em"}, Class="dps_val")) + TD('Endurance'))
	t <= TR(TD(INPUT(type="number", Id="ImpaleStacks", value="0", data_normal="1", style={"width": "3em"}, Class="dps_val")) + TD('Number of Impales on Target'))
	doc['Flags'] <= STRONG('Misc Counts:') + ' The "count" of various things affecting your build.' + t + BR()

	data = ['Attack', 'Spell']
	t = make_table(data, 2, 'Type')
	doc['Flags'] <= STRONG('Type:') + ' Generally select 1 based on your combat style' + t + BR()

	data = ['Mace', 'Bow', 'Wand', 'Claw',
	        'Staff', 'Sword', 'Axe', 'Dagger',
	        'Trap', 'Mine', 'Totem']
	t = make_table(data, 4, 'Class')
	doc['Flags'] <= STRONG('Class:') + ' Select your weilded weapon types. Trap/Mine/Totem if you are using those supports' + t + BR()

	data = ['Elemental', 'Fire', 'Cold', 'Lightning',
	        'Projectile', 'Melee', 'Area', 'Spectre',
	        'Exerted', 'Trigger', 'Vaal']
	t = make_table(data, 4, 'Tags')
	doc['Flags'] <= STRONG('Tags:') + ' Check all the tags that match your primary skill' + t + BR()

	data = ['Shield', ('DualWielding', 'Dual Wielding'), ('TwoHandedWeapon', 'Two Handed Weapon')]
	t = make_table(data, 3, 'Hands')
	doc['Flags'] <= STRONG('Hands:') + ' Choose 1 based on wielded weapons' + t + BR()

	data = [('KilledRecently', 'You Kill'), ('MinionsKilledRecently', 'Minion Kill'), ('NoRecentKill', 'Not Kill'),
	        ('CritRecently', 'Crit'), ('NoRecentCrit', 'Not Crit'), ('UsedMinionSkillRecently', 'Minion Skill'),
	        'Stun', 'Shatter', ('beShocked', 'Be Shocked')]
	t = make_table(data, 3, 'Recently')
	doc['Flags'] <= STRONG('Recently:') + " Tic all the things your build can do 'recently'" + t + BR()

	data = [('EnemyPoisoned', 'Poisoned'), ('EnemyBlinded', 'Blinded'), ('EnemyIgnited', 'Ignited'), ('EnemyBurning', 'Burning'),
	        ('EnemyChilled', 'Chilled'), ('EnemyFrozen', 'Frozen'), ('EnemyShocked', 'Shocked')]
	t = make_table(data, 4, 'Enemy is')
	doc['Flags'] <= STRONG('Enemy is:') + ' Status effects on your target' + t + BR()

	data = ['Spellslinger', ('SpellslingerDW', 'Spellslinger(DW)'), 'BattleMage',
	        ('Leeching', 'Leeching (Generic)'), ('leechLife', 'Leeching Life'), ('leechMana', 'Leeching Mana'),
	        ('UsingFlask', 'Flasked'), ]
	t = make_table(data, 3, 'You are/have')
	doc['Flags'] <= STRONG('You are/have:') + ' Tic all the things affecting you' + t + P(STRONG('Spellslinger/Battlemage Notes:') + " Only select, at max, one of the Spellslingers and remember Spellslinger only works with wands. Physical damage is not correct as it depends on base item, quality, %ipd. Existing search mods don't allow for a meaningful weight to be generated.") + BR()

	data = [('NearbyRareUnique', 'Nearby Rare or Unique Monster'), ('NearbyEnemy', 'Nearby Enemy (helm mods)'), ('otherringshaper', 'Other Ring is Shaper'), ('otherringelder', 'Other Ring is Elder')]
	t = make_table(data, 1, 'Other Options')
	doc['Flags'] <= STRONG('Other options:') + ' choices that don\'t neatly fit a section' + BR() + t


# Initialize the changelog
def init_change():
	doc['Changelog'] <= P('2021/03/06: Added Culling Strike (v2 mods.json).  Note that culling dps assumes "perfect culls" at exactly 10% hp against non-healing targets, so actual damage gain will be less.')
	doc['Changelog'] <= P('2021/03/02: Bugfix: Some Precursor mods that can also appear on rares were restricted.')
	doc['Changelog'] <= P('2021/02/24: Implemented dozens of new mods including nearby resist(helmets) and aura effectiveness(weapons/corruptions).')
	doc['Changelog'] <= P('2021/02/22: Mods are now sorted for culling based on their total weights, not per point.')
	doc['Changelog'] <= P('2021/02/21: Updated UI and added support for array of weights in query string.')
	doc['Changelog'] <= P('2021/02/08: Battlemage added, pseudomods re-enabled. Please report any issues.')


# Function creates and updates the main section to show a summary for current selections
def init_main():
	t = doc['Main']
	t.text = ''
	t <= P("This page is updated as you make changes on the Weights and Flags page and only shows non-zero weights and set flags.  Changes to weights here are also reflected on those pages.")
	table = TABLE()
	th = TR()
	th <= TH("Damage")
	th <= TH("Jewel Mod")
	table <= th
	for m in mjson[current_version]:
		if float(doc[m['name']].value):
			table <= TR(TD(f'<input type="number" data-id="{m["name"]}" value="{doc[m["name"]].value}" step="0.1", class="main_weight">') + TD(m['desc']))
	t <= table
	table = TABLE(TR(TH("Flag Group") + TH("Value")))
	flags = {}
	for elt in doc.get(selector='.flag_val'):
		temp = elt
		if temp.checked and temp['data-type'] != 'ignore':
			if temp['data-type'] not in flags:
				flags[temp['data-type']] = []
			flags[temp['data-type']].append(temp['data-id'])
	# Special section for charge counts
	charge_count = []
	for elt in [doc['PowerCount'], doc['FrenzyCount'], doc['EnduranceCount'], doc['ImpaleStacks']]:
		if int(elt.value):
			name = elt['id'][:-5] if elt['id'] != 'ImpaleStacks' else "Number of Impales on Target"
			charge_count.append(f"{name} ({elt.value})")
	if charge_count:
		flags['Misc Counts'] = charge_count
	for f in flags:
		table <= TR(TD(f) + TD(', '.join(flags[f])))
	t <= P("Summary of set flags.  Make changes on Flags page.") + table

	@bind('.main_weight', 'change')
	def update_weight(ev):
		tmp = ev.target
		doc[tmp['data-id']].value = tmp.value


init_page()

