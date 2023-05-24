#!/usr/bin/python3
"""Initiates a Flask web application.

The application is configured to listen on IP address 0.0.0.0 and port 5000.
Routes:
    /cities_by_states: HTML page with list of all states and related cities.
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """It showcases an HTML page that exhibits a comprehensive list of states 
    along with their associated cities.

    States/cities are sorted by name.
    """
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
