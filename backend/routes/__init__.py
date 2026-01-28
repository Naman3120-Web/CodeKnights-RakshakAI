from routes.zones import router as zones_router
from routes.crimes import router as crimes_router
from routes.predictions import router as predictions_router
from routes.patrol_suggestions import router as patrol_suggestions_router
from routes.crime_stats import router as crime_stats_router
from routes.police_stations import router as police_stations_router

__all__ = [
    "zones_router",
    "crimes_router",
    "predictions_router",
    "patrol_suggestions_router",
    "crime_stats_router",
    "police_stations_router",
]