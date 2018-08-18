from datetime import datetime
import uuid

from api.database import Database


class Session:
    def __init__(self, id, course):
        self.id = id
        self.course = course
        self.start = datetime.now()
        self.end = datetime.now()
        self.day = datetime.now()
        self.location = "SAD"
        with Database() as db:
            if db.exists("session", id=self.id):
                sql = 'SELECT start, "end", "day", location FROM "session" WHERE id = %s AND course_id = %s'
                self.start, self.end, self.day, self.location = db.query(sql, self.id, self.course, limit=1)[0]
            else:
                raise KeyError('Session Time {} not found'.format(self.id))

    @classmethod
    def create(cls, course, start, end, day, location):
        with Database() as db:
            id = uuid.uuid4()
            sql = 'INSERT INTO "session" (id, course, start, "end", "day", location) VALUES (%s, %s, %s, %s, %s, %s)'

            db.query(sql, id, course, start, end, day, location)

        return Session(id, course)
