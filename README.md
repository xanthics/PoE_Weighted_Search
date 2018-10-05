A collection of files for generating pathofexile.com/trade queries for jewels and statsticks

Usage
-----

**genjewels** 

Creates/updates jewellist.txt with a list of jewels that need to be added to Path of Building to figure out the dps values for 1 point in each stat

As pointed out by github user coldino, you can edit your My Documents/Path of Building/Settings.xml directly.  The lines from jewellistxml.txt should be added directly after the `<SharedItems>` tag.  `<Shared Items>` should be right after `</Accounts>`

***

**genmods** 

Creates modlist.py which is a list of all currently valid mod id: description pairs returned by the poe api

***

**gensearchparams**

First update dps(with values from POB), the minion flags, and selections with valid flags.  Then run this file to generate a search string for pathofexile.com/trade with your various mod weights.  This sometimes fails to load but resubmitting has worked every time so far