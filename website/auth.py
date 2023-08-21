from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash#don't want to store the actual user's password
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()#find the user in our db
        if user:
            if check_password_hash(user.password, password):#confirm the correct password
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.overview'))#redirect to overview page
            else:
                flash('Incorrect password, try again.', category='error')#error message for incorrect password
        else:
            flash('Email does not exist.', category = 'error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()#logout the user
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')#get user information
        firstname = request.form.get('firstname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()#check if email exists already
        if user:
            flash('This email already has an account', category='error')
            redirect(url_for('views.overview'))
        elif len(email)<4:
            flash('enter valid email', category='error')
        elif len(firstname)<2:
            flash('enter valid name', category='error')
        elif password1!=password2:
            flash('passwords must be the same', category='error')
        else:
            #add user to database
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(password1, method='scrypt'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('account created!', category='success')
            return redirect(url_for('views.overview'))
        
    return render_template("sign_up.html", user=current_user)