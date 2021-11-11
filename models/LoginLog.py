from peewee import *
from database import database as db
from datetime import datetime
from models.User import User


class LoginLog(Model):
    time = DateTimeField(default=datetime.now(), null=False)
    device = CharField(null=True)
    user = ForeignKeyField(User, backref="has_login", null=False, on_delete="CASCADE")

    def __str__(self):
        return str(self.user) + " login at " + str(self.time)

    class Meta:
        database = db
        primary_key = CompositeKey('user', 'time')
