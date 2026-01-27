import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import google.genai as genai
from dotenv import load_dotenv
import os

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("safecity_data/crimes.csv")

# Parse date_time to extract hour, day, month
df['date_time'] = pd.to_datetime(df['date_time'])
df['hour'] = df['date_time'].dt.hour
df['day'] = df['date_time'].dt.day
df['month'] = df['date_time'].dt.month

# Generate next crime ID for predictions
next_crime_id = df['id'].max() + 1

# -------------------------------
# Encode categorical data
# -------------------------------
le = LabelEncoder()
df["crime_type_enc"] = le.fit_transform(df["crime_type"])
# Note: area encoding removed as it's not used in the model

# -------------------------------
# HOTSPOT DETECTION (Clustering)
# -------------------------------
kmeans = KMeans(n_clusters=3, random_state=42)
df["hotspot_cluster"] = kmeans.fit_predict(df[["latitude", "longitude"]])

# Identify hotspot cluster (highest density)
hotspot_cluster_id = df["hotspot_cluster"].value_counts().idxmax()

# -------------------------------
# RISK LABEL CREATION
# -------------------------------
df["risk"] = df["hour"].apply(lambda h: 1 if (h >= 20 or h <= 4) else 0)

# -------------------------------
# Train Risk Prediction Model
# -------------------------------
X = df[["latitude", "longitude", "hour", "day", "month", "hotspot_cluster"]]
y = df["risk"]

model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
model_rf.fit(X, y)

# -------------------------------
# REAL-TIME USER INPUT
# -------------------------------
print("Enter the details for risk prediction:")
area = input("Area: ")
latitude = float(input("Latitude: "))
longitude = float(input("Longitude: "))
hour = int(input("Hour (0-23): "))
day = int(input("Day (1-31): "))
month = int(input("Month (1-12): "))
crime_type = input("Crime Type: ")

sample = {
    "area": area,
    "latitude": latitude,
    "longitude": longitude,
    "hour": hour,
    "day": day,
    "month": month,
    "crime_type": crime_type
}

# Note: area encoding removed as it's not used in the model

# Predict hotspot cluster
sample_cluster = kmeans.predict(
    [[sample["latitude"], sample["longitude"]]]
)[0]

# Predict risk
risk_pred = model_rf.predict(
    [[
        sample["latitude"],
        sample["longitude"],
        sample["hour"],
        sample["day"],
        sample["month"],
        sample_cluster
    ]]
)[0]

# -------------------------------
# FINAL ML OUTPUT (Gemini-ready)
# -------------------------------
# Construct date_time from inputs (assuming year 2026)
date_time = f"2026-{sample['month']:02d}-{sample['day']:02d}T{sample['hour']:02d}:00:00"

ml_output = {
    "id": next_crime_id,
    "area": sample["area"],
    "coordinates": {
        "latitude": sample["latitude"],
        "longitude": sample["longitude"]
    },
    "time": {
        "hour": sample["hour"],
        "day": sample["day"],
        "month": sample["month"]
    },
    "date_time": date_time,
    "crime_type": sample["crime_type"],
    "hotspot": bool(sample_cluster == hotspot_cluster_id),
    "risk_level": "High Risk!!!" if risk_pred == 1 else "Low Risk"
}

print("\nML OUTPUT:")
print(ml_output)

# -------------------------------
# GOOGLE GEMINI AI INTEGRATION
# -------------------------------
load_dotenv()
api_key = os.getenv("gemini_api_key")

# Configure Gemini API (replace with your actual API key)
client = genai.Client(api_key=api_key)

# Create prompt for patrolling suggestions and next crime chances
prompt = """
Analyze the provided area to generate a crime prevention strategy and predictive assessment.

### **Patrolling & Risk Assessment**

* **Strategy:** Define patrol frequency, timing, and focus points based on risk levels and crime types.
* **Probability:** Rate the likelihood of the next incident (**Low/Medium/High**) for the next hour, 24 hours, and week.

### **Infrastructure & Prediction**

* **CCTV:** Recommend specific, realistic installation points (junctions/access paths) near the coordinates.
* **Location Prediction:** Identify the most likely coordinates () for the next incident based on proximity and historical patterns.

### **Output Format**

Return **only** a JSON object with the following keys:

* `latitude`: [Predicted Lat]
* `longitude`: [Predicted Long]
* `expected_crime_time_window`: [Estimated timeframe]
* `suggestions`: [A list of 5-6 professional prevention points]

**Constraint:** No conversational filler; provide the JSON only.
"""

# Generate response
try:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print("\nGemini AI Suggestions:")
    print(response.text)
except Exception as e:
    print(f"\nError with Gemini API: {e}")
    print("Please check your API key or try again later.")
