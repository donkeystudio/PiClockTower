# PiClockTower
Turn your Raspberry Pi into a Westminster clock tower. A chime will be played every hour at :00 minute and follow by one bell strike for each hour from midnight or 12 noon. Feel free to extend this project to support quarter chimes (15 minutes interval).

## [Docker](https://hub.docker.com/r/donkeystudio/piclocktower)
Supported architectures: `linux/arm/v7`

## Startup Configuration
```
python3 main.py --help
usage: main.py [-h]
               [-cfrm {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}]
               [-cto {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}]

optional arguments:
  -h,           --help                  show this help message and exit
  -cfrm {0-23}, --chime_from {0-23}     Regulate chime starting time. (default: 0)
  -cto {0-23},  --chime_to {0-23}       Regulate chime ending time (default: 23)
```