from flask import Flask, render_template, jsonify, request, abort

from api.user import User

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api/user', methods=['GET'])
def view_users():
    return jsonify([user.json() for user in User.list_users()])


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


@app.route('/api/user/<user>/courses', methods=['GET'])
def view_user_courses(user):
    try:
        user = User(user)
    except KeyError:
        abort(404)
    return jsonify([course.json() for course in user.get_courses()])


if __name__ == '__main__':
    app.run(debug=True, port=2468)
