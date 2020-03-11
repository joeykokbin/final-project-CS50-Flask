from flask import render_template, url_for, session, request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from flask import current_app as app
from flask_login import current_user
from flask import session, Markup, flash
from database import db, User, Product, Order
from datetime import date, datetime
from helpers import apology, allowed_file, modal
import os

@app.route("/add_pics", methods = ["GET", "POST"])
def onetime():

    product1 = Product(sell_id = 1, prodName = "Tiramisu Heaven", prodDesc = "Had a taste of this and I am already in heaven. You can be in heaven too, unless you have tattoos, or are short, or drink alcohol. /joke", prodPrice = 59.90, prodPath ="seller1product1img1.jpg,seller1product1img2.jpg,seller1product1img3.jpg", listdate = date.today())
    product2 = Product(sell_id = 1, prodName = "CNY 2020 Mahjong Cake", prodDesc = "Have you struck lottery before? If no, this is the chance for your beloved friends or family to savour that moment where they pull out money and you end up paying for it.", prodPrice = 30.00, prodPath ="seller1product2img1.jpg,seller1product1img2.jpg", listdate = date.today())
    product3 = Product(sell_id = 1, prodName = "Oriental Cheongsam Prosperity", prodDesc = "Get dressed for the occasion with this elegantly tailored cheongsam longevity cake! Featuring handmade oriental buttons, cherry blossoms, a gold acrylic topper and fondant peaches, this celebratory cake will certainly be the best dressed at the cny party!", prodPrice = 45.00, prodPath ="seller1product3img1.jpg,seller1product1img2.jpg,seller1product1img3.jpg", listdate = date.today())
    product4 = Product(sell_id = 1, prodName = "Chocolate Cherry Elegance", prodDesc = "Looking for something luxurious yet simple and elegant? This decadent chocolate-coated cake with gold painted cherries on top will be sure to be the star of your table!", prodPrice = 60.00, prodPath ="seller1product4img1.jpg,seller1product1img2.jpg", listdate = date.today())
    product5 = Product(sell_id = 1, prodName = "Harry Potter and the Golden Snitch", prodDesc = "HARRY! DID YA PUT YA NAM IN THE GOBELT OF FIYAH", prodPrice = 100.00, prodPath ="seller1product5img1.jpg", listdate = date.today())
    product6 = Product(sell_id = 1, prodName = "The Perfect Cream Cake", prodDesc = "Cream so creamy you'd think you're eating it from a cow.", prodPrice = 79.90, prodPath ="seller1product6img1.jpg", listdate = date.today())
    product7 = Product(sell_id = 1, prodName = "Cake de Rose", prodDesc = "Cake of rose. A perfect alternative for valentines day if you forgot to buy roses, despite every single friend of yours telling you to buy.", prodPrice = 109.90, prodPath ="seller1product7img1.jpg", listdate = date.today())
    product8 = Product(sell_id = 1, prodName = "Unicorn Cake", prodDesc = "Something so rare I bet you 99.90 you have not tried it before. Try it now. ", prodPrice = 99.90, prodPath ="seller1product8img1.jpg", listdate = date.today())
    product9 = Product(sell_id = 2, prodName = "The Perfect Cheese Cake", prodDesc = "No words can describe how this tastes. But numbers can. 10/10", prodPrice = 50.0, prodPath ="seller1product1img1.jpg", listdate = date.today())
    product10 = Product(sell_id = 2, prodName = "Yin and Yang", prodDesc = "Cheesecake, deliciously covered in butter flakes (left) and chocolate flakes (right). Each mouth is so so smooth, and the taste never leaves your mouth! Prices are for individual cakes.", prodPrice = 39.90, prodPath ="seller1product2img1.jpg", listdate = date.today())
    product11 = Product(sell_id = 2, prodName = "Test Cake", prodDesc = "This is a test cake. Buy at your own peril! (Seriously, buy it.)", prodPrice = 30.0, prodPath ="seller1product3img1.jpg", listdate = date.today())

    db.session.add(product1)
    db.session.add(product2)
    db.session.add(product3)
    db.session.add(product4)
    db.session.add(product5)
    db.session.add(product6)
    db.session.add(product7)
    db.session.add(product8)
    db.session.add(product9)
    db.session.add(product10)
    db.session.add(product11)
    db.session.commit()

    return "done"

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
