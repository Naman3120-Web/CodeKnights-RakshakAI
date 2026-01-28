import csv
from datetime import datetime
from database import SessionLocal, engine, Base
from models.zone import Zone, AreaType
from models.crime import Crime, CrimeType
from models.crime_stat import CrimeStat
from models.police_stations import PoliceStation, StationType

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Path to your CSV files
CSV_FOLDER = "csv_files"

def parse_datetime(date_str: str) -> datetime:
    """Parse datetime from various formats"""
    formats = [
        "%Y-%m-%dT%H:%M:%S",  # ISO format: 2025-01-27T01:03:56
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse date: {date_str}")

def map_area_type(area_type_str: str) -> AreaType:
    """Map CSV area types to AreaType enum"""
    mapping = {
        "residential": AreaType.RESIDENTIAL,
        "market": AreaType.MARKET,
        "highway": AreaType.HIGHWAY,
        # Map additional types to closest match
        "commercial": AreaType.MARKET,      # commercial → market
        "industrial": AreaType.HIGHWAY,     # industrial → highway (or add to enum)
    }
    return mapping.get(area_type_str.lower(), AreaType.RESIDENTIAL)

def map_crime_type(crime_type_str: str) -> CrimeType:
    """Map CSV crime types to CrimeType enum"""
    mapping = {
        "theft": CrimeType.THEFT,
        "assault": CrimeType.ASSAULT,
        "accident": CrimeType.ACCIDENT,
    }
    return mapping.get(crime_type_str.lower(), CrimeType.THEFT)

def map_station_type(station_type_str: str) -> StationType:
    """Map CSV station types to StationType enum"""
    mapping = {
        "main station": StationType.MAIN_STATION,
        "traffic division": StationType.TRAFFIC_DIVISION,
        "chowki (outpost)": StationType.CHOWKI,
    }
    return mapping.get(station_type_str.lower(), StationType.MAIN_STATION)

def clear_tables(db):
    """Clear existing data (optional)"""
    db.query(CrimeStat).delete()
    db.query(Crime).delete()
    db.query(PoliceStation).delete()  # Add this line
    db.query(Zone).delete()
    db.commit()
    print("🗑️  Cleared existing data")

def import_zones(db):
    """Import zones from CSV"""
    csv_path = f"{CSV_FOLDER}/zones.csv"
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            zone = Zone(
                id=int(row['id']),
                zone_name=row['zone_name'],
                center_lat=float(row['center_lat']),
                center_lng=float(row['center_lng']),
                radius=int(row['radius']),
                area_type=map_area_type(row['area_type'])
            )
            db.add(zone)
            count += 1
    
    db.commit()
    print(f"✅ Imported {count} zones")

def import_crimes(db):
    """Import crimes from CSV"""
    csv_path = f"{CSV_FOLDER}/crime.csv"
    count = 0
    batch_size = 500  # Commit every 500 records for large files
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            crime = Crime(
                id=int(row['id']),
                crime_type=map_crime_type(row['crime_type']),
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                date_time=parse_datetime(row['date_time']),
                area_name=row['area_name'],
                zone_id=int(row['zone_id'])
            )
            db.add(crime)
            count += 1
            
            # Batch commit for performance
            if count % batch_size == 0:
                db.commit()
                print(f"   ... imported {count} crimes")
    
    db.commit()
    print(f"✅ Imported {count} crimes")

def import_crime_stats(db):
    """Import crime stats from CSV"""
    csv_path = f"{CSV_FOLDER}/crime_stats.csv"
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            stat = CrimeStat(
                id=int(row['id']),
                zone_id=int(row['zone_id']),
                crime_type=map_crime_type(row['crime_type']),
                crime_count=int(row['crime_count']),
                start_date=parse_datetime(row['start_date']),
                end_date=parse_datetime(row['end_date'])
            )
            db.add(stat)
            count += 1
    
    db.commit()
    print(f"✅ Imported {count} crime stats")

def import_police_stations(db):
    """Import police stations from CSV"""
    csv_path = f"{CSV_FOLDER}/police_stations.csv"
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station = PoliceStation(
                id=int(row['id']),
                station_name=row['station_name'],
                zone_id=int(row['zone_id']),
                latitude=float(row['latitude']),
                longitude=float(row['longitude']),
                contact_number=row['contact_number'],
                station_type=map_station_type(row['station_type']),
                personnel_count=int(row['personnel_count']),
                has_lockup=row['has_lockup'].lower() == 'true'
            )
            db.add(station)
            count += 1
    
    db.commit()
    print(f"✅ Imported {count} police stations")

def main():
    """Main import function"""
    print("\n🚀 Starting CSV Import for Rakshak AI...\n")
    
    db = SessionLocal()
    
    try:
        # Optional: Clear existing data first
        clear_tables(db)
        
        # Import in order (zones first due to foreign keys)
        import_zones(db)
        import_crimes(db)
        import_crime_stats(db)
        import_police_stations(db)  # Add this line
        
        print("\n✅ All imports completed successfully!")
        print(f"\n📊 Database: rakshak_ai.db")
        
    except Exception as e:
        print(f"\n❌ Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()