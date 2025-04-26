import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

# Setup base directory and connect to database
basedir = os.path.abspath(os.path.dirname(__file__))
conn = sqlite3.connect(os.path.join(basedir, "instance", "calendar.db"))
query = "SELECT title, description, date, time FROM event"
df = pd.read_sql_query(query, conn)
conn.close()

# Convert date and time columns
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S", errors="coerce").dt.time

# Extract weekday and hour
df["weekday"] = df["date"].dt.day_name()
df["hour"] = pd.to_datetime(df["time"], errors="coerce").dt.hour

# Analyze Events per Weekday
weekday_counts = df["weekday"].value_counts().sort_index()

# Print a nicely formatted summary
print("\n=== Events per Weekday ===")
for day, count in weekday_counts.items():
    print(f"{day}: {count} events")

# Analyze Most Common Event Start Hours
if df["hour"].notna().any():
    hour_counts = df["hour"].value_counts().sort_index()
    print("\n=== Event Start Times (by Hour) ===")
    for hour, count in hour_counts.items():
        print(f"{hour}:00 - {count} events")
else:
    print("\nNo time data available for events.")

# Plot a Pie Chart of Events by Weekday (without saving)
colors = ["#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#C299FF", "#FFD700", "#FFB6C1"]

plt.figure(figsize=(8, 8))
weekday_counts.plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    title='Event Distribution by Weekday'
)
plt.ylabel('')  # Hide y-label for cleaner appearance
plt.tight_layout()
plt.show()

print("\n✅ Pie chart shown successfully!")
