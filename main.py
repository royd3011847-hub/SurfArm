# imports:
import busio
import board
import adafruit_pca9685 as PCA9685
import time
import calcArmDegrees
import math

 
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685.PCA9685(i2c, address=0x41)

time.sleep(0.1)

pca.frequency = 200 # hz
actual_frequency = 212.8
minDuty = 6972
maxDuty = 34864

# duty min: 4873
# duty max: 26649

# 0 degree duty: 500 ms
# 180 degree duty: 2500 ms
def ms_to_duty(ms : float):
    global actual_frequency
    duty_cycle = ms/(1000000/actual_frequency)
    return int(duty_cycle * 65535)


# 0 degrees = 500 ms
#180 degrees = 2500 ms
def degrees_to_ms(degrees: float):
     ms = 500.0
     ms += 2000/180 * degrees
     return ms
     
def degrees_to_duty(degrees: float):
    return ms_to_duty(degrees_to_ms(degrees))
    

 
pca.channels[0].duty_cycle = degrees_to_duty(90)
pca.channels[1].duty_cycle = degrees_to_duty(90)

try:
    for channel in range(16): # there are 16 total, only using 8 here
        pca.channels[channel].duty_cycle = ms_to_duty(0.0)
    time.sleep(2.0)
    
    
    while True:
        time.sleep(0.1)
        x = float(input("Enter x:"))
        y = float(input("Enter y:"))
        (servo0Deg, servo1Deg) = calcArmDegrees.arm_degrees(x, y)
        
        print("servo0Deg: "+str(servo0Deg))
        print("servo1Deg: "+str(servo1Deg))
        #servo 0
        duty0 = degrees_to_duty(servo0Deg)
        print("duty0: "+str(duty0))
        if minDuty > duty0 or duty0 > maxDuty:
            print("out of range")
        else:
            channel = 0
            pca.channels[channel].duty_cycle = duty0
        
        #servo 1
        duty1 = degrees_to_duty(servo1Deg)
        print("duty0: "+str(duty1))
        if minDuty > duty1 or duty1 > maxDuty:
            print("out of range")
        else:
            channel = 1
            pca.channels[channel].duty_cycle = duty1
        

except KeyboardInterrupt:
    for channel in range(16): # there are 16 total, only using 8 here
        pca.channels[channel].duty_cycle = ms_to_duty(500)
