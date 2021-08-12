"""
Sample program to acuuire temperature and humidity data.
Target : Raspberrypi model 3B+ / Rasperrypi zero WH

@author: Hayato
"""

import RPi.GPIO as GPIO
from time import sleep
from DHT11_Python import dht11


GPIO_PIN = 4
INTERVAL = 15
RETRY_TIME = 2
MAX_RETRY_COUNT = 20

def gpio_initialize():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def gpio_end():
    GPIO.cleanup()


class Monitor(object):
    
    def __init__(self, gpio):
        self.gpio = gpio

    def get_value(self):
        sensor = dht11.DHT11(pin=self.gpio)
        retry_count = 0
        while True:
            retry_count += 1
            read_value = sensor.read()
            if read_value.is_valid():
                return read_value.temperature, read_value.humidity
            elif retry_count >= MAX_RETRY_COUNT:
                return 99.9, 99.9
            sleep(RETRY_TIME)

if __name__ == '__main__':

    gpio_initialize()
    try:
        monitor = Monitor(GPIO_PIN)
        while True:
            temp, hum = monitor.get_value()
            print("Temerature : {0} C  Humidity : {1} %".format(temp, hum))
            sleep(INTERVAL)
    except KeyboardInterrupt:
        print("Finish ! : Read Value...")
        pass
    
    gpio_end()
