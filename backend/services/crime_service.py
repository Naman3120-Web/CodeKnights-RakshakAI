from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from models.crime import Crime, CrimeType
from schemas.crime import CrimeCreate, CrimeUpdate
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
import google.genai as genai
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables with explicit path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class CrimeAIService:
    """
    AI/ML Service for crime prediction and analysis
    """
    
    def __init__(self):
        self.kmeans = None
        self.model_rf = None
        self.hotspot_cluster_id = None
        self.is_trained = False
        self._init_gemini()
    
    def _init_gemini(self):
        """Initialize Gemini AI client"""
        api_key = os.getenv("gemini_api_key")
        if api_key:
            self.gemini_client = genai.Client(api_key=api_key)
        else:
            self.gemini_client = None
    
    def train_models(self, db: Session) -> bool:
        """Train ML models using crime data from database"""
        # Fetch all crimes from database
        crimes = db.query(Crime).all()
        
        if len(crimes) < 10:  # Need minimum data to train
            return False
        
        # Convert to DataFrame
        data = [{
            'id': c.id,
            'latitude': c.latitude,
            'longitude': c.longitude,
            'date_time': c.date_time,
            'crime_type': c.crime_type.value if c.crime_type is not None else None,
            'area_name': c.area_name,
            'zone_id': c.zone_id
        } for c in crimes]
        
        df = pd.DataFrame(data)
        
        # Parse date_time to extract hour, day, month
        df['date_time'] = pd.to_datetime(df['date_time'])
        df['hour'] = df['date_time'].apply(lambda x: x.hour)
        df['day'] = df['date_time'].apply(lambda x: x.day)
        df['month'] = df['date_time'].apply(lambda x: x.month)
        
        # KMeans clustering for hotspot detection
        n_clusters = min(3, len(df))  # Ensure we don't have more clusters than data points
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        df["hotspot_cluster"] = self.kmeans.fit_predict(df[["latitude", "longitude"]])
        
        # Identify hotspot cluster (most frequent)
        self.hotspot_cluster_id = df["hotspot_cluster"].value_counts().idxmax()
        
        # Define risk based on hour (night time = high risk)
        df["risk"] = df["hour"].apply(lambda h: 1 if (h >= 20 or h <= 4) else 0)
        
        # Train Random Forest classifier
        X = df[["latitude", "longitude", "hour", "day", "month", "hotspot_cluster"]]
        y = df["risk"]
        
        self.model_rf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model_rf.fit(X, y)
        
        self.is_trained = True
        return True
    
    def predict_risk(
        self,
        latitude: float,
        longitude: float,
        hour: int,
        day: int,
        month: int
    ) -> Dict[str, Any]:
        """Predict risk level for a given location and time"""
        if not self.is_trained or self.kmeans is None or self.model_rf is None:
            raise HTTPException(
                status_code=400, 
                detail="Models not trained. Call train_models first."
            )
        
        # Predict cluster for the location
        assert self.kmeans is not None
        assert self.model_rf is not None
        sample_cluster = self.kmeans.predict([[latitude, longitude]])[0]
        
        # Predict risk
        risk_pred = self.model_rf.predict([[
            latitude,
            longitude,
            hour,
            day,
            month,
            sample_cluster
        ]])[0]
        
        # Build date_time string
        date_time = f"2026-{month:02d}-{day:02d}T{hour:02d}:00:00"
        
        return {
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "time": {
                "hour": hour,
                "day": day,
                "month": month
            },
            "date_time": date_time,
            "hotspot": bool(sample_cluster == self.hotspot_cluster_id),
            "risk_level": "High Risk" if risk_pred == 1 else "Low Risk"
        }
    
    def analyze_crime(
        self,
        area: str,
        latitude: float,
        longitude: float,
        hour: int,
        day: int,
        month: int,
        crime_type: str
    ) -> Dict[str, Any]:
        """Full crime analysis with ML prediction"""
        if not self.is_trained:
            raise HTTPException(
                status_code=400,
                detail="Models not trained. Call train_models first."
            )
        
        # Predict cluster
        assert self.kmeans is not None
        assert self.model_rf is not None
        sample_cluster = self.kmeans.predict([[latitude, longitude]])[0]
        
        # Predict risk
        risk_pred = self.model_rf.predict([[
            latitude,
            longitude,
            hour,
            day,
            month,
            sample_cluster
        ]])[0]
        
        date_time = f"2026-{month:02d}-{day:02d}T{hour:02d}:00:00"
        
        return {
            "area": area,
            "coordinates": {
                "latitude": latitude,
                "longitude": longitude
            },
            "time": {
                "hour": hour,
                "day": day,
                "month": month
            },
            "date_time": date_time,
            "crime_type": crime_type,
            "hotspot": bool(sample_cluster == self.hotspot_cluster_id),
            "risk_level": "High Risk" if risk_pred == 1 else "Low Risk"
        }
    
    def get_patrol_suggestions(
        self,
        latitude: float,
        longitude: float,
        area: str,
        crime_type: str
    ) -> Dict[str, Any]:
        """Get AI-powered patrol suggestions using Gemini"""
        if not self.gemini_client:
            raise HTTPException(
                status_code=500,
                detail="Gemini API not configured. Set gemini_api_key in .env"
            )
        
        prompt = f"""
Analyze the provided area to generate a crime prevention strategy and predictive assessment.

Area: {area}
Coordinates: ({latitude}, {longitude})
Recent Crime Type: {crime_type}

### **Patrolling & Risk Assessment**

* **Strategy:** Define patrol frequency, timing, and focus points based on risk levels and crime types.
* **Probability:** Rate the likelihood of the next incident (**Low/Medium/High**) for the next hour, 24 hours, and week.

### **Infrastructure & Prediction**

* **CCTV:** Recommend specific, realistic installation points (junctions/access paths) near the coordinates.
* **Location Prediction:** Identify the most likely coordinates for the next incident based on proximity and historical patterns.

### **Output Format**

Return **only** a JSON object with the following keys:

* `latitude`: [Predicted Lat]
* `longitude`: [Predicted Long]
* `expected_crime_time_window`: [Estimated timeframe]
* `suggestions`: [A list of 5-6 professional prevention points]

**Constraint:** No conversational filler; provide the JSON only.
"""
        
        response = None
        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            # Parse response - attempt to extract JSON
            if not response or not response.text:
                raise ValueError("Empty response from Gemini API")
            
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            
            return json.loads(response_text)
        except json.JSONDecodeError:
            return {"raw_response": response.text if response else "No response"}
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error with Gemini API: {str(e)}"
            )


