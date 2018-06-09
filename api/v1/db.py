from peewee import SqliteDatabase, ForeignKeyField, CharField, Model, IntegerField

db = SqliteDatabase('datapackmanager.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    id = IntegerField(primary_key=True)


class Category(BaseModel):
    name = CharField()
    id = IntegerField(primary_key=True)


class DataPack(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    description = CharField(max_length=10000)
    category = ForeignKeyField(Category)
    author = ForeignKeyField(User)


class Version(BaseModel):
    name = CharField()
    datapack = ForeignKeyField(DataPack)


db.create_tables([DataPack, Category, Version, User])
__all__ = ('DataPack', 'Category', 'Version', 'db')
