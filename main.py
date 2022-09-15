from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from clock_tower import ClockTower


parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument("-cfrm", "--chime_from", default=0,  type=int, choices=range(0,24), help="Regulate chime starting time.")
parser.add_argument("-cto", "--chime_to",    default=23, type=int, choices=range(0,24), help="Regulate chime ending time")
args = vars(parser.parse_args())

START_TIME  = args["chime_from"]
END_TIME    = args["chime_to"]

if __name__ == '__main__':
    if START_TIME <= END_TIME:
        ClockTower(START_TIME, END_TIME).run()