# Singleton instance of AI service
crime_ai_service = CrimeAIService()


class CrimeService:
    """
    Service class for Crime business logic
    Similar to @Service in Spring Boot
    """
    
    # ========== CRUD Operations ==========
    
    @staticmethod
    def get_by_id(db: Session, crime_id: int) -> Crime:
        """Get crime by ID"""
        crime = db.query(Crime).filter(Crime.id == crime_id).first()
        if not crime:
            raise HTTPException(status_code=404, detail="Crime record not found")
        return crime
    
    @staticmethod
    def get_all(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Crime]:
        """Get all crimes with pagination"""
        return db.query(Crime).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, crime_data: CrimeCreate) -> Crime:
        """Create new crime record"""
        crime = Crime(
            crime_type=crime_data.crime_type,
            latitude=crime_data.latitude,
            longitude=crime_data.longitude,
            date_time=crime_data.date_time,
            area_name=crime_data.area_name,
            zone_id=crime_data.zone_id
        )
        db.add(crime)
        db.commit()
        db.refresh(crime)
        return crime
    
    @staticmethod
    def update(db: Session, crime_id: int, crime_data: CrimeUpdate) -> Crime:
        """Update existing crime record"""
        crime = CrimeService.get_by_id(db, crime_id)
        
        # Update only provided fields
        update_data = crime_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(crime, field, value)
        
        db.commit()
        db.refresh(crime)
        return crime
    
    @staticmethod
    def delete(db: Session, crime_id: int) -> Crime:
        """Delete crime record"""
        crime = CrimeService.get_by_id(db, crime_id)
        db.delete(crime)
        db.commit()
        return crime
    
    # ========== Business Logic ==========
    
    @staticmethod
    def get_by_zone(
        db: Session, 
        zone_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Crime]:
        """Get all crimes in a specific zone"""
        return db.query(Crime)\
            .filter(Crime.zone_id == zone_id)\
            .offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_type(
        db: Session, 
        crime_type: CrimeType
    ) -> List[Crime]:
        """Get crimes filtered by type"""
        return db.query(Crime)\
            .filter(Crime.crime_type == crime_type).all()
    
    @staticmethod
    def get_recent(
        db: Session, 
        days: int = 30
    ) -> List[Crime]:
        """Get crimes from last N days"""
        since_date = datetime.now() - timedelta(days=days)
        return db.query(Crime)\
            .filter(Crime.date_time >= since_date)\
            .order_by(Crime.date_time.desc()).all()
    
    @staticmethod
    def get_crime_count_by_zone(db: Session) -> List[dict]:
        """Get crime count grouped by zone"""
        results = db.query(
            Crime.zone_id,
            func.count(Crime.id).label("count")
        ).group_by(Crime.zone_id).all()
        
        return [{"zone_id": r.zone_id, "count": r.count} for r in results]
    
    @staticmethod
    def get_crimes_in_radius(
        db: Session,
        lat: float,
        lng: float,
        radius_km: float = 1.0
    ) -> List[Crime]:
        """Get crimes within a radius (simplified calculation)"""
        # Approximate degree to km conversion
        lat_range = radius_km / 111.0
        lng_range = radius_km / 85.0  # Approximate for Mumbai's latitude
        
        return db.query(Crime).filter(
            Crime.latitude.between(lat - lat_range, lat + lat_range),
            Crime.longitude.between(lng - lng_range, lng + lng_range)
        ).all()
    
    # ========== AI/ML Operations ==========
    
    @staticmethod
    def train_ai_models(db: Session) -> Dict[str, Any]:
        """Train AI models with current crime data"""
        success = crime_ai_service.train_models(db)
        if success:
            return {"status": "success", "message": "Models trained successfully"}
        return {"status": "error", "message": "Insufficient data to train models"}
    
    @staticmethod
    def predict_crime_risk(
        latitude: float,
        longitude: float,
        hour: int,
        day: int,
        month: int
    ) -> Dict[str, Any]:
        """Predict crime risk for a location and time"""
        return crime_ai_service.predict_risk(latitude, longitude, hour, day, month)
    
    @staticmethod
    def analyze_crime_report(
        area: str,
        latitude: float,
        longitude: float,
        hour: int,
        day: int,
        month: int,
        crime_type: str
    ) -> Dict[str, Any]:
        """Full ML analysis of a crime report"""
        return crime_ai_service.analyze_crime(
            area, latitude, longitude, hour, day, month, crime_type
        )
    
    @staticmethod
    def get_ai_patrol_suggestions(
        latitude: float,
        longitude: float,
        area: str,
        crime_type: str
    ) -> Dict[str, Any]:
        """Get AI-powered patrol suggestions"""
        return crime_ai_service.get_patrol_suggestions(
            latitude, longitude, area, crime_type
        )