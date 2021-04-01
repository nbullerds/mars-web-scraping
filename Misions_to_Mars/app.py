from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_phone

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/phone_app")


@app.route("/")
def index():

    return #


if __name__ == "__main__":
    app.run(debug=True)