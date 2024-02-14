from unittest.mock import patch

import Sensors as mf

def test_temperatureThread():
    result = []
    test_arr = [[90,10], [50,200], [50,50]]
    pass_arr = [True,True,False]

    for item in test_arr:
        result = result.append(mf.temperatureThread(True, item))

    assert (result == pass_arr)

def test_slideSwitchThread():
    result = []
    test_input = [True,False]
    pass_arr = [True,False]
    for item in test_input:
        with patch('button.read_slide_switch') as test_input:

            test_input.return_value = item

            result = result.append(mf.slideSwitchThread())

    assert (result == pass_arr)

def test_lightingThread():
    result = []
    test_input = [800, 600]
    pass_arr = [True, False]
    for item in test_input:
        with patch('adc.get_adc_value') as test_input:
            test_input.return_value = item

            result = result.append(mf.lightingThread())

    assert (result == pass_arr)

def test_motorThread():
    result = []
    test_input = 2
    pass_arr = [True, 0]
    with patch('buzz.turn_on') as buzz_on, \
    patch('valve.set_motor_speed') as motor, \
    patch('turn_on_led') as led_on, \
    patch('turn_off_led') as led_off, \
    patch('buzz.turn_off') as buzz_off:
        buzz_on.return_value = True
        buzz_off.return_value = True
        led_on.return_value = True
        led_off.return_value = True
        motor.return_value = True

        result = mf.motorThread(True,test_input)

    assert (result == pass_arr)

def test_nof():
    mf.noifThread(True)
    assert True
