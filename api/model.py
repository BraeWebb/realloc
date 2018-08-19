import uuid
import hashlib
from datetime import datetime

from api.database import Database


def convert_time(time):
    return "{}:{}".format(time.hour, time.minute)


class User:
    def __init__(self, id):
        self.id = id
        self.email = "test@example.com"
        self.permissions = 0
        with Database() as db:
            if db.exists("user", id=self.id):
                sql = 'SELECT "email", permission FROM "user" WHERE id = %s'
                self.email, self.permissions = db.query(sql, self.id, limit=1)[0]
            else:
                raise KeyError('User {} not found'.format(self.id))

        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    @classmethod
    def by_email(cls, email):
        with Database() as db:
            if db.exists("user", email=email):
                sql = 'SELECT id FROM "user" WHERE email = %s'
                id = db.query(sql, email)[0][0]
            else:
                raise KeyError('User {} not found'.format(email))

        return User(id)

    @classmethod
    def create(cls, email, password, permissions):
        with Database() as db:
            if db.exists("user", email=email):
                return None

            password = hashlib.sha224(bytes(password, "utf-8")).hexdigest()

            id = uuid.uuid4().int
            id = int(str(id)[:10])
            sql = 'INSERT INTO "user" (id, email, permission, password) VALUES (%s, %s, %s, %s)'

            db.query(sql, id, email, permissions, password)

        return User(id)

    @classmethod
    def login(cls, email, password):
        with Database() as db:
            password = hashlib.sha224(bytes(password, "utf-8")).hexdigest()
            sql = 'SELECT "id", password FROM "user" WHERE email = %s'

            user_id, db_password = db.query(sql, email)[0]
        if password == db_password:
            return User(user_id)
        return None


    def update(self, email, permissions):
        with Database() as db:
            sql = 'UPDATE "user" SET (email, permission) = (%s, %s) where id = %s'
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

    def get_id(self):
        return self.id

    def get_courses(self):
        with Database() as db:
            sql = 'SELECT course_id FROM course_association WHERE user_id = %s'
            result = db.query(sql, self.id)

            return [Course(row[0]) for row in result]

    def get_availability(self):
        with Database() as db:
            sql = 'SELECT "day", start, "type" FROM availability WHERE user_id = %s'
            result = db.query(sql, self.id)
            results = []
            for r in result:
                results.append([r[0], convert_time(r[1]), r[2]])

            return results

    def add_availability(self, day, start, type):
        with Database() as db:
            db.query('DELETE FROM "availability" WHERE user_id = %s', self.id)
            insert_query = 'INSERT INTO "availability" (user_id, "day", start, "type") VALUES (%s, %s, %s, %s)'
            db.query(insert_query, self.id, day, start, type)

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
                self.name = db.query(sql, self.id, limit=1)[0][0]
            else:
                raise KeyError('Course {} not found'.format(self.id))

    @classmethod
    def create(cls, name):
        with Database() as db:
            id = uuid.uuid4().int
            id = int(str(id)[:10])
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
            sql = 'SELECT id FROM "session" WHERE course_id = %s'
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
            id = uuid.uuid4().int
            id = int(str(id)[:10])
            sql = 'INSERT INTO "session" (id, course, start, "end", "day", location) VALUES (%s, %s, %s, %s, %s, %s)'

            db.query(sql, id, course, start, end, day, location)

        return Session(id, course)

    def json(self):
        return {"id": self.id, "course": self.course,
                "start": "{}:{}".format(self.start.hour, self.start.minute),
                "end": "{}:{}".format(self.start.hour, self.start.minute),
                "day": self.day, "location": self.location}


# TODO: Plz remove
class FakeUser(User):
    def __init__(self, id):
        self.id = id
        self.email = "test@example.com"
        self.permissions = 0
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False


User = FakeUser
