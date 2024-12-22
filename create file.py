import csv
with open("temperature_stats.csv", "a", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "High Today", " Time  ", "Low Today", "  Time ", "high yesterday", "  Time", "lo yesterday", "  Time", "high Year", " date ", "Low Year", " date "])

