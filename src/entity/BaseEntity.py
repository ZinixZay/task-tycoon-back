from peewee import Model
from src.database import db


class BaseEntity(Model):
    class Meta:
        database = db
