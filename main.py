from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import threading
from clock_tower import ClockTower
import logging

from end_points.chime_mode import ChimeMode
from model.credential import Credential
from server.api_server import APIServer


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-cfrm","--chime_from", default=0,         type=int, choices=range(0,24), help="Regulate chime starting time.")
parser.add_argument("-cto", "--chime_to",   default=23,        type=int, choices=range(0,24), help="Regulate chime ending time")
parser.add_argument("-log", "--log_file",   default=None,      type=str,                      help="Location of the log file. Default is system log")
parser.add_argument("-d",   "--debug_level",default="WARNING", type=str,                      help="Debug Level CRITICAL/ERROR/WARNING/INFO/DEBUG.")
parser.add_argument("-u",   "--user",       default=None,                                     help="Username to access API")
parser.add_argument("-pwd", "--password",   default=None,                                     help="Password to access API")
parser.add_argument("-p",   "--port",       default=8080,      type=int,                      help="Port")
parser.add_argument("-mc", "--main_chime",  default="chimes/MainTune.wav",                    help="Path to main chime in WAV format.")
parser.add_argument("-hc", "--hour_chime",  default="chimes/BellToll.wav",                    help="Path to hour chime in WAV format.")
args = vars(parser.parse_args())

START_TIME  = args["chime_from"]
END_TIME    = args["chime_to"]
LOG_FILE    = args["log_file"]
LOG_LEVEL   = args["debug_level"]
USER        = args["user"]
PWD         = args["password"]
PORT        = args["port"]
MAIN_CHIME  = args["main_chime"]
HOUR_CHIME  = args["hour_chime"]

if __name__ == '__main__':
    logging.basicConfig(filename=LOG_FILE, format='%(asctime)s %(levelname)s [%(name)s] %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level = LOG_LEVEL.upper())
    if START_TIME <= END_TIME:
        clock = ClockTower(START_TIME, END_TIME)
        clock.set_chimes_path(MAIN_CHIME, HOUR_CHIME)

        #API Resources
        ChimeMode.credential = Credential(USER, PWD)
        ChimeMode.clock      = clock
        
        #Setup API Server and end-points
        server = APIServer("Pi Clock Tower API")
        server.add_resource('/chime', ChimeMode)
        threading.Thread(target=lambda: server.start('0.0.0.0', PORT, debug=LOG_LEVEL.upper()==logging.getLevelName(logging.DEBUG))).start()
        clock.run()