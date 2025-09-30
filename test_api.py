
import requests
import json
from datetime import date, timedelta

API_BASE_URL = "https://ml-api-rqhj.onrender.com"

def test_health():
    print("🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("✅ Health check passed!\n")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}\n")
        return False

def test_root():
    print("📋 Testing Root Endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Root endpoint working!\n")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}\n")
        return False

def test_rain_prediction(test_date):
    print(f"🌧️ Testing Rain Prediction for {test_date}...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/predict/rain/",
            params={"date": test_date}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Rain prediction successful!\n")
        return True
    except Exception as e:
        print(f"❌ Rain prediction failed: {e}\n")
        return False

def test_precipitation_prediction(test_date):
    print(f"💧 Testing Precipitation Prediction for {test_date}...")
    try:
        response = requests.get(
            f"{API_BASE_URL}/predict/precipitation/fall/",
            params={"date": test_date}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print("✅ Precipitation prediction successful!\n")
        return True
    except Exception as e:
        print(f"❌ Precipitation prediction failed: {e}\n")
        return False

def main():
    print("🚀 Starting Open Meteo ML API Tests\n")
    print("=" * 50)
    
    today = date.today()
    test_dates = [
        today.isoformat(),
        (today - timedelta(days=1)).isoformat(),
        (today - timedelta(days=7)).isoformat(),
    ]
    health_ok = test_health()
    root_ok = test_root()
    
    if not health_ok or not root_ok:
        print("❌ Basic endpoints failed. Check your deployment URL and try again.")
        return
    
    print("🧪 Running Prediction Tests...")
    print("=" * 30)
    
    for test_date in test_dates:
        print(f"\n📅 Testing Date: {test_date}")
        print("-" * 25)
        
        rain_ok = test_rain_prediction(test_date)
        
        precip_ok = test_precipitation_prediction(test_date)
        
        if rain_ok and precip_ok:
            print(f"✅ All tests passed for {test_date}!")
        else:
            print(f"❌ Some tests failed for {test_date}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")

if __name__ == "__main__":
    main()
