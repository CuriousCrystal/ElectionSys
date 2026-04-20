"""
Test script to verify the new features are working correctly
"""
import requests
import time

BASE_URL = "http://localhost:8000"

def test_authentication():
    print("\n=== Testing Authentication ===")
    
    # Test login with admin
    response = requests.post(f"{BASE_URL}/api/auth/login", data={
        "username": "admin",
        "password": "admin123"
    })
    
    if response.status_code == 200:
        print("✓ Admin login successful")
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test get current user
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        if response.status_code == 200:
            print(f"✓ Retrieved user info: {response.json()['full_name']} ({response.json()['role']})")
        else:
            print("✗ Failed to get user info")
        
        return token
    else:
        print("✗ Admin login failed")
        return None

def test_zones(token):
    print("\n=== Testing Zone Data ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/zones", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Retrieved {len(data['zones'])} zones")
        for zone_name, zone_data in data['zones'].items():
            print(f"  - {zone_name}: {zone_data['status']} (Density: {zone_data['density']}%, Wait: {zone_data['wait_time']}min)")
    else:
        print("✗ Failed to get zone data")

def test_recommendations(token):
    print("\n=== Testing Recommendations ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/recommendations", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Best gate: {data['best_gate']['name']} (Wait: {data['best_gate']['wait_time']}min)")
        print(f"✓ Best restroom: {data['best_restroom']['name']} (Wait: {data['best_restroom']['wait_time']}min)")
    else:
        print("✗ Failed to get recommendations")

def test_alerts():
    print("\n=== Testing Alerts ===")
    
    # Test recent alerts (no auth required)
    response = requests.get(f"{BASE_URL}/api/alerts/recent")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Retrieved {data['count']} recent alerts")
    else:
        print("✗ Failed to get recent alerts")
    
    # Test unread count
    response = requests.get(f"{BASE_URL}/api/alerts/unread-count")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Unread alerts: {data['unread_count']}")
    else:
        print("✗ Failed to get unread count")

def test_analytics(token):
    print("\n=== Testing Analytics ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Wait a bit for data to accumulate
    print("Waiting for data collection...")
    time.sleep(10)
    
    # Test zone history
    response = requests.get(f"{BASE_URL}/api/analytics/zones/history?hours=1", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Retrieved {data['data_points']} historical data points")
    else:
        print("✗ Failed to get zone history")
    
    # Test zone report
    response = requests.get(f"{BASE_URL}/api/analytics/zones/report?hours=1", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Generated report for {len(data['zones'])} zones")
    else:
        print("✗ Failed to generate report")
    
    # Test alerts summary
    response = requests.get(f"{BASE_URL}/api/analytics/alerts/summary?hours=1", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Alert summary: {data['total_alerts']} total, {data['unread_alerts']} unread")
    else:
        print("✗ Failed to get alert summary")

def main():
    print("Starting Event Management System Tests...")
    print(f"Testing against: {BASE_URL}")
    
    # Wait for server to be ready
    print("\nWaiting for server to be ready...")
    time.sleep(3)
    
    # Test authentication
    token = test_authentication()
    
    if not token:
        print("\n✗ Authentication failed. Stopping tests.")
        return
    
    # Test zones
    test_zones(token)
    
    # Test recommendations
    test_recommendations(token)
    
    # Test alerts
    test_alerts()
    
    # Test analytics
    test_analytics(token)
    
    print("\n=== Tests Complete ===")
    print("Check the API documentation at http://localhost:8000/docs for more details")

if __name__ == "__main__":
    main()
