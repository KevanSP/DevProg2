from threading import Thread
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


def temperatureThread(test_mode, temp_humi):
    global Output, Run_Multithread
    while Run_Multithread:
        if not test_mode:
            temperature, humidity = temp.read_temp_humidity()
        else:
            temperature, humidity = temp_humi

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
        threshold_lighting = 700
        lighting = adc.get_adc_value(0)
        # print ("Lighting value", lighting)
        if lighting > threshold_lighting:
            Output = True
    return Output


def motorThread(test_mode, test_count):
    global Output, Run_Multithread, count
    if test_mode:
        Output = True
        count = test_count
    while Run_Multithread:
        while Output:
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
    return Output, count


def turn_off_led():
    led.set_output(1, 0)


def turn_on_led():
    led.set_output(1, 1)


def main():
    t1 = Thread(target=temperatureThread)
    t1.start()
    t2 = Thread(target=slideSwitchThread)
    t2.start()
    t3 = Thread(target=motorThread)
    t3.start()
    t4 = Thread(target=lightingThread)
    t4.start()


if __name__ == "__main__":
    initialize_hardware()
    main()
