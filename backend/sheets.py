import csv
from os import path
from api import database


def read_timetable(file_name, course_id):
    """
    Reads CSV file containing course timetable information and returns corresponding Session objects.

    :param file_name: CSV file to be read
    :return: Sessions parsed from CSV file
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
            sessions.append(create_session(row, course_id))
    return sessions


def add_sessions(sessions):
    """
    Add each of the given sessions to the database.

    :param sessions: Sessions to be added
    :return: None
    """
    with database.Database() as connection:
        for session in sessions:
            if connection.exists("session", course_id=session.course_id, session_id=session.session_id):
                continue
            connection.query("INSERT INTO SESSION", None)


def create_session(row, course_id):
    """
    Creates Session instance using given CSV row.

    :param row: Session data
    :type row: list<str>
    :return: Session instance representation of CSV data
    """
    return Session(course_id, row[0], row[1], row[2], row[3])


class Session:
    """
    Session data class.
    """

    def __init__(self, course_id, session_id, day, start_time, end_time):
        self.course_id = course_id
        self.session_id = session_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return "Session:course_id={}, session_id={}, day={}, start_time={}, end_time={}".format(self.course_id,
                                                                                                self.session_id,
                                                                                                self.day,
                                                                                                self.start_time,
                                                                                                self.end_time)


if __name__ == "__main__":
    pass
