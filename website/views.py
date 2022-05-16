from flask import Blueprint, redirect, render_template, request, url_for, flash
import main_scraper

views = Blueprint("views", __name__)

@views.route('/', methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        search_words = request.form["search_words"]
        search_location = request.form["search_location"]
        return redirect(url_for(".results", search = search_words, location = search_location))
    else:
        return render_template("home.html")

@views.route('/results', methods = ["POST", "GET"])
def results():
    search = request.args['search']
    location = request.args['location']
    data = main_scraper.get_all_data(search, location)
    return render_template("results.html", data = data)

@views.route('/login', methods = ["POST", "GET"])
def login():
    return render_template("login.html")

@views.route('/signup', methods = ["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if "@" not in email and ".com" not in email:
            flash("Invalid Email", category='error')
        elif password1 != password2:
            flash("Passwords do not match!", category='error')
        elif len(password1) < 7:
            flash("Passwords must be at least 6 characters.", category='error')
        elif len(firstName) < 2:
            flash("First name must be longer than 1 character", category="error")
        else:
            flash("Account Created!!!", category="success")
    return render_template("signup.html")