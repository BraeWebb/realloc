from backend.structs import *
from backend.algo import Allocator

import sys

MAX = sys.maxsize


def test_multi_tutors():
    a = Person("Alice")
    b = Person("Bob")
    c = Person("Charlie")
    d = Person("Dave")

    t1 = Session("T01")
    t2 = Session("T02")
    t3 = Session("T03")
    t4 = Session("T04")
    t1.set_slots(2)

    a.set_prefs({t1: MAX, t2: 1, t3: 2, t4: MAX})
    b.set_prefs({t1: 2, t2: 1, t3: 3, t4: MAX})
    c.set_prefs({t1: 3, t2: MAX, t3: MAX, t4: 2})
    d.set_prefs({t1: 1, t2: MAX, t3: MAX, t4: MAX})

    alloc = Allocator([a, b, c, d], [t1, t2, t3, t4])
    alloc.run()

    print(a, ":", a.get_allocs())
    print(b, ":", b.get_allocs())
    print(c, ":", c.get_allocs())
    print(d, ":", d.get_allocs())


def test_clash():
    a = Person("Alice")
    b = Person("Bob")
    c = Person("Charlie")
    d = Person("Dave")

    t1 = Session("T01")
    t2 = Session("T02")
    t3 = Session("T03")
    t4 = Session("T04")

    a.set_prefs({t1: MAX, t2: 1, t3: 2, t4: MAX})
    b.set_prefs({t1: 2, t2: 1, t3: 3, t4: MAX})
    c.set_prefs({t1: 2, t2: MAX, t3: MAX, t4: 1})
    d.set_prefs({t1: 1, t2: MAX, t3: MAX, t4: MAX})

    t2.add_clash(t3)
    t3.add_clash(t2)

    alloc = Allocator([a, b, c, d], [t1, t2, t3, t4])
    alloc.run()

    print(a, ":", a.get_allocs())
    print(b, ":", b.get_allocs())
    print(c, ":", c.get_allocs())
    print(d, ":", d.get_allocs())


def test_more_sessions():
    a = Person("Alice")
    b = Person("Bob")
    c = Person("Charlie")
    d = Person("Dave")

    t1 = Session("T01")
    t2 = Session("T02")
    t3 = Session("T03")
    t4 = Session("T04")
    t5 = Session("T05")

    a.set_prefs({t1: MAX, t2: 1, t3: 2, t4: MAX, t5: MAX})
    b.set_prefs({t1: 2, t2: 1, t3: 3, t4: MAX, t5: 4})
    c.set_prefs({t1: 3, t2: MAX, t3: MAX, t4: 2, t5: 1})
    d.set_prefs({t1: 1, t2: MAX, t3: MAX, t4: MAX, t5: 2})

    alloc = Allocator([a, b, c, d], [t1, t2, t3, t4, t5])
    alloc.run()

    print(a, ":", a.get_allocs())
    print(b, ":", b.get_allocs())
    print(c, ":", c.get_allocs())
    print(d, ":", d.get_allocs())


def test_more_people():
    a = Person("Alice")
    b = Person("Bob")
    c = Person("Charlie")
    d = Person("Dave")
    e = Person("Emily")

    t1 = Session("T01")
    t2 = Session("T02")
    t3 = Session("T03")
    t4 = Session("T04")

    a.set_prefs({t1: MAX, t2: 1, t3: 2, t4: MAX})
    b.set_prefs({t1: 2, t2: 1, t3: 3, t4: MAX})
    c.set_prefs({t1: 2, t2: MAX, t3: MAX, t4: 1})
    d.set_prefs({t1: 1, t2: MAX, t3: MAX, t4: MAX})
    e.set_prefs({t1: MAX, t2: MAX, t3: 2, t4: 1})

    alloc = Allocator([a, b, c, d, e], [t1, t2, t3, t4])
    alloc.run()

    print(a, ":", a.get_allocs())
    print(b, ":", b.get_allocs())
    print(c, ":", c.get_allocs())
    print(d, ":", d.get_allocs())
    print(e, ":", e.get_allocs())


def test_basic():
    a = Person("Alice")
    b = Person("Bob")
    c = Person("Charlie")
    d = Person("Dave")

    t1 = Session("T01")
    t2 = Session("T02")
    t3 = Session("T03")
    t4 = Session("T04")

    a.set_prefs({t1: MAX, t2: 1, t3: 2, t4: MAX})
    b.set_prefs({t1: 2, t2: 1, t3: 3, t4: MAX})
    c.set_prefs({t1: 2, t2: MAX, t3: MAX, t4: 1})
    d.set_prefs({t1: 1, t2: MAX, t3: MAX, t4: MAX})

    alloc = Allocator([a, b, c, d], [t1, t2, t3, t4])
    alloc.run()

    print(a, ":", a.get_allocs())
    print(b, ":", b.get_allocs())
    print(c, ":", c.get_allocs())
    print(d, ":", d.get_allocs())

if __name__ == "__main__":
    test_multi_tutors()
