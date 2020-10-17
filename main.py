import os
import json
import requests
import shutil
from configparser import ConfigParser
from requests.adapters import HTTPAdapter
steam_install_path = r"C:\Program Files (x86)\Steam"
user_path = ''.join([steam_install_path, r'\userdata'])
grid_cache = ''.join([steam_install_path, r'\appcache\librarycache'])


config = ConfigParser()

config.read('settings.ini')


STEAM_API_KEY = config.get('keys','steam_api_key')
STEAM_ID = config.get('ids', 'steam_full_id')
STEAM_GRID_API_KEY = config.get('keys','steamgrid_api_key')
STEAM_PROFILE_ID = config.get('ids', 'steam_profile_id')
URL = ''.join(['http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=',
                   STEAM_API_KEY,
                   '&steamid=',
                   str(STEAM_ID),
                    '&format=json'])
def get_owned_games():
    dictonary_of_games = json.loads(requests.get(URL).text)
    game_count = dictonary_of_games['response']['game_count']
    appids_to_scan =[game['appid'] for game in dictonary_of_games['response']['games']]
    appids_to_scan = sorted(appids_to_scan)
    return appids_to_scan, game_count


def get_no_arts(games, total):
    list_to_scan = []
    def check_for_default_art(game, index, total):
        cover_url = ''.join(
            [
                'https://steamcdn-a.akamaihd.net/steam/apps/',
                str(game),
                '/library_600x900.jpg'
            ]
        )
        s = requests.Session()
        s.mount('https://steamcdn-a.akamaihd.net/steam/apps/', HTTPAdapter(max_retries=50))

        r = s.get(cover_url, stream=True)
        if r.status_code == 404:
            print(game, ":", index, "of", total, "No Offical art found, added to list to scan on SteamGridDB")
            list_to_scan.append(game)

        elif r.status_code == 200:
            print(game, ":", index, "of", total, "Art Found")
        else:
            print("Some other error on this call")
    for index, game in enumerate(games):
        check_for_default_art(game, index, total)
    return list_to_scan


def steam_to_griddb_id(list_to_grab):
    list_of_grid_ids = []
    list_of_steam_ids = []
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {STEAM_GRID_API_KEY}"})
    s.mount("https://www.steamgriddb.com/api/v2",HTTPAdapter(max_retries=50))
    for id in list_to_grab:
        r = s.get(''.join(["https://www.steamgriddb.com/api/v2/games/steam/", str(id)]))
        dump = json.loads(r.text)
        if dump['success'] == True:
            list_of_steam_ids.append(id)
            list_of_grid_ids.append(dump['data']['id'])
            print(f"Match for steam ID {id}, Game Name : {dump['data']['name']}, grid_db id is {dump['data']['id']}",)
    dict_map = dict(zip(list_of_grid_ids, list_of_steam_ids))
    print(dict_map)
    return dict_map, list_of_grid_ids

def get_grids(l,id_map):
    options = {"dimensions": "600x900", "types": "static", "nsfw": False, "humor": False}
    grids = []
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {STEAM_GRID_API_KEY}"})
    s.mount("https://www.steamgriddb.com/api/v2",HTTPAdapter(max_retries=50))
    for game in l:
        r = s.get(''.join(["https://www.steamgriddb.com/api/v2/grids/game/", str(game)]), stream=True)
        r = json.loads(r.text)
        if r['data']:
            r = r['data'][0]
            r = r['url']
            r = s.get(r, stream=True)
            with open(''.join([r"C:\Program Files (x86)\Steam\userdata", "\\", STEAM_PROFILE_ID,  "\config\grid", '\\', str(id_map[game]), 'p', '.png']), "wb") as f:
                f.write(r.content)
        else:
            print("No result for", str(id_map[game]))
    return None

get_grids([5250672],{5250672: 242150})
games, count = get_owned_games()
no_default_art_list = get_no_arts(games, count)
id_map, list_to_download = steam_to_griddb_id(no_default_art_list)
get_grids(list_to_download, id_map)

