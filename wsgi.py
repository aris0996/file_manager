#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
import sys
from app import app
from config import config

# Get configuration from environment
config_name = os.environ.get('FLASK_CONFIG') or 'production'
app.config.from_object(config[config_name])

# Initialize application
config[config_name].init_app(app)

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=5000)
else:
    # For production WSGI servers
    application = app 