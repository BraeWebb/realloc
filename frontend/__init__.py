from flask import Flask, render_template, jsonify, request, abort, url_for, redirect
from flask_login import LoginManager, login_required, login_user, logout_user
from backend.backend_run import run

from api.model import User, Session, Course

app = Flask(__name__)
app.secret_key = "Real Secure Totally Unbreakable Secret Key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        return User(user_id)
    except KeyError:
        return None


@app.route('/')
def index():
    login_user(User(0))
    return render_template("promo.html")


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route('/coordinator')
@login_required
def coordinator():
    return render_template("coordinator.html")


@app.route('/availability')
@login_required
def availability():
    return render_template("availability.html")


@app.route('/allocations')
def allocations():
    return render_template("allocations.html", tutors=[{"email": "fred@fred.com", "allocation": "T02, T03"}])


@app.route('/times')
@login_required
def times():
    return render_template("times.html")


@app.route('/signup')
def signup():
    next_url = request.args.get('next')
    return render_template('signup.html', next=next_url)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.unauthorized_handler
def unauthorized_handle():
    return render_template('unauthorized.html')


@app.route('/api/execute', methods=['POST'])
def execute_algorithm():
    users = request.form.get('users').split("\n")
    #pull users from DB

    classes = request.form.get('classes')  # {session name: [day, start, end]}


@app.route('/api/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.login(email, password)

    if user is None:
        return "Error occurred logging in"

    login_user(user)
    next_url = request.form.get('next')

    return redirect(next_url or url_for('index'))


@app.route('/api/signup', methods=['POST'])
def signup_api():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.create(email, password, 0)

    if user is None:
        return "Error occurred signing up"

    login_user(user)
    next_url = request.form.get('next')

    return redirect(next_url or url_for('index'))


@app.route('/api/user', methods=['GET'])
def view_users():
    return jsonify([user.json() for user in User.list_users()])


@app.route('/api/user', methods=['POST'])
def create_user():
    user = User.create(request.form.get('email'), request.form.get('password'),
                       request.form.get('permissions'))
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
    return jsonify(user.get_availability())


@app.route('/api/user/<user>/availability', methods=['POST'])
def add_availability(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    user.add_availability(request.form.get("day"), request.form.get("start"),
                          request.form.get("type"))
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
    return jsonify(course.get_allocation(revision))


@app.route('/api/course', methods=['POST'])
def create_course():
    course = Course.create(request.form.get('name'))
    return jsonify(**course.json()), 201


@app.route('/api/session', methods=['POST'])
def create_session():
    session = Session.create(request.form.get('course'), request.form.get('start'), request.form.get('end'),
                             request.form.get('day'), request.form.get('location'))
    return jsonify(**session.json()), 201


@app.route('api/user/<user>/availability', methods=['DELETE'])
def remove_availability(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    user.remove_availability()
    return jsonify(**user.json())


if __name__ == '__main__':
    app.run(debug=True, port=5433)
