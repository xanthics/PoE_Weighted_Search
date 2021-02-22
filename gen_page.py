from browser import document as doc
from browser.html import TABLE, TR, TH, TD, BUTTON, DIV, STRONG, INPUT, LABEL, P, BR, H1, H3, UL, LI, A, SELECT, OPTION

from browser import bind
from browser.local_storage import storage

from gensearchparams import gensearchparams
from leaguelist import leagues
from baselist import bases
from modsjson import mjson

saved_states = ["NoCraftedMods", "NoImplicitMods", "NearbyRareUnique", "PseudoMods"]

storage_key = "poe_weighted_search"


# Setter storage so that we can differentiate values on this site from others at the same domain
def set_storage(key, val):
	storage["{}-{}".format(storage_key, key)] = val


# Getting for storage so that we can differentiate values on this site from others at the same domain
def get_storage(key):
	return storage["{}-{}".format(storage_key, key)]


# Check if a value exists in storage
def check_storage(key):
	return "{}-{}".format(storage_key, key) in storage


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
	for elt in doc.get(selector='input[type="number"]'):
		dps[elt.id] = float(elt.value)/float(elt.getAttribute("data-normal"))
	dps['extrarandom'] = (dps['extrafire'] + dps['extracold'] + dps['extralightning']) / 3
	selections = set()
	for elt in doc.get(selector='input[type="checkbox"]'):
		if elt.checked:
			selections.add(elt.id)
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


def process_querystring():
	if 'vals' in doc.query:
		n_arr = doc.query['vals'].strip('[]').split(',')
		print(n_arr)
		for c, val in enumerate(n_arr[1:]):
			if val != '0':
				doc[mjson[c]['name']].value = float(val)
	else:
		for elt in doc.get(selector='input[type="number"]'):
			if elt.id not in ["MaxWeight", "BaseWeight", "WeightedMod"]:
				try:
					elt.value = doc.query[elt.id]
				except KeyError:
					elt.value = 0
	try:
		flags = doc.query["Flags"].strip(',').split(',')
		for f in flags:
			try:
				doc[f].checked = True
			except KeyError:
				print("Flag '{}' recieved but not currently supported.".format(f))
		if 'conditionCritRecently' not in flags:
			doc["NoRecentCrit"].checked = True
		if 'conditionKilledRecently' not in flags:
			doc["NoRecentKill"].checked = True
	except KeyError:
		print("No Flags parameter passed in query string")

	for val in ['Skill', 'Character']:
		try:
			if doc.query[val]:
				doc[val] <= doc.query[val]
		except KeyError:
			doc[val].style.display = "none"

	# Set default states
	doc["PseudoMods"].checked = True
	for _f in saved_states:
		if check_storage(_f):
			doc[_f].checked = bool(get_storage(_f))


def create_league_list():
	sel = SELECT(size=1, multiple=False, id="league")
	for league in leagues:
		sel <= OPTION(league)
	doc['leaguelist'] <= sel
	if check_storage('league') and get_storage('league') in leagues:
		doc['league'].value = get_storage('league')


def create_base_list():
	sel = SELECT(size=1, multiple=False, id="base")
	for base in bases:
		sel <= OPTION(base)
	doc['baselist'] <= sel
	if check_storage('base') and get_storage('base') in bases:
		doc['base'].value = get_storage('base')


def init_page():
	create_league_list()
	create_base_list()
	pages = ['Main', 'Weights', 'Flags', 'About', 'Changelog']
	for c, page in enumerate(pages):
		doc['buttons'] <= BUTTON(page, data_id=page, Class=f'page{" current_tab" if not c else ""}', Id=f'b_{page}')
		doc['main'] <= DIV(Id=page)
		if c:
			doc[page].style.display = 'none'

	init_about()
	init_weight()
	init_flags()
	init_change()

	@bind('.page', 'click')
	def change_page(ev):
		val = ev.target['data-id']
		doc[val].style.display = 'block'
		doc[f'b_{val}'].attrs['class'] = 'current_tab page'
		idx = pages.index(val)
		for i in pages[:idx] + pages[idx+1:]:
			doc[i].style.display = 'none'
			doc[f'b_{i}'].attrs['class'] = 'page'


def init_about():
	t = doc['About']
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
	t <= P("You need to add jewels to Path of Building, if you have not yet done so.")
	t <= A("Text file to add jewels by hand", href="jewellist.txt", target="_blank")
	t <= P(A("xml file to add jewels direction to Path of Building Settings (at your own risk). ", href="jewellistxml.txt", target="_blank") + "As pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly. The lines from jewellistxml.txt should be added directly after the <SharedItems> tag. <Shared Items> should be right after </Accounts>. If you only have <SharedItems/> in that file, you will need to replace it with <SharedItems></SharedItems>")
	t <= P("You then need to spec an empty jewel node on your tree, or modify an item to have an empty socket, in PoB and mouse over each added jewel for the values to add in this table. After filling in the table and selection the relevant mods, click \"Generate Query\" and a query string will be created for you.")


def init_weight():
	t = TABLE()
	th = TR()
	th <= TH("Damage")
	th <= TH("Jewel Mod")
	t <= th
	for m in mjson:
		t <= TR(TD('<input type="number" id="{}" value="0" data-normal="{}" step="0.1">'.format(m['name'], m['count'])) + TD(m['desc']))
	doc['Weights'] <= t


