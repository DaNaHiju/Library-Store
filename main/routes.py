from flask import Flask, request, render_template, Blueprint

main = Blueprint('main', __name__)


@main.route("/", methods=["GET"])
def home():
    return render_template("pages/home.html")


