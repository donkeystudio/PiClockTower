import time
import os


class ClockTower:

    max_range       = range(0, 24)
    allowed_range   = range(0, 24)

    path_main_chime = 'chimes/MainTune.wav'
    path_hour_chime = 'chimes/BellToll.wav'

    is_quiet_time = False;
    
    def __init__(self) -> None:
        pass

    def __init__(self,start:int, end:int) -> None:
        self.set_chime_period(start, end)


    def set_chime_period(self,start:int, end:int):
        if start in self.max_range and end in self.max_range and start <= end:
            self.allowed_range = range(start, end+1)


    def set_chimes_path(self, path_main_chime=None, path_hour_chime=None):
        if path_main_chime is not None:
            self.path_main_chime = path_main_chime
        
        if path_hour_chime is not None:
            self.path_hour_chime = path_hour_chime
    

    def set_quiet_time(self, is_quiet_time:bool):
        self.is_quiet_time = is_quiet_time


    def chime(self):
        if self.is_quiet_time:
            return
        
        hour = time.localtime().tm_hour
        minute = time.localtime().tm_min
        
        #doesn't play too early or too late
        if hour in self.allowed_range:
            #ensure it is tolling time
            if minute == 0:
                #adjust for 24 hour time
                if hour > 12:
                    hour -= 12
                
                #tolling in action
                os.system(f'aplay -q {self.path_main_chime}')
                #plays a different amount of bell tolls depending on the hour
                while(hour > 0):
                    os.system(f'aplay -q {self.path_hour_chime}')
                    hour -= 1
                    time.sleep(0.5)


    def run(self):
        #main loop
        while True:   
            self.chime()
            #makes sure it doesn't run more than once per hour
            time.sleep(60)
