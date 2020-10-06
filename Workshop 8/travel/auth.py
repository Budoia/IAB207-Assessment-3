from flask import Blueprint, request, session, render_template
from .forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    error = None
    if loginForm.validate_on_submit():
        
        username = loginForm.username.data
        pad = loginForm.password.data

        u = User.query.filter_by(name=username).first()
        if u is None:
            error = 'Incorrect Username or Password'

        elif not check_password_hash(u.password_hash, pwd):
            error = 'Incorrect Username or Password'
        
        if error is None:
            login_user(u)
            return redirect(url_for('main.index'))
        
        else:
            flash(error, 'danger')

    return render_template('user.html', form=loginForm, heading='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    registrationForm = RegisterForm()
    if registerForm.validate_on_submit():
        
        username = RegisterForm.username.data
        email = registrationForm.email_id.data
        pwd = RegisterForm.password.data

        u = User.query.filter_by(name = username).first()
        if u:
            flasj('Username already exists. Please pick another', 'info')
            return redirect(url_for('auth.login'))
        
        pwd_hash = generate_password_hash(pwd)
        new_user = User(name = username, emailid = email,  password_has = pwd_hash)

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.index'))

        else:
            return render_template('user.html', form=registrationForm, heading='Register')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))