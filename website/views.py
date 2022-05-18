from flask import Blueprint, redirect, render_template, request, url_for, flash
import main_scraper
from website.models import SavedJob, User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint("views", __name__)

@views.route('/', methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        search_words = request.form["search_words"]
        search_location = request.form["search_location"]
        return redirect(url_for(".results", search = search_words, location = search_location))
    else:
        return render_template("home.html", user=current_user)

@views.route('/results', methods = ["POST", "GET"])
def results():
    search = request.args['search']
    location = request.args['location']
    data = main_scraper.get_all_data(search, location)
    # Part of implementation of saving jobs from the list of results
    # if request.method == 'POST':
    #     saved_job = request.form['card']['card-body']
    #     print(saved_job)
    #     # new_saved = SavedJob(title=saved_job, user_id=current_user.id)
    #     # db.session.add(new_saved)
    #     # db.session.commit()
    #     # flash("Job Saved", category='success')
    return render_template("results.html", data = data, user=current_user)

@views.route('/login', methods = ["POST", "GET"])
def login():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@views.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist.', category='error')
        elif "@" not in email and ".com" not in email:
            flash("Invalid Email", category='error')
        elif password1 != password2:
            flash("Passwords do not match!", category='error')
        elif len(password1) < 7:
            flash("Passwords must be at least 6 characters.", category='error')
        elif len(first_name) < 2:
            flash("First name must be longer than 1 character", category="error")
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account Created and Logged In!!!", category="success")
            return redirect(url_for('.home'))
    return render_template("signup.html", user=current_user)

@views.route('/logout', methods = ["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash("Logged Out.", category="success")
    return redirect(url_for('.login'))

@views.route('/saved', methods = ["POST", "GET"])
@login_required
def saved():
    return render_template('saved.html', user=current_user)