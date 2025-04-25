from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from extensions import db
from models import Event
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from flask import send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'calendar.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'gurungsangeeta52@gmail.com'
app.config['MAIL_PASSWORD'] = 'lbue iaaw ihov ahxy'
app.config['MAIL_DEFAULT_SENDER'] = 'gurungsangeeta52@gmail.com'

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

mail = Mail(app)
db.init_app(app)

@app.route("/")
def index():
    """Render the main calendar interface."""
    return render_template("index.html")

@app.route("/get_events")
def get_events():
    """Return all calendar events in JSON format for the frontend."""
    events = Event.query.all()
    event_list = [{"id": e.id, "title": e.title, "description": e.description, "start": str(e.date), "time": str(e.time) if e.time else ""} for e in events]
    return jsonify(event_list)

@app.route("/add_event", methods=["POST"])
def add_event():
    """
    Handle adding a new calendar event.
    Supports optional recurring settings.
    """
    data = request.json
    if not data.get("title") or not data.get("date"):
        return jsonify({"status": "error", "message": "Title and date are required!"}), 400

    try:
        event_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        event_time = datetime.strptime(data["time"], "%H:%M").time() if data.get("time") else None

        new_event = Event(
            title=data["title"],
            description=data.get("description", ""),
            date=event_date,
            time=event_time,
            is_recurring=data.get("is_recurring", False),
            recurrence_type=data.get("recurrence_type"),
            recurrence_count=int(data.get("recurrence_count", 0))
        )
        db.session.add(new_event)
        db.session.flush()

        if new_event.is_recurring:
            recurrence_type = new_event.recurrence_type
            count = new_event.recurrence_count
            interval = 1 if recurrence_type == "daily" else 7 if recurrence_type == "weekly" else 0
            if interval > 0 and count > 1:
                generate_recurring_events(new_event, count - 1, interval)

        db.session.commit()
        return jsonify({"status": "success"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

def generate_recurring_events(base_event, count, interval_days):
    """
    Recursively create and add recurring events to the database.
    Args:
        base_event (Event): The base event object
        count (int): Number of additional recurrences to create
        interval_days (int): Days between each recurrence (e.g., 1 = daily, 7 = weekly)
    """
    if count <= 0:
        return []
    next_date = base_event.date + timedelta(days=interval_days)
    new_event = Event(
        title=base_event.title,
        description=base_event.description,
        date=next_date,
        time=base_event.time,
        is_recurring=True,
        recurrence_type=base_event.recurrence_type,
        recurrence_count=base_event.recurrence_count
    )
    db.session.add(new_event)
    db.session.flush()
    return [new_event] + generate_recurring_events(new_event, count - 1, interval_days)

@app.route("/edit_event/<int:event_id>", methods=["POST"])
def edit_event(event_id):
    """Edit an existing event given its ID."""
    data = request.json
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "error", "message": "Event not found"}), 404

    try:
        event.title = data.get("title", event.title)
        event.description = data.get("description", "")
        event.date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        event.time = datetime.strptime(data["time"], "%H:%M").time() if data.get("time") else None
        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/delete_event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Delete an event from the database."""
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"status": "error", "message": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"status": "success"})

@app.route("/get_upcoming_events")
def get_upcoming_events():
    """Return all upcoming events from today onward."""
    today = datetime.today().date()
    upcoming_events = Event.query.filter(Event.date >= today).order_by(Event.date).all()

    event_list = [{"title": e.title, "date": str(e.date)} for e in upcoming_events]
    return jsonify(event_list)


@app.route("/get_todays_reminders")
def get_todays_reminders():
    """Return reminders for events scheduled for today."""
    today = datetime.today().date()
    today_events = Event.query.filter(Event.date == today).all()

    print(f"📅 Today: {today}")
    for event in today_events:
        print(f"Found: {event.title} at {event.time}")

    reminder_list = [
        {"title": e.title, "time": str(e.time) if e.time else "All Day"}
        for e in today_events
    ]
    return jsonify(reminder_list)



@app.route("/send_upcoming_reminders")
def send_upcoming_reminders():
    """Send email reminders for events occurring within the next 30 minutes."""
    now = datetime.now()
    window = now + timedelta(minutes=30)
    today = now.date()
    events = Event.query.filter(Event.date == today).all()

    print("🕒 Now:", now)
    print("📅 Checking events for:", today)

    sent_any = False
    for e in events:
        if e.time:
            event_datetime = datetime.combine(e.date, e.time)
            print(f"🔍 Found event: {e.title} at {event_datetime}")
            if now < event_datetime <= window:
                print(f"Sending email for event: {e.title}")
                send_reminder_email("gurungsangeeta52@gmail.com", e.title, e.time)  # update recipient
                sent_any = True
            else:
                print(f"⏳ Skipped: {e.title} is not within 30 minutes")

    if not sent_any:
        print("No events matched the 30-minute window.")

    return jsonify({"status": "done"})


def send_reminder_email(to_email, event_title, event_time):
    """
    Send an email reminder to the specified recipient.
    Args:
        to_email (str): Recipient email address
        event_title (str): Title of the event
        event_time (str): Time of the event
    """
    msg = Message(
        subject=f"Reminder: {event_title} at {event_time}",
        recipients=[to_email],
        body=f"Don't forget! You have \"{event_title}\" scheduled at {event_time}."
    )
    mail.send(msg)

@scheduler.task('interval', id='send_reminders_job', minutes=5, misfire_grace_time=900)
def scheduled_email_check():
    """
    Scheduled task that runs every 5 minutes to check for upcoming events
    occurring within the next 30 minutes. If found, an email reminder is sent.
    """
    with app.app_context():
        now = datetime.now()
        window = now + timedelta(minutes=30)
        events = Event.query.filter(Event.date == now.date()).all()

        for e in events:
            if e.time:
                event_time = datetime.combine(e.date, e.time)
                if now < event_time <= window:
                    send_reminder_email("gurungsangeeta52@gmail.com", e.title, e.time)

@app.route("/export_pdf")
def export_pdf():
    """Generate and download a PDF file containing all calendar events."""
    with app.app_context():
        events = Event.query.order_by(Event.date).all()
        file_path = os.path.join(os.path.dirname(__file__), "calendar_export.pdf")
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 12)
        y = 750

        c.drawString(100, y, "📅 Calendar Events Export")
        y -= 30

        for e in events:
            line = f"{e.date} - {e.title} at {e.time if e.time else 'All Day'}"
            c.drawString(100, y, line)
            y -= 20
            if y < 50:
                c.showPage()
                y = 750

        c.save()
        return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
