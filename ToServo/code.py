import board
import pwmio
import digitalio
from adafruit_motor import servo, motor
import time
import simpleio

def set_pins_as_digital_output(pin):
    digout = digitalio.DigitalInOut(pin)
    digout.direction = digitalio.Direction.OUTPUT
    return digout

def set_turn_rate(new_turn_rate):
    my_servo.throttle = new_turn_rate


# INITIALISE LEDS #

LED_PINS = [
    board.GP0, # {{{
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP16,
    board.GP17,
    board.GP26,
    board.GP27,
    board.GP28# }}}
]

LEDS = list(map(set_pins_as_digital_output, LED_PINS))

PIEZO_SPEAKER = board.GP22

# Initialise buttons #
btn1 = digitalio.DigitalInOut(board.GP20)
btn2 = digitalio.DigitalInOut(board.GP21)

# Initialising a continuous servo on left-most SERVO pin (GP12)
pwm_gp12 = pwmio.PWMOut(board.GP12, duty_cycle=2**15, frequency=50)
my_servo = servo.ContinuousServo(pwm_gp12)


# Initialise turning rate and starting LED indicator
turn_rate = 0
current_led = 6
set_turn_rate(turn_rate)

while True:
    LEDS[6].value = True
    btn1_pressed = not btn1.value
    btn2_pressed = not btn2.value
    first_led_off = not LEDS[0].value
    last_led_off = not LEDS[12].value

    if btn1_pressed:
        if last_led_off:
            simpleio.tone(PIEZO_SPEAKER, 800, 0.05)
            turn_rate+=0.01
            LEDS[current_led].value = False
            current_led+=1
            LEDS[current_led].value = True
        else:
            simpleio.tone(PIEZO_SPEAKER, 500, 0.05)
            simpleio.tone(PIEZO_SPEAKER, 250, 0.05)

    elif btn2_pressed:
        if first_led_off:
            simpleio.tone(PIEZO_SPEAKER, 600, 0.05)
            turn_rate-=0.01
            LEDS[current_led].value = False
            current_led-=1
            LEDS[current_led].value = True
        else:
            simpleio.tone(PIEZO_SPEAKER, 500, 0.05)
            simpleio.tone(PIEZO_SPEAKER, 250, 0.05)

    set_turn_rate(turn_rate)
    time.sleep(0.3)

