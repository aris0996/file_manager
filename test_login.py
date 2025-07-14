#!/usr/bin/env python3
"""
Test login functionality for File Manager & Terminal
"""

import requests
import hashlib
import json
import time

def test_login(base_url, username, password):
    """Test login functionality"""
    session = requests.Session()
    
    print(f"\nTesting login: {username} / {password}")
    print("-" * 50)
    
    # Get login page
    try:
        print("1. Accessing login page...")
        response = session.get(f"{base_url}/login")
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Cannot access login page: {response.status_code}")
            return False
        else:
            print("   ✅ Login page accessible")
    except Exception as e:
        print(f"   ❌ Cannot connect to {base_url}: {e}")
        return False
    
    # Check debug endpoints
    try:
        print("2. Checking debug endpoints...")
        response = session.get(f"{base_url}/debug/users")
        if response.status_code == 200:
            users_data = response.json()
            print(f"   ✅ Users endpoint accessible")
            print(f"   Users found: {len(users_data.get('users', []))}")
            for user in users_data.get('users', []):
                print(f"     - {user['username']} ({user['role']})")
        else:
            print(f"   ⚠️  Users endpoint not accessible: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Debug endpoint error: {e}")
    
    # Try to login
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        print("3. Attempting login...")
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 302:  # Redirect after successful login
            print("   ✅ Login successful - Redirect detected")
            
            # Check session after login
            try:
                response = session.get(f"{base_url}/debug/session")
                if response.status_code == 200:
                    session_data = response.json()
                    print(f"   Session data: {json.dumps(session_data, indent=2)}")
                else:
                    print(f"   ⚠️  Cannot check session: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️  Session check error: {e}")
            
            return True
        else:
            print(f"   ❌ Login failed - No redirect")
            print(f"   Response content: {response.text[:200]}...")
            return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return False

def test_direct_hash(username, password):
    """Test password hashing directly"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    print(f"\nDirect hash test for {username} / {password}:")
    print(f"Hash: {password_hash}")
    
    # Expected hashes from reset_users.py
    expected_hashes = {
        'admin': '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',
        'user': 'e606e38b0d8c19b24cf0ee3808183162ea7cd63ff7912dbb22b5e803286b4446',
        'test': 'ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae'
    }
    
    if username in expected_hashes:
        if password_hash == expected_hashes[username]:
            print("✅ Hash matches expected value")
            return True
        else:
            print("❌ Hash does not match expected value")
            print(f"Expected: {expected_hashes[username]}")
            return False
    else:
        print("⚠️  Username not in expected hashes")
        return True

def main():
    print("=" * 60)
    print("File Manager & Terminal - Login Test")
    print("=" * 60)
    
    base_url = "http://localhost:5000"
    
    # Test password hashing
    print("\nTesting password hashing:")
    test_direct_hash('admin', 'admin123')
    test_direct_hash('user', 'user123')
    test_direct_hash('test', 'test123')
    
    # Test login cases
    test_cases = [
        ('admin', 'admin123'),
        ('user', 'user123'),
        ('test', 'test123'),
        ('admin', 'wrong_password'),
        ('user', 'wrong_password'),
        ('nonexistent', 'password')
    ]
    
    print(f"\nTesting login functionality at {base_url}:")
    successful_logins = 0
    
    for username, password in test_cases:
        if test_login(base_url, username, password):
            successful_logins += 1
        time.sleep(1)  # Small delay between tests
    
    print(f"\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Successful logins: {successful_logins}/{len(test_cases)}")
    
    if successful_logins >= 3:  # admin, user, test should work
        print("✅ Login system is working correctly")
    else:
        print("❌ Login system has issues")
        print("\nTroubleshooting steps:")
        print("1. Make sure the application is running")
        print("2. Check if the port 5000 is correct")
        print("3. Check application logs for errors")
        print("4. Try restarting the application")

if __name__ == '__main__':
    main() 