def make_table(data, w):
	t = TABLE()
	tr = TR()
	for c, d in enumerate(data, 1):
		if isinstance(d, str):
			tr <= TD(LABEL(INPUT(type='checkbox', Id=d) + d))
		else:
			tr <= TD(LABEL(INPUT(type='checkbox', Id=d[0]) + d[1]))
		if not c % w:
			t <= tr
			tr = TR()
	if c % w:
		t <= tr
	return t


def init_flags():
	data = [('useFrenzyCharges', 'Frenzy'), ('usePowerCharges', 'Power'), ('useEnduranceCharges', 'Endurance')]
	t = make_table(data, 3)
	doc['Flags'] <= STRONG('Charges:') + ' Do you sustain charges?' + t + BR()

	t = TABLE()
	t <= TR(TD(INPUT(type="number", name="PowerCount", value="0", data_normal="1", style={"width": "3em"})) + TD('Power'))
	t <= TR(TD(INPUT(type="number", name="FrenzyCount", value="0", data_normal="1", style={"width": "3em"})) + TD('Frenzy'))
	t <= TR(TD(INPUT(type="number", name="EnduranceCount", value="0", data_normal="1", style={"width": "3em"})) + TD('Endurance'))
	doc['Flags'] <= STRONG('Charge Count:') + ' The max number of each type of charge your build sustains' + t + BR()

	data = ['Attack', 'Spell']
	t = make_table(data, 2)
	doc['Flags'] <= STRONG('Type:') + ' Generally select 1 based on your combat style' + t + BR()

	data = ['Mace', 'Bow', 'Wand', 'Claw',
	        'Staff', 'Sword', 'Axe', 'Dagger',
	        'Trap', 'Mine', 'Totem']
	t = make_table(data, 4)
	doc['Flags'] <= STRONG('Class:') + ' Select your weilded weapon types. Trap/Mine/Totem if you are using those supports' + t + BR()

	data = ['Elemental', 'Fire', 'Cold', 'Lightning',
	        'Projectile', 'Melee', 'Area', 'Spectre',
	        'Exerted', 'Trigger', 'Vaal']
	t = make_table(data, 4)
	doc['Flags'] <= STRONG('Tags:') + ' Check all the tags that match your primary skill' + t + BR()

	data = ['Shield', ('DualWielding', 'Dual Wielding'), ('TwoHandedWeapon', 'Two Handed Weapon')]
	t = make_table(data, 3)
	doc['Flags'] <= STRONG('Hands:') + ' Choose 1 based on wielded weapons' + t + BR()

	data = [('conditionKilledRecently', 'You Kill'), ('conditionMinionsKilledRecently', 'Minion Kill'), ('NoRecentKill', 'Not Kill'),
	        ('conditionCritRecently', 'Crit'), ('NoRecentCrit', 'Not Crit'), ('conditionUsedMinionSkillRecently', 'Minion Skill'),
	        'Stun', 'Shatter', ('beShocked', 'Be Shocked')]
	t = make_table(data, 3)
	doc['Flags'] <= STRONG('Recently:') + " Tic all the things your build can do 'recently'" + t + BR()

	data = [('conditionEnemyPoisoned', 'Poisoned'), ('conditionEnemyBlinded', 'Blinded'), ('conditionEnemyIgnited', 'Ignited'), ('conditionEnemyBurning', 'Burning'),
	        ('conditionEnemyChilled', 'Chilled'), ('conditionEnemyFrozen', 'Frozen'), ('conditionEnemyShocked', 'Shocked')]
	t = make_table(data, 4)
	doc['Flags'] <= STRONG('Enemy is:') + ' Status effects on your target' + t + BR()

	data = ['Spellslinger', ('SpellslingerDW', 'Spellslinger(DW)'), 'BattleMage',
	        ('conditionUsingFlask', 'Flasked'), ('leechLife', 'Leeching Life'), ('leechMana', 'Leeching Mana')]
	t = make_table(data, 3)
	doc['Flags'] <= STRONG('You are/have:') + ' Tic all the things affecting you' + t + P(STRONG('Spellslinger/Battlemage Notes:') + " Only select, at max, one of the Spellslingers and remember Spellslinger only works with wands. Physical damage is not correct as it depends on base item, quality, %ipd. Existing search mods don't allow for a meaningful weight to be generated.") + BR()

	data = [('NoCraftedMods', 'Ignore Crafted Mods'), ('NoImplicitMods', 'Ignore Implicit Mods'), ('NearbyRareUnique', 'Nearby Rare or Unique Monster'), ('PseudoMods', 'Use PseudoMods in Search')]
	t = make_table(data, 1)
	doc['Flags'] <= STRONG('Other options:') + ' choices that don\'t neatly fit a section' + BR() + 'PseudoMods is experimental. Please report any issues.' + t + BR()


def init_change():
	doc['Changelog'] <= P('2021/02/28: Updated UI and added support for array of weights in query string.')
	doc['Changelog'] <= P('2021/02/08: Battlemage added, pseudomods re-enabled. Please report any issues.')


init_page()
doc["query"].style.display = "none"
doc["notice"].style.display = "none"
doc["414by"].style.display = "none"
b_generate = BUTTON("Generate Query")
b_generate.bind("click", generate_query)
doc["generate"] <= b_generate
process_querystring()
doc["loading"].style.display = "none"
