import uuid
from datetime import datetime

from api.database import Database


class User:
    def __init__(self, id):
        self.id = id
        self.email = "test@example.com"
        self.permissions = 0
        with Database() as db:
            if db.exists("user", id=self.id):
                sql = 'SELECT "email", permissions FROM "user" WHERE id = %s'
                self.email, self.permissions = db.query(sql, self.id, limit=1)[0]
            else:
                raise KeyError('User {} not found'.format(self.id))

    @classmethod
    def create(cls, email, permissions):
        with Database() as db:
            id = uuid.uuid4()
            sql = 'INSERT INTO "user" (id, email, permissions) VALUES (%s, %s, %s)'

            db.query(sql, id, email, permissions)

            return User(id)

    def update(self, email, permissions):
        with Database() as db:
            sql = 'UPDATE "user" SET (email, permissions) = (%s, %s) where id = %s'
            db.query(sql, email, permissions, self.id)

    @staticmethod
    def list_users():
        with Database() as db:
            sql = 'SELECT id FROM "user"'
            result = db.query(sql)

            return [User(row[0]) for row in result]

    def json(self):
        return {"id": self.id, "email": self.email,
                "permissions": self.permissions}

    def get_courses(self):
        with Database() as db:
            sql = 'SELECT course_id FROM course_association WHERE user_id = %s'
            result = db.query(sql, self.id)

            return [Course(row[0]) for row in result]

    def get_availability(self):
        with Database() as db:
            sql = 'SELECT "day", start, "end" FROM availability WHERE user_id = %s'
            result = db.query(sql, self.id)

            return result

    def add_availability(self, day, start, end):
        with Database() as db:
            sql = 'INSERT INTO "availability" (user_id, "day", start, "end") VALUES (%s, %s, %s, %s)'
            db.query(sql, self.id, day, start, end)

    def get_allocations(self, revision, course):
        with Database() as db:
            sql = 'SELECT "session_id" FROM allocation WHERE user_id = %s AND revision = %s AND course_id = %s'
            result = db.query(sql, self.id, revision, course)

            return [Session(row[0], course) for row in result]

class Course:
    def __init__(self, id):
        self.id = id
        self.name = "CSSE1001"
        with Database() as db:
            if db.exists("course", id=self.id):
                sql = 'SELECT "name" FROM "course" WHERE id = %s'
                self.name = db.query(sql, self.id, limit=1)[0]
            else:
                raise KeyError('Course {} not found'.format(self.id))

    @classmethod
    def create(cls, name):
        with Database() as db:
            id = uuid.uuid4()
            sql = 'INSERT INTO "course" (id, "name") VALUES (%s, %s)'

            db.query(sql, id, name)

        return Course(id)

    @staticmethod
    def list_courses():
        with Database() as db:
            sql = 'SELECT id FROM "course"'
            result = db.query(sql)

            return [Course(row[0]) for row in result]

    def json(self):
        return {"id": self.id, "name": self.name}

    def get_allocation(self, revision):
        with Database() as db:
            sql = 'SELECT "session_id", "user_id" FROM allocation WHERE revision = %s AND course_id = %s'
            result = db.query(sql, revision, self.id)

            return result

    def get_users(self):
        with Database() as db:
            sql = 'SELECT user_id FROM course_association WHERE course_id = %s'
            result = db.query(sql, self.id)

            return [User(row[0]) for row in result]

    def get_sessions(self):
        with Database() as db:
            sql = 'SELECT id FROM session WHERE course_id = %s'
            result = db.query(sql, self.id)

            return [Session(row[0]) for row in result]

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

    def json(self):
        return self.__dict__