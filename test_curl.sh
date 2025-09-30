API_URL="https://your-app-name.onrender.com"

echo "🚀 Testing Open Meteo ML API"
echo "=============================="

echo "🏥 Testing Health..."
curl -X GET "$API_URL/health/" | jq .

echo -e "\n📋 Testing Root Endpoint..."
curl -X GET "$API_URL/" | jq .

echo -e "\n🌧️ Testing Rain Prediction..."
curl -X GET "$API_URL/predict/rain/?date=2024-01-15" | jq .

echo -e "\n💧 Testing Precipitation Prediction..."
curl -X GET "$API_URL/predict/precipitation/fall/?date=2024-01-15" | jq .

echo -e "\n✅ Tests complete!"
