from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from models import db, login_manager
from routes import auth_bp, products_bp
from routes import auth_bp, products_bp, cart_bp, orders_bp

app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)