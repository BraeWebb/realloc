from typing import Dict, List


class AlgorithmError(Exception):
    pass


class Person:
    def __init__(self, name: str):
        self._name = name

        self._priority = 1

        self._prefs = {}
        self._allocs = []

    def get_name(self) -> str:
        return self._name

    def set_priority(self, priority):
        self._priority = priority

    def get_priority(self):
        return self._priority

    def set_prefs(self, prefs: Dict['Session', int]):
        self._prefs = prefs

    def set_pref(self, session, pref):
        self._prefs[session] = pref

    def get_pref(self, session: 'Session') -> int:
        return self._prefs[session]

    def set_allocs(self, allocs: List['Session']):
        self._allocs = allocs

    def get_allocs(self) -> List['Session']:
        return self._allocs

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"Person({str(self)})"

    def __hash__(self):
        return hash(self._name)


class Session:
    def __init__(self, id_: str):
        self._id = id_
        self._slots = 1

        self._clashes = []

    def get_id(self):
        return self._id

    def set_slots(self, slots):
        self._slots = slots

    def get_slots(self):
        return self._slots

    def set_clashes(self, clashes: List['Session']):
        self._clashes = clashes

    def get_clashes(self) -> List['Session']:
        return self._clashes

    def add_clash(self, clash):
        self._clashes.append(clash)

    def copy(self):
        copy = SessionCopy(self)
        self.add_clash(copy)
        return copy

    def __str__(self):
        return self._id

    def __repr__(self):
        return f"Session({str(self)})"


class SessionCopy(Session):
    def __init__(self, parent):
        super().__init__(parent.get_id())
        self._parent = parent
        self.set_clashes(list(parent.get_clashes()))
        self.add_clash(parent)

    def get_parent(self):
        return self._parent

    def __repr__(self):
        return f"SessionCopy({str(self)})"