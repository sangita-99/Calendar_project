# 📅 Customizable Calendar Web Application

## 📝 Project Name
**Customizable Calendar Web Application**

## 📚 Description, Purpose, and Value

The **Customizable Calendar Web Application** is a personal event management tool built with Flask. It allows users to:

- Add, edit, and delete one-time or recurring events
- Set specific times for events and manage them interactively
- View today’s reminders and upcoming events
- Toggle between light and dark mode for better accessibility
- Export all scheduled events to a downloadable PDF file
- Receive **email reminders** 30 minutes before scheduled events
- Analyze scheduling habits using **Pandas** and **Matplotlib** to visualize event distributions

**Purpose**:  
This application provides an efficient and easy-to-use system for organizing personal schedules, ensuring that users never miss important tasks or appointments.

**Value**:  
Combines user-friendly design with backend automation to help users track their daily routines, optimize their schedules, and improve time management.

## 🛠 Technologies Used

| Technology        | Purpose                             |
|------------------|-------------------------------------|
| **Python (Flask)**   | Backend web application            |
| **SQLAlchemy**       | ORM and database management (SQLite)  |
| **Flask-Mail**       | Sending email reminders             |
| **Flask-APScheduler**| Scheduled background jobs          |
| **FullCalendar.js**  | Dynamic interactive calendar UI     |
| **Bootstrap 5**      | Responsive frontend design         |
| **HTML/CSS/JavaScript** | UI structure and interactions   |
| **Pandas**           | Data analysis of event distribution |
| **Matplotlib**       | Visualization of event patterns     |
| **ReportLab**        | Exporting event lists to PDF         |

## ⚙️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sangita-99/Calendar_project.git
   cd Calendar_project/src
   ```

2. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Required Packages**:
   ```bash
   pip install -r ../requirements.txt
   ```

4. **Configure Gmail for Email Reminders**:
   - Enable **2-Step Verification** on your Gmail account.
   - Generate a **16-character App Password** from your Google Account security settings.
   - Update the `MAIL_USERNAME` and `MAIL_PASSWORD` fields in `app.py` with your Gmail and App Password.

5. **Prepare the Database**:
   ```bash
   python
   >>> from app import db, app
   >>> with app.app_context():
   ...     db.create_all()
   ```

6. **Run the Application**:
   ```bash
   python app.py
   ```

7. **Access the App**:  
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🎥 YouTube Video Link


## 📂 GitHub Repository Link
[🔗 https://github.com/sangita-99/Calendar_project.git]

