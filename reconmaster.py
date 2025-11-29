#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 ReconMaster - Professional Recon Framework                   ║
║                              for Kali Linux                                  ║
║                                                                              ║
║    A beautiful, powerful, automated, and intelligent reconnaissance tool     ║
║                    for bug bounty hunters and pentesters                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import json
import time
import re
import shutil
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class Colors:
    """Professional color scheme for beautiful terminal output"""
    # Main colors
    CYAN = '\033[96m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    
    # Bright variants
    BRIGHT_CYAN = '\033[36m'
    BRIGHT_GREEN = '\033[32m'
    BRIGHT_YELLOW = '\033[33m'
    BRIGHT_RED = '\033[31m'
    
    # Background colors
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'
    BG_RED = '\033[41m'
    BG_YELLOW = '\033[43m'
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    
    # Reset
    RESET = '\033[0m'

class ReconMaster:
    """Main reconnaissance framework class"""
    
    def __init__(self):
        self.domain = ""
        self.output_dir = ""
        self.tools_status = {}
        self.results = {}
        self.setup_complete = False
        
    def display_banner(self):
        """Display beautiful ASCII banner"""
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                  ║
║ ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗   ║
║ ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗  ║
║ ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝  ║
║ ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██╔██╔  ██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗  ║
║ ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║╚═╝  ██║██║  ██║███████║   ██║   ███████╗██║  ██║  ║
║ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝  ║
║                                                                                                  ║ 
║                                                                                                  ║
║                  {Colors.WHITE}Professional Reconnaissance Framework v1.0{Colors.CYAN}                                      ║ 
║                        {Colors.WHITE}For Kali Linux Bug Bounty Hunters{Colors.CYAN}                                         ║                                           
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

{Colors.RESET}
"""
        print(banner)
        
    def check_tool_installation(self, tool_name, install_command=None):
        """Check if a tool is installed and provide installation guidance"""
        try:
            subprocess.run([tool_name, '--version'], capture_output=True, check=True)
            self.tools_status[tool_name] = {'installed': True, 'path': tool_name}
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Try alternative names
            alternatives = {
                'subfinder': ['subfinder', 'github.com/projectdiscovery/subfinder/v2/cmd/subfinder'],
                'naabu': ['naabu', 'github.com/projectdiscovery/naabu/v2/cmd/naabu'],
                'httpx': ['httpx', 'github.com/projectdiscovery/httpx/cmd/httpx'],
                'dnsx': ['dnsx', 'github.com/projectdiscovery/dnsx/cmd/dnsx'],
                'katana': ['katana', 'github.com/projectdiscovery/katana/cmd/katana'],
                'nuclei': ['nuclei', 'github.com/projectdiscovery/nuclei/v3/cmd/nuclei']
            }
            
            alt_names = alternatives.get(tool_name, [tool_name])
            for alt_name in alt_names:
                try:
                    subprocess.run([alt_name, '--version'], capture_output=True, check=True)
                    self.tools_status[tool_name] = {'installed': True, 'path': alt_name}
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            self.tools_status[tool_name] = {
                'installed': False, 
                'install_command': install_command or f'sudo apt install {tool_name}'
            }
            return False
    
    def initialize_tools(self):
        """Initialize and check all required tools"""
        tools_to_check = [
            ('subfinder', 'go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest'),
            ('amass', 'sudo apt install amass'),
            ('assetfinder', 'go install github.com/tomnomnom/assetfinder@latest'),
            ('dnsx', 'go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest'),
            ('httpx', 'go install github.com/projectdiscovery/httpx/cmd/httpx@latest'),
            ('naabu', 'go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest'),
            ('nmap', 'sudo apt install nmap'),
            ('katana', 'go install github.com/projectdiscovery/katana/cmd/katana@latest'),
            ('gau', 'go install github.com/lc/gau@latest'),
            ('waybackurls', 'go install github.com/tomnomnom/waybackurls@latest'),
            ('wafw00f', 'sudo apt install wafw00f'),
            ('nuclei', 'go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest')
        ]
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Checking Tool Installation Status...{Colors.RESET}\n")
        
        for tool, install_cmd in tools_to_check:
            status = "✔" if self.check_tool_installation(tool, install_cmd) else "✘"
            color = Colors.GREEN if status == "✔" else Colors.RED
            print(f"  {color}[{status}] {tool.capitalize()}{Colors.RESET}")
            
        print(f"\n{Colors.YELLOW}[!] Install missing tools using the suggested commands above{Colors.RESET}\n")
    
    def setup_domain(self):
        """Setup domain and create output directory"""
        if self.setup_complete:
            change = input(f"\n{Colors.YELLOW}[?] Current domain: {self.domain}. Change domain? (y/n): {Colors.RESET}").lower().strip()
            if change != 'y':
                return True
        
        domain = input(f"\n{Colors.CYAN}[+] Enter target domain (e.g., example.com): {Colors.RESET}").strip()
        if not domain:
            print(f"{Colors.RED}[!] Domain cannot be empty!{Colors.RESET}")
            return False
            
        # Validate domain format
        domain_pattern = r'^[a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]?\.[a-zA-Z]{2,}$'
        if not re.match(domain_pattern, domain):
            print(f"{Colors.RED}[!] Invalid domain format!{Colors.RESET}")
            return False
            
        self.domain = domain
        self.output_dir = f"output-{domain}"
        
        # Create output directory
        try:
            Path(self.output_dir).mkdir(exist_ok=True)
            Path(f"{self.output_dir}/logs").mkdir(exist_ok=True)
            print(f"\n{Colors.GREEN}[✔] Created output directory: {self.output_dir}/{Colors.RESET}")
            self.setup_complete = True
            return True
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to create directory: {e}{Colors.RESET}")
            return False
    
    def run_command(self, command, output_file=None, timeout=300):
        """Run command with timeout and output handling"""
        try:
            if output_file:
                with open(output_file, 'w') as f:
                    result = subprocess.run(
                        command, shell=True, stdout=f, stderr=subprocess.STDOUT,
                        timeout=timeout, text=True
                    )
            else:
                result = subprocess.run(
                    command, shell=True, capture_output=True,
                    timeout=timeout, text=True
                )
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"{Colors.RED}[!] Command timed out after {timeout} seconds{Colors.RESET}")
            return False
        except Exception as e:
            print(f"{Colors.RED}[!] Command failed: {e}{Colors.RESET}")
            return False
    
    def merge_and_dedup_files(self, input_files, output_file):
        """Merge multiple files and remove duplicates"""
        try:
            unique_lines = set()
            for file_path in input_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        unique_lines.update(line.strip() for line in f if line.strip())
            
            with open(output_file, 'w') as f:
                for line in sorted(unique_lines):
                    f.write(f"{line}\n")
            
            return len(unique_lines)
        except Exception as e:
            print(f"{Colors.RED}[!] Error merging files: {e}{Colors.RESET}")
            return 0
    
    def display_menu(self):
        """Display the main menu with beautiful formatting"""
        menu = f"""
{Colors.CYAN}{Colors.BOLD}
╔═════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                         RECONMASTER MAIN MENU                                           ║
╠═════════════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                         ║
║    {Colors.WHITE}[1] Subdomain Enumeration{Colors.CYAN}      - Discover subdomains using multiple tools                            ║
║    {Colors.WHITE}[2] DNS Resolution{Colors.CYAN}           - Resolve DNS records for found subdomains                              ║
║    {Colors.WHITE}[3] Alive Hosts Check{Colors.CYAN}        - Check which hosts are alive via HTTP                                  ║
║    {Colors.WHITE}[4] Fast Port Scan{Colors.CYAN}          - Quick port scan using Naabu                                            ║
║    {Colors.WHITE}[5] Full Port Scan{Colors.CYAN}          - Comprehensive scan with Nmap                                           ║
║    {Colors.WHITE}[6] URL Collection{Colors.CYAN}          - Gather URLs from multiple sources                                      ║
║    {Colors.WHITE}[7] WAF Detection{Colors.CYAN}           - Identify Web Application Firewalls                                     ║
║    {Colors.WHITE}[8] Vulnerability Scan{Colors.CYAN}      - Scan for vulnerabilities with Nuclei                                   ║
║    {Colors.WHITE}[9] FULL AUTOMATED RECON{Colors.CYAN}    - Run complete reconnaissance sequence                                   ║
║                                                                                                         ║   
║    {Colors.WHITE}[C] Change Domain{Colors.CYAN}           - Set a different target domain                                          ║
║    {Colors.WHITE}[I] Initialize Tools{Colors.CYAN}        - Check and install required tools                                       ║
║    {Colors.WHITE}[H] Help{Colors.CYAN}                   - Show detailed help information                                          ║
║    {Colors.WHITE}[Q] Quit{Colors.CYAN}                   - Exit the framework                                                      ║
║                                                                                                         ║
╚═════════════════════════════════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        print(menu)
        
        if self.domain:
            print(f"{Colors.GREEN}[✔] Current Domain: {self.domain}{Colors.RESET}")
            print(f"{Colors.GREEN}[✔] Output Directory: {self.output_dir}/{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}[!] No domain selected. Please choose option C first.{Colors.RESET}\n")
    
    def show_help(self):
        """Display comprehensive help information"""
        help_text = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                          RECONMASTER HELP GUIDE                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.WHITE}{Colors.BOLD}OVERVIEW:{Colors.RESET}
    ReconMaster is a professional reconnaissance framework that combines multiple
    security tools into a single, powerful interface for bug bounty hunting and
    penetration testing.

