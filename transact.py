from flask import render_template, Blueprint, flash, jsonify, redirect, url_for, request, session, Markup
from flask_login import login_required, current_user
from flask import current_app as app
from database import db, User, Product, Order

from helpers import apology, allowed_file, modal
from werkzeug.utils import secure_filename
import os
from datetime import date, datetime
from sqlalchemy import inspect

# will house routes: buy and order history.
transact_bp = Blueprint('transact_bp', __name__)

@transact_bp.route("/browse", methods=["GET", "POST"])
def browse():
    """Browse cakes on sale"""

    modaltext = modal()
    listofproducts = Product.query.all()

    for i in range(len(listofproducts)):
        listofproducts[i].prodPath = listofproducts[i].prodPath.split(",")
        listofproducts[i].prodPrice = str(format(listofproducts[i].prodPrice, '.2f'))

    # db.session.rollback()
    return render_template("transact/browse.html", modal = modaltext, listofproducts = listofproducts, mycount = range(len(listofproducts)))

@transact_bp.route("/product/<product>", methods=["GET", "POST"])
def productlist(product):

    ''' this should be a pass-through function '''
    ''' pass the results of this function to another one'''
    ''' try it with a form'''
    modaltext = modal()

    #https://stackoverflow.com/questions/8398726/using-the-post-method-with-html-anchor-tags
    if request.method == "POST":
        path = request.form.get("name")
        sell_id = path[6]
        productnum = path[14]
        # print("Path is {}, Sell id is {}, productnum is {}".format(path, sell_id, productnum))

        # Default, by prod id, i.e. by time. since we have seller id, we can just use prod id
        targetproduct = Product.query.filter_by(sell_id = sell_id).all()
        finalproduct = targetproduct[int(productnum) - 1]
        # print(finalproduct.prodid)
        # print(finalproduct.prodPath)

        return render_template("transact/product.html", modal = modaltext, finalproduct = finalproduct), 200
    else:
        # From main page gallery
        prodname = request.args.get("prodid")

        # From main page gallery
        if prodname:
            # print(prodname)
            prodname = prodname.split("/")[-1].strip("?").replace("-"," ")
            # print(prodname)

        # From new posting, with no element id identifier
        else:
            prodname = request.url.split("/")[-1]
            prodname = prodname.replace("-"," ")

        finalproduct = Product.query.filter_by(prodName = prodname).first()
        # print(finalproduct)
        # print(request.method)
        # print(request.headers.get("Referer"))
        return render_template("transact/product.html", modal = modaltext, finalproduct = finalproduct), 200

@transact_bp.route("/post", methods = ["GET", "POST"])
@login_required
def post():

    modaltext = modal()
    # User submits a listing of cakes. Each listing should have 3 pictures of cakes to show, with specified sizes.
    if request.method == "POST":

        price = request.form.get("postprice")
        name = request.form.get("posttitle")
        description = request.form.get("postdescription")

        # Server side validation in case Javascript is disabled.
        if not price or not name or not description:
            flash("Incomplete form. Did you forget to key in the details?")
            return redirect(request.url)

        try:
            price = float(price)
        except:
            flash("Please input numbers and decimals only.")
            return redirect(request.url)

        # Check for uploaded files.
        if 'file' not in request.files:
            flash('No files found')
            return redirect(request.url)

        file1 = request.files.getlist('file')

        if file1[0].filename == '':
            flash("No selected file for 1st or 2nd image. Please check and submit again.")
            return redirect(request.url)

        sell_id = current_user.id
        prodpath = ''
        count = len(Product.query.filter_by(sell_id = sell_id).all()) + 1
        for i in range(len(file1)):
            if file1[i].filename == '':
                continue
            if allowed_file(file1[i].filename):
                filename = secure_filename(file1[i].filename)
                newfilename = "seller" + str(sell_id) + "product" + str(count) + "img" + str(i + 1) + "." + str(filename.split(".", 1)[1])
                file1[i].save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
                prodpath += newfilename
            else:
                flash("Please only upload pictures. Accepted formats are: .png, .jpeg, .jpg")
                return redirect(request.url)

            prodpath += ','

        newproduct = Product(sell_id = sell_id, prodName = name, prodDesc = description, prodPrice = price, prodPath = prodpath, listdate = date.today())
        db.session.add(newproduct)
        db.session.commit()

        message = "Listing Uploaded! Click <a href = " + "'/product/" + name.replace(" ","-") + "'" + "class = 'alert-link'>here</a>" + " to see your new listing!"
        flash(Markup(message))
        return redirect("/")
    else:
        return render_template("transact/post.html", modal = modaltext)

