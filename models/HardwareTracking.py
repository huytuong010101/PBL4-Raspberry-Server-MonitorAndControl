from peewee import *
from database import database as db
from datetime import datetime


class HardwareTracking(Model):
    time = DateTimeField(primary_key=True, default=datetime.now())
    ram_percent = FloatField(null=True)
    cpu_percent = FloatField(null=True)
    temperature_percent = FloatField(null=True)
    network_send = FloatField(null=True)
    network_receive = FloatField(null=True)

    def __str__(self):
        return f"{self.time}: cpu = {self.cpu_percent}%," \
               f" ram = {self.ram_percent}%, temperature = " \
               f"{self.temperature_percent}C, " \
               f"network_send = {self.network_send}," \
               f" network_receive = {self.network_receive}"

    class Meta:
        database = db
