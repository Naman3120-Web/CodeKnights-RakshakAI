import pandas as pd
import random

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
FILENAME = "patrol_suggestions.csv"

# We load predictions manually or simulate the link
# For this script, we assume the same structure as above (12 zones)
zones_info = [
    (1, "High", "Colaba"), (2, "High", "Bandra"), (3, "Medium", "Andheri"), 
    (4, "High", "Dadar"), (5, "Medium", "Kurla"), (6, "Medium", "Highway"), 
    (7, "Low", "Borivali"), (8, "Medium", "Juhu"), (9, "Low", "Powai"), 
    (10, "Medium", "Chembur"), (11, "Medium", "Malad"), (12, "High", "Lower Parel")
]

suggestions_pool = {
    "High": [
        "Deploy static patrol units at main market entry points between 10 AM and 8 PM.",
        "Increase bike patrols during evening peak hours (6 PM - 10 PM) to deter theft.",
        "Set up temporary checkpoints to monitor vehicle movement post-midnight.",
        "Crowd control measures recommended near station areas during rush hour."
    ],
    "Medium": [
        "Conduct spot checks at entry points during late evening shifts.",
        "Enhance night patrolling (11 PM - 3 AM) in secluded pockets.",
        "Station traffic interceptors to monitor speeding on main roads.",
        "Increase visibility near bus depots and rickshaw stands."
    ],
    "Low": [
        "Maintain standard beat marshall rounds; no specific surge required.",
        "Focus on community engagement and awareness drives.",
        "Routine surveillance of public parks and playgrounds."
    ]
}

data = []
prediction_id_start = 101

for i, (zone_id, risk, area) in enumerate(zones_info):
    # Pick a random suggestion appropriate for the risk level
    text = random.choice(suggestions_pool[risk])
    
    # Customize text slightly for realism
    if "market" in text and risk == "High":
        text = text.replace("market", f"{area} Market")
    
    data.append([
        500 + i + 1,      # ID
        zone_id,
        risk,
        text,
        prediction_id_start + i  # Link to prediction ID
    ])

df = pd.DataFrame(data, columns=["id", "zone_id", "risk_level", "suggestion_text", "prediction_id"])
df.to_csv(FILENAME, index=False)
print(f"✅ Generated patrol suggestions in '{FILENAME}'")