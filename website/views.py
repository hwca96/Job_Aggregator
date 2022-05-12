from flask import Blueprint, redirect, render_template, request, url_for

views = Blueprint("views", __name__)

@views.route('/', methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        search_words = request.form["search_words"]
        return redirect(url_for(".results", search = search_words))
    else:
        return render_template("home.html")

@views.route('/results', methods = ["POST", "GET"])
def results():
    search = request.args['search']
    return render_template("results.html", search = search)

@views.route('/login', methods = ["POST", "GET"])
def login():
    return render_template("login.html")