from flask import render_template, flash, redirect, url_for, request

from flask_login import current_user, login_user, logout_user

from app import app, db
from app.models import User
from app.forms import LoginForm, RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        print(current_user.username)
        return render_template('index.html', title='Home', user={'username': current_user.username})
    user = {'username': ''}
    posts = [
        {
            'author': {'username': 'Anki'},
            'body': 'Beautiful day in Ahmedabad!'
        },
        {
            'author': {'username': 'Ankit'},
            'body': 'This is the Home Page!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print(current_user.username)
        return render_template('index.html', title='Home', user={'username': current_user.username})#redirect(url_for('index',user_name = ))

    form = LoginForm()
    print(form, '<---Form')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
        else:
            login_user(user, remember=form.remember_me.data)
            return render_template('index.html', title='Home', user={'username': current_user.username})#redirect(url_for('index',user_name = ))


    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)
