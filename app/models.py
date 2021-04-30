from app import db

SQLALCHEMY_DATABASE_URI = 'sqlite:///usermanage.db'

SQLALCHEMY_BINDS = {
    'users': 'sqlite:///users.db',
    'appmeta': 'sqlite:///appmeta.db'
}

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    year = db.relationship("Years",backref = "users")

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

class Years(db.Model):
    __tablename__ = 'years'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(User.id))

    content = db.relationship("Content",backref = "years")

    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __repr__(self):
        return '<year %r>' % self.year

class Content(db.Model):
    __tablename__ = 'content'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, unique=True)
    data = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey(Years.id))

    def __init__(self, month, data):
        self.month = month
        self.data = data

    def __repr__(self):
        return '<month %r>' % self.month