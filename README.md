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

***

**HOWTO**

1) Download the entire project and extract all files to the same location.

2) Import jewels in to Path of Building.  Either one at a time from jewellist.txt or directly in to your PoB settings from jewellistxml.txt

3) Install Python 3 from [https://www.python.org/](https://www.python.org/) 

4) Run IDLE(start->search)) that was installed in step 3.  File->Open and find gensearchparams.py

5) In PoB spec an empty jewel node.  Use the dps values given by mousing over the jewels from step 2, as if they were inserted in the empty jewel slot, to update the dps values in gensearchparams.py

6) update miniondamage and minionattackspeed to True or False depending on tree/gear

7) update selections to reflect your build.  At the time of this readme it is set up for a GC miner that is using a shield.

8) Choose Run->Run Module (shortcut F5).  This will output the search string to console.  It will also update querystring.txt

9) Copy+paste the search string in to your favorite browser.

10) Modify search parameters as desired from there.  Change the weight field from 7500 to a lower or higher value to show more or less items.  Change the basetype to one-hand melee for statsticks.

***

I am in the (slow) process of expanding the mod lists to support dps searchs for all the gear slots.  If you want something added, please open an issue so it can be tracked.

Feedback appreciated on [Reddit](https://www.reddit.com/r/pathofexiledev/comments/9jkwru/python_tool_to_generate_search_strings_for_dps/)