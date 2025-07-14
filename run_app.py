#!/usr/bin/env python3
"""
Enhanced File Manager & Terminal Application Runner
"""

import os
import sys
import argparse
from app import app
from config import config

def main():
    """Main application runner"""
    parser = argparse.ArgumentParser(description='File Manager & Terminal Application')
    parser.add_argument('--config', choices=['development', 'production', 'testing'], 
                       default='development', help='Configuration to use')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers (production only)')
    
    args = parser.parse_args()
    
    # Load configuration
    app.config.from_object(config[args.config])
    
    # Override debug if specified
    if args.debug:
        app.config['DEBUG'] = True
    
    # Initialize application
    config[args.config].init_app(app)
    
    print("=" * 60)
    print("File Manager & Terminal Web Application")
    print("=" * 60)
    print(f"Configuration: {args.config}")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Debug: {app.config['DEBUG']}")
    print(f"Upload Folder: {app.config['UPLOAD_FOLDER']}")
    print(f"Max File Size: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
    print("=" * 60)
    
    if args.config == 'production':
        print("Production mode detected!")
        print("Consider using a WSGI server like Gunicorn:")
        print(f"gunicorn --bind {args.host}:{args.port} --workers {args.workers} wsgi:application")
        print("=" * 60)
    
    print("Starting application...")
    print("Access the application at:")
    print(f"  http://{args.host}:{args.port}")
    print(f"  http://localhost:{args.port}")
    print()
    print("Default credentials:")
    print("  Admin: admin / admin123")
    print("  User:  user / user123")
    print()
    print("Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=app.config['DEBUG'],
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 