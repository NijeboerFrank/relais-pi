from flask import Flask
import RPi.GPIO as GPIO
import time

sleep_time = 2

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

# Init list with pin numbers

pinList = [2, 3, 4, 17]

# Loop through pins and set mode and state to 'high'

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)




@app.route("/")
def basic_test():
    return "Server works!"


@app.route("/1")
def run_4():
    GPIO.output(pinList[0], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[0], GPIO.HIGH)
    return "Switch light 1!"


@app.route("/2")
def run_3():
    GPIO.output(pinList[1], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[1], GPIO.HIGH)
    return "Switch light 2!"


@app.route("/3")
def run_2():
    GPIO.output(pinList[2], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[2], GPIO.HIGH)
    return "Switch light 3!"


@app.route("/4")
def run_1():
    GPIO.output(pinList[3], GPIO.LOW)
    time.sleep(sleep_time)
    GPIO.output(pinList[3], GPIO.HIGH)
    return "Switch light 4!"
