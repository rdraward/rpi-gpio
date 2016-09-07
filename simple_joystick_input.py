#!/usr/bin/python
#--------------------------------------
# This script reads data from a
# MCP3008 ADC device using the SPI bus.
#
# Addition: Recreate the fun from your
# favourite Mario Party games!  Who can
# spin the joystick the fastest and light
# up the LEDs without suffering from
# permanent damage to their palms?
#
# Extra fun: don't ever connect the last LED!
#
# Analogue joystick version!
#
# Original Joystik Demo Author : Matt Hawkins
# Date   : 17/04/2014
# http://www.raspberrypi-spy.co.uk/
#
# MP Update Author: Riley Draward
#
#--------------------------------------
 
import spidev
import time
import os
import RPi.GPIO as GPIO
from array import array

GPIO.setmode(GPIO.BOARD)

# Set up GPIO pins for LEDs
gpio_pins = [7, 29, 31, 33, 35, 37]

def setUpLEDs():
  for i in gpio_pins:
    GPIO.setup(i, GPIO.OUT)

# Turn off all LEDs
def turnOffLEDs():
  for i in gpio_pins:
    GPIO.output(i, False)

# Set number of LEDs active
def ledSwitch(x):
  num_pins = len(gpio_pins)
  if x > 1000:
    return gpio_pins[num_pins - 1]
  if x > 800:
    return gpio_pins[num_pins - 2]
  if x > 600:
    return gpio_pins[num_pins - 3]
  if x > 400:
    return gpio_pins[num_pins - 4]
  if x > 200:
    return gpio_pins[num_pins - 5]
  if x >= 0:
    return gpio_pins[num_pins - 6]

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Define sensor channels
# (channels 3 to 7 unused)
swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Store running difference in x and y values
js_total = 0 
x_prev = 0
y_prev = 0
 
# Define delay between readings (s)
delay = 0.1
reset_timer = 0
try:
  setUpLEDs()
 
  while True:
 
    # Read the joystick position data
    vrx_pos = ReadChannel(vrx_channel)
    vry_pos = ReadChannel(vry_channel)
 
    js_total += (abs(x_prev - vrx_pos) + abs(y_prev - vry_pos))
    x_prev = vrx_pos
    y_prev = vry_pos

    print(js_total)

    # TODO: Intellegently get values in a range of 0 - 1000
    total_norm = js_total / 10
    GPIO.output(ledSwitch(total_norm), True)


    # Read switch state (switch difficulty in future?)
    #swt_val = ReadChannel(swt_channel)
    time.sleep(delay)

    # You only have 5 seconds
    reset_timer += delay
    if reset_timer >= 5:
      turnOffLEDs()
      js_total = 0

except KeyboardInterrupt:
   GPIO.cleanup()

