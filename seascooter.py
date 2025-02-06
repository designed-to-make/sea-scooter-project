#this module includes all functions that light be required to log data from sensors.
#07/02/2025
#update verion 0.03

from time import sleep, time

# Check that the current not negative and a buffer overrun number around 82000 if so make negative else pass raw value.
def real_current(raw_reading):
    if raw_reading > 45000:
        actual_current = raw_reading - 81920
    else:
        actual_current = raw_reading
    return actual_current


def av_current(ina_obj, samples):
    sample_number = 1
    readings =[]
    while sample_number < samples+1:
        raw_reading =  ina_obj.current
        reading = real_current(raw_reading)
        readings.append(reading)
        sample_number = sample_number+1
        sleep (0.001)
    else:
        return sum(readings)/(samples)


def log_state(last_time_stamp,pressure, temp, humid, current, voltage, control_state):
        log_time = time()
        if last_time_stamp+5 < log_time:
            last_time_stamp = log_time
            r_press	= str(round(pressure,1)) 		# in hPa
            r_temp 	= str(round(temp, 1)) 			# in Degress C
            r_humid	= str(round(humid,1)) 			# in %
            r_curr	= str(round(current,3)) 	# in Amps
            r_volt	= str(round(voltage,3))			# in Volts
            r_cont	= str(round(control_state,0))	# in throttle % if +ve else if -ve = Auxillary switch activated
            
            values_to_log = [log_time, r_press, r_temp, r_humid, r_curr, r_volt, r_cont]
            
            str_vtl = str(values_to_log)
            f = open("scoot_log.txt", "a")
            f.write(str_vtl)
            f.close()
            last_time_stamp = log_time
        else:
            print('skipped logging')
              
        return last_time_stamp

def reed_speed_control(Pin_Aux,P_20,P_60,P_100):
    state = [Pin_Aux.value(),P_20.value(),P_60.value(),P_100.value()]
    state_values = [-10,0,50,100]
    if sum(state) == 0:
        signal = 0
    else:
        signal = dot_product(state,state_values)/(sum(state))
    return int(round(signal,0))
    
def dot_product(v1, v2):
    """
    Computes the dot product of two vectors of equal length.
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have the same length.")
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result
