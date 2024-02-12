from hal import hal_led as led
from hal import hal_buzzer as buzz
from hal import hal_input_switch as button
from hal import hal_temp_humidity_sensor as temp
from hal import hal_dc_motor as valve
from threading import Thread
from hal import hal_ir_sensor as ir
from time import sleep
from hal import  hal_adc as adc

Output = 0
count =0

Run_Multithread = True  # Define Run_Multithread

def initialize_hardware():
    led.init()
    temp.init()
    button.init()
    valve.init()
    buzz.init()
    adc.init()
    valve.set_motor_speed(0)
    turn_off_led()
    buzz.turn_off()
    

def thread1():
    global Output, Run_Multithread
    while Run_Multithread:
        temperature, humidity = temp.read_temp_humidity()
        print(temperature,humidity)
        if temperature > 80 or humidity > 100:
            Output = True
            

def thread2():
    global Output, Run_Multithread
    while Run_Multithread:
        #print(Output)
        p = button.read_slide_switch()
        if p == True:
            Output = True
def thread4():
    global Output, Run_Multithread
    while Run_Multithread:
        threshold_lighting = 700
        lighting = adc.get_adc_value(0)
        #print ("Lighting value", lighting)
        if lighting > threshold_lighting:
            Output = True
            
    
           
def thread3():
    global Output, Run_Multithread, count
    while Run_Multithread:
        while Output == True:
            if count <= 10:
                buzz.turn_on()
                valve.set_motor_speed(60)
                turn_on_led()
                sleep(0.5)
                turn_off_led()
                sleep(0.5)
                count+=1
                print(count)
            else:
                Output = False
                count = 0
                buzz.turn_off()
                valve.set_motor_speed(0)
                print(Output)
      
    
def turn_off_led():
    led.set_output(1, 0)

def turn_on_led():
    led.set_output(1, 1)

def main():
    t1 = Thread(target=thread1)
    t1.start()
    t2 = Thread(target=thread2)
    t2.start()
    t3 = Thread(target=thread3)
    t3.start()
    t4 = Thread(target=thread4)
    t4.start()

    
        # Note: count is not defined or used in the original code, so I'm assuming it's not needed.

if __name__ == "__main__":
    initialize_hardware()
    main()


