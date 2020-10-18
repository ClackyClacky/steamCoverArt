Steam Art Getter
================
Grabs art from [steamgridDB](https://www.steamgriddb.com/) to fill in the gaps where there is no official art in the right format.

Installation
============
*   __Python__

    https://www.python.org 
    
    __Only tested on 3.9 but can't see why it wouldn't work on any python3 version above 3.4__

*   __Steam API Key__

    Get from [here](https://steamcommunity.com/dev/apikey) once you are signed in.
    
    If you don't have a web address just type random text in.

*   __Steam Grid DB API Key__

    Log into steamgridddb and navigate to the preferences tab and generate an API Key. 


if you want to use this script in a virtual environment then set that up and run the pip command 
```python
pip install -r requirements.txt
``` 
then run with 
```
python main.py
```

After configuring your `settings.ini` file to your needs.

Settings.ini
============
This file is used to store different constants.

You will need to make a copy of the `settings_blank.ini` file and rename it to `settings.ini`

```ini
[keys]
; get from https://www.steamgriddb.com/profile/preferences when logged in, no quotes please around value
steamgrid_api_key =
; get from https://steamcommunity.com/dev/apikey, no quotes around value
steam_api_key =

[ids]
; get from the calculator on https://steamdb.info/calculator/, it's in the steamID field , no quotes
steam_full_id =
; get from the calculator, the number in the AccountID , no quotes
steam_profile_id =

[paths]
; only change if yours is different
steam_grid_path = C:\Program Files (x86)\Steam\userdata

[settings]
;Items Enum:"alternate" "blurred" "white_logo" "material" "no_logo"
;Filter results by style. Multiple styles can be provided as comma separated strings.
styles = alternate

;Items Enum:"460x215" "920x430" "600x900" "342x482" "660x930"
;Filter results by image dimensions. Multiple dimensions can be provided as comma separated strings.
dimensions = 600x900

;items Enum:"static" "animated"
;Filter results by image type. Multiple types can be provided as comma separated strings.
types = static
;string
;Set to false to filter out nsfw, true to only include nsfw, any to include both.
nsfw = false

;humor
;Set to false to filter out humor, true to only include humor, any to include both.
humor = false
```