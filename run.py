import os
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_login import LoginManager
from flask import Flask, Blueprint, request, session
from tempfile import mkdtemp
from datetime import timedelta
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

login_manager = LoginManager()

# Create function for app creation and configuration.
def create_app(test_config = None):
    # Create and configure the application
    app = Flask(__name__, instance_relative_config = False)
    app.config.from_pyfile(os.path.join(".", "config.py"))

    # Declare everything we need in this application:
    with app.app_context():

        from database import db, Order, Product, User #DB and tables
        from auth import auth_bp #Authentication blueprint
        from transact import transact_bp #Website blueprint
        import auth, transact, routes #import routes

        # Initialise Plugins
        db.init_app(app)
        db.create_all()
        login_manager.init_app(app)
        Session(app)
        # migrate = Migrate(app, db) #To add migration support


        # Register Blueprints - These help to compartmentalise routes.
        app.register_blueprint(auth_bp)
        # app.register_blueprint(content.content_bp)
        app.register_blueprint(transact_bp)

        # Ensure responses aren't cached
        @app.after_request
        def after_request(response):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Expires"] = 0
            response.headers["Pragma"] = "no-cache"
            return response

        # Listen for errors
        # for code in default_exceptions:
        #     app.errorhandler(code)(errorhandler)

        # print("auth is in {}".format(main.auth.__file__))
        # print("transact is in {}".format(main.transact.__file__))
        # print("routes is in {}".format(main.routes.__file__))
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()

    # https://flask.palletsprojects.com/en/1.1.x/server/
    # flask run --no-reload


    # for rule in app.url_map.iter_rules():
    #     print("rule is {}".format(rule))
    # print("main working dir = {}".format(os.getcwd()))
