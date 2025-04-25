# Import SQLAlchemy from Flask extension
from flask_sqlalchemy import SQLAlchemy

# Initialize a global SQLAlchemy instance
# This is used in app.py and models.py to define and manage the database
db = SQLAlchemy()
 