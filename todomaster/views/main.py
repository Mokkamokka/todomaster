from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_restful import Api, reqparse, abort, fields, marshal_with
from flask_login import login_required, current_user
from todomaster.models import Todo
from todomaster.models import UserModel
from todomaster import db

main = Blueprint('main', __name__)
api = Api(main)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/all')
@login_required
def user_todolist():
    page = request.args.get('page', 1, type=int)
    user = UserModel.query.filter_by(email=current_user.email).first_or_404()
    todos = Todo.query.filter_by(user_id=user.id).paginate(page=page, per_page=3)
    return render_template('all_todos.html', todos=todos, user=user)


@main.route('/new')
@login_required
def new_todolist():
    return render_template('create_todolist.html')


@main.route('/new', methods=['POST'])
@login_required
def new_todolist_post():
    theme = request.form.get('theme')
    summary = request.form.get('summary')

    todo = Todo(theme=theme, summary=summary, user_id=current_user.id)
    db.session.add(todo)
    db.session.commit()

    flash('Your todolist has been added!')
    return redirect(url_for('main.user_todolist'))


@main.route('/todo/<int:todo_id>/update', methods=['GET', 'POST'])
@login_required
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.theme = request.form['theme']
        todo.summary = request.form['summary']
        db.session.commit()
        flash('Your todo has been updated!')
        return redirect(url_for('main.user_todolist'))
    return render_template('update_todo.html', todo=todo)


@main.route('/todo/<int:todo_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_todolist(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    flash('Your todolist has been deleted!')
    return redirect(url_for('main.user_todolist'))

