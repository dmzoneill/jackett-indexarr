import json
import sqlite3

import requests


def configure(
    jackett_endpoint,
    jackett_api_key,
    jackett_cookie,
    sonarr_db,
    radarr_db,
    lidarr_db,
    readarr_db,
):

    headers = {
        "content-type": "application/json",
        "Accept-Charset": "UTF-8",
        "Cookie": jackett_cookie,
    }

    r = requests.get(jackett_endpoint + "/api/v2.0/indexers", headers=headers)

    wanted_tv_categories = ["tv", "sorozat", "series"]
    wanted_movie_categories = ["tv", "film", "movie"]
    wanted_book_categories = ["book"]
    wanted_music_categories = ["mp3", "flac", "music"]
    excluded = ["ru", "hu", "3d", "bd", "bluray", "fr", "cam", "iso", "rip"]

    sonarr_trackers = {}
    radarr_trackers = {}
    readarr_trackers = {}
    lidarr_trackers = {}

    for tracker in r.json():

        if tracker["configured"] is False:
            continue

        tracker_name = tracker["name"].lower().replace(" ", "")

        tv_tracker_entry = {
            "minimumSeeders": 1,
            "seedCriteria": {},
            "baseUrl": jackett_endpoint,
            "apiPath": "/api/v2.0/indexers/" + tracker_name + "/results/torznab/",
            "apiKey": jackett_api_key,
            "categories": [],
            "animeCategories": [],
        }

        movie_tracker_entry = {
            "minimumSeeders": 1,
            "seedCriteria": {},
            "baseUrl": jackett_endpoint,
            "apiPath": "/api/v2.0/indexers/" + tracker_name + "/results/torznab/",
            "apiKey": jackett_api_key,
            "categories": [],
            "animeCategories": [],
        }

        book_tracker_entry = {
            "minimumSeeders": 1,
            "seedCriteria": {},
            "baseUrl": jackett_endpoint,
            "apiPath": "/api/v2.0/indexers/" + tracker_name + "/results/torznab/",
            "apiKey": jackett_api_key,
            "categories": [],
            "animeCategories": [],
        }

        music_tracker_entry = {
            "minimumSeeders": 1,
            "seedCriteria": {},
            "baseUrl": jackett_endpoint,
            "apiPath": "/api/v2.0/indexers/" + tracker_name + "/results/torznab/",
            "apiKey": jackett_api_key,
            "categories": [],
            "animeCategories": [],
        }

        for tv_category in tracker["caps"]:
            name = tv_category["Name"].lower().replace(" ", "")
            if any(y in name for y in wanted_tv_categories):
                if not any(x in name for x in excluded):
                    if int(tv_category["ID"]) not in tv_tracker_entry["categories"]:
                        tv_tracker_entry["categories"].append(int(tv_category["ID"]))

        for movie_category in tracker["caps"]:
            name = movie_category["Name"].lower().replace(" ", "")
            if any(y in name for y in wanted_movie_categories):
                if not any(x in name for x in excluded):
                    if (
                        int(movie_category["ID"])
                        not in movie_tracker_entry["categories"]
                    ):
                        movie_tracker_entry["categories"].append(
                            int(movie_category["ID"])
                        )

        for book_category in tracker["caps"]:
            name = book_category["Name"].lower().replace(" ", "")
            if any(y in name for y in wanted_book_categories):
                if not any(x in name for x in excluded):
                    if int(book_category["ID"]) not in book_tracker_entry["categories"]:
                        book_tracker_entry["categories"].append(
                            int(book_category["ID"])
                        )

        for music_category in tracker["caps"]:
            name = music_category["Name"].lower().replace(" ", "")
            if any(y in name for y in wanted_music_categories):
                if not any(x in name for x in excluded):
                    if (
                        int(music_category["ID"])
                        not in music_tracker_entry["categories"]
                    ):
                        music_tracker_entry["categories"].append(
                            int(music_category["ID"])
                        )

        if len(tv_tracker_entry["categories"]) > 0:
            sonarr_trackers[tracker_name] = tv_tracker_entry

        if len(movie_tracker_entry["categories"]) > 0:
            radarr_trackers[tracker_name] = movie_tracker_entry

        if len(book_tracker_entry["categories"]) > 0:
            readarr_trackers[tracker_name] = book_tracker_entry

        if len(music_tracker_entry["categories"]) > 0:
            lidarr_trackers[tracker_name] = music_tracker_entry

    for X in ["radarr", "sonarr", "readarr", "lidarr"]:
        sqliteConnection = None
        try:
            db_path = "./config/" + X + "/" + X + ".db"
            if X == "sonarr":
                db_path = sonarr_db if sonarr_db is not None else db_path

            if X == "radarr":
                db_path = radarr_db if radarr_db is not None else db_path

            if X == "lidarr":
                db_path = lidarr_db if lidarr_db is not None else db_path

            if X == "readarr":
                db_path = readarr_db if readarr_db is not None else db_path

            sqliteConnection = sqlite3.connect(db_path)
            cursor = sqliteConnection.cursor()

            arr = False

            if X == "radarr":
                arr = radarr_trackers
            elif X == "sonarr":
                arr = sonarr_trackers
            elif X == "readarr":
                arr = readarr_trackers
            elif X == "lidarr":
                arr = lidarr_trackers

            for tracker_key in arr:

                sqlite_select_Query = (
                    'select count(*) from "main"."Indexers" where Name = "'
                    + tracker_key
                    + '"'
                )
                cursor.execute(sqlite_select_Query)
                record = cursor.fetchall()
                if int(record[0][0]) == 0:
                    sql = ""

                    if X == "sonarr" or X == "radarr":
                        sql = "INSERT INTO Indexers ('Name', 'Implementation', 'Settings', 'ConfigContract',"
                        sql += "'EnableRss', 'EnableAutomaticSearch', 'EnableInteractiveSearch', 'Priority', 'Tags', 'DownloadClientId')"
                        sql += " VALUES ( '{name}', 'Torznab', '{config}', 'TorznabSettings', '1', '1', '1', '25', null, '0');"
                    elif X == "readarr" or X == "lidarr":
                        sql = "INSERT INTO Indexers ('Name', 'Implementation', 'Settings', 'ConfigContract',"
                        sql += "'EnableRss', 'EnableAutomaticSearch', 'EnableInteractiveSearch', 'Priority')"
                        sql += " VALUES ( '{name}', 'Torznab', '{config}', 'TorznabSettings', '1', '1', '1', '25');"

                    json_object = json.dumps(arr[tracker_key], indent=4)
                    sql = sql.format(name=tracker_key, config=json_object)
                    cursor.execute(sql)
                    sqliteConnection.commit()
                    print(X + " : " + sql)

            cursor.close()

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")
