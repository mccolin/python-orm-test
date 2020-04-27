"""
Pony ORM
https://docs.ponyorm.org/
"""

from pony.orm import *


db = Database()


class LogEntityEvents():
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

db.bind(provider='sqlite', filename=':memory:')

db.generate_mapping(create_tables=True)

with db_session():
    f = Family(name="Hart")
    p = Person(family=f, name="Jim", age="69", gender="male")
    p = Person(family=f, name="Bee", age="69", gender="female")
    f = Family(name="McCloskey")
    p = Person(family=f, name="Colin", age=37, gender="male")
    p = Person(family=f, name="Liz", age=36, gender="female")
    p = Person(family=f, name="Bennett", age=6, gender="male")
    p = Person(family=f, name="Lila", age=2, gender="female")

    n_families = count(f for f in Family)
    n_people = count(p for p in Person)
    n_mccloskey = count(p for p in Person if p.family == f)

    print("There are", n_people, "people in", n_families, "families")

    for f in select(f for f in Family):
        n = count(p for p in Person if p.family == f)
        a = avg(p.age for p in Person if p.family == f)
        print("There are", n, "members of the", f.name, "family, with an average age of", a)

