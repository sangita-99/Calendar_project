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
2. **Install Required Packages**:
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Configure Gmail for Email Reminders**:
   - Enable **2-Step Verification** on your Gmail account.
   - Generate a **16-character App Password** from your Google Account security settings.
   - Update the `MAIL_USERNAME` and `MAIL_PASSWORD` fields in `app.py` with your Gmail and App Password.
  *This step isn't really necessary unless you want to get an email reminder 30 minutes before the event. And more reminder on 5 minutes interval in your email account*
4. **Prepare the Database**:
    ```bash
   python create_db.py
   ```


5. **Run the Application**:
   ```bash
   python app.py
   ```

6. **Access the App**:  
   Open your browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

## 🎥 YouTube Video Link
[🔗 https://youtu.be/4CF4wyR61-o]


## 📂 GitHub Repository Link
[🔗 https://github.com/sangita-99/Calendar_project.git]

