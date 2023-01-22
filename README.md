# jackett indexarr

Sets up radarr, sonarr, readarr & lidarr with the configured trackers in jackett

Jackett connection setup
```
export jackett_cookie="get the cookie from chrome session"
export jackett_endpoint="http://192.168.0.30:9117"
export jackett_api_key="dddddddddddddddddddddddddddddddddddddddddd"
```

Define where sonarr, radarr & lidarr dbs are
```
export sonarr_db="/home/to/sonarr/sonarr.db"
export radarr_db="/home/to/radarr/radarr.db"
export lidarr_db="/home/to/lidarr/lidarr.db"
```

Execute it
```
pip install jackett-indexerarr
jackett-indexerarr
```