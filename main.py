from flask import Flask
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

@app.route("/")
def basic_test():
    return "Server works!"