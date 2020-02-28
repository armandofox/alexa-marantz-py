import os
import time
from random import randint

from meross_iot.cloud.devices.power_plugs import GenericPlug
from meross_iot.cloud.devices.light_bulbs import GenericBulb

from meross_iot.manager import MerossManager
from meross_iot.meross_event import MerossEventType

class MerossDriver():

    MEROSS_EMAIL = os.environ.get('MEROSS_EMAIL')
    MEROSS_PASSWORD = os.environ.get('MEROSS_PASSWORD')

    def __init__(self, email=MEROSS_EMAIL, password=MEROSS_PASSWORD):
        self.mm = MerossManager(email, password)
        self.mm.start()

    def switch(name, func):
        dev = self.mm.get_device_by_name(name)
        if (func == 'on'):
            dev.turn_on()
        elif (func == 'off'):
            dev.turn_off()
