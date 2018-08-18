import uuid

from api.database import Database

#from api.user import User

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

    def json(self):
        return {"id": self.id, "name": self.name}

    def get_allocation(self, revision):
        with Database() as db:
            sql = 'SELECT "session_id", "user_id" FROM allocation WHERE revision = %s AND course_id = %s'
            result = db.query(sql, revision, self.id)

            return result
