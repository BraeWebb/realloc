import csv
from os import path


def read_timetable_sheet(file_name):
    """
    :param file_name:
    :return:
    """
    if path.splitext(file_name)[1] != ".csv":
        # Temporary
        raise Exception("File must be a .csv")
    sessions = []
    with open(file_name, newline='') as f:
        sheet_reader = csv.reader(f, delimiter=',', quotechar='|')
        for i, row in enumerate(sheet_reader):
            if i == 0:
                continue
            sessions.append(create_session(row))
    return sessions


def add_sessions(sessions):
    pass


def create_session(row):
    """
    Creates Session instance using given CSV row.

    :param row: Session data
    :type row: list<str>
    :return: Session instance representation of CSV data
    """
    sid = row[0]
    day = row[1]
    start_time = row[2]
    end_time = row[3]
    return Session(sid, day, start_time, end_time)


class Session:

    def __init__(self, sid, day, start_time, end_time):
        self.sid = sid
        self.day = day
        self.start_time = start_time
        self.end_time = end_time


if __name__ == "__main__":
    pass
