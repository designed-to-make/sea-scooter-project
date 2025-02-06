#Main program to run at boot
06/02/2025
#V0.03 with ota SUCCESS


from machine import Pin, I2C, PWM
from time import sleep, sleep_ms
from bme680 import *
from ina260 import INA260, AveragingCount, ConversionTime
from seascooter import *
from ota import OTAUpdater
from WIFI_CONFIG import SSID, PASSWORD

#check for OTA updates
firmware_url = "https://raw.githubusercontent.com/designed-to-make/sea-scooter-project/"

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
ota_updater.download_and_install_update_if_available()

ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "seascooter.py")
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

    

while True:
    pressure 		= bme.pressure # hPa
    temp	 		= bme.temperature # degrees 
    humid			= bme.humidity # %
    current			= av_current(ob_ina260, 10)/1000 #Amps
    voltage			= ob_ina260.voltage # Volts
    control_value 	= reed_speed_control(p_aux,p_0,p_50,p_100)
    
    if control_value >=0:
        m_pwm.duty_u16(3*control_value)
        
    else:
        m_pwm.duty_u16(0)
        #####write auxillary function to call####
    
    lts = log_state(lts,pressure, temp, humid, current, voltage, control_value)
    sleep_ms(100)
    print(m_pwm.duty_u16(),control_value)
    
    
            
    
