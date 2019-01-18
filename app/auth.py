from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from app import database
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for
from flask_login import login_required
from flask import session


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=25)])


@app.route('/login', methods=['GET', 'POST'])
def login_check():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = authorization_func(username, password)
        if user:
            login_user(user, remember=False)
            session['status'] = 'login'
            return redirect(url_for('index'))
        prompt = 'Invalid username or password'
        return redirect(url_for('login_check'))
    return render_template('login.html', form=form)


def authorization_func(username, password):
    user = database.UserList.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        user = database.UserList.query.filter_by(username=username).first()
        email_exist = database.UserList.query.filter_by(email=email).first()
        if user is None and email_exist is None:
            password = generate_password_hash(password, method='sha256')
            new_user = database.UserList(username=username, password=password, email=email)
            database.db.session.add(new_user)
            database.db.session.commit()
            return redirect(url_for('login_check'))
        else:
            prompt = ''
            if user:
                prompt = 'Invalid username - already existed. '
            if email_exist:
                prompt += 'Invalid email - already existed. Please signed in.'
            return render_template('signup.html', form=form, prompt=prompt)
    return render_template('signup.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    session['status'] = 'None'
    return redirect(url_for('index'))


@app.route('/login_index')
@login_required
def login_index():
    """ Index page. Return the template.

    :return: template, the template of index html when login.
    """
    return render_template('login_index.html')


@app.route('/')
def index():
    """ Index page. Return the template.

    :return: template, the template of index html.
    """
    if 'status' in session and session['status'] == 'login':
        return redirect(url_for('login_index'))
    return render_template('index.html')
