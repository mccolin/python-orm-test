"""
Pony ORM
https://docs.ponyorm.org/
"""

from pony.orm import *


db = Database()
db.bind(provider='sqlite', filename=':memory:')


class LogEntityEvents(db.Entity):
    def print_log(self, msg: str):
        print(msg, self)

    def before_insert(self):
        self.print_log("Before Insert")

    def before_update(self):
        self.print_log("Before Update")

    def before_delete(self):
        self.print_log("Before Delete")
    


class Family(db.Entity, LogEntityEvents):
    id = PrimaryKey(int, auto=True)
    name = Required(str, index=True)
    members = Set('Person')


class Person(db.Entity, LogEntityEvents):
    id = PrimaryKey(int, auto=True)
    family = Required(Family)
    name = Required(str, index=True)
    age = Required(int)
    gender = Optional(str)


@db.on_connect(provider='sqlite')
def on_connect(db, connection):
    print("Connection established")
    print("-> Database:", db)
    print("-> Connection:", connection)

    f = Family(name="McCloskey")
    p = Person(family=f, name="Colin", age=37, gender="male")
    p = Person(family=f, name="Liz", age=36, gender="female")
    p = Person(family=f, name="Bennett", age=6, gender="male")
    p = Person(family=f, name="Lila", age=2, gender="female")


db.bind(**options)
db.generate_mapping(create_tables=True)
