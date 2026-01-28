"""
Script to generate predictions and patrol suggestions for all zones
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, Base
from models.zone import Zone
from models.crime import Crime
from models.prediction import Prediction
from models.patrol_suggestion import PatrolSuggestion
import random
from services.crime_service import CrimeAIService

# Unique suggestion templates for each zone type
HIGH_RISK_SUGGESTIONS = [
    "Deploy additional patrol units during peak hours (8PM-2AM). Install mobile CCTV units at key intersections. Coordinate with local businesses for real-time incident reporting.",
    "Increase foot patrol frequency by 50%. Establish temporary police checkpoints during weekends. Partner with neighborhood watch groups for enhanced surveillance.",
    "Station dedicated response team within zone. Implement predictive patrol routes based on historical crime patterns. Deploy plainclothes officers in hotspot areas.",
    "Activate rapid response protocol with 5-minute response target. Install additional street lighting in dark zones. Conduct regular business security audits.",
    "Deploy drone surveillance during night hours. Establish mobile command center for real-time coordination. Increase visible police presence at transit points.",
    "Implement 24/7 patrol coverage with overlapping shifts. Partner with private security firms for extended coverage. Install panic buttons in high-traffic commercial areas.",
]

MEDIUM_RISK_SUGGESTIONS = [
    "Maintain enhanced patrol schedule with focus on evening hours. Conduct monthly community safety meetings. Review and update emergency response protocols.",
    "Increase patrol visibility during morning and evening rush hours. Collaborate with local schools for safety awareness programs. Monitor social media for early threat detection.",
    "Implement beat policing strategy with dedicated officers. Establish communication channels with residential associations. Conduct periodic safety drills.",
    "Focus patrols on identified micro-hotspots. Partner with metro/transit authorities for coordinated security. Install community alert systems.",
    "Deploy bicycle patrol units for better street coverage. Establish direct hotline with local business owners. Conduct regular risk assessments.",
    "Rotate patrol patterns to prevent predictability. Engage youth through community outreach programs. Monitor ATM and bank areas during business hours.",
]

LOW_RISK_SUGGESTIONS = [
    "Maintain standard patrol frequency. Continue community engagement initiatives. Monitor for any emerging crime patterns.",
    "Conduct routine patrols with emphasis on visibility. Support neighborhood watch activities. Keep emergency response times optimal.",
    "Focus on preventive measures and community relations. Organize periodic safety awareness campaigns. Maintain readiness for rapid deployment if needed.",
    "Regular patrol schedule sufficient. Prioritize building relationships with residents. Stay vigilant for any unusual activities.",
    "Standard patrol coverage adequate. Continue positive community interactions. Monitor zone for any changes in crime trends.",
    "Maintain presence through regular drive-throughs. Support local events with security presence. Keep communication channels open with community leaders.",
]

def generate_predictions_for_zones(db: Session):
    """Generate predictions for all zones with unique suggestions"""
    
    # Clear existing predictions and suggestions
    db.query(PatrolSuggestion).delete()
    db.query(Prediction).delete()
    db.commit()
    print("Cleared existing predictions and suggestions.")
    
    zones = db.query(Zone).all()
    
    if not zones:
        print("No zones found in database. Please import zones first.")
        return
    
    print(f"Found {len(zones)} zones. Generating predictions...")
    
    suggestion_index = {"High": 0, "Medium": 0, "Low": 0}
    
    for zone in zones:
        # Count crimes in this zone
        crime_count = db.query(Crime).filter(Crime.zone_id == zone.id).count()
        
        # Calculate risk based on crime density
        if crime_count == 0:
            risk_level = "Low"
            risk_score = random.uniform(0.1, 0.3)
            expected_crimes = random.randint(0, 2)
        elif crime_count < 50:
            risk_level = random.choice(["Low", "Medium"])
            risk_score = random.uniform(0.3, 0.5)
            expected_crimes = random.randint(2, 8)
        elif crime_count < 200:
            risk_level = random.choice(["Medium", "High"])
            risk_score = random.uniform(0.5, 0.75)
            expected_crimes = random.randint(8, 20)
        else:
            risk_level = "High"
            risk_score = random.uniform(0.75, 1.0)
            expected_crimes = random.randint(15, 35)
        
        # Generate prediction for this zone (single prediction per zone)
        future_date = datetime.now() + timedelta(days=30)
        predicted_month = f"{future_date.year}-{future_date.month:02d}"
        
        prediction = Prediction(
            zone_id=zone.id,
            predicted_month=predicted_month,
            risk_level=risk_level,
            risk_score=risk_score,
            expected_crimes=expected_crimes,
            generated_at=datetime.now()
        )
        db.add(prediction)
        db.flush()  # Get the ID
        
        # Get unique suggestion for this zone
        if risk_level == "High":
            suggestions_list = HIGH_RISK_SUGGESTIONS
            idx = suggestion_index["High"] % len(suggestions_list)
            suggestion_index["High"] += 1
        elif risk_level == "Medium":
            suggestions_list = MEDIUM_RISK_SUGGESTIONS
            idx = suggestion_index["Medium"] % len(suggestions_list)
            suggestion_index["Medium"] += 1
        else:
            suggestions_list = LOW_RISK_SUGGESTIONS
            idx = suggestion_index["Low"] % len(suggestions_list)
            suggestion_index["Low"] += 1
        
        suggestion_text = f"{zone.zone_name}: {suggestions_list[idx]}"
        
        suggestion = PatrolSuggestion(
            zone_id=zone.id,
            risk_level=risk_level,
            suggestion_text=suggestion_text,
            prediction_id=prediction.id
        )
        db.add(suggestion)
        print(f"Created: {zone.zone_name} - {risk_level} risk (crimes: {crime_count})")
    
    db.commit()
    print("✅ All predictions generated successfully!")

def main():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = Session(engine)
    
    try:
        generate_predictions_for_zones(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
