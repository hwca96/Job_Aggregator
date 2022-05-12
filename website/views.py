from flask import Blueprint, redirect, render_template, request, url_for
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