from datetime import datetime, timedelta
import logging
import sched
import time
import os
import pytz


class ClockTower:

    max_range       = range(0, 24)
    allowed_range   = range(0, 24)

    path_main_chime = 'chimes/MainTune.wav'
    path_hour_chime = 'chimes/BellToll.wav'

    is_quiet_time   = False;
    time_scheduler  = sched.scheduler(time.time, time.sleep)
    scheduler_list  = [time_scheduler]

    _logger = logging.getLogger(__name__)
    
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
        self._logger.debug(f'In now at:{datetime.now()}')
        if self.is_quiet_time is False:
            time_now = datetime.now()
            hour = time_now.hour
            minute = time_now.minute
            
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

        #Schedule for the next chime
        self.scheduler_list.append(self.time_scheduler)


    def schedule_next_chime(self, scheduler: sched.scheduler):
        time_now = datetime.now()
        next_hour = datetime.strptime(f'{time_now.day}-{time_now.month}-{time_now.year} {time_now.hour}:00:00', '%d-%m-%Y %H:%M:%S') + timedelta(hours=1)
        delay = (next_hour.astimezone(pytz.utc) - time_now.astimezone(pytz.utc)).total_seconds()
        self._logger.debug(f'Next chime is at:{next_hour}, Delay: f{delay}')
        scheduler.enter(delay,1, self.chime)
        scheduler.run()

    
    def monitor_scheduler(self):
        while True:
            if len(self.scheduler_list) > 0:
                self.schedule_next_chime(self.scheduler_list.pop())


    def run(self):
        #Start this will do
        self.monitor_scheduler()
