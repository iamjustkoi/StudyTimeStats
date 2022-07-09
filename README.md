# <p align="center"><img src="raw/stats_icon.svg"> Study Time Stats</p>
<p align="center">Add some total study time and ranged study time statistics to Anki's main window!</p>  
<p align="center"><img src=".github/main_ui.png"></p>

## Installation  
Install from [Anki-Web](https://ankiweb.net/shared/info/1247171202)  
Or from Anki (Tools -> Add-ons -> Get Add-ons..)
> 1247171202

## Options Menu  
### General
These settings can be used to change the visibility, look, and text of the rendered stats, as well as how the add-on should filter the total review time.  
<p align="center"><img src=".github/options_general.png"></p>

### Advanced
These settings can change other UI options, whether the add-on should filter out or include deleted card reviews, and which decks it should consider when counting review time.
<p align="center"><img src=".github/options_advanced.png"></p>

## Text Macros
The add-on can also filter text in the custom labels input to show information based on what's set in the config (e.g. "Past %range" to "Past Week"). These can be used multiple times and will update whenever Anki's main window reloads.

### Available Macros:
##### General
+ `%range` - the currently selected range format (Week, 2 Weeks, Month, Year)
+ `%from_date` - range filter's start date using the system's locale (2022-06-30)
+ `%from_day` - range filter's starting day using a compact format (Sun)
+ `%from_full_day` - range filter's full start day (Sunday)
+ `%from_month` - range filter's month name using a compact format (Sep)
+ `%from_full_month` - range filter's full month name (September)
+ `%days` - total days the range filter checks against (17)
##### Advanced
These macros will each index the received review logs and output its individual value-unit combination (e.g. "%total_hrs" -> "3.14 hrs").
+ `%total_hrs` - total study time
+ `%range_hrs` - ranged study time
+ `%last_cal_hrs` - total study time of the last calendar range
+ `%last_day_hrs` - total study time of the previous day
##### Misc
+ `%%` - returns a single % symbol and doesn't apply the text macro (%, %range, etc)

#### Bugs/Issues:
Please post any issues or feedback you might have on [GitHub](https://github.com/iamjustkoi/StudyTimeStats/issues).
<br></br>  

Wish you the best! -koi

MIT License  
©2022 JustKoi (iamjustkoi)  
