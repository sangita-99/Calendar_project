from flask import Flask, render_template, redirect, url_for, request
from extensions import db
from models import Event
from forms import EventForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SECRET_KEY'] = 'supersecretkey'

db.init_app(app)

@app.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)

# ✅ Add this route for adding events
@app.route('/add', methods=['GET', 'POST'])
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data
        )
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_event.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
