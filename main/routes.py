from flask import render_template, url_for, session, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask import current_app as app
from flask import session, Markup, flash
from main.database import db, User, Product, Order
from main.helpers import apology, allowed_file, modal
import os

# Beginning of application
@app.route("/")
def index():

    modaltext = modal()

    listofproducts = Product.query.all()

    sell_id = 1
    listofproducts = Product.query.filter_by(sell_id = sell_id).all()
    # Filter by item name; currently hardcoded. Should be retrieved from a list elsewhere.
    title = ["Guardians of the Galaxy", "Taste o' Goodness", "Galaxy Cake", "Yin & Yang"]
    path = []
    name = ["stageimg", "noshow", "noshow", "noshow"]
    img_id =["stageimg", "noshow1", "noshow2", "noshow3"]
    tagid = ["image0", "image1", "image2", "image3"]
    tagname = ["textshow", "textnoshow", "textnoshow","textnoshow"]
    desc = []
    prodids = []

    # print("Check main index page buy button links. ")
    # print(app.config)
    # print(dir(app.config))
    # print(request.cookies)
# ''' sesison is deleted after timedelta, but remember token is still there, which is why is still logged in. '''

    for products in listofproducts:
        # print(products.prodName)
        if products.prodName in title:
            target = os.path.join(app.config['UPLOAD_FOLDER'], products.prodPath).replace("\\","/").strip(",")
            # print(target)
            path.append(target)
            desc.append(products.prodDesc)
            prodids.append(products.prodName.replace(" ", "-"))

    # print(prodids)
    # Landing page. For simplicity, I should just show the default home page.
    # print("user = {}, usertype = {}".format(session["user"], session["usertype"]))

    return render_template("index.html", prodid = prodids, modal = modaltext, title = title, path = path, name = name, img_id = img_id, tagid = tagid, tagname = tagname, desc = desc), 200


@app.route("/visits-counter/")
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # reading and updating session data
    else:
        session['visits'] = 1 # setting session data

    print(app.config['PERMANENT_SESSION_LIFETIME'])
    print(app.config['SESSION_PERMANENT'])

    return "Total visits: {}".format(session.get('visits'))