{Colors.WHITE}{Colors.BOLD}WORKFLOW:{Colors.RESET}
    1. {Colors.CYAN}Set Target Domain{Colors.RESET} - Configure your target
    2. {Colors.CYAN}Run Subdomain Enumeration{Colors.RESET} - Discover subdomains
    3. {Colors.CYAN}DNS Resolution{Colors.RESET} - Resolve DNS records
    4. {Colors.CYAN}Alive Hosts Check{Colors.RESET} - Find live targets
    5. {Colors.CYAN}Port Scanning{Colors.RESET} - Discover open services
    6. {Colors.CYAN}URL Collection{Colors.RESET} - Gather endpoint URLs
    7. {Colors.CYAN}WAF Detection{Colors.RESET} - Identify protection systems
    8. {Colors.CYAN}Vulnerability Scanning{Colors.RESET} - Find security issues
    9. {Colors.CYAN}Review Summary{Colors.RESET} - Analyze results

{Colors.WHITE}{Colors.BOLD}OUTPUT STRUCTURE:{Colors.RESET}
    output-domain.com/
    ├── subdomains_raw.txt      # Raw subdomain results
    ├── subdomains.txt          # Cleaned subdomain list
    ├── dns_resolved.txt        # DNS resolution results
    ├── alive.txt               # Live hosts
    ├── ports_fast.txt          # Quick port scan results
    ├── ports_full.txt          # Detailed port scan results
    ├── urls.txt                # Collected URLs
    ├── waf_summary.txt         # WAF detection results
    ├── nuclei_output.txt       # Vulnerability scan results
    ├── summary.txt             # Complete recon summary
    └── logs/                   # Execution logs

{Colors.WHITE}{Colors.BOLD}TOOL REQUIREMENTS:{Colors.RESET}
    • Subfinder      - Subdomain discovery
    • Amass          - Passive subdomain enumeration
    • Assetfinder    - Alternative subdomain finder
    • DNSx           - DNS resolution tool
    • HTTPx          - HTTP probing tool
    • Naabu          - Fast port scanner
    • Nmap           - Network mapper
    • Katana         - Web crawler
    • Gau            - Get All URLs
    • Waybackurls    - Wayback Machine URLs
    • Wafw00f        - WAF detection
    • Nuclei         - Vulnerability scanner

