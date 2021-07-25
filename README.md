This project works best in conjunction with [PoB-Item-Tester](https://github.com/VolatilePulse/PoB-Item-Tester)

The web based version of this is hosted at [https://xanthics.github.io/PoE_Weighted_Search/](https://xanthics.github.io/PoE_Weighted_Search/)

A collection of files for generating pathofexile.com/trade queries for jewels and statsticks

Overview
********

**index.html**

Primary interface  for generating weighted searches.

---

**genjewels** 

Creates/updates jewellist.txt with a list of jewels that need to be added to Path of Building to figure out the dps values for 1 point in each stat

As pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly.  The lines from jewellistxml.txt should be added directly after the `<SharedItems>` tag.  `<Shared Items>` should be right after `</Accounts>`

---

**genmods** 

Creates modlist.py which is a list of all currently valid mod id: description pairs returned by the poe api

---

**gensearchparams**

Given a dictionary of stat weights and a set of tags, generates a search string for pathofexile.com/trade