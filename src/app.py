from flask import Flask, render_template, request, jsonify
from extensions import db
from models import Event
from datetime import datetime, timedelta  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_events")
def get_events():
    events = Event.query.all()
    event_list = [{"id": e.id, "title": e.title, "start": str(e.date)} for e in events]
    return jsonify(event_list)

@app.route("/add_event", methods=["POST"])
def add_event():
    data = request.json
    if not data.get("title") or not data.get("date"):
        return jsonify({"status": "error", "message": "Title and date are required!"}), 400

    try:
        event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        event_time = None
        if data.get("time") and data["time"] != "":
            event_time = datetime.strptime(data["time"], "%H:%M").time()

        new_event = Event(
            title=data["title"],
            description=data.get("description", ""),
            date=event_date,
            time=event_time
        )
        db.session.add(new_event)
        db.session.commit()

        print("✅ Event added successfully:", new_event)  # Debugging Output
        return jsonify({"status": "success"}), 201
    except Exception as e:
        print("❌ Error saving event:", e)  # Debugging Output
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route("/get_upcoming_events")
def get_upcoming_events():
    try:
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        upcoming_events = Event.query.filter(Event.date >= today).order_by(Event.date).all()

        event_list = [{"title": e.title, "date": str(e.date)} for e in upcoming_events]

        print("Upcoming Events:", event_list)
        return jsonify(event_list)
    except Exception as e:
        print("❌ Error fetching upcoming events:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/get_todays_reminders")
def get_todays_reminders():
    try:
        today = datetime.today().date()
        today_events = Event.query.filter(Event.date == today).all()

        reminder_list = [{"title": e.title, "time": str(e.time) if e.time else "All Day"} for e in today_events]

        print("Today's Reminders:", reminder_list)
        return jsonify(reminder_list)
    except Exception as e:
        print("❌ Error fetching today's reminders:", e)
        return jsonify({"error": str(e)}), 500



@app.route("/edit_event/<int:event_id>", methods=["POST"])
def edit_event(event_id):
    data = request.json
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "error", "message": "Event not found"}), 404
    event.title = data.get("title", event.title)
    db.session.commit()
    return jsonify({"status": "success"})


@app.route("/delete_event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "error", "message": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"status": "success"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
