from peewee import *
from database import database as db
from datetime import datetime


class User(Model):
    username = CharField(max_length=255, null=False, primary_key=True)
    fullname = CharField(max_length=255, null=False)
    password = CharField(max_length=255, null=False)
    avatar = CharField(max_length=225, null=True)
    email = CharField(max_length=255, null=True)
    is_admin = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now())
    created_by = ForeignKeyField("self", backref="created", null=True, on_delete="SET NULL")

    def __str__(self):
        return self.username

    class Meta:
        database = db
