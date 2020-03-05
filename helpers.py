import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", message = escape(message)), code

def allowed_file(filename):
    allowed_extensions = {'png', 'jpeg', 'jpg'}
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions


def modal():
    with open("static/modal.txt", "r") as file:
        modal1 = file.read().split("/n")
    modal1 = [i.strip("/n") for i in modal1]

    return modal1
