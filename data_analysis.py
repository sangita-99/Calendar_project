import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import sqlite3

# Connect to the calendar database
conn = sqlite3.connect("instance/calendar.db")
query = "SELECT title, description, date, time FROM event"
df = pd.read_sql_query(query, conn)
conn.close()

# Convert date and time columns
df["date"] = pd.to_datetime(df["date"])
df["time"] = pd.to_datetime(df["time"], errors="coerce").dt.time

# Extract weekday and hour
df["weekday"] = df["date"].dt.day_name()
df["hour"] = pd.to_datetime(df["time"], errors="coerce").dt.hour

# Events per weekday
weekday_counts = df["weekday"].value_counts().sort_index()
print("📊 Events per Weekday:")
print(weekday_counts)

# Most common event hour
if df["hour"].notna().any():
    hour_counts = df["hour"].value_counts().sort_index()
    print("\n⏰ Event Start Times (hourly):")
    print(hour_counts)
else:
    print("\n(No event times found.)")

# Pie chart of event distribution by weekday
import matplotlib.pyplot as plt

colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#C299FF", "#FFD700", "#FFB6C1"]
plt.figure(figsize=(8, 8))
weekday_counts.plot(kind='pie',
                    autopct='%1.1f%%',
                    startangle=140,
                    colors=colors,
                    title='Event Distribution by Weekday')
plt.ylabel('')  # Hide y-label for a cleaner pie chart
plt.tight_layout()
plt.savefig("weekday_distribution_pie.png")
print("📈 Pie chart saved as weekday_distribution_pie.png")
