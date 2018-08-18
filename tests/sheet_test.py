import unittest
from backend.sheets import read_timetable

FILE_NAME = "data\\timetable-template.csv"

class TestSheets(unittest.TestCase):
    def setup_method(self, test_method):
        pass

    def test_sheet_read(self):
        sessions = read_timetable(FILE_NAME, "COMP3506")
        print(sessions)


if __name__ == '__main__':
    unittest.main()
