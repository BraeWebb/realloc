from typing import List
from .structs import *
import random
import munkres
import sys


class Allocator:

    def __init__(self, people: List[Person], sessions: List[Session]):
        self._people = people
        self._orig_sessions = list(sessions)
        self._sessions = sessions

        self._matrix = None
        self._priority_list = None

    def run(self):
        self._preprocess()
        self._exec()
        self._postprocess()

    def _pre_resolve_clashes(self):
        checked = set()
        for session in self._sessions:
            if session not in checked:
                all_clashes = [session]
                for clash in session.get_clashes():
                    checked.add(clash)
                    all_clashes.append(clash)
                for person in self._people:
                    r = random.randint(0, len(all_clashes) - 1)
                    for i, clash in enumerate(all_clashes):
                        if i != r:
                            person.set_pref(clash, sys.maxsize)

    def _fill_slots(self):
        self._sessions = list(self._orig_sessions)
        for session in self._orig_sessions:
            for i in range(session.get_slots() - 1):
                copy = session.copy()
                for p in self._people:
                    p.set_pref(copy, p.get_pref(copy.get_parent()))
                self._sessions.append(copy)

    def _fill_people(self):
        while len(self._people) < len(self._sessions):
            for p in list(self._people):
                for i in range(p.get_priority()):
                    self._people.append(p)

    def _gen_matrix(self):
        self._matrix = []
        random.shuffle(self._people)
        for person in self._people:
            row = []
            for session in self._sessions:
                pref = person.get_pref(session)
                row.append(pref)
            self._matrix.append(row)

    def _preprocess(self):
        self._fill_slots()
        self._fill_people()
        self._pre_resolve_clashes()
        self._gen_matrix()

    def _exec(self):
        m = munkres.Munkres()
        indexes = m.compute(self._matrix)
        for row, col in indexes:
            person = self._people[row]
            session = self._sessions[col]
            if isinstance(session, SessionCopy):
                person.get_allocs().append(session.get_parent())
            else:
                person.get_allocs().append(session)

    def _check_ok(self):
        for person in self._people:
            for session in person.get_allocs():
                if person.get_pref(session) == sys.maxsize:
                    raise AlgorithmError("Invalid preference")

    def _postprocess(self):
        self._check_ok()
