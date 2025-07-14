import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB
    
    # Allowed file extensions for upload
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg',
        'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
        'zip', 'rar', 'tar', 'gz', '7z',
        'py', 'js', 'html', 'css', 'json', 'xml', 'csv', 'md',
        'mp3', 'mp4', 'avi', 'mov', 'wmv',
        'log', 'ini', 'conf', 'cfg', 'yml', 'yaml'
    }
    
    # Terminal Configuration
    COMMAND_TIMEOUT = int(os.environ.get('COMMAND_TIMEOUT', 60))  # seconds
    MAX_COMMAND_LENGTH = int(os.environ.get('MAX_COMMAND_LENGTH', 1000))
    
    # Security Configuration
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Dangerous command patterns (regex)
    DANGEROUS_COMMAND_PATTERNS = [
        r'rm\s+-rf\s+/',           # rm -rf /
        r'sudo\s+',                # sudo commands
        r'su\s+',                  # su commands
        r'chmod\s+777',            # chmod 777
        r'dd\s+if=',               # dd if=
        r':\(\)\{\s*:\|:\s*&\s*\};:',  # fork bomb
        r'wget\s+.*\|\s*bash',     # wget | bash
        r'curl\s+.*\|\s*bash',     # curl | bash
        r'nc\s+',                  # netcat
        r'ncat\s+',                # ncat
        r'telnet\s+',              # telnet
        r'ssh\s+.*\|\s*bash',      # ssh | bash
        r'chown\s+.*\s+/',         # chown on root
        r'chmod\s+.*\s+/',         # chmod on root
        r'mkfs\s+',                # filesystem creation
        r'fdisk\s+',               # disk partitioning
        r'format\s+',              # disk formatting
        r'init\s+',                # init commands
        r'shutdown\s+',            # shutdown commands
        r'reboot\s+',              # reboot commands
        r'halt\s+',                # halt commands
        r'poweroff\s+',            # poweroff commands
    ]
    
    # Protected system paths
    PROTECTED_PATHS = [
        '/', '/home', '/etc', '/var', '/usr', '/bin', '/sbin',
        '/boot', '/dev', '/proc', '/sys', '/tmp', '/root'
    ]
    
    # User roles and permissions
    USER_ROLES = {
        'admin': {
            'can_delete': True,
            'can_upload': True,
            'can_execute_commands': True,
            'can_view_system_info': True,
            'can_manage_users': True
        },
        'user': {
            'can_delete': False,
            'can_upload': True,
            'can_execute_commands': True,
            'can_view_system_info': False,
            'can_manage_users': False
        },
        'viewer': {
            'can_delete': False,
            'can_upload': False,
            'can_execute_commands': False,
            'can_view_system_info': False,
            'can_manage_users': False
        }
    }
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'app.log')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Performance Configuration
    MAX_FILES_PER_PAGE = int(os.environ.get('MAX_FILES_PER_PAGE', 100))
    SEARCH_TIMEOUT = int(os.environ.get('SEARCH_TIMEOUT', 30))
    PREVIEW_MAX_SIZE = int(os.environ.get('PREVIEW_MAX_SIZE', 5000))  # characters
    
    # System Monitoring Configuration
    MONITORING_INTERVAL = int(os.environ.get('MONITORING_INTERVAL', 2))  # seconds
    MONITORING_ENABLED = os.environ.get('MONITORING_ENABLED', 'True').lower() == 'true'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create upload directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(app.config['LOG_FILE'])
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Stricter security settings for production
    COMMAND_TIMEOUT = 30  # Shorter timeout
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload
    
    # Additional dangerous patterns for production
    DANGEROUS_COMMAND_PATTERNS = Config.DANGEROUS_COMMAND_PATTERNS + [
        r'cat\s+/etc/passwd',      # Read password file
        r'cat\s+/etc/shadow',      # Read shadow file
        r'cat\s+/proc/version',    # Read system version
        r'cat\s+/proc/cpuinfo',    # Read CPU info
        r'cat\s+/proc/meminfo',    # Read memory info
        r'cat\s+/proc/net/tcp',    # Read network info
        r'cat\s+/proc/net/udp',    # Read network info
        r'cat\s+/proc/net/raw',    # Read network info
        r'cat\s+/proc/net/unix',   # Read network info
        r'cat\s+/proc/net/dev',    # Read network info
        r'cat\s+/proc/net/route',  # Read network info
        r'cat\s+/proc/net/arp',    # Read network info
        r'cat\s+/proc/net/stat',   # Read network info
        r'cat\s+/proc/net/snmp',   # Read network info
        r'cat\s+/proc/net/netstat', # Read network info
        r'cat\s+/proc/net/ip_conntrack', # Read network info
        r'cat\s+/proc/net/nf_conntrack', # Read network info
        r'cat\s+/proc/net/ip_tables_names', # Read network info
        r'cat\s+/proc/net/ip_tables_matches', # Read network info
        r'cat\s+/proc/net/ip_tables_targets', # Read network info
        r'cat\s+/proc/net/ip6_tables_names', # Read network info
        r'cat\s+/proc/net/ip6_tables_matches', # Read network info
        r'cat\s+/proc/net/ip6_tables_targets', # Read network info
    ]

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    
    # Use temporary directories for testing
    UPLOAD_FOLDER = '/tmp/test_uploads'
    LOG_FILE = '/tmp/test_app.log'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 