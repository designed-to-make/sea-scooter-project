from seascooter import *
from time import sleep

def throttle_ramp(control_value,ramp_speed,step):
    
    throttle = int(round(control_value*ramp_speed*step,0))
    
    return throttle #out of 66000

def loose_gear_sync(current, throttle, ramp_speed,step,current_trip):
    if current <current_trip and throttle >5000:
        throttle = 0
        step = 1
        new_ramp_speed = ramp_speed
        sleep(3)
        return throttle, new_ramp_speed, step
    elif current > 1 and step == 50: # if reach 100 and gear still synced then start again with higher throttle ramp rate
            throttle = 0
            step = 1
            new_ramp_speed = ramp_speed + 400
            return throttle, new_ramp_speed, step
    
    return throttle, ramp_speed, step
            
        
        
        