@transact_bp.route("/cart", methods = ["GET"])
@login_required
def cart():

    modaltext = modal()
    user_to_add = User.query.filter_by(id = current_user.id).first()
    items = user_to_add.cart_details
    # user_visitor = user_to_add

    today = date.today()
    totalproducts = []
    todelete = []
    for item in items.split(" "):
        if item == "" or item == " ":
            continue
        else:
            # print("item is {}".format(item))
            prodid = item.split("-")[0]
            delivery = item.split("-")[1]
            qty = item.split("-")[2]
            orderdate = "-".join(item.split("-")[3:])

            delta = today - datetime.strptime(orderdate, "%Y-%m-%d").date()
            # print(delta)

            if delta.days > 15:
                todelete.append(item)
                continue
            else:
                totalproducts.append([Product.query.filter_by(prodid = prodid).first(), delivery, qty, orderdate])

    for i in todelete:
        user_to_add.cart_details = items.replace(i, "",1)
                # totalproducts.append(Product.query.filter_by(prodid = prodid).first())
            # print("prodid = {}, delivery = {}, sellerid = {}, orderdate = {}".format(prodid, delivery, sellerid, orderdate))
    db.session.commit()


    return render_template("transact/cart.html", totalproducts = totalproducts, modal = modaltext),200

# you cannot 'retrieve' adding products to cart, therefore only method is "POST"
@transact_bp.route("/add", methods = ["POST"])
@login_required
def add_to_cart():

    quantity = request.form.get("order_quantity")
    deliver = request.form.get("deliver_collect")
    prodid = request.form.get("hidden_prodid")

    # print(quantity, deliver, prodid)
    # Should yield only one result.
    # item_to_add = Product.query.filter_by(prodid = prodid).first()
    user_to_add = User.query.filter_by(id = current_user.id).first()
    stringtoadd = prodid + "-" + deliver + "-" + quantity + "-" + str(date.today()) + " "

    # name = item_to_add.prodName.replace(" ", "-")
    # targetpath = r"/product/" + name

    #stringtoadd is in the format of prodid, deliver/collect, order quantity, date of cart add.
    original = user_to_add.cart_details + stringtoadd
    user_to_add.cart_details = original
    db.session.commit()
    return jsonify(True)

@transact_bp.route('/empty', methods = ["GET"])
@login_required
def empty_cart():

    ''' Something to do with retrieving a copy and not an actual object itself.'''
    user_to_empty = User.query.filter_by(id = current_user.id).first()
    # inspection = inspect(user_to_empty)

    # print("before is {}, pending = {}".format(user_to_empty.cart_details, inspection.pending))
    user_to_empty.cart_details = " " # this line does not change anything, so session commit is useless.

    db.session.commit()

    # user_to_empty = User.query.filter_by(id = current_user.id).first()
    # print("after is {}, pending = {}".format(user_to_empty.cart_details, inspection.pending))

    return redirect(url_for("transact_bp.cart"))

