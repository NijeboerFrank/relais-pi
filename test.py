"""
Program to check if all the wires are working and the Pi can communicate with the relay board
"""
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Init list with pin numbers

pinList = [2, 3, 4, 17]

# Loop through pins and set mode and state to 'high'

for i in pinList:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.HIGH)

# Set the sleep time
sleep_time = 2

# Turns on the outputs of the relays on the board one-by-one
try:

    GPIO.output(2, GPIO.LOW)
    print("ONE")
    time.sleep(sleep_time)
    GPIO.output(3, GPIO.LOW)
    print("TWO")
    time.sleep(sleep_time)
    GPIO.output(4, GPIO.LOW)
    print("THREE")
    time.sleep(sleep_time)
    GPIO.output(17, GPIO.LOW)
    print("FOUR")
    time.sleep(sleep_time)
    GPIO.cleanup()
    print("END")


# End program cleanly with keyboard
except KeyboardInterrupt:
    print(" Quit")

    # Reset GPIO settings
    GPIO.cleanup()
