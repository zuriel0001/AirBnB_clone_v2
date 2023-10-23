#!/usr/bin/python3
"""
    Starts a Flask web application that listens on 0.0.0.0, port 5000.
    Routes:
        /hbnb: HBnB home page.
"""
from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    """ Displays 'Hello HBNB!' """
    return "Hello HBNB!"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Displays 'C' followed by whats in <text>." """
    return 'c {}'.format(text.replace("_", " "))


@app.route('/python', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text):
    """ def doc """
    return 'Python {}'.format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ /number/<n>: display “n is a number” only if n is an integer """
    return '{} is a number'.format(n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """
        Displays an HTML page if only <n> is an integer
        States whether <n> is odd or even in the body
    """
    if n % 2 == 0:
        p = 'even'
    else:
        p = 'odd'
    return render_template('6-number_odd_or_even.html', number=n, parity=p)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """ Diplay states in database"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close(error):
    """ close all running services"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
        Displays HTML page with list of all states and related cities.

        The states and cities are sorted by name.
    """
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """ Route function for /states and /states/<id> """
    not_found = False
    if id is not None:
        states = storage.all(State, id)
        with_id = True
        if len(states) == 0:
            not_found = True
    else:
        states = storage.all(State)
        with_id = False
    return render_template('9-states.html', states=states,
                           with_id=with_id, not_found=not_found)


@app.route('/hbnb', strict_slashes=False)
def hbnb2():
    """ Route function for /states and /states/<id>
        Displays the main HBnB filters HTML page
    """
    amenities = storage.all(Amenity)
    states = storage.all(State)
    return render_template('100-hbnb.html', states=states, amenities=amenities)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
