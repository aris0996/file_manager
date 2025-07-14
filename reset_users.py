#!/usr/bin/env python3
"""
Reset and check user credentials for File Manager & Terminal
"""

import hashlib
import os
import sys

def create_user(username, password, role='user'):
    """Create a user with hashed password"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return {
        'username': username,
        'password': password,
        'password_hash': password_hash,
        'role': role
    }

def main():
    print("=" * 60)
    print("File Manager & Terminal - User Management")
    print("=" * 60)
    
    # Create users
    users = {
        'admin': create_user('admin', 'admin123', 'admin'),
        'user': create_user('user', 'user123', 'user'),
        'test': create_user('test', 'test123', 'user')
    }
    
    print("\nCurrent Users:")
    print("-" * 40)
    for username, user in users.items():
        print(f"Username: {user['username']}")
        print(f"Password: {user['password']}")
        print(f"Role: {user['role']}")
        print(f"Hash: {user['password_hash']}")
        print("-" * 40)
    
    # Test password verification
    print("\nTesting password verification:")
    print("-" * 40)
    
    test_cases = [
        ('admin', 'admin123'),
        ('admin', 'wrong_password'),
        ('user', 'user123'),
        ('user', 'wrong_password'),
        ('test', 'test123')
    ]
    
    for username, password in test_cases:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = users.get(username)
        
        if user and user['password_hash'] == password_hash:
            print(f"✅ {username} / {password} - VALID")
        else:
            print(f"❌ {username} / {password} - INVALID")
    
    # Generate Python code for app.py
    print("\n" + "=" * 60)
    print("Python Code for app.py:")
    print("=" * 60)
    
    print("\n# Enhanced user management")
    print("users = {")
    for i, (username, user) in enumerate(users.items(), 1):
        print(f"    {i}: User({i}, '{user['username']}', '{user['password_hash']}', '{user['role']}'),")
    print("}")
    
    # Generate test login script
    print("\n" + "=" * 60)
    print("Test Login Script:")
    print("=" * 60)
    
    test_script = '''#!/usr/bin/env python3
import requests
import hashlib

def test_login(base_url, username, password):
    """Test login functionality"""
    session = requests.Session()
    
    # Get login page
    try:
        response = session.get(f"{base_url}/login")
        if response.status_code != 200:
            print(f"❌ Cannot access login page: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to {base_url}: {e}")
        return False
    
    # Try to login
    login_data = {
        'username': username,
        'password': password
    }
    
    try:
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        
        if response.status_code == 302:  # Redirect after successful login
            print(f"✅ Login successful: {username} / {password}")
            return True
        else:
            print(f"❌ Login failed: {username} / {password} (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

if __name__ == '__main__':
    base_url = "http://localhost:5000"
    
    test_cases = [
        ('admin', 'admin123'),
        ('user', 'user123'),
        ('admin', 'wrong_password'),
        ('user', 'wrong_password')
    ]
    
    print("Testing login functionality...")
    for username, password in test_cases:
        test_login(base_url, username, password)
'''
    
    print(test_script)
    
    # Save test script
    with open('test_login.py', 'w') as f:
        f.write(test_script)
    
    print(f"\n✅ Test script saved to: test_login.py")
    print(f"Run with: python test_login.py")

if __name__ == '__main__':
    main() 