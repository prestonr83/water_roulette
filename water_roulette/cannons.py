# -*- coding: utf-8 -*-
"""Setup GPIO Pins for cannons and provide class for firing.

.. module: water_roulette.cannons

"""
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(22, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(4, GPIO.OUT, initial=GPIO.HIGH)


class Cannon(object):
    """Provides a cannon object with firing method.

    Attributes:
        number: The cannone number to assign.
        duration: How long the cannon should fire.
    """

    cannon_map = {
        1: 18,
        2: 17,
        3: 22,
        4: 23,
        5: 24,
        6: 4
    }

    def __init__(self, number, duration):
        self.number = number
        self.duration = duration

    def fire(self):
        """Fire the cannon."""
        cannons = [Cannon.cannon_map[cannon] for cannon in self.number]
        GPIO.output(cannons, GPIO.LOW)
        time.sleep(self.duration)
        GPIO.output(cannons, GPIO.HIGH)
        return True

    def fire_all(self):
        GPIO.output([18,17,22,23,24,4], GPIO.LOW)
        time.sleep(self.duration)
        GPIO.output([18,17,22,23,24,4], GPIO.HIGH)