import uuid

from api.database import Database

from api.course import Course
from api.session import Session


class User:
    def __init__(self, id):
        self.id = id
        self.email = "test@example.com"
        self.permissions = 0
        with Database() as db:
            if db.exists("user", id=self.id):
                sql = 'SELECT "email", permissions FROM "user" WHERE id = %s'
                self.date, self.payer, self.payee = db.query(sql, self.id, limit=1)[0]
            else:
                raise KeyError('User {} not found'.format(self.id))

    @classmethod
    def create(cls, email, permissions):
        with Database() as db:
            id = uuid.uuid4()
            sql = 'INSERT INTO "user" (id, email, permissions) VALUES (%s, %s, %s)'

            db.query(sql, id, email, permissions)

        return User(id)

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

    def get_allocations(self, revision, course):
        with Database() as db:
            sql = 'SELECT "session_id" FROM allocation WHERE user_id = %s AND revision = %s AND course_id = %s'
            result = db.query(sql, self.id, revision, course)

            return [Session(row[0], course) for row in result]
