"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort
from app.forms import RegisterForm, LoginForm, AppendForm
from app.models import User, Data
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash
import time
import random, string
from datetime import datetime, timedelta
from functools import wraps

admins = ['dogsuned']

@app.context_processor
def inject_user():
    return dict(user=current_user)

def logo_info(info):
    flash(info, category="info")

def logo_error(error):
    flash(error, category="error")

def generate_key():
    tmp = random.sample(string.ascii_letters + string.digits, 8)
    key = ''.join(tmp)
    return key

def get_date():
    return time.strftime("%Y-%m-%d", time.localtime(time.time()))

def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):  # 让某个函数来继承我们的参数
        if current_user.name not in admins:
            abort(404)
        return f(*args, **kwargs)

    return decorated_function

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        user = User.query.filter_by(name=name).first()

        if user == None:
            if name in admins:
                user = User(name = name, password = pwd, registered = 1, enable = 1, date = get_date(), authkey = generate_key())
                db.session.add(user)
                db.session.commit()
            else:
                logo_info('账号未注册，请联系管理员')
        else:
            if user.registered == 0:
                return redirect(url_for('register'))

            if user.enable == 0:
                logo_info('登陆失败, 请联系管理员')
            else:
                if (str(user.password) == pwd):
                    session.permanent = True
                    app.permanent_session_lifetime = timedelta(hours = 1)
                # if user and user.check_password_hash(pwd):
                    login_user(user)
                    if user.name in admins:
                        return redirect(url_for('home'))
                    else:
                        return redirect(url_for('details', name = user.name))
                else:
                    logo_info("密码错误")
    return render_template('login.html', title='用户登录', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        authkey = form.authkey.data
        pwd = form.pwd.data

        user = User.query.filter_by(name=username).first()
        if user == None:
            logo_info('暂无权限，请联系管理员')
        else:
            if authkey == user.authkey:
                user.password = pwd
                user.date = get_date()
                user.registered = 1
                db.session.commit()
                logo_info('注册成功，请登录')
                return redirect(url_for('login'))
            else:
                logo_info('注册口令无效')

    if form.pwd.errors:
        logo_info(form.pwd.errors[0])
    if form.confirm.errors:
        logo_info(form.confirm.errors[0])
    if form.username.errors:
        logo_info(form.username.errors[0])

    return render_template('register.html', title='用户注册', form=form)

@app.route('/')
@login_required
@admin_auth
def home():
    return render_template('home.html', title = "主页")


@app.route('/about/')
@login_required
def about():
    """Render the website's about page."""
    return render_template('about.html', title = "关于", name="Dogsuned")

@app.route('/AllUsers')
@login_required
@admin_auth
def AllUsers():
    label = ('序号', '姓名', '注册口令', '状态', '用户控制', '注册日期')
    users = db.session.query(User).all() # or you could have used User.query.all()

    return render_template('view.html', title = "用户信息", label = label, users=users)

@app.route('/AddUser', methods=['POST', 'GET'])
@login_required
@admin_auth
def AddUser():
    user_form = AppendForm()

    if request.method == 'POST':
        if user_form.validate_on_submit():
            # Get validated data from form
            name = user_form.username.data # You could also have used request.form['name']

            if user_form.already_exsist(name):
                flash('user %s already exist' % name)
                return redirect(url_for('AddUser'))

            # save user to database
            user = User(name = name, authkey = generate_key(), enable = 1, password = generate_key(), date = get_date(), registered = 0)
            db.session.add(user)
            db.session.commit()

            flash('User %s successfully added' % name)
            return redirect(url_for('AllUsers'))

    flash_errors(user_form)
    return render_template('append.html', title = "添加用户", form=user_form)


@app.route('/DelUser/<name>')
@login_required
@admin_auth
def DeleteUser(name):
    user = User.query.filter_by(name=name).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('user %s delete success' % name)
    return redirect(url_for('AllUsers'))


@app.route('/UserEnable/<name>')
@login_required
@admin_auth
def UserEnable(name):
    user = User.query.filter_by(name=name).first()
    if user:
        user.enable = 1
        db.session.commit()
        flash('用户 [ %s ] 已启用' % name)
    else:
        flash('操作失败')
    return redirect(url_for('AllUsers'))

@app.route('/UserDisable/<name>')
@login_required
@admin_auth
def UserDisable(name):
    user = User.query.filter_by(name=name).first()

    if user:
        user.enable = 0
        db.session.commit()
        flash('用户 [ %s ] 已禁用' % name)
    else:
        flash('操作失败')
    return redirect(url_for('AllUsers'))

@app.route('/details/<name>')
@login_required
def details(name):
    return render_template('details.html', title = "个人薪资", name=name)


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
    return render_template('404.html', title = "lost"), 404


if __name__ == '__main__':
    app.run(debug=True)
