# Study Time Stats
Adds a total and ranged study time statistic to Anki's main window.  

![Main UI](./github/main_ui.png)

## Options Menu  
### General
These can be used to change the look/wording of the text and how the addon should filter the total time studied.  
![General Options Window](./github/options_general.png)  

### Excluded Decks
Any decks added to this menu won't be considered when calculating how much time's been spent studying. It will also hide the UI on the selected deck's screens.  
![General Options Window](./github/options_excluded.png)  

## Text Macros
The addon can filter text in the custom label inputs to show information based on what's set in its options (e.g. "Past %range" can filter to "Past Week"). These can be used multiple times and change based on the most recent update to the addon's config or the next time the Anki window reloads.

#### Available Macros:
+ **%range** - the currently selected range format (Week, 2 Weeks, Month, Year)
+ **%from_date** - range filter's start date using the system's locale (2022-06-30)
+ **%from_day** - range filter's starting day using a compact format (Sun)
+ **%from_full_day** - range filter's full start day (Sunday)
+ **%days** - total days the range filter checks against (17)
+ **%%** - returns a single % symbol and doesn't apply the text macro (%, %range, etc)

Have any issues or feedback? Feel free to post on the project's issue section on [GitHub](https://github.com/iamjustkoi/StudyTimeStats/issues)!
<br></br>  

Wish you the best! -koi

©2022 JustKoi (iamjustkoi)  
Under the MIT License.  
