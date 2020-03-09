from flask import render_template, url_for, session, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask import current_app as app
from flask import session, Markup, flash
from database import db, User, Product, Order
from helpers import apology, allowed_file, modal
import os

# Beginning of application
@app.route("/")
def index():

    modaltext = modal()

    listofproducts = Product.query.all()
    # for prod in listofproducts:
    #     print(prod.prodName)
    #     print(prod.prodid)
    #     print(prod.prodPath)

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
        target = os.path.join(app.config['UPLOAD_FOLDER'], products.prodPath).replace("\\","/").strip(",")
        path.append(target)
        desc.append(products.prodDesc)
        prodids.append(products.prodName.replace(" ", "-"))
        title.append(products.prodName)

    print(path)
    # print(prodids)
    # Landing page. For simplicity, I should just show the default home page.
    # print("user = {}, usertype = {}".format(session["user"], session["usertype"]))

    return render_template("index.html", prodid = prodids, modal = modaltext, title = title, path = path, name = name, img_id = img_id, tagid = tagid, tagname = tagname, desc = desc), 200
