import json
from configparser import ConfigParser
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm

config = ConfigParser()

config.read('settings.ini')

STEAM_API_KEY = config.get('keys', 'steam_api_key')
STEAM_ID = config.get('ids', 'steam_full_id')
STEAM_GRID_API_KEY = config.get('keys', 'steamgrid_api_key')
STEAM_PROFILE_ID = config.get('ids', 'steam_profile_id')
STEAM_GRID_PATH = config.get('paths', 'steam_grid_path')
STYLES = config.get('settings', 'styles')
NSFW = config.get('settings', 'nsfw')
HUMOR = config.get('settings', 'humor')
TYPES = config.get('settings', 'types')
DIMENSIONS = config.get('settings', 'dimensions')
SCRAPE_TYPE = config.get('scan_mode', 'scan_mode')

if SCRAPE_TYPE == 'library_600x900_2x':
    STEAM_GRID_API_URL = "https://www.steamgriddb.com/api/v2/grids/game/"
    PICTURE_STRING = 'p'
    STEAM_IMAGE_NAME = '.'.join([SCRAPE_TYPE, 'jpg'])
    PICTURE_NAME = '.'.join([PICTURE_STRING, 'jpg'])
    OPTIONS = {"dimensions": DIMENSIONS, "types": TYPES, "nsfw": NSFW, "humor": HUMOR}
if SCRAPE_TYPE == 'library_hero':
    STEAM_GRID_API_URL = "https://www.steamgriddb.com/api/v2/heroes/game/"
    PICTURE_STRING = '_hero'
    STEAM_IMAGE_NAME = '.'.join([SCRAPE_TYPE, 'jpg'])
    PICTURE_NAME = '.'.join([PICTURE_STRING, 'jpg'])
    OPTIONS = {"dimensions": DIMENSIONS, "types": TYPES, "nsfw": NSFW, "humor": HUMOR}
if SCRAPE_TYPE == 'logo':
    STEAM_GRID_API_URL = "https://www.steamgriddb.com/api/v2/logos/game/"
    PICTURE_STRING = '_logo'
    STEAM_IMAGE_NAME = '.'.join([SCRAPE_TYPE, 'png'])
    PICTURE_NAME = '.'.join([PICTURE_STRING, 'png'])
    OPTIONS = {"types": TYPES, "nsfw": NSFW, "humor": HUMOR}


def get_library():
    steam_api_url = ''.join(['http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=',
                             STEAM_API_KEY,
                             '&steamid=',
                             str(STEAM_ID),
                             '&format=json'])
    dictonary_of_games = json.loads(requests.get(steam_api_url).text)
    game_count = dictonary_of_games['response']['game_count']
    appids_to_scan = [game['appid'] for game in dictonary_of_games['response']['games']]
    appids_to_scan = sorted(appids_to_scan)
    return appids_to_scan, game_count


def get_no_arts(games, total):
    list_to_scan = []

    def check_for_default_art(game, index, total):
        cover_url = ''.join(
            [
                'https://steamcdn-a.akamaihd.net/steam/apps/',
                str(game),
                '/',
                STEAM_IMAGE_NAME
            ]
        )
        s = requests.Session()
        s.mount('https://steamcdn-a.akamaihd.net/steam/apps/', HTTPAdapter(max_retries=50))

        r = s.get(cover_url, stream=True)
        if r.status_code == 404:
            list_to_scan.append(game)
            return False

        elif r.status_code == 200:
            return True

    pbar = tqdm(games, position=0, leave=True)
    matches = 0
    no_match = 0
    for index, game in (enumerate(pbar)):
        pbar.set_description(f"Scanning Steam App ID  {game}")
        x = check_for_default_art(game, index, total)
        if x:
            matches = matches + 1
            pbar.set_postfix_str(f"Default art exists: {matches}, No Default art : {no_match}")
        else:
            no_match = no_match + 1
            pbar.set_postfix_str(f"Default art exists: {matches}, No default art : {no_match}")

    return list_to_scan


def steam_to_griddb_id(list_to_grab):
    list_of_grid_ids = []
    list_of_steam_ids = []
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {STEAM_GRID_API_KEY}"})
    s.mount("https://www.steamgriddb.com/api/v2", HTTPAdapter(max_retries=50))
    progress = tqdm(list_to_grab, position=0, leave=True)
    for id in progress:
        r = s.get(''.join(["https://www.steamgriddb.com/api/v2/games/steam/", str(id)]))
        dump = json.loads(r.text)
        if dump['success'] == True:
            progress.set_description(
                f"Game Name : {dump['data']['name']} steam ID {id} , grid_db id is {dump['data']['id']}")
            list_of_steam_ids.append(id)
            list_of_grid_ids.append(dump['data']['id'])
    dict_map = dict(zip(list_of_grid_ids, list_of_steam_ids))
    print(dict_map)
    return dict_map, list_of_grid_ids


def get_grids(l, id_map):
    grids = []
    s = requests.Session()
    s.headers.update({"Authorization": f"Bearer {STEAM_GRID_API_KEY}"})
    s.mount("https://www.steamgriddb.com/api/v2", HTTPAdapter(max_retries=50))
    for game in l:
        r = s.get(''.join([STEAM_GRID_API_URL, str(game)]), params=OPTIONS, stream=True)
        r = json.loads(r.text)
        if r['data']:
            r = r['data'][0]
            r = r['url']
            r = s.get(r, stream=True)
            grid_path = '\\'.join([STEAM_GRID_PATH, STEAM_PROFILE_ID, "config\grid\\"])
            Path(grid_path).mkdir(parents=True, exist_ok=True)
            with open(''.join([grid_path, str(id_map[game]), PICTURE_NAME]), "wb") as f:
                f.write(r.content)
        else:
            print("No result for", str(id_map[game]))
    return None



if __name__ == '__main__':
    games, count = get_library()
    no_default_art_list = tqdm(get_no_arts(games, count))
    id_map, list_to_download = steam_to_griddb_id(no_default_art_list)
    get_grids(list_to_download, id_map)
