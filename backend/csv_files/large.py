import pandas as pd
import random
import numpy as np

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
FILENAME = "police_stations.csv"

# We use the same 12 Zones from previous steps to maintain Foreign Key consistency
zones = [
    {"id": 1, "name": "South Mumbai (Colaba)", "lat": 18.9220, "lng": 72.8347},
    {"id": 2, "name": "Bandra West", "lat": 19.0596, "lng": 72.8295},
    {"id": 3, "name": "Andheri East", "lat": 19.1136, "lng": 72.8697},
    {"id": 4, "name": "Dadar Central", "lat": 19.0178, "lng": 72.8478},
    {"id": 5, "name": "Kurla West", "lat": 19.0726, "lng": 72.8795},
    {"id": 6, "name": "Vikhroli Highway", "lat": 19.0989, "lng": 72.9304},
    {"id": 7, "name": "Borivali West", "lat": 19.2312, "lng": 72.8567},
    {"id": 8, "name": "Juhu", "lat": 19.0980, "lng": 72.8260},
    {"id": 9, "name": "Powai", "lat": 19.1197, "lng": 72.9050},
    {"id": 10, "name": "Chembur", "lat": 19.0450, "lng": 72.8900},
    {"id": 11, "name": "Malad Mindspace", "lat": 19.1860, "lng": 72.8360},
    {"id": 12, "name": "Lower Parel", "lat": 18.9930, "lng": 72.8300},
]

station_types = ["Main Station", "Traffic Division", "Chowki (Outpost)"]
data = []
station_id_counter = 1001

print(f"Generating police stations for {len(zones)} zones...")

for zone in zones:
    # 1. ALWAYS generate a Main Station for the zone
    # Jitter location slightly (approx 50-100m) so it's not exact center
    lat_main = zone['lat'] + np.random.normal(0, 0.001)
    lng_main = zone['lng'] + np.random.normal(0, 0.001)
    
    # Generate realistic phone number (022-2xxx-xxxx)
    phone_main = f"022-2{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    # Clean up zone name for station name (remove brackets)
    clean_name = zone['name'].split('(')[0].strip()
    
    data.append([
        station_id_counter,
        f"{clean_name} Police Station",
        zone['id'],
        round(lat_main, 6),
        round(lng_main, 6),
        phone_main,
        "Main Station",
        random.randint(40, 120), # Personnel count
        True # Has Lockup
    ])
    station_id_counter += 1

    # 2. RANDOMLY add a Traffic Division or Chowki (50% chance)
    if random.choice([True, False]):
        sub_type = random.choice(["Traffic Division", "Chowki (Outpost)"])
        
        # Jitter location a bit further away (approx 500m)
        lat_sub = zone['lat'] + np.random.normal(0, 0.005)
        lng_sub = zone['lng'] + np.random.normal(0, 0.005)
        
        phone_sub = f"022-2{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        
        station_name = f"{clean_name} {sub_type}"
        personnel = random.randint(15, 40) if sub_type == "Traffic Division" else random.randint(5, 12)
        has_lockup = False
        
        data.append([
            station_id_counter,
            station_name,
            zone['id'],
            round(lat_sub, 6),
            round(lng_sub, 6),
            phone_sub,
            sub_type,
            personnel,
            has_lockup
        ])
        station_id_counter += 1

# ==========================================
# 💾 SAVE TO CSV
# ==========================================
columns = [
    "id", 
    "station_name", 
    "zone_id", 
    "latitude", 
    "longitude", 
    "contact_number", 
    "station_type", 
    "personnel_count", 
    "has_lockup"
]

df = pd.DataFrame(data, columns=columns)
df.to_csv(FILENAME, index=False)

print(f"✅ Success! Generated {len(df)} stations in '{FILENAME}'")
print(df.head())