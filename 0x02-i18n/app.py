#!/usr/bin/env python3
"""Module for task 8
"""
from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
import pytz

app = Flask(__name__)

app.url_map.strict_slashes = False


class Config:
    """Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@app.route("/")
def index() -> str:
    """The index function displays the home page of the web application.

    It retrieves the current time based on the inferred time zone using the
    format_datetime() function.
    The time is stored in flask.g.time for use in the index.html template.

    Returns:
        str: contents of the home page.
    """
    g.time = format_datetime()
    return render_template("index.html")


@babel.localeselector
def get_locale() -> str:
    """"Returns the preferred locale for the user.

    The order of priority is:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request header
    4. Default locale

    Returns:
        str: The preferred locale.
    """
    # Get the locale parameter from the incoming request
    locale = request.args.get('locale')
    # Get list of supported languages from Config
    supported_languages = app.config["LANGUAGES"]
    if locale and locale in supported_languages:
        # If the locale parameter is present and is a supported locale,
        # return it
        return locale
    # Locale from user settings
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user() -> Union[Dict, None]:
    """Returns a user dictionary based on the given ID

    Returns:
        Union[Dict, None]: The user dictionary if found, otherwise None.
    """
    # Get the user_id from the login_as URL parameters
    login_id = request.args.get('login_as')
    # If the user ID exists in the URL parameters
    if login_id:
        # Get the user dictionary from the `users` dictionary using the user ID
        return users.get(int(login_id))
    # If the user ID does not exist in the URL parameters, return None
    return None


@app.before_request
def before_request() -> None:
    """Function to be executed before every request.
    """
    # Use the get_user function to get the user details
    user = get_user()
    # Set the user as a global variable on flask.g
    g.user = user


# Use the timezoneselector decorator to set the get_timezone function as the
# timezone selector
@babel.timezoneselector
def get_timezone() -> str:
    """Return the user's preferred timezone.

    Returns:
        str: The user's preferred timezone.
    """
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


# Register the before_request function to be executed before every request
app.before_request(before_request)


if __name__ == "__main__":
    app.run(debug=True)
