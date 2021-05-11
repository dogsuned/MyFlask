"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm
from app.models import User, Data
# from flask_login import login_required
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
import time

@app.context_processor
def inject_user():
    return dict(user=current_user)


@app.route('/')
@app.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('show_users.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        user = User.query.filter_by(name=name).first()
        # if user and user.check_password_hash(pwd):
        if user:
            login_user(user)
            flash('登陆成功。', category='info')
            return redirect(url_for('show_users'))
        else:
            flash("密码或账户错误。", category='error')
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('再见！')
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        pwd = form.pwd.data
        user = User(name=username, email=email)
        user.generate_password_hash(pwd)
        db.session.add(user)
        db.session.commit()
        flash('注册成功', category='info')
        return redirect(url_for('login'))
    return render_template('register.html', title='注册', form=form)


def get_all_users():
    return db.session.query(User).all()


def get_user_wage(name):
    users = get_all_users()
    # for user in users:
    #     if (user.name == name):
    #         return Content.query.filter(Content.user_id == user.uuid).all()
    #         # return db.session.query(Content).filter(Content.user_id == user.uuid).all()
    return None


@app.route('/home')
def home():
    return render_template('about.html')


@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Dogsuned")


@app.route('/test/<name>')
def test(name):
    return "%s" % name


@app.route('/users')
@login_required
def show_users():
    label = ('姓名', '密码')
    users = db.session.query(User).all() # or you could have used User.query.all()

    return render_template('show_users.html', label = label, users=users)


@app.route('/add-user', methods=['POST', 'GET'])
@login_required
def add_user():
    user_form = LoginForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.username.data # You could also have used request.form['name']
            password = user_form.password.data # You could also have used request.form['email']

            users = db.session.query(User).all()
            for user in users:
                if user.name == name:
                    flash('user %s already exist' % name)
                    return redirect(url_for('add_user'))

            # save user to database
            user = User(name = name, password = password)
            db.session.add(user)
            db.session.commit()

            flash('User successfully added')
            return redirect(url_for('show_users'))

    flash_errors(user_form)
    return render_template('add_user.html', form=user_form)


@app.route('/deluser/<name>')
@login_required
def del_user(name):
    users = db.session.query(User).all()
    for user in users:
        print(str(user.name))
        if str(user.name).strip() == name.strip():
            db.session.delete(user)
            db.session.commit()
            flash('user %s delete success' % name)
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
