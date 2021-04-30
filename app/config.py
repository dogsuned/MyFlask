SQLALCHEMY_DATABASE_URI = 'sqlite:///usermanage.db'

SQLALCHEMY_BINDS = {
    'users': 'sqlite:///users.db',
    'appmeta': 'sqlite:///appmeta.db'
}
