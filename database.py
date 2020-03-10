# Attempting to create database objects with SQLAlchemy.
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


db = SQLAlchemy(session_options = {"autoflush": False})

class Order(UserMixin, db.Model):
    __tablename__ = 'order'
    orderid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    buyerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    sellerid = db.Column(db.Integer, db.ForeignKey('user.id'))
    unitprice = db.Column(db.Float, nullable = False)
    productid = db.Column(db.Integer, db.ForeignKey('product.prodid'))
    order_date = db.Column(db.Date, nullable = False)

    buyer = db.relationship("User", foreign_keys = [buyerid])
    seller = db.relationship("User",foreign_keys = [sellerid])
    product = db.relationship("Product", foreign_keys = [productid])

''' https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers'''
''' https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database'''

# Products should be listed by sellers.
# Assume unlimited quantity for each listing.
class Product(UserMixin, db.Model):
    __tablename__ = 'product'
    prodid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    sell_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    prodName = db.Column(db.String(256), nullable = False)
    prodDesc = db.Column(db.String(512), nullable = False)
    prodPrice = db.Column(db.Float, nullable = False)
    prodPath = db.Column(db.String(256), nullable = False)
    listdate = db.Column(db.Date, nullable = False)
    nsales = db.Column(db.Integer, default = 0)
    productsold = db.relationship("Order", back_populates = "product")

    lister = db.relationship("User", foreign_keys = [sell_id])

    def __init__(self, sell_id, prodName, prodDesc, prodPrice, prodPath, listdate):
        self.sell_id = sell_id
        self.prodName = prodName
        self.prodDesc = prodDesc
        self.prodPrice = prodPrice
        self.prodPath = prodPath
        self.listdate = listdate

    def __repr__(self):
        return '<Product %r>' % self.prodid

class UserSession(UserMixin, db.Model):
    __tablename__ = 'usersession'
    sessid = db.Column(db.Integer, primary_key = True, autoincrement = True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime(timezone = True), default = func.now())

    user = db.relationship("User", foreign_keys = [userid])

    def __init__(self, sessid, userid, timestamp):
        self.sessid = sessid
        self.userid = userid
        self.timestamp = timestamp

    def __repr__(self):
        return '<session %r' % self.sessid

# Only have Buyers, and anonymous user.
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String(256), unique = True, nullable = False)
    password = db.Column(db.String(256), nullable = True)
    cash = db.Column(db.Float, default = 1000)
    usertype = db.Column(db.String(256), nullable = False)
    cart_details = db.Column(db.Text(), nullable = True, default = " ")

    def __init__(self, username, password, usertype):
        self.username = username
        self.set_password(password)
        self.authenticated = False
        self.usertype = usertype

    def __repr__(self):
        return '<User %r>' % self.id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the username to satisfy Flask-Login's requirements."""
        return self.username
