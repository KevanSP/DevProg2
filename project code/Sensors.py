from threading import Thread
import Notification as noif
from time import sleep
from hal import hal_adc as adc
from hal import hal_buzzer as buzz
from hal import hal_dc_motor as valve
from hal import hal_input_switch as button
from hal import hal_led as led
from hal import hal_temp_humidity_sensor as temp

Output = 0
count = 0

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


def temperatureThread():
    global Output, Run_Multithread
    while Run_Multithread:
        temperature, humidity = temp.read_temp_humidity()
        # print(temperature, humidity)
        if temperature > 80 or humidity > 100:
            Output = True
    return Output


def slideSwitchThread():
    global Output, Run_Multithread
    while Run_Multithread:
        # print(Output)
        Output = button.read_slide_switch()
    return Output


def lightingThread():
    global Output, Run_Multithread
    while Run_Multithread:
        threshold_lighting = 1000
        lighting = adc.get_adc_value(0)
        # print ("Lighting value", lighting)
        if lighting > threshold_lighting:
            Output = True
    return Output


def motorThread():
    global Output, Run_Multithread, count
    while Run_Multithread:
        if Output:
            while True:
                if count <= 10:
                    buzz.turn_on()
                    valve.set_motor_speed(60)
                    turn_on_led()
                    sleep(0.5)
                    turn_off_led()
                    sleep(0.5)
                    count += 1
                    # print(count)
                else:
                    Output = False
                    count = 0
                    buzz.turn_off()
                    valve.set_motor_speed(0)
                    # print(Output)
                    return
    return Output, count

def noifThread():
    while Run_Multithread:
        if Output:
            noif.Send_Notif('Sensor Detection', 'One Of The Sensor Detected Possible Fire.')
        sleep(5)


def turn_off_led():
    led.set_output(1, 0)


def turn_on_led():
    led.set_output(1, 1)


def main():
    initialize_hardware()
    t1 = Thread(target=temperatureThread)
    t1.start()
    t2 = Thread(target=slideSwitchThread)
    t2.start()
    t3 = Thread(target=motorThread)
    t3.start()
    t4 = Thread(target=lightingThread)
    t4.start()
    t5 = Thread(target=noifThread)
    t5.start()


if __name__ == "__main__":
    main()
