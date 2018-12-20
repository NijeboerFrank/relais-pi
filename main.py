from flask import Flask
import RPi.GPIO as GPIO
import time
import atexit

sleep_time = 1

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Init list with pin numbers
# Order depending on how the GPIO pins are hooked up, in this case GPIO 17 controls relay 1
pinList = [17, 4, 3, 2]

# Loop through pins and set mode and state to 'high'
print("setting pins")
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)


@app.route("/")
def basic_test():
    return "Server works!"


@app.route("/4")
def run_4():
    switch_relay(number=4, slp_time=1)
    return "Switched light 4!"


@app.route("/3")
def run_3():
    switch_relay(number=3, slp_time=1)
    return "Switched light 3!"


@app.route("/2")
def run_2():
    switch_relay(number=2, slp_time=1)
    return "Switched light 2!"


@app.route("/1")
def run_1():
    switch_relay(number=1, slp_time=1)
    return "Switched light 1!"


def switch_relay(number, slp_time):
    slp = slp_time
    GPIO.output(pinList[number - 1], GPIO.LOW)
    time.sleep(slp)
    GPIO.output(pinList[number - 1], GPIO.HIGH)


@atexit.register
def exit_app():
    """
    This function is called when the server is stopped. This is important for a clean exit of the GPIO pins.
    """
    print("  Exiting Server...")
    GPIO.cleanup()


def callback_input(pin):
    GPIO.output(pinList[1], GPIO.input(12))


GPIO.add_event_detect(12, GPIO.RISING, callback=callback_input)  # add rising edge detection on a channel
