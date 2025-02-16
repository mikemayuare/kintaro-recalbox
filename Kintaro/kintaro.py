#!/usr/bin/python -u
# Copyright 2017 Michael Kirsch

import time
import os
import RPi.GPIO as GPIO
import logging

class SNES:

    def __init__(self):
        # GPIOs
        self.led_pin = 7
        self.fan_pin = 8
        self.reset_pin = 3
        self.power_pin = 5
        self.check_pin = 10

        # vars
        self.fan_hysteresis = 20
        self.fan_starttemp = 60
        self.debounce_time = 0.1

        # path
        self.temp_command = 'cat /sys/class/thermal/thermal_zone0/temp'

        # Set up logging
        logging.basicConfig(
            level=logging.DEBUG,
            filename='/tmp/kintaro.log',
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        # Set the GPIOs
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.fan_pin, GPIO.OUT)
        GPIO.setup(self.power_pin, GPIO.IN)
        GPIO.setup(self.reset_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.check_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pwm = GPIO.PWM(self.fan_pin, 50)
        self.pwm.start(0)

    def power_interrupt(self, channel):
        logging.debug('Power button interrupt triggered.')
        time.sleep(self.debounce_time)
        if GPIO.input(self.power_pin) == GPIO.HIGH and GPIO.input(self.check_pin) == GPIO.LOW:
            self.led(0)
            logging.info('Shutting down the system.')
            os.system("shutdown -h now")
        logging.getLogger().handlers[0].flush()

    def reset_interrupt(self, channel):
        logging.debug('Reset button interrupt triggered.')
        if GPIO.input(self.reset_pin) == GPIO.LOW:
            time.sleep(self.debounce_time)
            while GPIO.input(self.reset_pin) == GPIO.LOW:
                self.blink(15, 0.1)
                os.system("reboot")
        logging.getLogger().handlers[0].flush()

    def pcb_interrupt(self, channel):
        GPIO.cleanup()  # when the pcb is pulled clean all the used GPIO pins

    def temp(self):     #returns the gpu temoperature
        res = os.popen(self.temp_command).readline()
        return float((res.replace("temp=", "").replace("'C\n", "")))

    def pwm_fancontrol(self,hysteresis, starttemp, temp):
        perc = 100.0 * ((temp - (starttemp - hysteresis)) / (starttemp - (starttemp - hysteresis)))
        perc=min(max(perc, 0.0), 100.0)
        self.pwm.ChangeDutyCycle(float(perc))

    def led(self,status):  #toggle the led on of off
        if status == 0:       #the led is inverted
            GPIO.output(self.led_pin, GPIO.LOW)
        if status == 1:
            GPIO.output(self.led_pin, GPIO.HIGH)

    def blink(self,amount,interval): #blink the led
        for x in range(amount):
            self.led(1)
            time.sleep(interval)
            self.led(0)
            time.sleep(interval)

    def check_fan(self):
        self.pwm_fancontrol(self.fan_hysteresis,self.fan_starttemp,self.temp())  # fan starts at 60 degrees and has a 5 degree hysteresis

    def attach_interrupts(self):
        if GPIO.input(self.check_pin) == GPIO.LOW:  # check if there is an pcb and if so attach the interrupts
            GPIO.add_event_detect(self.check_pin, GPIO.RISING,callback=self.pcb_interrupt)  # if not the interrupt gets attached
            if GPIO.input(self.power_pin) == GPIO.HIGH: #when the system gets startet in the on position it gets shutdown
                os.system("shutdown -h now")
            else:
                self.led(1)
                GPIO.add_event_detect(self.reset_pin, GPIO.FALLING, callback=self.reset_interrupt)
                GPIO.add_event_detect(self.power_pin, GPIO.RISING, callback=self.power_interrupt)
        else:       #no pcb attached so lets exit
            GPIO.cleanup()
            exit()

snes = SNES()
snes.attach_interrupts()

while True:
    time.sleep(5)
    snes.led(1)
    snes.check_fan()