{Colors.YELLOW}Missing tools will be automatically detected and installation
commands will be provided.{Colors.RESET}

{Colors.WHITE}{Colors.BOLD}TIPS:{Colors.RESET}
    • Run tools in sequence for best results
    • Use Full Automated Recon for complete workflow
    • Check the summary.txt file after each scan
    • Monitor logs/ directory for detailed execution info
    • Results are automatically deduplicated and cleaned

{Colors.CYAN}Press Enter to return to main menu...{Colors.RESET}
"""
        print(help_text)
        input()
    
    def suggest_next_steps(self, completed_task):
        """Intelligently suggest next steps based on completed task"""
        suggestions = {
            'subdomains': [
                ('DNS Resolution', '2'),
                ('Alive Hosts Check', '3'),
                ('Full Automated Recon', '9')
            ],
            'dns_resolution': [
                ('Alive Hosts Check', '3'),
                ('Fast Port Scan', '4'),
                ('Full Port Scan', '5')
            ],
            'alive_hosts': [
                ('Fast Port Scan', '4'),
                ('URL Collection', '6'),
                ('WAF Detection', '7')
            ],
            'port_scan': [
                ('URL Collection', '6'),
                ('WAF Detection', '7'),
                ('Vulnerability Scan', '8')
            ],
            'urls': [
                ('WAF Detection', '7'),
                ('Vulnerability Scan', '8')
            ],
            'waf_detection': [
                ('Vulnerability Scan', '8'),
                ('Review Summary', 'View Results')
            ]
        }
        
        if completed_task in suggestions:
            print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Recommended Next Steps:{Colors.RESET}")
            for desc, option in suggestions[completed_task]:
                print(f"  {Colors.YELLOW}→ {desc} (Option {option}){Colors.RESET}")
            print()
    
    def run_subdomain_enumeration(self):
        """Run comprehensive subdomain enumeration"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Subdomain Enumeration...{Colors.RESET}\n")
        
        tools_used = []
        raw_files = []
        
        # Subfinder
        if self.tools_status.get('subfinder', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Subfinder...{Colors.RESET}")
            subfinder_output = f"{self.output_dir}/subfinder_raw.txt"
            cmd = f"subfinder -d {self.domain} -all -recursive -o {subfinder_output}"
            if self.run_command(cmd, timeout=600):
                tools_used.append('Subfinder')
                raw_files.append(subfinder_output)
                print(f"{Colors.GREEN}[✔] Subfinder completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Subfinder failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Subfinder not installed, skipping{Colors.RESET}")
        
        # Amass (passive only for speed)
        if self.tools_status.get('amass', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Amass (passive)...{Colors.RESET}")
            amass_output = f"{self.output_dir}/amass_raw.txt"
            cmd = f"amass enum -passive -d {self.domain} -o {amass_output}"
            if self.run_command(cmd, timeout=900):
                tools_used.append('Amass')
                raw_files.append(amass_output)
                print(f"{Colors.GREEN}[✔] Amass completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Amass failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Amass not installed, skipping{Colors.RESET}")
        
        # Assetfinder
        if self.tools_status.get('assetfinder', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Assetfinder...{Colors.RESET}")
            assetfinder_output = f"{self.output_dir}/assetfinder_raw.txt"
            cmd = f"assetfinder --subs-only {self.domain} > {assetfinder_output}"
            if self.run_command(cmd):
                tools_used.append('Assetfinder')
                raw_files.append(assetfinder_output)
                print(f"{Colors.GREEN}[✔] Assetfinder completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Assetfinder failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Assetfinder not installed, skipping{Colors.RESET}")
        
        if not raw_files:
            print(f"{Colors.RED}[!] No subdomain tools available!{Colors.RESET}")
            return
        
        # Merge and deduplicate results
        final_output = f"{self.output_dir}/subdomains.txt"
        raw_combined = f"{self.output_dir}/subdomains_raw.txt"
        
        # First create combined raw file
        self.merge_and_dedup_files(raw_files, raw_combined)
        
        # Clean and validate subdomains
        print(f"{Colors.YELLOW}[*] Cleaning and validating subdomains...{Colors.RESET}")
        try:
            with open(raw_combined, 'r') as f:
                subdomains = set()
                for line in f:
                    subdomain = line.strip().lower()
                    if subdomain and self.domain in subdomain:
                        # Basic validation
                        if subdomain.replace('.', '').replace('-', '').isalnum():
                            subdomains.add(subdomain)
            
            with open(final_output, 'w') as f:
                for subdomain in sorted(subdomains):
                    f.write(f"{subdomain}\n")
            
            count = len(subdomains)
            print(f"{Colors.GREEN}[✔] Found {count} unique subdomains{Colors.RESET}")
            
            # Update results
            self.results['subdomains'] = count
            
            # Display sample results
            print(f"\n{Colors.CYAN}[*] Sample subdomains found:{Colors.RESET}")
            sample = list(subdomains)[:10]
            for subdomain in sample:
                print(f"  {Colors.WHITE}• {subdomain}{Colors.RESET}")
            if count > 10:
                print(f"  {Colors.DIM}... and {count-10} more{Colors.RESET}")
            
            self.suggest_next_steps('subdomains')
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error processing subdomains: {e}{Colors.RESET}")
    
    def run_dns_resolution(self):
        """Run DNS resolution on found subdomains"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        subdomains_file = f"{self.output_dir}/subdomains.txt"
        if not os.path.exists(subdomains_file):
            print(f"{Colors.RED}[!] No subdomains found! Run subdomain enumeration first.{Colors.RESET}")
            return
        
        if not self.tools_status.get('dnsx', {}).get('installed'):
            print(f"{Colors.RED}[!] DNSx not installed! Install with: go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting DNS Resolution...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/dns_resolved.txt"
        cmd = f"dnsx -l {subdomains_file} -a -aaaa -cname -ns -ptr -mx -soa -resp -o {output_file}"
        
        if self.run_command(cmd, timeout=300):
            # Count results
            try:
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                    count = len(lines)
                
                print(f"{Colors.GREEN}[✔] DNS resolution completed{Colors.RESET}")
                print(f"{Colors.GREEN}[✔] Resolved {count} DNS records{Colors.RESET}")
                
                # Display sample results
                print(f"\n{Colors.CYAN}[*] Sample DNS records:{Colors.RESET}")
                for line in lines[:5]:
                    print(f"  {Colors.WHITE}• {line.strip()}{Colors.RESET}")
                if count > 5:
                    print(f"  {Colors.DIM}... and {count-5} more{Colors.RESET}")
                
                self.results['dns_resolved'] = count
                self.suggest_next_steps('dns_resolution')
                
            except Exception as e:
                print(f"{Colors.RED}[!] Error reading DNS results: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] DNS resolution failed{Colors.RESET}")
    
    def run_alive_hosts_check(self):
        """Check which hosts are alive using HTTPx"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        subdomains_file = f"{self.output_dir}/subdomains.txt"
        if not os.path.exists(subdomains_file):
            print(f"{Colors.RED}[!] No subdomains found! Run subdomain enumeration first.{Colors.RESET}")
            return
        
        if not self.tools_status.get('httpx', {}).get('installed'):
            print(f"{Colors.RED}[!] HTTPx not installed! Install with: go install github.com/projectdiscovery/httpx/cmd/httpx@latest{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Checking Alive Hosts...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/alive.txt"
        cmd = f"httpx -l {subdomains_file} -ports 80,443,8080,8443,3000,5000,8000,9000 -timeout 10 -o {output_file}"
        
        if self.run_command(cmd, timeout=600):
            # Count results
            try:
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                    count = len(lines)
                
                print(f"{Colors.GREEN}[✔] Alive hosts check completed{Colors.RESET}")
                print(f"{Colors.GREEN}[✔] Found {count} alive hosts{Colors.RESET}")
                
                # Display sample results
                print(f"\n{Colors.CYAN}[*] Sample alive hosts:{Colors.RESET}")
                for line in lines[:5]:
                    print(f"  {Colors.WHITE}• {line.strip()}{Colors.RESET}")
                if count > 5:
                    print(f"  {Colors.DIM}... and {count-5} more{Colors.RESET}")
                
                self.results['alive_hosts'] = count
                self.suggest_next_steps('alive_hosts')
                
            except Exception as e:
                print(f"{Colors.RED}[!] Error reading alive hosts results: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Alive hosts check failed{Colors.RESET}")
    
    def run_fast_port_scan(self):
        """Run fast port scan using Naabu"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            # Fallback to subdomains file
            alive_file = f"{self.output_dir}/subdomains.txt"
            if not os.path.exists(alive_file):
                print(f"{Colors.RED}[!] No hosts to scan! Run subdomain enumeration first.{Colors.RESET}")
                return
        
        # Check if Naabu is available, fallback to Nmap
        use_naabu = self.tools_status.get('naabu', {}).get('installed')
        use_nmap = self.tools_status.get('nmap', {}).get('installed')
        
        if not use_naabu and not use_nmap:
            print(f"{Colors.RED}[!] No port scanning tools available!{Colors.RESET}")
            return
        
        scanner = "Naabu" if use_naabu else "Nmap"
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Fast Port Scan with {scanner}...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/ports_fast.txt"
        
        if use_naabu:
            # Naabu fast scan on common ports
            cmd = f"naabu -l {alive_file} -p 1-1000 -rate 1000 -o {output_file}"
            timeout = 300
        else:
            # Nmap fast scan
            cmd = f"nmap -iL {alive_file} -p 1-1000 -T4 --open -oG {output_file}"
            timeout = 600
        
        if self.run_command(cmd, timeout=timeout):
            print(f"{Colors.GREEN}[✔] Fast port scan completed with {scanner}{Colors.RESET}")
            
            # Process and display results
            try:
                results = []
                with open(output_file, 'r') as f:
                    for line in f:
                        if use_naabu:
                            # Naabu format: host:port
                            if ':' in line:
                                host, port = line.strip().split(':')
                                results.append(f"{host}:{port}")
                        else:
                            # Nmap format processing
                            if '/open/' in line:
                                parts = line.split()
                                if len(parts) >= 2:
                                    host = parts[1]
                                    # Extract ports
                                    ports_match = re.search(r'(\d+)/open/', line)
                                    if ports_match:
                                        port = ports_match.group(1)
                                        results.append(f"{host}:{port}")
                
                count = len(results)
                print(f"{Colors.GREEN}[✔] Found {count} open ports{Colors.RESET}")
                
                # Create clean output file
                with open(output_file, 'w') as f:
                    for result in sorted(results):
                        f.write(f"{result}\n")
                
                # Display sample results
                print(f"\n{Colors.CYAN}[*] Sample open ports:{Colors.RESET}")
                for result in results[:10]:
                    print(f"  {Colors.WHITE}• {result}{Colors.RESET}")
                if count > 10:
                    print(f"  {Colors.DIM}... and {count-10} more{Colors.RESET}")
                
                self.results['fast_ports'] = count
                self.suggest_next_steps('port_scan')
                
            except Exception as e:
                print(f"{Colors.RED}[!] Error processing port scan results: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Fast port scan failed{Colors.RESET}")
    
    def run_full_port_scan(self):
        """Run comprehensive port scan using Nmap"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        if not self.tools_status.get('nmap', {}).get('installed'):
            print(f"{Colors.RED}[!] Nmap not installed! Install with: sudo apt install nmap{Colors.RESET}")
            return
        
        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            alive_file = f"{self.output_dir}/subdomains.txt"
            if not os.path.exists(alive_file):
                print(f"{Colors.RED}[!] No hosts to scan! Run subdomain enumeration first.{Colors.RESET}")
                return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Full Port Scan with Nmap...{Colors.RESET}\n")
        print(f"{Colors.YELLOW}[!] This may take a while. Press Ctrl+C to skip.{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/ports_full.txt"
        cmd = f"nmap -iL {alive_file} -p- -sV -sC -O --open -T4 -oA {output_file.replace('.txt', '')}"
        
        if self.run_command(cmd, timeout=3600):  # 1 hour timeout
            print(f"{Colors.GREEN}[✔] Full port scan completed{Colors.RESET}")
            
            # Process results
            try:
                xml_file = output_file.replace('.txt', '.xml')
                if os.path.exists(xml_file):
                    # Parse XML results
                    import xml.etree.ElementTree as ET
                    tree = ET.parse(xml_file)
                    root = tree.getroot()
                    
                    results = []
                    for host in root.findall('host'):
                        address = host.find('address').get('addr')
                        for port in host.find('ports').findall('port'):
                            if port.find('state').get('state') == 'open':
                                port_num = port.get('portid')
                                service = port.find('service')
                                service_name = service.get('name', 'unknown')
                                version = service.get('version', '')
                                product = service.get('product', '')
                                
                                info = f"{service_name}"
                                if product:
                                    info += f" {product}"
                                if version:
                                    info += f" {version}"
                                
                                results.append(f"{address}:{port_num} ({info})")
                    
                    count = len(results)
                    print(f"{Colors.GREEN}[✔] Found {count} detailed service results{Colors.RESET}")
                    
                    # Save processed results
                    with open(output_file, 'w') as f:
                        for result in sorted(results):
                            f.write(f"{result}\n")
                    
                    # Display sample results
                    print(f"\n{Colors.CYAN}[*] Sample service discoveries:{Colors.RESET}")
                    for result in results[:10]:
                        print(f"  {Colors.WHITE}• {result}{Colors.RESET}")
                    if count > 10:
                        print(f"  {Colors.DIM}... and {count-10} more{Colors.RESET}")
                    
                    self.results['full_ports'] = count
                    self.suggest_next_steps('port_scan')
                    
            except Exception as e:
                print(f"{Colors.RED}[!] Error processing full scan results: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Full port scan failed{Colors.RESET}")
    
    def run_url_collection(self):
        """Collect URLs from multiple sources"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting URL Collection...{Colors.RESET}\n")
        
        tools_used = []
        raw_files = []
        
        # Katana
        if self.tools_status.get('katana', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Katana crawler...{Colors.RESET}")
            katana_output = f"{self.output_dir}/katana_raw.txt"
            cmd = f"katana -u {self.domain} -d 3 -o {katana_output}"
            if self.run_command(cmd, timeout=300):
                tools_used.append('Katana')
                raw_files.append(katana_output)
                print(f"{Colors.GREEN}[✔] Katana completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Katana failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Katana not installed, skipping{Colors.RESET}")
        
        # Gau (Get All URLs)
        if self.tools_status.get('gau', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Gau...{Colors.RESET}")
            gau_output = f"{self.output_dir}/gau_raw.txt"
            cmd = f"gau {self.domain} > {gau_output}"
            if self.run_command(cmd, timeout=300):
                tools_used.append('Gau')
                raw_files.append(gau_output)
                print(f"{Colors.GREEN}[✔] Gau completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Gau failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Gau not installed, skipping{Colors.RESET}")
        
        # Waybackurls
        if self.tools_status.get('waybackurls', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Waybackurls...{Colors.RESET}")
            wayback_output = f"{self.output_dir}/waybackurls_raw.txt"
            cmd = f"waybackurls {self.domain} > {wayback_output}"
            if self.run_command(cmd, timeout=300):
                tools_used.append('Waybackurls')
                raw_files.append(wayback_output)
                print(f"{Colors.GREEN}[✔] Waybackurls completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Waybackurls failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Waybackurls not installed, skipping{Colors.RESET}")
        
        if not raw_files:
            print(f"{Colors.RED}[!] No URL collection tools available!{Colors.RESET}")
            return
        
        # Merge and deduplicate results
        final_output = f"{self.output_dir}/urls.txt"
        
        print(f"{Colors.YELLOW}[*] Merging and cleaning URL results...{Colors.RESET}")
        try:
            unique_urls = set()
            for file_path in raw_files:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line in f:
                            url = line.strip()
                            if url and url.startswith(('http://', 'https://')):
                                # Clean URL
                                url = url.split('#')[0]  # Remove fragments
                                if not url.endswith(('.jpg', '.png', '.gif', '.css', '.js', '.ico')):
                                    unique_urls.add(url)
            
            with open(final_output, 'w') as f:
                for url in sorted(unique_urls):
                    f.write(f"{url}\n")
            
            count = len(unique_urls)
            print(f"{Colors.GREEN}[✔] Found {count} unique URLs{Colors.RESET}")
            
            # Display sample results
            print(f"\n{Colors.CYAN}[*] Sample URLs found:{Colors.RESET}")
            sample = list(unique_urls)[:10]
            for url in sample:
                print(f"  {Colors.WHITE}• {url}{Colors.RESET}")
            if count > 10:
                print(f"  {Colors.DIM}... and {count-10} more{Colors.RESET}")
            
            self.results['urls'] = count
            self.suggest_next_steps('urls')
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error processing URL results: {e}{Colors.RESET}")
    
    def run_waf_detection(self):
        """Detect Web Application Firewalls"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found! Run alive hosts check first.{Colors.RESET}")
            return
        
        if not self.tools_status.get('wafw00f', {}).get('installed'):
            print(f"{Colors.RED}[!] Wafw00f not installed! Install with: sudo apt install wafw00f{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting WAF Detection...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/waf_summary.txt"
        
        # Read alive hosts
        try:
            with open(alive_file, 'r') as f:
                hosts = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}[!] Error reading alive hosts: {e}{Colors.RESET}")
            return
        
        results = []
        total_hosts = len(hosts)
        
        print(f"{Colors.YELLOW}[*] Testing {total_hosts} hosts for WAF...{Colors.RESET}")
        
        for i, host in enumerate(hosts):
            print(f"  Progress: {i+1}/{total_hosts} - Testing {host}", end='\r')
            
            cmd = f"wafw00f {host}"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                
                # Parse wafw00f output
                if 'is behind' in output:
                    waf_match = re.search(r'is behind\s+(.+?)\s+WAF', output)
                    if waf_match:
                        waf_name = waf_match.group(1).strip()
                        results.append(f"{host}: {waf_name}")
                        print(f"  {Colors.RED}[WAF] {host}: {waf_name}{Colors.RESET}")
                    else:
                        results.append(f"{host}: WAF detected (unknown type)")
                        print(f"  {Colors.RED}[WAF] {host}: Unknown{Colors.RESET}")
                elif 'No WAF detected' in output:
                    results.append(f"{host}: No WAF")
                else:
                    results.append(f"{host}: Unknown/Error")
                    
            except subprocess.TimeoutExpired:
                results.append(f"{host}: Timeout")
            except Exception as e:
                results.append(f"{host}: Error - {str(e)}")
        
        print(f"\n{Colors.GREEN}[✔] WAF detection completed{Colors.RESET}")
        
        # Save results
        try:
            with open(output_file, 'w') as f:
                for result in results:
                    f.write(f"{result}\n")
            
            # Count WAF results
            waf_count = len([r for r in results if 'WAF' in r and 'No WAF' not in r])
            no_waf_count = len([r for r in results if 'No WAF' in r])
            
            print(f"{Colors.GREEN}[✔] Results saved to {output_file}{Colors.RESET}")
            print(f"\n{Colors.CYAN}[*] WAF Detection Summary:{Colors.RESET}")
            print(f"  {Colors.RED}• Hosts with WAF: {waf_count}{Colors.RESET}")
            print(f"  {Colors.GREEN}• Hosts without WAF: {no_waf_count}{Colors.RESET}")
            print(f"  {Colors.WHITE}• Total tested: {total_hosts}{Colors.RESET}")
            
            self.results['waf_detected'] = waf_count
            self.results['waf_total'] = total_hosts
            self.suggest_next_steps('waf_detection')
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error saving WAF results: {e}{Colors.RESET}")
    
    def run_vulnerability_scan(self):
        """Run vulnerability scanning with Nuclei"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found! Run alive hosts check first.{Colors.RESET}")
            return
        
        if not self.tools_status.get('nuclei', {}).get('installed'):
            print(f"{Colors.RED}[!] Nuclei not installed! Install with: go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Vulnerability Scan...{Colors.RESET}\n")
        
        # Ask about template updates
        update_templates = input(f"{Colors.YELLOW}[?] Update Nuclei templates before scanning? (y/n): {Colors.RESET}").lower().strip()
        if update_templates == 'y':
            print(f"{Colors.YELLOW}[*] Updating Nuclei templates...{Colors.RESET}")
            if self.run_command("nuclei -ut", timeout=600):
                print(f"{Colors.GREEN}[✔] Templates updated{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Template update failed, continuing...{Colors.RESET}")
        
        output_file = f"{self.output_dir}/nuclei_output.txt"
        cmd = f"nuclei -l {alive_file} -t exposures/,misconfiguration/,vulnerabilities/ -severity low,medium,high,critical -o {output_file}"
        
        print(f"{Colors.YELLOW}[*] Running Nuclei vulnerability scan...{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] This may take several minutes...{Colors.RESET}")
        
        if self.run_command(cmd, timeout=1800):  # 30 minutes
            # Process results
            try:
                with open(output_file, 'r') as f:
                    lines = f.readlines()
                
                # Categorize vulnerabilities by severity
                vulnerabilities = {'critical': [], 'high': [], 'medium': [], 'low': []}
                
                for line in lines:
                    line = line.strip()
                    if '[critical]' in line:
                        vulnerabilities['critical'].append(line)
                    elif '[high]' in line:
                        vulnerabilities['high'].append(line)
                    elif '[medium]' in line:
                        vulnerabilities['medium'].append(line)
                    elif '[low]' in line:
                        vulnerabilities['low'].append(line)
                
                total_vulns = sum(len(v) for v in vulnerabilities.values())
                
                print(f"{Colors.GREEN}[✔] Vulnerability scan completed{Colors.RESET}")
                print(f"\n{Colors.CYAN}[*] Vulnerability Summary:{Colors.RESET}")
                print(f"  {Colors.RED}[Critical] {len(vulnerabilities['critical'])}{Colors.RESET}")
                print(f"  {Colors.RED}[High]     {len(vulnerabilities['high'])}{Colors.RESET}")
                print(f"  {Colors.YELLOW}[Medium]   {len(vulnerabilities['medium'])}{Colors.RESET}")
                print(f"  {Colors.GREEN}[Low]      {len(vulnerabilities['low'])}{Colors.RESET}")
                print(f"  {Colors.WHITE}Total:     {total_vulns}{Colors.RESET}")
                
                # Display critical and high severity findings
                if vulnerabilities['critical'] or vulnerabilities['high']:
                    print(f"\n{Colors.RED}[!] Critical/High Severity Findings:{Colors.RESET}")
                    for vuln in vulnerabilities['critical'][:5] + vulnerabilities['high'][:5]:
                        print(f"  {Colors.RED}• {vuln[:100]}...{Colors.RESET}")
                
                self.results['vulnerabilities'] = total_vulns
                self.results['critical_vulns'] = len(vulnerabilities['critical'])
                self.results['high_vulns'] = len(vulnerabilities['high'])
                
            except Exception as e:
                print(f"{Colors.RED}[!] Error processing vulnerability results: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Vulnerability scan failed{Colors.RESET}")
    
    def run_full_automated_recon(self):
        """Run complete automated reconnaissance sequence"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting FULL AUTOMATED RECON...{Colors.RESET}\n")
        print(f"{Colors.YELLOW}[!] This will run all available reconnaissance tools.{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Estimated time: 15-60 minutes depending on target size.{Colors.RESET}\n")
        
        # Confirm with user
        confirm = input(f"{Colors.YELLOW}[?] Continue with full automated recon? (y/n): {Colors.RESET}").lower().strip()
        if confirm != 'y':
            print(f"{Colors.YELLOW}[!] Cancelled by user.{Colors.RESET}")
            return
        
        # Clear previous results
        self.results = {}
        start_time = time.time()
        
        # Phase 1: Subdomain Enumeration
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 1: SUBDOMAIN ENUMERATION                      ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run subdomain enumeration? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_subdomain_enumeration()
        else:
            print(f"{Colors.YELLOW}[!] Skipping subdomain enumeration{Colors.RESET}")
        
        # Phase 2: DNS Resolution
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 2: DNS RESOLUTION                             ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run DNS resolution? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_dns_resolution()
        else:
            print(f"{Colors.YELLOW}[!] Skipping DNS resolution{Colors.RESET}")
        
        # Phase 3: Alive Hosts Check
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 3: ALIVE HOSTS CHECK                          ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run alive hosts check? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_alive_hosts_check()
        else:
            print(f"{Colors.YELLOW}[!] Skipping alive hosts check{Colors.RESET}")
        
        # Phase 4: Port Scanning
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 4: PORT SCANNING                              ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run fast port scan? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_fast_port_scan()
        else:
            print(f"{Colors.YELLOW}[!] Skipping fast port scan{Colors.RESET}")
        
        if input(f"{Colors.YELLOW}[?] Run full port scan? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_full_port_scan()
        else:
            print(f"{Colors.YELLOW}[!] Skipping full port scan{Colors.RESET}")
        
        # Phase 5: URL Collection
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 5: URL COLLECTION                             ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run URL collection? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_url_collection()
        else:
            print(f"{Colors.YELLOW}[!] Skipping URL collection{Colors.RESET}")
        
        # Phase 6: WAF Detection
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 6: WAF DETECTION                              ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run WAF detection? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_waf_detection()
        else:
            print(f"{Colors.YELLOW}[!] Skipping WAF detection{Colors.RESET}")
        
        # Phase 7: Vulnerability Scanning
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          PHASE 7: VULNERABILITY SCANNING                     ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        if input(f"{Colors.YELLOW}[?] Run vulnerability scan? (y/n): {Colors.RESET}").lower().strip() == 'y':
            self.run_vulnerability_scan()
        else:
            print(f"{Colors.YELLOW}[!] Skipping vulnerability scan{Colors.RESET}")
        
        # Generate final summary
        end_time = time.time()
        duration = int(end_time - start_time)
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════════════╗")
        print(f"║                          RECONNAISSANCE COMPLETED                           ║")
        print(f"╚══════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        self.generate_summary(duration)
        
        print(f"\n{Colors.GREEN}[✔] Full automated recon completed in {duration} seconds{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] All results saved to: {self.output_dir}/{Colors.RESET}")
    
    def generate_summary(self, duration=None):
        """Generate comprehensive reconnaissance summary"""
        summary_file = f"{self.output_dir}/summary.txt"
        
        try:
            with open(summary_file, 'w') as f:
                f.write("="*80 + "\n")
                f.write("                        RECONMASTER SUMMARY REPORT\n")
                f.write("="*80 + "\n\n")
                
                f.write(f"Target Domain: {self.domain}\n")
                f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                if duration:
                    f.write(f"Total Duration: {duration} seconds\n")
                f.write(f"Output Directory: {self.output_dir}\n\n")
                
                f.write("-"*80 + "\n")
                f.write("                           DISCOVERY RESULTS\n")
                f.write("-"*80 + "\n\n")
                
                # Subdomains
                subdomains_count = self.results.get('subdomains', 0)
                f.write(f"Subdomains Discovered: {subdomains_count}\n")
                if subdomains_count > 0:
                    f.write(f"  • File: {self.output_dir}/subdomains.txt\n")
                
                # DNS Resolution
                dns_count = self.results.get('dns_resolved', 0)
                f.write(f"DNS Records Resolved: {dns_count}\n")
                if dns_count > 0:
                    f.write(f"  • File: {self.output_dir}/dns_resolved.txt\n")
                
                # Alive Hosts
                alive_count = self.results.get('alive_hosts', 0)
                f.write(f"Alive Hosts Found: {alive_count}\n")
                if alive_count > 0:
                    f.write(f"  • File: {self.output_dir}/alive.txt\n")
                
                # Port Scanning
                fast_ports = self.results.get('fast_ports', 0)
                full_ports = self.results.get('full_ports', 0)
                f.write(f"Open Ports (Fast Scan): {fast_ports}\n")
                if fast_ports > 0:
                    f.write(f"  • File: {self.output_dir}/ports_fast.txt\n")
                f.write(f"Service Details (Full Scan): {full_ports}\n")
                if full_ports > 0:
                    f.write(f"  • File: {self.output_dir}/ports_full.txt\n")
                
                # URLs
                urls_count = self.results.get('urls', 0)
                f.write(f"URLs Collected: {urls_count}\n")
                if urls_count > 0:
                    f.write(f"  • File: {self.output_dir}/urls.txt\n")
                
                # WAF Detection
                waf_total = self.results.get('waf_total', 0)
                waf_detected = self.results.get('waf_detected', 0)
                f.write(f"WAF Detection Results: {waf_detected}/{waf_total} hosts protected\n")
                if waf_total > 0:
                    f.write(f"  • File: {self.output_dir}/waf_summary.txt\n")
                
                # Vulnerabilities
                vuln_count = self.results.get('vulnerabilities', 0)
                critical_count = self.results.get('critical_vulns', 0)
                high_count = self.results.get('high_vulns', 0)
                f.write(f"Vulnerabilities Found: {vuln_count}\n")
                if vuln_count > 0:
                    f.write(f"  • Critical: {critical_count}\n")
                    f.write(f"  • High: {high_count}\n")
                    f.write(f"  • File: {self.output_dir}/nuclei_output.txt\n")
                
                f.write("\n" + "-"*80 + "\n")
                f.write("                            TOOL STATUS\n")
                f.write("-"*80 + "\n\n")
                
                for tool, status in self.tools_status.items():
                    if status.get('installed'):
                        f.write(f"✔ {tool.capitalize()}: Installed\n")
                    else:
                        f.write(f"✘ {tool.capitalize()}: Not Installed\n")
                        if 'install_command' in status:
                            f.write(f"  Install: {status['install_command']}\n")
                
                f.write("\n" + "-"*80 + "\n")
                f.write("                         RECOMMENDATIONS\n")
                f.write("-"*80 + "\n\n")
                
                # Generate recommendations based on results
                recommendations = []
                
                if subdomains_count > 100:
                    recommendations.append("Large attack surface discovered - focus on high-value targets")
                
                if vuln_count > 0:
                    recommendations.append("Vulnerabilities found - prioritize critical and high severity issues")
                    if critical_count > 0:
                        recommendations.append("CRITICAL vulnerabilities require immediate attention")
                
                if waf_detected < waf_total * 0.5:
                    recommendations.append("Many hosts lack WAF protection - consider for deeper testing")
                
                if alive_count < subdomains_count * 0.1:
                    recommendations.append("Low alive host ratio - investigate DNS/CDN configurations")
                
                recommendations.extend([
                    "Review all output files for detailed findings",
                    "Perform manual testing on interesting endpoints",
                    "Consider authenticated testing if credentials available",
                    "Monitor for changes with periodic re-scanning"
                ])
                
                for i, rec in enumerate(recommendations, 1):
                    f.write(f"{i}. {rec}\n")
                
                f.write("\n" + "="*80 + "\n")
                f.write("                    ReconMaster - Professional Recon Framework\n")
                f.write("="*80 + "\n")
            
            print(f"\n{Colors.GREEN}[✔] Summary generated: {summary_file}{Colors.RESET}")
            
            # Display summary
            print(f"\n{Colors.CYAN}{Colors.BOLD}[*] RECON SUMMARY:{Colors.RESET}")
            print(f"  {Colors.WHITE}• Subdomains: {self.results.get('subdomains', 0)}{Colors.RESET}")
            print(f"  {Colors.WHITE}• Alive Hosts: {self.results.get('alive_hosts', 0)}{Colors.RESET}")
            print(f"  {Colors.WHITE}• Open Ports: {self.results.get('fast_ports', 0) + self.results.get('full_ports', 0)}{Colors.RESET}")
            print(f"  {Colors.WHITE}• URLs Found: {self.results.get('urls', 0)}{Colors.RESET}")
            print(f"  {Colors.WHITE}• WAF Protected: {self.results.get('waf_detected', 0)}/{self.results.get('waf_total', 0)}{Colors.RESET}")
            
            vuln_count = self.results.get('vulnerabilities', 0)
            if vuln_count > 0:
                critical = self.results.get('critical_vulns', 0)
                high = self.results.get('high_vulns', 0)
                print(f"  {Colors.RED}• Vulnerabilities: {vuln_count} (Critical: {critical}, High: {high}){Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error generating summary: {e}{Colors.RESET}")
    
    def run(self):
        """Main execution loop"""
        self.display_banner()
        
        # Initialize tools
        self.initialize_tools()
        
        # Main menu loop
        while True:
            self.display_menu()
            
            choice = input(f"{Colors.CYAN}[+] Select option: {Colors.RESET}").strip().upper()
            
            if choice == '1':
                self.run_subdomain_enumeration()
            elif choice == '2':
                self.run_dns_resolution()
            elif choice == '3':
                self.run_alive_hosts_check()
            elif choice == '4':
                self.run_fast_port_scan()
            elif choice == '5':
                self.run_full_port_scan()
            elif choice == '6':
                self.run_url_collection()
            elif choice == '7':
                self.run_waf_detection()
            elif choice == '8':
                self.run_vulnerability_scan()
            elif choice == '9':
                self.run_full_automated_recon()
            elif choice == 'C':
                self.setup_domain()
            elif choice == 'I':
                self.initialize_tools()
            elif choice == 'H':
                self.show_help()
            elif choice == 'Q':
                print(f"\n{Colors.GREEN}[✔] Thank you for using ReconMaster!{Colors.RESET}")
                print(f"{Colors.CYAN}    Happy hunting! 🎯{Colors.RESET}\n")
                break
            else:
                print(f"{Colors.RED}[!] Invalid option! Please try again.{Colors.RESET}")
            
            if choice != 'H':
                input(f"\n{Colors.CYAN}[*] Press Enter to continue...{Colors.RESET}")

def main():
    """Main entry point"""
    try:
        recon_master = ReconMaster()
        recon_master.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Interrupted by user. Goodbye!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Fatal error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
