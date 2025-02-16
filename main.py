#Main program to run at boot
07/02/2025
#V0.11 with ota SUCCESS


from os import statvfs
from machine import Pin, I2C, PWM
from time import sleep, sleep_ms, localtime,time_ns
from bme680 import *
from ina260 import INA260, AveragingCount, ConversionTime
from seascooter import *
from scooter_tests import *
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD
from sendmqtt import connectMQTT, publish
from ntptime import settime

#check for OTA updates
firmware_url = "https://raw.githubusercontent.com/designed-to-make/sea-scooter-project/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()


# RPi Pico - Pin assignment
i2c = I2C(0, scl=Pin(17), sda=Pin(16),freq=400000)

#reed switch pins
p_aux = Pin(27, Pin.IN, Pin.PULL_DOWN)
p_0 = Pin(26, Pin.IN, Pin.PULL_DOWN)
p_50 = Pin(18, Pin.IN, Pin.PULL_DOWN)
p_100 = Pin(19, Pin.IN, Pin.PULL_DOWN)

#Motor control pins
m_pwm = PWM(Pin(12))
m_forwards = Pin(11,Pin.OUT)
m_backwards = Pin(10,Pin.OUT)

#Intialise motor
m_pwm.freq(10000)
m_forwards.value(1)
m_backwards.value(0)
m_pwm.duty_u16(0)

#intialise the LED pin
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

#Add a short delay to wait until the I2C port has finished activating.
sleep_ms(100)
#intialise the BME680 sensor
bme = BME680_I2C(i2c=i2c)
#intialise the INA260 Sensor 
ob_ina260 = INA260(i2c)

#intilise variables
pressure 		= 0
temp			= 0
humid			= 0
current			= 0
voltage			= 0
control_state	= 0
lts				= 0

#measurements

#mqtt messaging set up
client = connectMQTT()

# intialse throttle and  ramp rate for tests

t_step = 1
throttle = 0
ramp_speed = 200
throttle = 1

while True:
    pressure 		= bme.pressure # hPa
    temp	 		= bme.temperature # degrees 
    humid			= bme.humidity # %
    #current			= av_current(ob_ina260, 10)/1000 #Amps
    voltage			= ob_ina260.voltage # Volts
    control_value 	= reed_speed_control(p_aux,p_0,p_50,p_100)
    throttle 		= control_value
    current_trip	= 1.5 #Amp
    
    if control_value >=0:
        throttle = control_value * ramp_speed * 3
        current			= av_current(ob_ina260, 10)/1000
        m_pwm.duty_u16(throttle)
        
    else:
             

        
        t_step = t_step + 1
        throttle = throttle_ramp(1,ramp_speed,t_step)
        m_pwm.duty_u16(throttle)
        sleep_ms(250)
        current			= av_current(ob_ina260, 10)/1000
        
        throttle, ramp_speed, t_step = loose_gear_sync(current, throttle, ramp_speed,t_step,current_trip)
        print('ramping...' ,throttle, ramp_speed, t_step)
    
    message = {
        "localtime": localtime(),
        "time (ns)":time_ns(),
        "current" : current,
        "throttle": throttle,
        "ramp speed": ramp_speed,
        "ramp step": t_step
        }
        
    publish(client,"powertest/system_state",str(message))
    publish(client,"powertest/current",str(current))
    publish(client,"powertest/throttle",str(throttle/650))
    publish(client,"powertest/pressure",str(pressure))
    publish(client,"powertest/temputature",str(temp))
    publish(client,"powertest/humidity",str(humid))
                
            
            
        #####write auxillary function to call####
    
    lts = log_state(lts,pressure, temp, humid, current, voltage, throttle)
    sleep_ms(10)
    print(m_pwm.duty_u16(),control_value, throttle)
    
    
    
            
    
