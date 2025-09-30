$API_URL = "https://your-app-name.onrender.com"

Write-Host "🚀 Testing Open Meteo ML API" -ForegroundColor Green
Write-Host "==============================" -ForegroundColor Green

Write-Host "🏥 Testing Health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$API_URL/health/" -Method GET
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
    Write-Host "✅ Health check passed!" -ForegroundColor Green
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n📋 Testing Root Endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$API_URL/" -Method GET
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
    Write-Host "✅ Root endpoint working!" -ForegroundColor Green
} catch {
    Write-Host "❌ Root endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🌧️ Testing Rain Prediction..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$API_URL/predict/rain/?date=2024-01-15" -Method GET
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
    Write-Host "✅ Rain prediction successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Rain prediction failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n💧 Testing Precipitation Prediction..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "$API_URL/predict/precipitation/fall/?date=2024-01-15" -Method GET
    Write-Host "Status: $($response.StatusCode)"
    Write-Host "Response: $($response.Content)"
    Write-Host "✅ Precipitation prediction successful!" -ForegroundColor Green
} catch {
    Write-Host "❌ Precipitation prediction failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n🎉 API Testing Complete!" -ForegroundColor Green
