#!/usr/bin/env python3
"""
Get locale from request
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Config Class"""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Determines the best match with our supported languages.
    This function uses Flask's request object to access the client's preferred
    languages and the app's supported languages (defined in the Config class)
    to determine the best match. The best match is then returned as the locale.

    Returns:
        str: The locale code for the best match (e.g. "en", "fr").
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    The index function displays the home page of the web application.
    Returns:
        str: contents of the home page.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
