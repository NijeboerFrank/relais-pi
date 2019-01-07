from flask import Flask
import RPi.GPIO as GPIO
import time
import atexit

sleep_time = 1

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Init list with pin numbers
# Order depending on how the GPIO pins are hooked up, in this case GPIO 17 controls relay 1
pin_list = [17, 4, 3, 2]
input_pin = 12
input_pins = [16, 20, 21]

# Loop through pins and set mode and state to 'high'
print("setting pins")
for i in pin_list:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# Set the pins for the GPIO input. PUD_DOWN means that when the pin has no input the value is low (0). Without this
# value the pin will 'float'.
for i in input_pins:
    GPIO.setup(i, GPIO.IN, GPIO.PUD_DOWN)

# Set the input pin for the 'control' pin.
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


@app.route("/input")
def check_input():
    inp = read_input()
    print(inp)
    return "%s, %s, %s" % (inp[0], inp[1], inp[2])


@app.route("/program/<int:program_id>")
def run_decimal(program_id):
    """
    If this is called it will turn on the relays in a binary representation of the decimal that is provided by the get
    request. After this is called there should be some input that signal the machine can start. This function will wait
    for that input and otherwise return a timeout.

    :param program_id: Decimal representation of the program ID number.
    """
    if 0 <= program_id < 16:
        switch_decimal(program_id)

        ret = GPIO.wait_for_edge(input_pin, GPIO.RISING, timeout=5000)
        if ret is None:
            return "Timeout occurred"
        else:
            switch_relay(1, 1.5)
            return "Switched %s!" % program_id

    else:
        return "Program ID must be between 0 and 15"


@app.route("/test/<int:program_id")
def run_test(program_id):
    if 0 <= program_id < 16:
        switch_decimal(program_id)
        return "Switched %s!" % program_id
    else:
        return "Program ID must be between 0 and 15"



def switch_decimal(decimal):
    """
    Function for switching on the relays in the form of a binary number.

    :param decimal: Decimal number that should be represented in binary.
    """
    binary = get_binary(decimal)
    switch_binary(binary)


def switch_binary(binary):
    """
    Function for switching on the relay in the form of a binary number.

    :param binary: Array containing the binary number.
    """
    on = []
    for b in range(0, len(binary)):
        if binary[b] > 0:
            on.append(b)
    for o in on:
        GPIO.output(pin_list[o], GPIO.LOW)
    time.sleep(sleep_time)
    for o in on:
        GPIO.output(pin_list[o], GPIO.HIGH)


def switch_relay(number, slp_time):
    """
    Function that switches a relay on.
    :param number: Which relay should be switched on.
    :param slp_time: How long should the relay be switched on. 
    """
    slp = slp_time
    GPIO.output(pin_list[number - 1], GPIO.LOW)
    time.sleep(slp)
    GPIO.output(pin_list[number - 1], GPIO.HIGH)


def read_input():
    ret = [GPIO.input(input_pins[0]), GPIO.input(input_pins[1]), GPIO.input(input_pins[2])]
    return ret


@atexit.register
def exit_app():
    """
    This function is called when the server is stopped. This is important for a clean exit of the GPIO pins.
    """
    print("  Exiting Server...")
    GPIO.cleanup()


def get_binary(decimal):
    """
    Function that gets an array that represents a decimal number.

    :param decimal: Decimal number that must be converted.
    :return: Array that represents a number number with 4 bits.
    """
    ret = [int(x) for x in bin(decimal)[2:]]
    while len(ret) < 4:
        ret.insert(0, 0)
    return ret


def callback_input(pin):
    """
    Function that keeps a relay powered on when a button is pressed. (In this case when GPIO 12 reads input)

    :param pin: Pin number of the GPIO pin.
    """
    while GPIO.input(pin) == 1:
        GPIO.output(pin_list[1], GPIO.LOW)
    GPIO.output(pin_list[1], GPIO.HIGH)


# Add callback for button press
# GPIO.add_event_detect(12, GPIO.RISING, callback=callback_input)  # add rising edge detection on a channel
