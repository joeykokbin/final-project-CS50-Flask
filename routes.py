from flask import render_template, url_for, session, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask import current_app as app
from flask_login import current_user
from flask import session, Markup, flash
from database import db, User, Product, Order
from helpers import apology, allowed_file, modal
import os

@app.before_request
def before_request_func():

    if current_user.is_authenticated:
        print("user is logged in.")
        allsessions = User.query.filter_by(id = current_user.id).all()
        print(allsessions.username)
        print(allsessions.usertype)

    else:
        print("user is anonymous")


# Beginning of application
@app.route("/")
def index():

    modaltext = modal()

    sell_id = 1
    listofproducts = Product.query.filter_by(sell_id = sell_id).all()
    # Filter by item name; currently hardcoded. Should be retrieved from a list elsewhere.
    title = []
    path = []
    name = ["stageimg", "noshow", "noshow", "noshow"]
    img_id =["stageimg", "noshow1", "noshow2", "noshow3"]
    tagid = ["image0", "image1", "image2", "image3"]
    tagname = ["textshow", "textnoshow", "textnoshow","textnoshow"]
    desc = []
    prodids = []
    target = ""

    for products in listofproducts[0:4]:
        # print(products.prodName)
        prodpath = products.prodPath.split(",")[0]
        target = os.path.join(app.config['UPLOAD_FOLDER'], prodpath)
        path.append(target)
        desc.append(products.prodDesc)
        prodids.append(products.prodName.replace(" ", "-"))
        title.append(products.prodName)

    # print(path)
    # print(prodids)
    # Landing page. For simplicity, I should just show the default home page.
    # print("user = {}, usertype = {}".format(session["user"], session["usertype"]))

    return render_template("index.html", prodid = prodids, modal = modaltext, title = title, path = path, name = name, img_id = img_id, tagid = tagid, tagname = tagname, desc = desc), 200
