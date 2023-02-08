#!/usr/bin/python3
"""Flask App """
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """render the states_list.html page and display the states created"""
    states = storage.all()
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown_db(exception):
    """teardown - remove current SQL session"""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
