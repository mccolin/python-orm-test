"""
Orator ActiveRecord-pattern ORM
https://orator-orm.com/
"""
from datetime import date, datetime
from orator import DatabaseManager, Schema, SoftDeletes
from orator import Model as OratorModel
from orator.orm import belongs_to, has_many
from orator.schema import Blueprint

config = {
    'db': {
        'driver': 'sqlite',
        'database': ':memory:',
    }
}

db = DatabaseManager(config)

OratorModel.set_connection_resolver(db)


###


schema = Schema(db)

with schema.create('articles') as table:
    table.increments('id')
    table.string('title')
    table.date('published_on')
    table.integer('author_id')
    table.integer('genre_id').default(1)
    table.enum('style', ['article', 'poem', 'song', 'list']).default('article')
    table.text('body')
    table.nullable_timestamps()
    table.soft_deletes()

with schema.create('comments') as table:
    table.increments('id')
    table.integer('article_id')
    table.integer('author_id')
    table.text('body')
    table.nullable_timestamps()
    table.soft_deletes()

with schema.create('authors') as table:
    table.increments('id')
    table.string('name')
    table.date('member_since')
    table.nullable_timestamps()

with schema.create('genres') as table:
    table.increments('id')
    table.string('name')
    table.nullable_timestamps()
    table.soft_deletes()


###


class Article(SoftDeletes, OratorModel):

    @belongs_to
    def author(self):
        return Author

    @belongs_to
    def genre(self):
        return Genre

    @has_many
    def comments(self):
        return Comment


class Author(OratorModel):

    __fillable__ = ['name', 'member_since']

    @has_many
    def articles(self):
        return Article

    @has_many
    def comments(self):
        return Comment


class Genre(OratorModel):

    @has_many
    def articles(self):
        return Article


class Comment(OratorModel):

    @belongs_to
    def author(self):
        return Author

    @belongs_to
    def article(self):
        return Article


####

import json

def out(obj):
    if "serialize" in dir(obj):
        obj = obj.serialize()
    print( json.dumps(obj, indent=2, sort_keys=True) )

colin = Author.create(name="Colin McCloskey", member_since=date(2000,12,20))
dibs = Author.create(name="David Heliotis", member_since=date(2001,1,3))

print("Authors")
out( Author.all() )

article = Article()
article.author().associate(colin)
article.title = "Snow Falling on Cedars"
article.body = "Lorem ipsum delicious tasty ipsum."
article.published_on = date(2000, 12, 20)
article.save()

print("Articles")
out( Article.all() )
