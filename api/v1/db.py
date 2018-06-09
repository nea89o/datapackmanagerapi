from peewee import SqliteDatabase, ForeignKeyField, CharField, Model, IntegerField, DateTimeField, BooleanField

db = SqliteDatabase('datapackmanager.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField()
    id = IntegerField(primary_key=True)
    email = CharField()
    password_hash = CharField()


class Category(BaseModel):
    name = CharField()
    id = IntegerField(primary_key=True)


class Tag(BaseModel):
    name = CharField(primary_key=True)


class DataPack(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    description = CharField(max_length=10000)
    category = ForeignKeyField(Category)
    author = ForeignKeyField(User)
    likes = IntegerField()
    dislikes = IntegerField()
    downloads = IntegerField()
    views = IntegerField()


class TagRelation(BaseModel):
    tag = ForeignKeyField(Tag)
    pack = ForeignKeyField(DataPack)


class Comment(BaseModel):
    id = IntegerField(primary_key=True)
    datapack = ForeignKeyField(DataPack)
    user = ForeignKeyField(User)
    mesage = CharField(max_length=2000)
    creation = DateTimeField()


class Version(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    datapack = ForeignKeyField(DataPack)
    prerelease = BooleanField()
    releaedate = DateTimeField()


db.create_tables([DataPack, Category, Version, User, Comment, TagRelation, Tag])
__all__ = ['DataPack', 'Category', 'Version', 'User', 'Comment', 'TagRelation', 'Tag']
