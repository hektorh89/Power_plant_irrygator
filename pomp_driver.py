#!/usr/bin/env python3
import time
from threading import local

import RPi.GPIO as GPIO
import os
import logging

path = os.path.abspath(os.path.dirname(__file__))


def get_logger(name):
    # global logger
    # if logger is None:
    log_file = os.path.join(path, 'plant.log')
    log_level = os.environ.get('DBG_LEVEL', 'INFO').upper()

    # if log level is set to debug than insert additional log information
    if log_level == 'DEBUG':
        console_formatter = logging.Formatter('%(asctime)s::%(levelname)s\t[%(filename)s]\t%(message)s')
    else:
        console_formatter = logging.Formatter(f'%(asctime)s::%(levelname)s::{name}\t%(message)s')

    console_log_handler = logging.StreamHandler()
    save_handler = logging.FileHandler(filename=log_file)
    console_log_handler.setFormatter(console_formatter)
    save_handler.setFormatter(console_formatter)
    console_log_handler.setLevel(log_level)
    save_handler.setLevel(log_level)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_log_handler)
    logger.addHandler(save_handler)
    return logger


class Pump:
    PUMP1 = 15
    PUMP2 = 18
    PUMP3 = 0
    PUMP4 = 5
    PUMP5 = 6
    PUMP6 = 13
    PUMP_LIST = [PUMP1, PUMP2, PUMP3, PUMP4, PUMP5, PUMP6]


class PumpDriver(Pump):

    logger = get_logger('PumpDriver')

    def __init__(self):
        self.logger.info("init")
        GPIO.setmode(GPIO.BCM)
        self._init_pump()
        self.off_all()

    def _init_pump(self):
        self.logger.info("init GPIO")
        for pump in self.PUMP_LIST:
            GPIO.setup(pump, GPIO.OUT)

    def off_all(self):
        self.logger.debug("off all")
        for pump in self.PUMP_LIST:
            self.off_pump(pump)

    def on_all(self):
        self.logger.debug("on all")
        for pump in self.PUMP_LIST:
            self.on_pump(pump)

    def on_pump(self, pump):
        self.logger.info(f"start pump nr: {pump}")
        GPIO.output(pump, GPIO.HIGH)

    def off_pump(self, pump):
        self.logger.debug(f"stop pump nr: {pump}")
        GPIO.output(pump, GPIO.LOW)

    def test(self):
        time.sleep(3)
        self.on_all()
        time.sleep(3)
        self.off_all()

    def clear(self):
        self.logger.info("Clear")
        GPIO.cleanup()


if __name__ == '__main__':
    driver = PumpDriver()
    time.sleep(3)
    driver.on_pump(Pump.PUMP4)
    # driver.on_all()
    time.sleep(5)
    driver.off_all()
    # driver.clear()
