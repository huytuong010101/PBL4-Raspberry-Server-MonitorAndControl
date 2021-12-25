from peewee import *
from database import database as db
from datetime import datetime
from models.User import User


class ActivityTracking(Model):
    act_id = AutoField(primary_key=True)
    time = DateTimeField(default=datetime.now(), null=False)
    action = TextField(null=False)
    user = ForeignKeyField(User, on_delete="SET NULL", null=True)

    def __str__(self):
        return self.user + " " + self.action + " at " + str(self.time)

    class Meta:
        database = db
