from flask import Blueprint, render_template, url_for, request, redirect
from flask_login import login_user, logout_user, login_required
from flask_restful import Api
from todomaster.services import User

auth = Blueprint('auth', __name__)
api = Api(auth)


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    if User.get_user(email):
        return redirect(url_for('auth.signup'))

    try:
        user = User.create_user(email=email, name=name, password=password)
    except Exception:
        return redirect(url_for('auth.signup'))
    return redirect(url_for('auth.login'))


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    check_user = User.check_in(email, password)
    if check_user is None:
        login_user(User.get_user(email), remember=remember)
        return redirect(url_for('main.profile'))
    else:
        return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



