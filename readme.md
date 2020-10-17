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

You will need to fill out the `keys` and `ids` section yourself with your own information, 
and the others can be tweaked to your preferences,