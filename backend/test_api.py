"""
Test script to verify all backend API endpoints
Run this after starting the backend server
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_test_result(test_name, success, data=None):
    """Pretty print test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"\n{status} - {test_name}")
    if data:
        print(f"Response: {json.dumps(data, indent=2, default=str)[:200]}...")

def test_health_check():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        success = response.status_code == 200 and response.json().get("status") == "healthy"
        print_test_result("Health Check", success, response.json())
        return success
    except Exception as e:
        print_test_result("Health Check", False, {"error": str(e)})
        return False

def test_get_crimes():
    """Test GET /api/crimes"""
    try:
        response = requests.get(f"{BASE_URL}/api/crimes", params={"limit": 5})
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Crimes", success, data)
        return success, data
    except Exception as e:
        print_test_result("GET Crimes", False, {"error": str(e)})
        return False, None

def test_get_zones():
    """Test GET /api/zones"""
    try:
        response = requests.get(f"{BASE_URL}/api/zones", params={"limit": 5})
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Zones", success, data)
        return success, data
    except Exception as e:
        print_test_result("GET Zones", False, {"error": str(e)})
        return False, None

def test_get_crimes_by_type():
    """Test GET /api/crimes/type/{type}"""
    try:
        response = requests.get(f"{BASE_URL}/api/crimes/type/theft")
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Crimes by Type (theft)", success, data)
        return success
    except Exception as e:
        print_test_result("GET Crimes by Type", False, {"error": str(e)})
        return False

def test_get_predictions():
    """Test GET /api/predictions"""
    try:
        response = requests.get(f"{BASE_URL}/api/predictions", params={"limit": 5})
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Predictions", success, data)
        return success, data
    except Exception as e:
        print_test_result("GET Predictions", False, {"error": str(e)})
        return False, None

def test_get_patrol_suggestions():
    """Test GET /api/patrol-suggestions"""
    try:
        response = requests.get(f"{BASE_URL}/api/patrol-suggestions", params={"limit": 5})
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Patrol Suggestions", success, data)
        return success, data
    except Exception as e:
        print_test_result("GET Patrol Suggestions", False, {"error": str(e)})
        return False, None

def test_get_crime_stats():
    """Test GET /api/crime-stats"""
    try:
        response = requests.get(f"{BASE_URL}/api/crime-stats", params={"limit": 5})
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Crime Stats", success, data)
        return success, data
    except Exception as e:
        print_test_result("GET Crime Stats", False, {"error": str(e)})
        return False, None

def test_create_crime(zone_id=1):
    """Test POST /api/crimes"""
    try:
        crime_data = {
            "crime_type": "theft",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "date_time": datetime.now().isoformat(),
            "area_name": "Test Area",
            "zone_id": zone_id
        }
        response = requests.post(f"{BASE_URL}/api/crimes", json=crime_data)
        success = response.status_code == 201
        data = response.json() if success else None
        print_test_result("POST Create Crime", success, data)
        return success, data
    except Exception as e:
        print_test_result("POST Create Crime", False, {"error": str(e)})
        return False, None

def test_crime_stats_by_zone():
    """Test GET /api/crimes/stats/by-zone"""
    try:
        response = requests.get(f"{BASE_URL}/api/crimes/stats/by-zone")
        success = response.status_code == 200
        data = response.json() if success else None
        print_test_result("GET Crime Stats by Zone", success, data)
        return success
    except Exception as e:
        print_test_result("GET Crime Stats by Zone", False, {"error": str(e)})
        return False

def run_all_tests():
    """Run all API tests"""
    print("=" * 60)
    print("🧪 SafeCity Backend API Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Health Check
    results.append(test_health_check())
    
    # Test 2: Get Zones
    zones_success, zones_data = test_get_zones()
    results.append(zones_success)
    
    # Test 3: Get Crimes
    crimes_success, crimes_data = test_get_crimes()
    results.append(crimes_success)
    
    # Test 4: Get Crimes by Type
    results.append(test_get_crimes_by_type())
    
    # Test 5: Get Predictions
    pred_success, pred_data = test_get_predictions()
    results.append(pred_success)
    
    # Test 6: Get Patrol Suggestions
    patrol_success, patrol_data = test_get_patrol_suggestions()
    results.append(patrol_success)
    
    # Test 7: Get Crime Stats
    stats_success, stats_data = test_get_crime_stats()
    results.append(stats_success)
    
    # Test 8: Crime Stats by Zone
    results.append(test_crime_stats_by_zone())
    
    # Test 9: Create Crime (if zones exist)
    if zones_data and len(zones_data) > 0:
        create_success, create_data = test_create_crime(zones_data[0]["id"])
        results.append(create_success)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Test Summary: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if sum(results) == len(results):
        print("🎉 All tests passed! Backend is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return sum(results) == len(results)

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
