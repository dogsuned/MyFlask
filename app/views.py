"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import UserForm, LoginForm
from app.models import User, Data
from flask_login import LoginManager, login_required
from werkzeug.security import generate_password_hash
import time

# login_manager = LoginManager()

# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
# login_manager.login_message = 'Access denied.'

# login_manager.init_app(app)

def get_all_users():
    return db.session.query(User).all()

def get_user_wage(name):
    users = get_all_users()
    # for user in users:
    #     if (user.name == name):
    #         return Content.query.filter(Content.user_id == user.uuid).all()
    #         # return db.session.query(Content).filter(Content.user_id == user.uuid).all()
    return None

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')

        print(type(password))
        print('name: %s password: %s' % (name, password))
        users = get_all_users()
        # print(users)
        for user in users:
            print(type(user.password))
            if (user.name == name):
                return redirect(url_for('show_users'))
                # print('+++++++++++++++++')
                # if (user.password == password):
                #     print("----------------")
                #     # login_user(curr_user)
                # else:
                #     print('密码错误')
                #     return redirect(url_for('login'))

        print('账号未注册')
        # return redirect(url_for('register'))
        # return redirect(url_for('login'))
    print('Wrong username or password!')
    return render_template('login.html')

# @app.route('/logout')
# # @login_required
# def logout():
#     logout_user()
#     return 'Logged out successfully!'

# @app.route('/test/<name>')
# def test(name):
#     return 'test %s' % name

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Dogsuned")

@app.route('/test/<name>')
def test(name):
    return "%s" % name

@app.route('/users')
def show_users():
    label = ('姓名', '密码')
    users = db.session.query(User).all() # or you could have used User.query.all()

    return render_template('show_users.html', label = label, users=users)

@app.route('/add-user', methods=['POST', 'GET'])
def add_user():
    user_form = LoginForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.name.data # You could also have used request.form['name']
            password = user_form.password.data # You could also have used request.form['email']

            users = db.session.query(User).all()
            for user in users:
                if user.name == name:
                    flash('user %s already exist' % name)
                    return redirect(url_for('add_user'))

            # save user to database
            user = User(name, password)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)

@app.route('/deluser/<name>')
def del_user(name):
    print('------------->')
    print(name)
    users = db.session.query(User).all()
    for user in users:
        print(user)
        if user.name.strip() == name.strip():
            print("delete--------- %s" % name)
            db.session.delete(user)
            db.session.commit()
            # flash('user %s delete success' % name)
    time.sleep(3)
    return redirect(url_for('show_users'))

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))

###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
