from flask import Flask, render_template, jsonify, request, abort

from api.model import User, Session, Course

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/user', methods=['GET'])
def view_users():
    # return jsonify([user.json() for user in User.list_users()])
    return jsonify([User(1).json()])


@app.route('/api/user', methods=['POST'])
def create_user():
    user = User.create(request.form.get('email'), request.form.get('permissions'))
    return jsonify(**user.json()), 201


@app.route('/api/user/<user>', methods=['GET'])
def view_user(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    return jsonify(**user.json())


@app.route('/api/user/<user>', methods=['PUT'])
def update_user(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    user.update(request.form.get('email'), request.form.get('permissions'))
    return jsonify(**user.json())


@app.route('/api/user/<user>/availability', methods=['GET'])
def view_availability(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    return jsonify(**user.get_availability())


@app.route('/api/user/<user>/availability', methods=['POST'])
def add_availability(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    user.add_availability(request.form.get("day"), request.form.get("start"),
                          request.form.get("end"))
    return jsonify(**user.json())


@app.route('/api/user/<user>/courses', methods=['GET'])
def view_user_courses(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    return jsonify([course.json() for course in user.get_courses()])


@app.route('/api/course', methods=['GET'])
def view_courses():
    return jsonify([course.json() for course in Course.list_courses()])


@app.route('/api/course/<course>', methods=['GET'])
def view_course(course):
    try:
        course = Course(course)
    except KeyError:
        abort(404)
    return jsonify(**course.json())


@app.route('/api/course/<course>/users', methods=['GET'])
def view_course_users(course):
    try:
        course = Course(course)
    except KeyError:
        abort(404)
    return jsonify([user.json() for user in course.get_users()])


def view_course_sessions(course):
    try:
        course = Course(course)
    except KeyError:
        abort(404)
    return jsonify([session.json() for session in course.get_sessions()])


@app.route('/api/user/<course>/allocation/<revision>', methods=['GET'])
def view_allocation(course, revision):
    try:
        course = Course(course)
    except KeyError:
        abort(404)
    return jsonify(**course.get_allocation(revision))


@app.route('/api/course', methods=['POST'])
def create_course():
    course = Course.create(request.form.get('name'))
    return jsonify(**course.json()), 201


@app.route('/api/session', methods=['POST'])
def create_session():
    session = Session.create(request.form.get('course'), request.form.get('start'), request.form.get('end'),
                             request.form.get('day'), request.form.get('location'))
    return jsonify(**session.json()), 201


if __name__ == '__main__':
    app.run(debug=True, port=5432)
