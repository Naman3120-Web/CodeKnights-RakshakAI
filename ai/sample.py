import csv
import os

# Create directory
output_dir = "safecity_data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- DATA DEFINITIONS ---

zones_data = [
    ["id", "zone_name", "center_lat", "center_lng", "radius", "area_type"],
    [1, "South Mumbai (Colaba & Fort)", 18.9220, 72.8347, 1500, "commercial"],
    [2, "Bandra West (Linking Road)", 19.0596, 72.8295, 1200, "market"],
    [3, "Andheri East (MIDC)", 19.1136, 72.8697, 2000, "commercial"],
    [4, "Dadar Central", 19.0178, 72.8478, 1000, "market"],
    [5, "Kurla West", 19.0726, 72.8795, 1400, "residential"],
    [6, "Eastern Express Highway (Vikhroli)", 19.0989, 72.9304, 3000, "highway"],
    [7, "Borivali West", 19.2312, 72.8567, 1600, "residential"],
    [8, "Juhu Beach Area", 19.0980, 72.8260, 1100, "market"]
]

crimes_data = [
    ["id", "crime_type", "zone_id", "latitude", "longitude", "date_time", "area_name"],
    [1001, "Theft", 1, 18.9231, 72.8352, "2025-10-12T14:30:00", "Colaba Causeway Market"],
    [1002, "Theft", 1, 18.9215, 72.8339, "2025-11-05T16:45:00", "Fort Business District"],
    [1003, "Assault", 1, 18.9201, 72.8360, "2025-12-20T23:15:00", "Back Bay Alley"],
    [1004, "Theft", 2, 19.0601, 72.8301, "2025-09-15T18:20:00", "Linking Road Shopping"],
    [1005, "Theft", 2, 19.0589, 72.8288, "2025-10-02T13:10:00", "Hill Road"],
    [1006, "Accident", 3, 19.1145, 72.8705, "2025-11-10T09:45:00", "MIDC Junction"],
    [1007, "Theft", 3, 19.1128, 72.8689, "2025-12-05T11:30:00", "Office Complex Parking"],
    [1008, "Theft", 4, 19.0185, 72.8482, "2025-10-25T17:00:00", "Flower Market"],
    [1009, "Assault", 5, 19.0735, 72.8788, "2025-12-31T01:30:00", "Residential Colony"],
    [1010, "Accident", 6, 19.0995, 72.9312, "2025-11-20T22:15:00", "Highway Slip Road"],
    [1011, "Accident", 6, 19.0982, 72.9298, "2025-12-15T08:50:00", "Express Highway Main Lane"],
    [1012, "Theft", 7, 19.2320, 72.8575, "2025-09-28T15:40:00", "Local Park"],
    [1013, "Theft", 8, 19.0985, 72.8255, "2025-10-30T19:20:00", "Juhu Tara Road"],
    [1014, "Assault", 2, 19.0575, 72.8310, "2026-01-05T02:00:00", "Carter Road Promenade"],
    [1015, "Theft", 4, 19.0170, 72.8470, "2025-11-12T10:15:00", "Station Bridge"],
    [1016, "Accident", 6, 19.1002, 72.9320, "2025-08-22T23:45:00", "Godrej Signal"],
    [1017, "Theft", 5, 19.0715, 72.8805, "2025-09-05T14:50:00", "Mall Entrance"],
    [1018, "Assault", 5, 19.0740, 72.8780, "2025-11-28T22:30:00", "Slum Pocket"],
    [1019, "Theft", 1, 18.9225, 72.8350, "2025-12-10T12:00:00", "Tourist Plaza"],
    [1020, "Accident", 3, 19.1150, 72.8710, "2026-01-10T18:30:00", "Metro Construction Site"]
]

stats_data = [
    ["id", "zone_id", "crime_type", "crime_count", "start_date", "end_date"],
    [1, 1, "Theft", 45, "2025-08-01", "2026-01-27"],
    [2, 1, "Assault", 12, "2025-08-01", "2026-01-27"],
    [3, 2, "Theft", 68, "2025-08-01", "2026-01-27"],
    [4, 2, "Assault", 8, "2025-08-01", "2026-01-27"],
    [5, 3, "Accident", 25, "2025-08-01", "2026-01-27"],
    [6, 3, "Theft", 30, "2025-08-01", "2026-01-27"],
    [7, 4, "Theft", 52, "2025-08-01", "2026-01-27"],
    [8, 5, "Assault", 18, "2025-08-01", "2026-01-27"],
    [9, 6, "Accident", 40, "2025-08-01", "2026-01-27"],
    [10, 6, "Theft", 10, "2025-08-01", "2026-01-27"],
    [11, 7, "Theft", 15, "2025-08-01", "2026-01-27"],
    [12, 8, "Theft", 28, "2025-08-01", "2026-01-27"]
]

predictions_data = [
    ["id", "zone_id", "predicted_month", "risk_level", "risk_score", "expected_crimes", "generated_at"],
    [101, 1, "2026-02", "High", 0.85, 55, "2026-01-27T10:00:00"],
    [102, 2, "2026-02", "High", 0.92, 75, "2026-01-27T10:00:00"],
    [103, 3, "2026-02", "Medium", 0.65, 40, "2026-01-27T10:00:00"],
    [104, 4, "2026-02", "High", 0.78, 50, "2026-01-27T10:00:00"],
    [105, 5, "2026-02", "Medium", 0.60, 35, "2026-01-27T10:00:00"],
    [106, 6, "2026-02", "Medium", 0.55, 30, "2026-01-27T10:00:00"],
    [107, 7, "2026-02", "Low", 0.30, 12, "2026-01-27T10:00:00"],
    [108, 8, "2026-02", "Medium", 0.48, 25, "2026-01-27T10:00:00"]
]

suggestions_data = [
    ["id", "zone_id", "risk_level", "suggestion_text", "prediction_id"],
    [501, 1, "High", "Deploy static patrol units at Colaba Causeway and Gateway tourist points.", 101],
    [502, 2, "High", "Increase bike patrols on Linking Road during evening peak hours.", 102],
    [503, 6, "Medium", "Station traffic interceptors on Eastern Express Highway post-midnight.", 106],
    [504, 5, "Medium", "Enhance night patrolling (11 PM - 3 AM) in residential pockets.", 105],
    [505, 4, "High", "Crowd control measures recommended near Dadar Station flower market.", 104],
    [506, 3, "Medium", "Conduct spot checks at MIDC entry points during late evening shifts.", 103],
    [507, 7, "Low", "Maintain standard beat marshall rounds; no specific surge required.", 107],
    [508, 8, "Medium", "Increase vigilance near Juhu Beach entrance on weekends.", 108]
]

# --- WRITE FILES ---

files = {
    "zones.csv": zones_data,
    "crimes.csv": crimes_data,
    "crime_stats.csv": stats_data,
    "predictions.csv": predictions_data,
    "patrol_suggestions.csv": suggestions_data
}

print("Generating files...")
for filename, data in files.items():
    path = os.path.join(output_dir, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(data)
    print(f"Created {path}")

print("\nDone! Check the 'safecity_data' folder.")