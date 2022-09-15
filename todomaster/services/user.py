from werkzeug.security import generate_password_hash, check_password_hash
from todomaster.models import UserModel
from todomaster import db
from sqlalchemy import exc


class User:
    def get_logid(user_id):
        return UserModel.query.get(int(user_id))

    def get_user(email):
        return UserModel.query.filter_by(email=email).first()

    def create_user(email, name, password):
        try:
            new_user = UserModel(email=email, name=name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            error = f"User with email {email} is already registered."
            db.session.rollback()
            raise Exception(error)
        return new_user

    def check_in(email, password):
        message = None
        user = User.get_user(email)
        if not user or not check_password_hash(user.password, password):
            message = f"The email or password is incorrect."
        return message
