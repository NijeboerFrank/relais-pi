from flask import Flask
import RPi.GPIO as GPIO
import time
import atexit

sleep_time = 1

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Init list with pin numbers

pinList = [2, 3, 4, 17]

# Loop through pins and set mode and state to 'high'
print("setting pins")
for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)


@app.route("/")
def basic_test():
    return "Server works!"


@app.route("/4")
def run_4():
    GPIO.output(pinList[0], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[0], GPIO.HIGH)
    return "Switched light 4!"


@app.route("/3")
def run_3():
    GPIO.output(pinList[1], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[1], GPIO.HIGH)
    return "Switched light 3!"


@app.route("/2")
def run_2():
    GPIO.output(pinList[2], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[2], GPIO.HIGH)
    return "Switched light 2!"


@app.route("/1")
def run_1():
    GPIO.output(pinList[3], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[3], GPIO.HIGH)
    return "Switched light 1!"


@atexit.register
def exit_app():
    print("  Exiting Server...")
    GPIO.cleanup()

