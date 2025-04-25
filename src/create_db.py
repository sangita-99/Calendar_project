import os
from app import db, app

# Get the absolute path to the instance folder
instance_folder = os.path.join(os.path.dirname(__file__), 'instance')

# ✅ Create instance/ folder if it does not exist
if not os.path.exists(instance_folder):
    os.makedirs(instance_folder)
    print("✅ 'instance/' folder created.")

# ✅ Now create the database
with app.app_context():
    try:
        db.create_all()
        print("✅ Database created successfully inside 'instance/calendar.db'.")
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
