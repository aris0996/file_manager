#!/usr/bin/env python3
"""
System Monitor for File Manager & Terminal application
"""

import os
import sys
import time
import json
import psutil
import argparse
from datetime import datetime
from pathlib import Path

class SystemMonitor:
    """Real-time system monitoring"""
    
    def __init__(self, log_file="logs/system_monitor.log"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(exist_ok=True)
        self.monitoring = False
    
    def get_system_info(self):
        """Get comprehensive system information"""
        try:
            # CPU information
            cpu_info = {
                'count': psutil.cpu_count(),
                'percent': psutil.cpu_percent(interval=1),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                'load_avg': os.getloadavg() if hasattr(os, 'getloadavg') else None
            }
            
            # Memory information
            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'free': memory.free,
                'percent': memory.percent,
                'cached': getattr(memory, 'cached', 0),
                'buffers': getattr(memory, 'buffers', 0)
            }
            
            # Disk information
            disk = psutil.disk_usage('/')
            disk_info = {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            }
            
            # Network information
            network = psutil.net_io_counters()
            network_info = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            # Process information
            process_info = {
                'total_processes': len(psutil.pids()),
                'current_process': {
                    'pid': os.getpid(),
                    'memory_percent': psutil.Process().memory_percent(),
                    'cpu_percent': psutil.Process().cpu_percent()
                }
            }
            
            # System uptime
            uptime = time.time() - psutil.boot_time()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu': cpu_info,
                'memory': memory_info,
                'disk': disk_info,
                'network': network_info,
                'processes': process_info,
                'uptime': uptime
            }
            
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def format_size(self, size_bytes):
        """Format size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def log_system_info(self, info):
        """Log system information to file"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(info) + '\n')
        except Exception as e:
            print(f"Error logging system info: {e}")
    
    def display_system_info(self, info):
        """Display system information in a formatted way"""
        if 'error' in info:
            print(f"❌ Error getting system info: {info['error']}")
            return
        
        timestamp = datetime.fromisoformat(info['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n{'='*60}")
        print(f"System Monitor - {timestamp}")
        print(f"{'='*60}")
        
        # CPU Information
        cpu = info['cpu']
        print(f"CPU Usage: {cpu['percent']:>6.1f}% | Cores: {cpu['count']}")
        if cpu['freq']:
            print(f"CPU Frequency: {cpu['freq']['current']/1000:.1f} GHz")
        if cpu['load_avg']:
            print(f"Load Average: {cpu['load_avg'][0]:.2f}, {cpu['load_avg'][1]:.2f}, {cpu['load_avg'][2]:.2f}")
        
        # Memory Information
        mem = info['memory']
        print(f"Memory Usage: {mem['percent']:>6.1f}% | {self.format_size(mem['used'])} / {self.format_size(mem['total'])}")
        print(f"Memory Available: {self.format_size(mem['available'])} | Free: {self.format_size(mem['free'])}")
        
        # Disk Information
        disk = info['disk']
        print(f"Disk Usage: {disk['percent']:>6.1f}% | {self.format_size(disk['used'])} / {self.format_size(disk['total'])}")
        print(f"Disk Free: {self.format_size(disk['free'])}")
        
        # Network Information
        net = info['network']
        print(f"Network: ↑ {self.format_size(net['bytes_sent'])} | ↓ {self.format_size(net['bytes_recv'])}")
        
        # Process Information
        proc = info['processes']
        print(f"Total Processes: {proc['total_processes']}")
        print(f"Current Process: PID {proc['current_process']['pid']} | "
              f"CPU: {proc['current_process']['cpu_percent']:.1f}% | "
              f"Memory: {proc['current_process']['memory_percent']:.1f}%")
        
        # Uptime
        uptime_seconds = info['uptime']
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        print(f"System Uptime: {days}d {hours}h {minutes}m")
        
        print(f"{'='*60}")
    
    def start_monitoring(self, interval=5, log_to_file=True, display=True):
        """Start continuous monitoring"""
        self.monitoring = True
        print(f"Starting system monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while self.monitoring:
                info = self.get_system_info()
                
                if log_to_file:
                    self.log_system_info(info)
                
                if display:
                    self.display_system_info(info)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
        except Exception as e:
            print(f"Monitoring error: {e}")
        finally:
            self.monitoring = False
    
    def get_top_processes(self, count=10):
        """Get top processes by CPU and memory usage"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            cpu_sorted = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:count]
            
            # Sort by memory usage
            memory_sorted = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:count]
            
            return {
                'top_cpu': cpu_sorted,
                'top_memory': memory_sorted
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def display_top_processes(self, processes):
        """Display top processes"""
        if 'error' in processes:
            print(f"❌ Error getting process info: {processes['error']}")
            return
        
        print(f"\n{'='*80}")
        print("TOP PROCESSES")
        print(f"{'='*80}")
        
        # Top CPU processes
        print("Top CPU Usage:")
        print(f"{'PID':<8} {'Name':<20} {'CPU %':<8} {'Memory %':<10}")
        print("-" * 50)
        for proc in processes['top_cpu']:
            print(f"{proc['pid']:<8} {proc['name'][:19]:<20} {proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f}")
        
        print()
        
        # Top memory processes
        print("Top Memory Usage:")
        print(f"{'PID':<8} {'Name':<20} {'CPU %':<8} {'Memory %':<10}")
        print("-" * 50)
        for proc in processes['top_memory']:
            print(f"{proc['pid']:<8} {proc['name'][:19]:<20} {proc['cpu_percent']:<8.1f} {proc['memory_percent']:<10.1f}")
        
        print(f"{'='*80}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='System Monitor')
    parser.add_argument('--interval', type=int, default=5, help='Monitoring interval in seconds')
    parser.add_argument('--no-log', action='store_true', help='Disable logging to file')
    parser.add_argument('--no-display', action='store_true', help='Disable display output')
    parser.add_argument('--top', action='store_true', help='Show top processes and exit')
    parser.add_argument('--once', action='store_true', help='Show system info once and exit')
    parser.add_argument('--log-file', default='logs/system_monitor.log', help='Log file path')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(args.log_file)
    
    if args.top:
        # Show top processes
        processes = monitor.get_top_processes()
        monitor.display_top_processes(processes)
    
    elif args.once:
        # Show system info once
        info = monitor.get_system_info()
        monitor.display_system_info(info)
        
        if not args.no_log:
            monitor.log_system_info(info)
    
    else:
        # Start continuous monitoring
        log_to_file = not args.no_log
        display = not args.no_display
        
        monitor.start_monitoring(
            interval=args.interval,
            log_to_file=log_to_file,
            display=display
        )

if __name__ == '__main__':
    main() 