@transact_bp.route('/removeproduct', methods = ["GET", "POST"])
@login_required
def remove_product():

    url = request.headers.get("Referer")

    value = request.form.get("remove_prodid")
    # Change to lowercase
    value = value.replace("D", "d")
    value = value.replace("C", "c")

    if "deliver" in value:
        delimethod = "deliver"
    else:
        delimethod = "collection"
    vallist = []
    vallist.append(value.split(delimethod)[0])
    vallist.append(delimethod)
    vallist.append(value.split(delimethod)[1][0])
    vallist.append(value[-10:])

    # print(vallist)
    replaceval = "-".join(vallist)
    # print(replaceval)
    user_to_empty = User.query.filter_by(id = current_user.id).first()
    # print(user_to_empty.cart_details)
    user_to_empty.cart_details = user_to_empty.cart_details.replace(replaceval, "", 1)
    db.session.commit()

    if url.split("/")[-1] == 'cart':
        return redirect(url_for("transact_bp.cart"))
    else:
        return redirect(url)

@transact_bp.route("/payment", methods = ["GET", "POST"])
@login_required
def payment():
    modaltext = modal()
    if request.method == "GET":
        #To make payment
        area = ["North", "South", "East", "West", "North-East", "North-West", "South-East", "South-West"]
        with open('static/paymentmodal.txt', 'r') as file:
            paymentmodalwords = file.read().split("/n")
            paymentmodalwords = [i.strip("/n") for i in paymentmodalwords]

        user_to_add = User.query.filter_by(id = current_user.id).first()
        items = user_to_add.cart_details
        totalproducts = []
        valuepayment = ""
        for item in items.split(" "):
            # print(item)
            if item == "" or item == " ":
                continue
            else:
                # print("item is {}".format(item))
                prodid = item.split("-")[0]
                delivery = item.split("-")[1]
                delivery = delivery[0].upper() + delivery[1:]
                qty = item.split("-")[2]
                orderdate = "-".join(item.split("-")[3:])

                totalproducts.append([Product.query.filter_by(prodid = prodid).first(), delivery, qty, orderdate])

                valuepayment += "prodid" + str(prodid) + delivery + " "

        # print(totalproducts)
        return render_template("transact/payment.html", modal = modaltext, area = area, paymentmodalwords = paymentmodalwords, totalproducts = totalproducts, valuepayment = valuepayment)

    else:
        #Delete form details, but still process order form.

        paymentitems = request.form.get("payproddetails")
        allform = request.form.to_dict(flat = False)
        # print(allform)

        # Get the remove_prodid
        products = request.form.get("remove_prodid")

        buy_id = current_user.id

        price = 0
        for item in paymentitems.split(" ")[0:-1]:
            produc = Product.query.filter_by(prodid = item[6]).first()
            producid = produc.prodid
            price = produc.prodPrice
            if item[7:] == "Deliver":
                price += 5

            seller = produc.sell_id
            neworder = Order(buyerid = buy_id, sellerid = seller, unitprice = price, productid = producid, order_date = date.today())
            db.session.add(neworder)

        currentuser = User.query.filter_by(id = current_user.id).first()

        #Paid for and so cart items will be deleted.
        currentuser.cart_details = ""
        db.session.commit()
        flash("Thank you for making the purchase. Your order will arrive instantaneously!")
        return redirect("/")

    return render_template("transact/cart.html"), 404


@transact_bp.route("/history", methods = ["GET"])
@login_required
def history():
    """Show history of transactions"""

    modaltext = modal()
    current_buyer_orders = Order.query.filter_by(buyerid = current_user.id).all()
    # print(current_buyer_orders)
    history = []

    for orders in current_buyer_orders:
        produc = Product.query.filter_by(prodid = orders.productid).first()
        produc_path = produc.prodPath
        produc_path = produc_path.split(",")[0]
        produc_price = produc.prodPrice
        produc_name = produc.prodName

        if ((orders.unitprice - 5) % produc_price) == 0:
            #means delivery
            deliverymethod = "Delivery"
            #should return an integer
            qty = (orders.unitprice-5)/produc_price

        else:
            deliverymethod = "Collection"
            qty = orders.unitprice/produc_price

        print("qty = {}".format(qty))
        print("prodprice = {}, unitprice = {}".format(produc.prodPrice, orders.unitprice))
        history.append([produc_path, produc_name, deliverymethod, qty, produc_price, orders.unitprice, orders.order_date])

    return render_template("transact/userorderhistory.html", modal = modaltext, history = history), 200
