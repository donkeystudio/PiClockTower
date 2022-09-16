# PiClockTower
Turn your Raspberry Pi into a Westminster clock tower. A chime will be played every hour at :00 minute and follow by one bell strike for each hour from midnight or 12 noon. Chime can be turned on/off via API (If you want to control it via Home Automation). Basic HTTP Authenticaion is supported. Feel free to extend this project to support quarter chimes (15 minutes interval).

## [Docker](https://hub.docker.com/r/donkeystudio/piclocktower)
Supported architectures: `linux/arm/v7`

## Startup Configuration
```
python3 main.py --help
usage: main.py [-h]
               [-cfrm {0-23}]   [-cto {0-23}]
               [-log LOG_FILE]  [-d DEBUG_LEVEL] 
               [-u USER]        [-pwd PASSWORD]   [-p PORT] 
               [-mc MAIN_CHIME] [-hc HOUR_CHIME]

optional arguments:
  -h,             --help                      show this help message and exit
  -cfrm {0-23},   --chime_from {0-23}         Regulate chime starting time. (default: 0)
  -cto {0-23},    --chime_to {0-23}           Regulate chime ending time (default: 23)
  -log LOG_FILE,  --log_file LOG_FILE         Location of the log file. Default is system log (default: None)
  -d DEBUG_LEVEL, --debug_level DEBUG_LEVEL   Debug Level CRITICAL/ERROR/WARNING/INFO/DEBUG. (default: WARNING)
  -u USER,        --user USER                 Username to access API (default: None)
  -pwd PASSWORD,  --password PASSWORD         Password to access API (default: None)
  -p PORT,        --port PORT                 Port (default: 8080)
  -mc MAIN_CHIME, --main_chime MAIN_CHIME     Path to main chime in WAV format. (default: chimes/MainTune.wav)
  -hc HOUR_CHIME, --hour_chime HOUR_CHIME     Path to hour chime in WAV format. (default: chimes/BellToll.wav)
```

## API End Points
### /chime
```http
GET /chime?mode=query
```
Query current chime status

```http
POST /chime?mode=update&action=on/off(Default)
```
Update mode. Turn on/off clock chime.

**Responses**

| Field | Type | Description |
| :--- | :--- | :--- |
| result | int | HTTP Status Code |
| status | string | Chime status. Either "quiet" or "chime" |

**Sample Response**
```json
{
    "result": 200,
    "status": "chime"
}
```