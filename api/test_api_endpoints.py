# Test API Endpoints
# Validates all v0.6 endpoints work end-to-end

import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8001"

def test_health():
    """Test health endpoint"""
    print("\n1. Testing GET /health...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.6.0"
    print(f"   [OK] Health check passed (version {data['version']})")

def test_scrape():
    """Test scraping endpoint"""
    print("\n2. Testing POST /scrape...")
    response = requests.post(f"{BASE_URL}/scrape?days=7")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total_articles" in data
    assert "by_source" in data
    print(f"   [OK] Scraping completed ({data['total_articles']} articles)")
    return data

def test_synthesize():
    """Test synthesis endpoint"""
    print("\n3. Testing POST /synthesize...")
    response = requests.post(f"{BASE_URL}/synthesize?region=Europe/Africa")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "briefing" in data
    assert data["briefing"]["region"] == "Europe/Africa"
    assert "bluf" in data["briefing"]
    assert len(data["briefing"]["sections"]) > 0
    print(f"   [OK] Briefing synthesized ({len(data['briefing']['sections'])} sections)")
    return data

def test_get_latest():
    """Test get latest briefing endpoint"""
    print("\n4. Testing GET /briefing/latest...")
    response = requests.get(f"{BASE_URL}/briefing/latest?region=Europe/Africa")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "briefing" in data
    print(f"   [OK] Latest briefing retrieved")
    return data

def test_generate_pdf():
    """Test PDF generation endpoint"""
    print("\n5. Testing POST /briefing/generate-pdf...")
    response = requests.post(f"{BASE_URL}/briefing/generate-pdf?region=Europe/Africa")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "pdf_path" in data
    print(f"   [OK] PDF generated: {data['pdf_path']}")
    return data

def test_get_pdf():
    """Test PDF serving endpoint"""
    print("\n6. Testing GET /briefing/latest/pdf...")
    response = requests.get(f"{BASE_URL}/briefing/latest/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000  # PDF should be > 1KB
    pdf_size_kb = len(response.content) / 1024
    print(f"   [OK] PDF served ({pdf_size_kb:.1f} KB)")
    return response

def main():
    print("=" * 60)
    print("SITREP API v0.6 - End-to-End Test")
    print("=" * 60)

    try:
        test_health()
        test_scrape()
        test_synthesize()
        test_get_latest()
        test_generate_pdf()
        test_get_pdf()

        print("\n" + "=" * 60)
        print("[OK] All API endpoints working correctly")
        print("=" * 60)
        print("\nv0.6 Backend API: READY FOR APPROVAL")

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        raise
    except requests.exceptions.ConnectionError:
        print("\n[FAIL] Could not connect to API server")
        print("   Make sure the server is running: python -m uvicorn main:app --port 8001")
        raise

if __name__ == "__main__":
    main()
