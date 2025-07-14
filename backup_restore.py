#!/usr/bin/env python3
"""
Backup and Restore utility for File Manager & Terminal application
"""

import os
import sys
import json
import shutil
import zipfile
import argparse
from datetime import datetime
from pathlib import Path

class BackupManager:
    """Manages backup and restore operations"""
    
    def __init__(self, backup_dir="backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self, include_logs=True, include_config=True):
        """Create a backup of the application data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"file_manager_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        print(f"Creating backup: {backup_name}")
        
        try:
            # Create backup directory
            backup_path.mkdir(exist_ok=True)
            
            # Backup uploads directory
            if os.path.exists("uploads"):
                print("  - Backing up uploads directory...")
                shutil.copytree("uploads", backup_path / "uploads", dirs_exist_ok=True)
            
            # Backup logs directory
            if include_logs and os.path.exists("logs"):
                print("  - Backing up logs directory...")
                shutil.copytree("logs", backup_path / "logs", dirs_exist_ok=True)
            
            # Backup configuration
            if include_config:
                print("  - Backing up configuration...")
                config_files = ["config.py", ".env"]
                for config_file in config_files:
                    if os.path.exists(config_file):
                        shutil.copy2(config_file, backup_path / config_file)
            
            # Create metadata
            metadata = {
                "backup_date": datetime.now().isoformat(),
                "version": "2.0",
                "includes": {
                    "uploads": os.path.exists("uploads"),
                    "logs": include_logs and os.path.exists("logs"),
                    "config": include_config
                },
                "file_count": self._count_files(backup_path)
            }
            
            with open(backup_path / "metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)
            
            # Create ZIP archive
            zip_path = self.backup_dir / f"{backup_name}.zip"
            print(f"  - Creating ZIP archive: {zip_path}")
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # Remove temporary directory
            shutil.rmtree(backup_path)
            
            print(f"✅ Backup created successfully: {zip_path}")
            return str(zip_path)
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            if backup_path.exists():
                shutil.rmtree(backup_path)
            return None
    
    def restore_backup(self, backup_file):
        """Restore from a backup file"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ Backup file not found: {backup_file}")
            return False
        
        print(f"Restoring from backup: {backup_path.name}")
        
        try:
            # Create temporary directory
            temp_dir = Path("temp_restore")
            temp_dir.mkdir(exist_ok=True)
            
            # Extract backup
            print("  - Extracting backup...")
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # Read metadata
            metadata_file = temp_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                print(f"  - Backup date: {metadata['backup_date']}")
                print(f"  - Version: {metadata['version']}")
            
            # Restore uploads
            uploads_backup = temp_dir / "uploads"
            if uploads_backup.exists():
                print("  - Restoring uploads directory...")
                if os.path.exists("uploads"):
                    shutil.rmtree("uploads")
                shutil.copytree(uploads_backup, "uploads")
            
            # Restore logs
            logs_backup = temp_dir / "logs"
            if logs_backup.exists():
                print("  - Restoring logs directory...")
                if os.path.exists("logs"):
                    shutil.rmtree("logs")
                shutil.copytree(logs_backup, "logs")
            
            # Restore configuration
            config_backup = temp_dir / "config.py"
            if config_backup.exists():
                print("  - Restoring configuration...")
                shutil.copy2(config_backup, "config.py")
            
            env_backup = temp_dir / ".env"
            if env_backup.exists():
                print("  - Restoring environment file...")
                shutil.copy2(env_backup, ".env")
            
            # Clean up
            shutil.rmtree(temp_dir)
            
            print("✅ Restore completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            return False
    
    def list_backups(self):
        """List available backups"""
        backups = []
        
        for backup_file in self.backup_dir.glob("*.zip"):
            try:
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    # Try to read metadata
                    try:
                        with zipf.open("metadata.json") as f:
                            metadata = json.load(f)
                            backups.append({
                                "file": backup_file.name,
                                "date": metadata.get("backup_date", "Unknown"),
                                "version": metadata.get("version", "Unknown"),
                                "size": backup_file.stat().st_size
                            })
                    except:
                        # No metadata, use file info
                        backups.append({
                            "file": backup_file.name,
                            "date": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat(),
                            "version": "Unknown",
                            "size": backup_file.stat().st_size
                        })
            except Exception as e:
                print(f"Warning: Could not read backup {backup_file.name}: {e}")
        
        return sorted(backups, key=lambda x: x["date"], reverse=True)
    
    def _count_files(self, directory):
        """Count files in directory"""
        count = 0
        for root, dirs, files in os.walk(directory):
            count += len(files)
        return count

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Backup and Restore utility')
    parser.add_argument('action', choices=['backup', 'restore', 'list'], 
                       help='Action to perform')
    parser.add_argument('--backup-file', help='Backup file for restore')
    parser.add_argument('--no-logs', action='store_true', help='Exclude logs from backup')
    parser.add_argument('--no-config', action='store_true', help='Exclude config from backup')
    parser.add_argument('--backup-dir', default='backups', help='Backup directory')
    
    args = parser.parse_args()
    
    backup_manager = BackupManager(args.backup_dir)
    
    if args.action == 'backup':
        include_logs = not args.no_logs
        include_config = not args.no_config
        
        backup_file = backup_manager.create_backup(include_logs, include_config)
        if backup_file:
            print(f"Backup saved to: {backup_file}")
        else:
            sys.exit(1)
    
    elif args.action == 'restore':
        if not args.backup_file:
            print("Error: --backup-file is required for restore")
            sys.exit(1)
        
        success = backup_manager.restore_backup(args.backup_file)
        if not success:
            sys.exit(1)
    
    elif args.action == 'list':
        backups = backup_manager.list_backups()
        
        if not backups:
            print("No backups found.")
        else:
            print("Available backups:")
            print("-" * 80)
            print(f"{'File':<30} {'Date':<25} {'Version':<10} {'Size':<10}")
            print("-" * 80)
            
            for backup in backups:
                size_mb = backup['size'] / (1024 * 1024)
                print(f"{backup['file']:<30} {backup['date']:<25} {backup['version']:<10} {size_mb:.1f}MB")

if __name__ == '__main__':
    main() 