from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    authkey = db.Column(db.String(16))
    registered = db.Column(db.Integer)
    enable = db.Column(db.Integer)
    date = db.Column(db.String(32))
    data = db.relationship('Data', backref = 'user')

    def generate_password_hash(self, pwd):
        self.pwd = pwd
        # self.pwd = generate_password_hash(pwd)

    def check_password_hash(self, pwd):
        if self.password == pwd:
            return True
        else:
            return False
        # return check_password_hash(self.pwd, pwd)

    def __repr__(self):
        return '<name %s password %s id %d>' % (self.name, self.password, self.id)

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    wage = db.Column(db.String(2048))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, year, month, wage):
        self.year = year
        self.month = month
        self.wage = wage

    def __repr__(self):
        return '<id %d year %d month %d wage %s user_id %d>' % (self.id, self.year, self.month, self.wage, self.user_id)
