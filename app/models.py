from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    data = db.relationship('Data', backref = 'user')

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<name %s password %s id %d>' % (self.name, self.password, self.id)

class Data(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    wage = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, year, month, wage):
        self.year = year
        self.month = month
        self.wage = wage

    def __repr__(self):
        return '<id %d year %d month %d wage %s user_id %d>' % (self.id, self.year, self.month, self.wage, self.user_id)
