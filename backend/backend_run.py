"""
People input format:
    {person name: {day: [[time, type], ...]}}

Session input format:
    {session name: [day, start, end]}
"""

from algo import Allocator
from structs import Person, Session
from pprint import pprint
import sys

RUN_COUNT = 10

TIMES = ["8:00am", "9:00am", "10:00am", "11:00am", "12:00pm", "13:00pm", "14:00pm", "15:00pm", "16:00pm", "17:00pm",
         "18:00pm", "19:00pm", "20:00pm"]


def time_lt(a, b):
    return TIMES.index(a) < TIMES.index(b)


def time_leq(a, b):
    return TIMES.index(a) <= TIMES.index(b)


def time_gt(a, b):
    return TIMES.index(a) > TIMES.index(b)


def time_geq(a, b):
    return TIMES.index(a) >= TIMES.index(b)


def time_in(day_a, start_a, end_a, day_b, start_b, end_b):
    """Returns if a is within b's hours"""
    b = (time_geq(start_a, end_a) and time_lt(start_a, end_b)) or \
        (time_leq(end_a, end_b) and time_gt(end_a, start_b))
    return b and day_a == day_b


def clash(day_a, start_a, end_a, day_b, start_b, end_b):
    """Returns if a and b clash"""
    return time_in(day_a, start_a, end_a, day_b, start_b, end_b) or \
           time_in(day_b, start_b, end_b, day_a, start_a, end_a)


def plus_1(time):
    return TIMES[TIMES.index(time) + 1]


def setup(people_input, session_input):

    people = []
    sessions = []
    session_times = {}

    for s in session_input:
        day, start, end = session_input[s]
        new = Session(s)
        session_times[(day, start, end)] = new
        sessions.append(new)
    compute_clashes(session_times)

    for p in people_input:
        new = Person(p)
        for t in session_times:
            i = session_times[t]
            a = is_avail(t, people_input[p])
            if not a:
                new.set_pref(i, sys.maxsize)
            elif a == 1:
                new.set_pref(i, 1)
            elif a == 2:
                new.set_pref(i, 5)
        people.append(new)

    return people, sessions


def run_multi(people, sessions):
    allocations = []
    for i in range(RUN_COUNT):
        try:
            a = Allocator(people, sessions)
            a.run()
            this = {}
            for p in people:
                this[p] = p.get_allocs()
            if this not in allocations:
                allocations.append(this)
        except:
            continue
    return allocations


def run(people_input, session_input):
    return run_multi(*setup(people_input, session_input))


def is_avail(session_time, person_details):
    day = session_time[0]
    start = session_time[1]
    end = session_time[2]
    need_be = False
    while time_lt(start, end):
        if [start, 2] in person_details[day]:
            need_be = True
        elif [start, 1] not in person_details[day]:
            return 0
        start = plus_1(start)
    if need_be:
        return 2
    return 1


def compute_clashes(session_times):
    for t in session_times:
        i = session_times[t]
        for u in session_times:
            j = session_times[u]
            if i != j and clash(t[0], t[1], t[2], u[0], u[1], u[2]):
                i.add_clash(j)
                j.add_clash(i)
                print(i, j)


if __name__ == "__main__":
    sessions = {
        "T01": [0, "8:00am", "9:00am"],
        "T02": [0, "9:00am", "10:00am"],
        "T03": [1, "9:00am", "10:00am"],
        "T04": [1, "10:00am", "11:00am"]
    }

    people = {
        "Alice": {0: [["8:00am", 1], ["9:00am", 1], ["10:00am", 1]], 1: [["8:00am", 0], ["9:00am", 0], ["10:00am", 0]]},
        "Bob": {0: [["8:00am", 0], ["9:00am", 0], ["10:00am", 0]], 1: [["8:00am", 1], ["9:00am", 1], ["10:00am", 1]]},
        "Charlie": {0: [["8:00am", 1], ["9:00am", 0], ["10:00am", 1]], 1: [["8:00am", 0], ["9:00am", 1], ["10:00am", 0]]},
        "Emily": {0: [["8:00am", 1], ["9:00am", 0], ["10:00am", 0]], 1: [["8:00am", 1], ["9:00am", 1], ["10:00am", 0]]}
    }

    pprint(run(people, sessions))