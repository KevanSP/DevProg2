import array
from hal import hal_led as led
from hal import hal_buzzer as buzz
from hal import hal_input_switch as button
from hal import hal_temp_humidity_sensor as temp
from hal import hal_servo as valve
from threading import Thread
from time import sleep

Output = 0
Run_Multithread = True  # Define Run_Multithread

def initialize_hardware():
    try:
        led.init()
        temp.init()
        button.init()
        valve.init()
        buzz.init()
        valve.set_servo_position(0)
        turn_0ff_led()
    except Exception as e:
        print(f"Initialization error: {e}")

def thread1():
    global Output, Run_Multithread
    while Run_Multithread:
        temperature, humidity = temp.read_temp_humidity()
        if temperature > 100 or humidity > 100:
            Output = 1

def thread2():
    global Output, Run_Multithread
    while Run_Multithread:
        if button.read_slide_switch():
            Output = 1

def turn_0ff_led():
    led.set_output(1, 0)

def turn_0n_led():
    led.set_output(1, 1)

def main():
    t1 = Thread(target=thread1)
    t1.start()
    t2 = Thread(target=thread2)
    t2.start()

    while Output == 1:
        print("Main program...")
        sleep(1)
    # Note: count is not defined or used in the original code, so I'm assuming it's not needed.

    for _ in range(10):  # Just as an example loop
        valve.set_servo_position(180)
        buzz.turn_on()
        turn_0n_led()
        sleep(4)  # 4000 ms converted to seconds

if __name__ == "__main__":
    initialize_hardware()
    main()
