# __init__.py
from bson import ObjectId
from datetime import timedelta
from flask import Flask
from flask_login import LoginManager, UserMixin
from pymongo import MongoClient
import os

app = Flask(__name__)

# Secret key configuration
# CHANGE THIS TO ENVIRONMENT VARIABLE LATER
app.secret_key = 'QXdv1dRwMqIfxK2Z3dANRXH22uisGOEp'

# Session cookie configurations for security
app.config['SESSION_COOKIE_SECURE'] = True  # Ensure cookies are sent over HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Control cookie sharing with other domains

# Optional: Configure the permanent session lifetime, for example, 7 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

# MongoDB connection setup
mongo_conn_str = os.environ.get('MONGO_CONN_STR')
client = MongoClient(mongo_conn_str)
db = client.LightingStoreDB

@login_manager.user_loader
def load_user(user_id):
    # Assuming user_id is just the stringified ObjectId
    u = db.users.find_one({'_id': ObjectId(user_id)})
    if not u:
        return None
    return User(u['_id'])

class User(UserMixin):
    # Assuming that user document has an '_id' field
    def __init__(self, user_id):
        self.id = str(user_id)

from app.routes import create_routes
app = create_routes(app, db, User)