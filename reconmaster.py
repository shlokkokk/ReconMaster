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

from email.mime import base
from itertools import count
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
from unittest import result

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

    def find_tool(self, name):
        paths = [
            shutil.which(name),
            f"/usr/local/bin/{name}",
            f"/usr/bin/{name}",
            f"/root/go/bin/{name}",
            f"/opt/recontools/{name}/{name}",
        ]
        for p in paths:
            if p and os.path.exists(p):
                return p
        return None

    def get_tool(self, name, fallback=None):
        """
        Return the best path to a tool:
        - Use self.tools_status[name]['path'] if it exists and is valid
        - Else use fallback if given
        - Else just return the name (hope it's in PATH)
        """
        info = self.tools_status.get(name)
        if isinstance(info, dict):
            path = info.get('path')
            if path and os.path.exists(path):
                return path
        return fallback or name


        
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
║                  {Colors.WHITE}Professional Reconnaissance Framework v2.0{Colors.CYAN}                                      ║ 
║                        {Colors.WHITE}For Kali Linux Bug Bounty Hunters{Colors.CYAN}                                         ║                                           
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝

{Colors.RESET}
"""
        print(banner)
        
    
    def check_tool_installation(self, tool_name, install_command=None):
        """
        Check if a tool is installed.

        - For normal CLI tools: ugh
        - For special tools (ParamSpider, Arjun, etc.): we handle them separately in initialize_tools()
        """
        path = self.find_tool(tool_name)


        if path:
            self.tools_status[tool_name] = {
                'installed': True,
                'path': path
            }
            return True

        # If not found, record as missing
        self.tools_status[tool_name] = {
            'installed': False,
            'install_command': install_command or f'sudo apt install {tool_name}'
        }
        return False
    
    def initialize_tools(self):
        """Initialize and check all required tools"""

        # CLI-based tools that MUST exist in PATH
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
            ('whatweb', 'sudo apt install whatweb'),
            ('sqlmap', 'sudo apt install sqlmap'),
            ('nuclei', 'go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest'),
            ('hakrawler', 'go install github.com/hakluke/hakrawler@latest'),
            ('ffuf', 'go install github.com/ffuf/ffuf@latest'),
            
            ('dalfox', 'go install github.com/hahwul/dalfox/v2@latest'),
            ('asnmap', 'go install github.com/projectdiscovery/asnmap/cmd/asnmap@latest'),
            ('gowitness', 'go install github.com/sensepost/gowitness@latest'),
            ('gf', 'go install github.com/tomnomnom/gf@latest'),

        
            ('massdns', 'binary expected at /usr/local/bin/massdns'),
        ]

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Checking Tool Installation Status...{Colors.RESET}\n")

        # 2️ Check CLI tools using check_tool_installation()
        for tool, install_cmd in tools_to_check:
            status = "✔" if self.check_tool_installation(tool, install_cmd) else "✘"
            color = Colors.GREEN if status == "✔" else Colors.RED
            print(f"  {color}[{status}] {tool.capitalize()}{Colors.RESET}")
        # 3️ Tools that DO NOT have CLI but exist as python files in /opt
        special_tools = {
            'paramspider': '/opt/recontools/ParamSpider/paramspider.py',
            'arjun': '/opt/recontools/Arjun/arjun.py',
            'xsstrike': '/opt/recontools/XSStrike/xsstrike.py',
            'smuggler': '/opt/recontools/smuggler/smuggler.py',
            'linkfinder': '/opt/recontools/LinkFinder/linkfinder.py',
            'subzy': self.find_tool('subzy'),
            'kr': self.find_tool('kr'),

        }

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Checking Python/Opt-based Tools...{Colors.RESET}\n")

        for name, path in special_tools.items():

            exists = os.path.exists(path) if isinstance(path, str) else bool(path)

            self.tools_status[name] = {
                'installed': exists,
                'path': path,
                'install_command': 'Installed via install.sh in /opt/recontools'
            }
            status = "✔" if exists else "✘"
            color = Colors.GREEN if exists else Colors.RED
            print(f"  {color}[{status}] {name.capitalize()}{Colors.RESET}")

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
        domain_pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
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
║    {Colors.WHITE}[2] DNS Resolution{Colors.CYAN}             - Resolve DNS records for found subdomains                            ║
║    {Colors.WHITE}[3] Alive Hosts Check{Colors.CYAN}          - Check which hosts are alive via HTTP                                ║
║    {Colors.WHITE}[4] Fast Port Scan{Colors.CYAN}             - Quick port scan using Naabu                                         ║
║    {Colors.WHITE}[5] Full Port Scan{Colors.CYAN}             - Comprehensive scan with Nmap                                        ║
║    {Colors.WHITE}[6] URL Collection{Colors.CYAN}             - Gather URLs from multiple sources                                   ║
║    {Colors.WHITE}[7] WAF Detection{Colors.CYAN}              - Identify Web Application Firewalls                                  ║
║    {Colors.WHITE}[8] Vulnerability Scan{Colors.CYAN}         - Scan for vulnerabilities with Nuclei                                ║
║    {Colors.WHITE}[9] FULL AUTOMATED RECON{Colors.CYAN}       - Run complete reconnaissance sequence                                ║
║    {Colors.WHITE}[10] Parameter Discovery{Colors.CYAN}       - ParamSpider + Arjun for hidden parameters                           ║
║    {Colors.WHITE}[11] JS Endpoint Extraction{Colors.CYAN}    - LinkFinder + JS parsing                                             ║
║    {Colors.WHITE}[12] Directory Fuzzing{Colors.CYAN}         - FFUF-based directory bruteforce                                     ║
║    {Colors.WHITE}[13] API Fuzzing{Colors.CYAN}               - API endpoint fuzzing with Kiterunner                                ║
║    {Colors.WHITE}[14] Subdomain Takeover Check{Colors.CYAN}  - Detect vulnerable subdomains (Subzy)                                ║
║    {Colors.WHITE}[15] Advanced URL Enum{Colors.CYAN}         - Deep crawling using Hakrawler                                       ║
║    {Colors.WHITE}[16] Screenshot Capture{Colors.CYAN}        - Take screenshots of alive hosts (Gowitness)                         ║
║    {Colors.WHITE}[17] DNS Bruteforce{Colors.CYAN}            - Bruteforce DNS with MassDNS                                         ║
║    {Colors.WHITE}[18] GF Filters{Colors.CYAN}                - Detect XSS, SQLi, LFI, SSRF, RCE patterns                           ║
║    {Colors.WHITE}[19] Tech Scan{Colors.CYAN}                 - Fingerprint technologies using WhatWeb                              ║ 
║    {Colors.WHITE}[20] SQLi Scan{Colors.CYAN}                 - Auto SQL Injection detection using SQLMap                           ║                                                                                                                                    
║    {Colors.WHITE}[D] Deep Recon Mode{Colors.CYAN}            - Run all advanced modules together                                   ║                                                                                    
║                                                                                                         ║
║    {Colors.WHITE}[C] Change Domain{Colors.CYAN}             - Set a different target domain                                        ║
║    {Colors.WHITE}[I] Initialize Tools{Colors.CYAN}          - Check and install required tools                                     ║
║    {Colors.WHITE}[H] Help{Colors.CYAN}                      - Show detailed help information                                       ║
║    {Colors.WHITE}[Q] Quit{Colors.CYAN}                      - Exit the framework                                                   ║
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

{Colors.WHITE}{Colors.BOLD}CORE WORKFLOW (MENU 1 - 9):{Colors.RESET}
    1. {Colors.CYAN}Set Target Domain{Colors.RESET} - Configure your target
    2. {Colors.CYAN}Run Subdomain Enumeration (1){Colors.RESET} - Discover subdomains
    3. {Colors.CYAN}DNS Resolution (2){Colors.RESET} - Resolve DNS records
    4. {Colors.CYAN}Alive Hosts Check (3){Colors.RESET} - Find live targets
    5. {Colors.CYAN}Port Scanning (4 & 5){Colors.RESET} - Discover open services
    6. {Colors.CYAN}URL Collection (6){Colors.RESET} - Gather endpoint URLs
    7. {Colors.CYAN}WAF Detection (7){Colors.RESET} - Identify protection systems
    8. {Colors.CYAN}Vulnerability Scanning (8){Colors.RESET} - Find security issues
    9. {Colors.CYAN}Full Automated Recon (9){Colors.RESET} - Run core chain 1-8

{Colors.WHITE}{Colors.BOLD}ADVANCED MODULES (MENU 10 - 20, D):{Colors.RESET}
    10. {Colors.CYAN}Parameter Discovery{Colors.RESET}         - ParamSpider + Arjun on URLs
    11. {Colors.CYAN}JS Endpoint Extraction{Colors.RESET}      - LinkFinder + custom secret finder
    12. {Colors.CYAN}Directory Fuzzing{Colors.RESET}           - FFUF with recursion and smart filters
    13. {Colors.CYAN}API Fuzzing{Colors.RESET}                 - Kiterunner (kr) on alive hosts
    14. {Colors.CYAN}Subdomain Takeover Check{Colors.RESET}    - Subzy + CNAME pattern check
    15. {Colors.CYAN}Advanced URL Enum{Colors.RESET}           - Hakrawler deep crawling
    16. {Colors.CYAN}Screenshot Capture{Colors.RESET}          - Gowitness on alive hosts
    17. {Colors.CYAN}DNS Bruteforce{Colors.RESET}              - MassDNS + merge into subdomains
    18. {Colors.CYAN}GF Filters{Colors.RESET}                  - gf for XSS, SQLi, LFI, SSRF, RCE, Redirect
    19. {Colors.CYAN}Tech Scan{Colors.RESET}                   - WhatWeb technology fingerprinting
    20. {Colors.CYAN}SQLi Scan{Colors.RESET}                   - SQLMap on parameterized URLs

    D.  {Colors.CYAN}Deep Recon Mode{Colors.RESET}
        Full advanced chain:
        URLs -> Advanced URLs -> JS endpoints -> Params -> Dir fuzzing ->
        API fuzzing -> Takeover -> GF filters -> Tech scan -> SQL scan ->
        Screenshots -> DNS bruteforce

{Colors.WHITE}{Colors.BOLD}OUTPUT STRUCTURE (MAIN):{Colors.RESET}
    output-domain.com/
    ├── subdomains_raw.txt          # Raw subdomain results (merged)
    ├── subdomains.txt              # Cleaned subdomain list
    ├── dns_resolved.txt            # DNS resolution results
    ├── alive.txt                   # Live hosts (httpx)
    ├── ports_fast.txt              # Fast port scan results (Naabu/Nmap)
    ├── ports_full.txt              # Full service scan (Nmap)
    ├── urls.txt                    # Base collected URLs (Katana/Gau/Wayback)
    ├── urls_final.txt              # All merged URLs (base + JS + advanced)
    ├── waf_summary.txt             # WAF detection results
    ├── nuclei_output.txt           # Vulnerability scan results (Nuclei)
    ├── summary.txt                 # ReconMaster summary report
    ├── logs/                       # Execution logs

{Colors.WHITE}{Colors.BOLD}OUTPUT STRUCTURE (ADVANCED MODULES):{Colors.RESET}
    ├── js_endpoints/               # JS URLs, endpoints, secrets
    │   ├── js_raw_urls.txt
    │   ├── js_files/
    │   ├── endpoints_raw.txt
    │   ├── endpoints.txt           # Clean JS endpoints
    │   └── secrets.txt             # Potential API keys/tokens
    ├── parameters/                 # ParamSpider + Arjun results
    │   ├── paramspider.txt
    │   ├── arjun.json
    │   └── parameters_final.txt
    ├── fuzzing/                    # FFUF directory fuzzing per host
    ├── api_fuzzing/                # Kiterunner (kr) API endpoints
    ├── takeover/                   # Subzy + CNAME fallback findings
    ├── screenshots/                # Gowitness screenshots
    ├── dns_bruteforce/             # MassDNS raw + bruteforced subdomains
    ├── advanced_urls/              # Hakrawler deep URLs
    ├── gf/                         # gf filtered URLs (xss, sqli, lfi, ssrf, rce, redirect)
    ├── tech_scan/                  # WhatWeb technology fingerprinting
    └── sqlmap/                     # SQLMap scan outputs

{Colors.WHITE}{Colors.BOLD}TOOL REQUIREMENTS (CORE):{Colors.RESET}
    • subfinder       - Subdomain discovery
    • amass           - Passive subdomain enumeration
    • assetfinder     - Alternative subdomain finder
    • dnsx            - DNS resolution
    • httpx           - HTTP probing (alive hosts)
    • naabu           - Fast port scanner
    • nmap            - Network mapper / detailed scan
    • katana          - Web crawler
    • gau             - Get All URLs (past data)
    • waybackurls     - Wayback Machine URLs
    • wafw00f         - WAF detection
    • nuclei          - Vulnerability scanner

{Colors.WHITE}{Colors.BOLD}TOOL REQUIREMENTS (ADVANCED):{Colors.RESET}
    • paramspider     - Parameter discovery from URLs
    • arjun           - Parameter discovery (wordlist-based)
    • ffuf            - Directory fuzzing
    • kr (kiterunner) - API fuzzing
    • subzy           - Subdomain takeover detection
    • hakrawler       - Deep URL enumeration
    • gowitness       - HTTP screenshot capture
    • massdns         - High performance DNS bruteforce
    • gf              - Filter URLs for XSS/SQLi/LFI/SSRF/RCE/Redirect
    • whatweb         - Technology fingerprinting
    • sqlmap          - SQL injection testing
    • linkfinder      - JS endpoint extraction

{Colors.YELLOW}Missing tools will be automatically detected and installation
commands will be suggested in the tool check module.{Colors.RESET}

{Colors.WHITE}{Colors.BOLD}TIPS:{Colors.RESET}
    • Run tools in logical sequence for best results (1 -> 2 -> 3 -> 4/5 -> 6 -> 7 -> 8).
    • Use Full Automated Recon (9) for a clean one-shot recon of the target.
    • Use Deep Recon Mode (D) once core recon is done for deeper hunting.
    • Check summary.txt after a full recon to see overall stats and next steps.
    • Monitor logs/ directory if something crashes or behaves unexpectedly.
    • Results are automatically deduplicated and merged wherever possible.

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
            subfinder_bin = self.get_tool('subfinder')
            cmd = f"{subfinder_bin} -d {self.domain} -all -recursive -o {subfinder_output}"
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
            amass_bin = self.get_tool('amass')
            cmd = f"amass enum -passive -d {self.domain} -o {amass_output}"
            if self.run_command(cmd, timeout=1800):
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
            assetfinder_bin = self.get_tool('assetfinder')
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
                        if re.match(r'^[a-zA-Z0-9.-]+$', subdomain):
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
        dnsx_bin = self.get_tool('dnsx')
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
        """Check which hosts are alive using HTTPx (JSON safe parser)"""
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

        # Use JSON output to avoid messy text output with metadata
        raw_httpx_output = f"{self.output_dir}/httpx_raw.json"
        httpx_bin = self.get_tool('httpx')
        cmd = (
            f"{httpx_bin} -l {subdomains_file} "
            f"-sc -title -ip -cdn -json "
            f"-threads 50 "
            f"-timeout 10 "
            f"-o {raw_httpx_output}"
        )

        if not self.run_command(cmd, timeout=600):
            print(f"{Colors.RED}[!] HTTPx scan failed{Colors.RESET}")
            return

        # Parse JSON results safely
        clean_hosts = []
        try:
            with open(raw_httpx_output, "r") as f:
                for line in f:
                    try:
                        j = json.loads(line)
                        clean_hosts.append(j["url"])
                    except:
                        continue
        except Exception as e:
            print(f"{Colors.RED}[!] Failed parsing HTTPx JSON: {e}{Colors.RESET}")
            return
        # Save clean alive hosts
        alive_file = f"{self.output_dir}/alive.txt"
        try:
            with open(alive_file, "w") as f:
                for h in sorted(set(clean_hosts)):
                    f.write(h + "\n")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed writing alive hosts: {e}{Colors.RESET}")
            return
        count = len(clean_hosts)
        if count == 0:
            print(f"{Colors.RED}[!] No alive hosts detected!{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Falling back to main domain during port scan...{Colors.RESET}")


        print(f"{Colors.GREEN}[✔] Alive hosts check completed{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Found {count} alive hosts{Colors.RESET}")
        # Sample output
        print(f"\n{Colors.CYAN}[*] Sample alive hosts:{Colors.RESET}")
        for h in clean_hosts[:5]:
            print(f"  {Colors.WHITE}• {h}{Colors.RESET}")
        if count > 5:
            print(f"  {Colors.DIM}... and {count-5} more{Colors.RESET}")
        self.results['alive_hosts'] = count
        self.suggest_next_steps('alive_hosts')

    
    def run_fast_port_scan(self):
        """Run fast port scan using Naabu"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        alive_file = f"{self.output_dir}/alive.txt"

        # Re-clean using HTTPX JSON to ensure valid URLs (avoids [200 OK] garbage)
        if os.path.exists(alive_file):
            print(f"{Colors.YELLOW}[*] Re-validating alive hosts using HTTPX JSON...{Colors.RESET}")

            httpx_recheck = f"{self.output_dir}/alive_recheck.json"
            httpx_bin = self.get_tool('httpx')
            cmd = (
                f"{httpx_bin} -l {alive_file} "
                f"-sc -title -ip -cdn -json "
                f"-threads 30 "
                f"-timeout 10 "
                f"-o {httpx_recheck}"
            )
            self.run_command(cmd, timeout=300)

            clean_hosts = []
            try:
                with open(httpx_recheck, "r") as f:
                    for line in f:
                        try:
                            j = json.loads(line)
                            clean_hosts.append(j["url"])
                        except:
                            continue
            except:
                clean_hosts = []    
            alive_clean = f"{self.output_dir}/alive_clean.txt"
            with open(alive_clean, "w") as f:
                for u in sorted(set(clean_hosts)):
                    f.write(u + "\n")

            alive_file = alive_clean

        #  Final fallback logic 
        hosts_to_scan = []

        # 1) Try alive hosts
        if os.path.exists(alive_file):
            with open(alive_file) as f:
                hosts_to_scan = [
                    h.replace("https://","").replace("http://","").split("/")[0]
                    for h in f if h.strip()
                ]


        # 2) If no alive hosts, try subdomains
        if not hosts_to_scan:
            sub_file = f"{self.output_dir}/subdomains.txt"
            if os.path.exists(sub_file):
                with open(sub_file) as f:
                    hosts_to_scan = [
                    h.replace("https://","").replace("http://","").split("/")[0]
                    for h in f if h.strip()
                ]
 
        # 3) If still nothing, fallback to main domain
        if not hosts_to_scan:
            # Ensure fallback domain is a valid URL (required for Naabu/Nmap)
            fallback = self.domain.strip()
            hosts_to_scan = [fallback]

            print(f"{Colors.YELLOW}[*] Using fallback target: {hosts_to_scan[0]}{Colors.RESET}")
        print()
        print(f"{Colors.CYAN}[*] Note: Some domains use CDNs (Cloudflare, Akamai, etc.)")
        print(f"{Colors.CYAN}    CDNs hide the real server IP, so Naabu might fail.")
        print(f"{Colors.CYAN}    If we detect a CDN, we'll auto-switch to Nmap.{Colors.RESET}\n")
        print()
        final_input = f"{self.output_dir}/ports_input.txt"
        with open(final_input, 'w') as f:
            for h in hosts_to_scan:
                f.write(h + "\n")
        alive_file = final_input

        #  CDN Detection 
        cdn_providers = ["cloudflare", "akamai", "imperva", "sucuri", "fastly", "cloudfront"]
        cdn_detected = False
        detected_provider = "Unknown"

        print(f"{Colors.YELLOW}[*] Checking for CDN...{Colors.RESET}")
        print(f"{Colors.DIM}[*] Hosts to check: {hosts_to_scan}{Colors.RESET}")

        try:
            for host in hosts_to_scan:
                dig_cmd = f"dig +short {host}"
                dig_res = subprocess.run(dig_cmd, shell=True, capture_output=True, text=True)
                ip_list = dig_res.stdout.strip().split("\n")  

                for ip in ip_list:
                    if not ip.strip():
                        continue
                
                    whois_cmd = f"whois {ip}"
                    whois_res = subprocess.run(whois_cmd, shell=True, capture_output=True, text=True)
                    whois_data = whois_res.stdout.lower()

                    for provider in cdn_providers:
                        if provider in whois_data:
                            cdn_detected = True
                            detected_provider = provider.capitalize()
                            break
                    
                    if cdn_detected:
                        break
                if cdn_detected:
                    break
        except Exception as e:
            print(f"{Colors.RED}[!] CDN check failed: {e}{Colors.RESET}")

        if not cdn_detected:
            print(f"{Colors.GREEN}[✔] No CDN detected{Colors.RESET}")

        
        # Check if Naabu is available, fallback to Nmap
        use_naabu = self.tools_status.get('naabu', {}).get('installed')
        use_nmap = self.tools_status.get('nmap', {}).get('installed')
        # If CDN detected, Naabu will fail → auto fallback to Nmap
        if cdn_detected:
            print(f"{Colors.RED}[!] CDN Detected: {detected_provider}{Colors.RESET}")
            print(f"{Colors.RED}[!] Naabu cannot scan CDN IPs -- switching to Nmap.{Colors.RESET}")

            if not use_nmap:
                print(f"{Colors.RED}[!] Nmap is also missing! Cannot continue.{Colors.RESET}")
                return
            use_naabu = False  # disable Naabu

        
        if not use_naabu and not use_nmap:
            print(f"{Colors.RED}[!] No port scanning tools available!{Colors.RESET}")
            return
        
        scanner = "Naabu" if use_naabu else "Nmap"
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Fast Port Scan with {scanner}...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/ports_fast.txt"
        
        if use_naabu:
            naabu_bin = self.get_tool('naabu')
            cmd = (
                f"{naabu_bin} -l {alive_file} "
                f"-p 1-65535 "
                f"-rate 2000 "
                f"-scan-all-ips "
                f"-host-retry 3 "
                f"-no-color "
                f"-o {output_file}"
            )
            timeout = 300
        else:
            nmap_bin = self.get_tool('nmap')
            cmd = f"{nmap_bin} -iL {alive_file} -p 1-1000 -T4 --open -oG {output_file}"
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
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Full Port Scan with Nmap...{Colors.RESET}\n")
        print(f"{Colors.YELLOW}[!] This may take a while. Press Ctrl+C to skip.{Colors.RESET}\n")

        hosts_to_scan = []

        alive_file_original = f"{self.output_dir}/alive.txt"

        # 1) Try alive hosts
        if os.path.exists(alive_file_original):
            with open(alive_file_original) as f:
                hosts_to_scan = [h.strip() for h in f if h.strip()]

        # 2) If empty, try subdomains
        if not hosts_to_scan:
            sub_file = f"{self.output_dir}/subdomains.txt"
            if os.path.exists(sub_file):
                with open(sub_file) as f:
                    hosts_to_scan = [h.strip() for h in f if h.strip()]
        # 3) If still empty, fallback to main domain
        if not hosts_to_scan:
            hosts_to_scan = [self.domain]

        # Write final input file for Nmap
        final_input = f"{self.output_dir}/ports_full_input.txt"
        with open(final_input, 'w') as f:
            for h in hosts_to_scan:
                f.write(h + "\n")
        alive_file = final_input
        
        output_file = f"{self.output_dir}/ports_full.txt"
        nmap_bin = self.get_tool('nmap')
        cmd = f"{nmap_bin} -iL {alive_file} -p- -sV -sC -O --open -T4 -oA {output_file.replace('.txt', '')}"
     
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
            katana_bin = self.get_tool('katana')
            cmd = f"{katana_bin} -u https://{self.domain} -d 3 -o {katana_output}"

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
            gau_bin = self.get_tool('gau')
            cmd = f"{gau_bin} {self.domain} > {gau_output}"

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
            wayback_bin = self.get_tool('waybackurls')
            cmd = f"{wayback_bin} {self.domain} > {wayback_output}"

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
                                if not url.endswith(('.jpg', '.png', '.gif', '.css', '.ico')):
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

            self.merge_all_urls()
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error processing URL results: {e}{Colors.RESET}")
    
    def run_waf_detection(self):
        """Detect Web Application Firewalls"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return
            
        # Load hosts with fallback (alive → subs → domain)
        hosts = []

        alive_file = f"{self.output_dir}/alive.txt"

        # 1) Try alive hosts
        if os.path.exists(alive_file):
            try:
                with open(alive_file) as f:
                    hosts = [h.strip() for h in f if h.strip()]
            except:
                hosts = []

        # 2) If empty, try subdomains
        if not hosts:
            sub_file = f"{self.output_dir}/subdomains.txt"
            if os.path.exists(sub_file):
                try:
                    with open(sub_file) as f:
                        hosts = [h.strip() for h in f if h.strip()]
                except:
                    hosts = []

        # 3) If still empty → use main domain
        if not hosts:
            hosts = [self.domain]

        
        if not self.tools_status.get('wafw00f', {}).get('installed'):
            print(f"{Colors.RED}[!] Wafw00f not installed! Install with: sudo apt install wafw00f{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting WAF Detection...{Colors.RESET}\n")
        
        output_file = f"{self.output_dir}/waf_summary.txt"
        
        results = []
        total_hosts = len(hosts)
        
        print(f"{Colors.YELLOW}[*] Testing {total_hosts} hosts for WAF...{Colors.RESET}")
        
        for i, host in enumerate(hosts):
            host = re.sub(r'^https?://', '', host).split('/')[0]
            print(f"  Progress: {i+1}/{total_hosts} - Testing {host}", end='\r')
            
            wafw00f_bin = self.get_tool('wafw00f')
            cmd = f"{wafw00f_bin} {host}"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
                output = result.stdout + result.stderr
                
                # Modern, reliable WAF detection
                out_low = output.lower()

                waf_name = None

                known_wafs = {
                    "cloudflare": "Cloudflare",
                    "akamai": "Akamai",
                    "sucuri": "Sucuri",
                    "imperva": "Imperva / Incapsula",
                    "incapsula": "Imperva / Incapsula",
                    "f5": "F5 Big-IP",
                    "barracuda": "Barracuda",
                    "citrix": "Citrix Netscaler",
                    "stackpath": "StackPath",
                    "radware": "Radware",
                    "fastly": "Fastly",
                    "aws": "AWS WAF",
                    "azure": "Azure Frontdoor",
                    "cloudfront": "AWS CloudFront",
                }

                # Correct WAF detection logic

                # First check explicit "No WAF"
                if "no waf detected" in out_low or "generic detection" in out_low:
                    results.append(f"{host}: No WAF")
                    continue  # move to next host

                # Try to match known WAF signatures
                waf_name = None
                for key, nice_name in known_wafs.items():
                    # strict whole-word match to avoid false positives
                    if re.search(rf"\b{key}\b", out_low):
                        waf_name = nice_name
                        break   
                if waf_name:
                    results.append(f"{host}: {waf_name}")
                    print(f"  {Colors.RED}[WAF] {host}: {waf_name}{Colors.RESET}")
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
            nuclei_bin = self.get_tool('nuclei')
            if self.run_command(f"{nuclei_bin} -ut", timeout=600):
                print(f"{Colors.GREEN}[✔] Templates updated{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Template update failed, continuing...{Colors.RESET}")
        
        output_file = f"{self.output_dir}/nuclei_output.txt"
        nuclei_bin = self.get_tool('nuclei')
        cmd = f"{nuclei_bin} -l {alive_file} -severity low,medium,high,critical -o {output_file}"

        print(f"{Colors.YELLOW}[*] Running Nuclei vulnerability scan...{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] This may take several minutes...{Colors.RESET}")
        
        if self.run_command(cmd, timeout=3600):  # 60 minutes
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

    def run_parameter_discovery(self):
        """Discover parameters using ParamSpider + Arjun"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Parameter Discovery...{Colors.RESET}\n")

        # Create output directory
        param_dir = f"{self.output_dir}/parameters"
        Path(param_dir).mkdir(exist_ok=True)

        #  PARAMSPIDER 
        if self.tools_status.get('paramspider', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running ParamSpider...{Colors.RESET}")
            output_ps = f"{param_dir}/paramspider.txt"
            paramspider_bin = self.get_tool('paramspider', "/opt/recontools/ParamSpider/paramspider.py")
            cmd = (
                f"python3 {paramspider_bin} "
                f"-d {self.domain} "
                f"--subs "
                f"--exclude woff,css,png,jpg,gif,svg "
                f"--level high "
                f"-o {param_dir}"
            )               


            if self.run_command(cmd, timeout=500):
                print(f"{Colors.GREEN}[✔] ParamSpider completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] ParamSpider failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] ParamSpider not installed — skipping{Colors.RESET}")

        #  ARJUN 
        if self.tools_status.get('arjun', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Arjun...{Colors.RESET}")

            urls_file = f"{self.output_dir}/urls.txt"
            if not os.path.exists(urls_file):
                print(f"{Colors.RED}[!] No URLs found. Run URL Collection first.{Colors.RESET}")
                return

            output_arjun = f"{param_dir}/arjun.json"
            arjun_bin = self.get_tool('arjun', "/opt/recontools/Arjun/arjun.py")
            cmd = (
                f"python3 {arjun_bin} "
                f"-i {urls_file} -t 20 --json -o {output_arjun}"
            )


            if self.run_command(cmd, timeout=1200):
                print(f"{Colors.GREEN}[✔] Arjun completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Arjun failed{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Arjun not installed — skipping{Colors.RESET}")

        #  MERGE RESULTS 
        print(f"\n{Colors.YELLOW}[*] Merging parameter results...{Colors.RESET}")

        final_output = f"{param_dir}/parameters_final.txt"
        found = set()

        try:
            # ParamSpider output
            ps_file = f"{param_dir}/paramspider.txt"
            if os.path.exists(ps_file):
                with open(ps_file) as f:
                    for line in f:
                        if "=" in line:
                            found.add(line.strip())

            # Arjun output
            arjun_file = f"{param_dir}/arjun.json"
            if os.path.exists(arjun_file):
                try:
                    data = json.load(open(arjun_file))
                    for entry in data:

                        # Get URL + params
                        url = entry.get("url")
                        params = entry.get("params", [])

                        #    FIX: remove existing query parameters
                        base = url.split("?")[0]

                        # Build FUZZ URLs
                        for p in params:
                            found.add(f"{base}?{p}=FUZZ")

                except Exception:
                    pass


            with open(final_output, 'w') as f:
                for p in sorted(found):
                    f.write(p + "\n")

            print(f"{Colors.GREEN}[✔] Parameters discovered: {len(found)}{Colors.RESET}")
            print(f"{Colors.GREEN}[✔] Saved to: {final_output}{Colors.RESET}")
            self.results['parameters'] = len(found)

        except Exception as e:
            print(f"{Colors.RED}[!] Failed merging parameter results: {e}{Colors.RESET}")

    def run_js_endpoint_extraction(self):
        """Extract JS endpoints using LinkFinder + custom JS parser"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting JS Endpoint Extraction...{Colors.RESET}\n")

        # Create folders
        js_dir = f"{self.output_dir}/js_endpoints"
        js_files_dir = f"{js_dir}/js_files"
        Path(js_dir).mkdir(exist_ok=True)
        Path(js_files_dir).mkdir(exist_ok=True)

        urls_file = f"{self.output_dir}/urls.txt"
        if not os.path.exists(urls_file):
            print(f"{Colors.RED}[!] No URLs found. Run URL Collection first.{Colors.RESET}")
            return

        #  FIND JS FILES 
        print(f"{Colors.YELLOW}[*] Extracting JS URLs...{Colors.RESET}")
        js_urls = set()

        try:
            with open(urls_file) as f:
                for url in f:
                    url = url.strip()
                    base = url.split("?")[0]
                    if base.lower().endswith(".js"):
                        js_urls.add(base)
                    
                    if ".js" in base.lower():
                        js_urls.add(base.split("?")[0])

        except:
            pass

        # Save raw JS URLs
        raw_js_list = f"{js_dir}/js_raw_urls.txt"
        with open(raw_js_list, "w") as f:
            for u in sorted(js_urls):
                f.write(u + "\n")

        print(f"{Colors.GREEN}[✔] Found {len(js_urls)} potential JS files{Colors.RESET}")

        #  DOWNLOAD JS FILES 
        print(f"{Colors.YELLOW}[*] Downloading JS files...{Colors.RESET}")
        downloaded_files = []

        for js in js_urls:
            try:
                fname = js.split("?")[0]  # remove ?query params
                fname = fname.replace("https://", "").replace("http://", "")
                fname = re.sub(r'[^A-Za-z0-9._-]', '_', fname)

                path = f"{js_files_dir}/{fname}"

                if self.run_command(f"curl -s -L '{js}' -o '{path}'", timeout=20):
                    downloaded_files.append(path)
            except:
                continue

        print(f"{Colors.GREEN}[✔] Downloaded {len(downloaded_files)} JS files{Colors.RESET}")

        #  RUN LINKFINDER 
        print(f"{Colors.YELLOW}[*] Extracting endpoints using LinkFinder...{Colors.RESET}")
        endpoints_output = f"{js_dir}/endpoints_raw.txt"

        open(endpoints_output, "w").close()

        for js_file in downloaded_files:
            linkfinder_bin = self.get_tool('linkfinder', "/opt/recontools/LinkFinder/linkfinder.py")
            cmd = (
                f"python3 {linkfinder_bin} "
                f"-i '{js_file}' -o cli --no-color --regex >> {endpoints_output}"
            )   

            self.run_command(cmd, timeout=60)

        #  FIND SECRETS 
        print(f"{Colors.YELLOW}[*] Detecting secrets in JS files...{Colors.RESET}")

        secret_patterns = [
            r"api[_-]?key\s*[:=]\s*['\"]([A-Za-z0-9_\-]{10,})['\"]",
            r"secret\s*[:=]\s*['\"]([A-Za-z0-9_\-]{10,})['\"]",
            r"token\s*[:=]\s*['\"]([A-Za-z0-9_\-]{10,})['\"]",
            r"aws_access_key_id\s*[:=]\s*['\"]([A-Z0-9]{16,})['\"]",
            r"aws_secret_access_key\s*[:=]\s*['\"]([A-Za-z0-9/+=]{30,})['\"]",
            r"[\"'](https?://[A-Za-z0-9/\-._?=&]+)[\"']",
        ]

        secrets_output = f"{js_dir}/secrets.txt"
        found_secrets = set()

        import re

        for path in downloaded_files:
            try:
                content = open(path).read()
                for pattern in secret_patterns:
                    matches = re.findall(pattern, content)
                    for m in matches:
                        found_secrets.add(str(m))
            except:
                pass

        with open(secrets_output, "w") as f:
            for s in sorted(found_secrets):
                f.write(s + "\n")

        print(f"{Colors.GREEN}[✔] Found {len(found_secrets)} potential secrets{Colors.RESET}")

        #  CLEAN ENDPOINTS 
        final_endpoints = f"{js_dir}/endpoints.txt"
        cleaned = set()

        try:
            import re
            with open(endpoints_output) as f:
                for line in f:
                    # Extract only valid URLs
                    matches = re.findall(r'https?://[^\s\'"]+', line)
                    for m in matches:
                        cleaned.add(m)
        except:
            pass

        with open(final_endpoints, "w") as f:
            for c in sorted(cleaned):
                f.write(c + "\n")

        print(f"{Colors.GREEN}[✔] Extracted {len(cleaned)} JS endpoints{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Results saved to: {js_dir}{Colors.RESET}")
        # Save result count for summary
        self.results['js_endpoints'] = len(cleaned)


       

    def run_directory_fuzzing(self):
        """Advanced directory fuzzing using FFUF with recursion, smart extensions, and per-host outputs"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('ffuf', {}).get('installed'):
            print(f"{Colors.RED}[!] FFUF not installed! Install with: go install github.com/ffuf/ffuf@latest{Colors.RESET}")
            return

        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found! Run Alive Hosts Check first.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Advanced Directory Fuzzing...{Colors.RESET}\n")

        # Prepare fuzzing folder
        fuzz_dir = f"{self.output_dir}/fuzzing"
        Path(fuzz_dir).mkdir(exist_ok=True)

        # Smart wordlist
        default_wordlist = "/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt"
        if not os.path.exists(default_wordlist):
            default_wordlist = "/usr/share/wordlists/dirb/common.txt"

        print(f"{Colors.YELLOW}[*] Using wordlist: {default_wordlist}{Colors.RESET}")

        # Read alive hosts
        with open(alive_file) as f:
            hosts = [h.strip() for h in f if h.strip()]

        extensions = "php,html,js,json,txt,bak,old"
        status_filter = "200,204,301,302,307,401,403"

        for host in hosts:
            if not host.strip():
                continue
            host = host.rstrip("/")
            if not host.startswith("http://") and not host.startswith("https://"):
                host = "https://" + host
            clean_host = host.replace("https://", "").replace("http://", "").replace("/", "_")
            host_dir = f"{fuzz_dir}/{clean_host}"
            Path(host_dir).mkdir(exist_ok=True)

            output_file = f"{host_dir}/ffuf_results.txt"

            print(f"\n{Colors.CYAN}[*] Fuzzing {host}{Colors.RESET}")

            ffuf_bin = self.get_tool('ffuf')
            cmd = (
                f"{ffuf_bin} -u {host}/FUZZ "
                f"-w {default_wordlist} "
                f"-recursion "
                f"-recursion-depth 2 "
                f"-e {extensions} "
                f"-fc 404 "
                f"-mc {status_filter} "
                f"-timeout 10 "
                f"-of md " 
                f"-o {output_file}"
            )

            if self.run_command(cmd, timeout=1200):
                print(f"{Colors.GREEN}[✔] Finished fuzzing {host}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] FFUF failed on {host}{Colors.RESET}")

        print(f"\n{Colors.GREEN}[✔] Directory fuzzing completed. Results saved under: {fuzz_dir}{Colors.RESET}")

    def run_advanced_url_enum(self):
        """Deep crawling using Hakrawler"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('hakrawler', {}).get('installed'):
            print(f"{Colors.RED}[!] Hakrawler not installed! Install with: go install github.com/hakluke/hakrawler@latest{Colors.RESET}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Advanced URL Enumeration (Hakrawler)...{Colors.RESET}\n")

        adv_dir = f"{self.output_dir}/advanced_urls"
        Path(adv_dir).mkdir(exist_ok=True)

        output_file = f"{adv_dir}/advanced_urls.txt"

        hakrawler_bin = self.get_tool('hakrawler')
        cmd = f"echo https://{self.domain} | {hakrawler_bin} -depth 3 -scope subs -plain > {output_file}"

        if self.run_command(cmd, timeout=600):
            print(f"{Colors.GREEN}[✔] Hakrawler completed{Colors.RESET}")

            try:
                with open(output_file) as f:
                    urls = [line.strip() for line in f if line.strip()]

                count = len(urls)

                print(f"{Colors.GREEN}[✔] Found {count} deep URLs{Colors.RESET}")
                print(f"\n{Colors.CYAN}[*] Sample results:{Colors.RESET}")

                for u in urls[:10]:
                    print(f"  {Colors.WHITE}• {u}{Colors.RESET}")
                
                if count > 10:
                    print(f"  {Colors.DIM}... and {count-10} more{Colors.RESET}")

            except Exception as e:
                print(f"{Colors.RED}[!] Error reading Hakrawler output: {e}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Hakrawler failed{Colors.RESET}")

        # Merge into final URLs
        self.merge_all_urls()

    def merge_all_urls(self):
        """Merge all URL sources into one master URL file"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Finalizing URL List (Merging All Sources)...{Colors.RESET}\n")

        final_file = f"{self.output_dir}/urls_final.txt"
        merged = set()

        # Base URL list
        base_urls = f"{self.output_dir}/urls.txt"
        if os.path.exists(base_urls):
            try:
                merged.update([line.strip() for line in open(base_urls) if line.strip()])
            except:
                pass

        # Hakrawler URLs
        hak_file = f"{self.output_dir}/advanced_urls/advanced_urls.txt"
        if os.path.exists(hak_file):
            try:
                merged.update([line.strip() for line in open(hak_file) if line.strip()])
            except:
                pass

        # JS endpoints
        js_file = f"{self.output_dir}/js_endpoints/endpoints.txt"
        if os.path.exists(js_file):
            try:
                merged.update([line.strip() for line in open(js_file) if line.strip()])
            except:
                pass
        # normalize URLs (remove trailing slash, strip spaces)
        normalized = set()
        for url in merged:
            u = url.strip()
            if u.endswith("/"):
                u = u[:-1]
            normalized.add(u)
        merged = normalized


        # Remove unwanted file types
        blacklist = (".png", ".jpg", ".jpeg", ".gif", ".svg",
                     ".css", ".woff", ".ttf", ".otf", ".ico",
                     ".mp4", ".mp3")

        cleaned = set()
        for url in merged:
            url = url.split("#")[0]
            if not url.lower().endswith(blacklist):
                cleaned.add(url)

        try:
            with open(final_file, 'w') as f:
                for u in sorted(cleaned):
                    f.write(u + "\n")

            print(f"{Colors.GREEN}[✔] Total merged URLs: {len(cleaned)}{Colors.RESET}")
            print(f"{Colors.GREEN}[✔] Saved to: {final_file}{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.RED}[!] Failed to write merged URL file: {e}{Colors.RESET}")

        return final_file

    def run_gf_filters(self):
        """Filter interesting URLs using gf (XSS, SQLi, LFI, SSRF, Redirect, RCE)"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('gf', {}).get('installed'):
            print(f"{Colors.RED}[!] gf not installed! Install with: go install github.com/tomnomnom/gf@latest{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Running GF filters on URLs...{Colors.RESET}\n")

        urls_file = f"{self.output_dir}/urls_final.txt"
        if not os.path.exists(urls_file):
            # fallback to plain urls.txt
            urls_file = f"{self.output_dir}/urls.txt"

        if not os.path.exists(urls_file):
            print(f"{Colors.RED}[!] No URL file found. Run URL Collection / Advanced URL Enum first.{Colors.RESET}")
            return

        gf_dir = f"{self.output_dir}/gf"
        Path(gf_dir).mkdir(exist_ok=True)

        patterns = ["xss", "sqli", "lfi", "ssrf", "redirect", "rce"]
        stats = {}

        for p in patterns:
            out_file = f"{gf_dir}/{p}.txt"
            cmd = f"cat '{urls_file}' | gf {p} > '{out_file}' 2>&1"

            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            stderr = result.stderr.lower()
            stdout = result.stdout.lower()

            # Detect GF not installed
            if "command not found" in stderr or "gf: not found" in stderr:
                print(f"{Colors.RED}[!] GF is not installed correctly!{Colors.RESET}")
                print(f"{Colors.YELLOW}[*] Install with: go install github.com/tomnomnom/gf@latest{Colors.RESET}")
                stats[p] = 0
                continue     # <-- LEGAL because we’re inside the loop

            # Detect missing GF pattern file
            if "pattern not found" in stderr or "no such file" in stderr:
                print(f"{Colors.RED}[!] GF pattern '{p}' is missing!{Colors.RESET}")
                print(f"{Colors.YELLOW}[*] Run: cp -r /path/to/patterns ~/.gf/patterns{Colors.RESET}")
                stats[p] = 0
                continue     # <-- LEGAL inside loop
            # Read valid GF output
            try:
                with open(out_file) as f:
                    lines = [l.strip() for l in f if l.strip()]
                stats[p] = len(lines)
            except:
                stats[p] = 0    

        print(f"{Colors.CYAN}[*] GF Filter Summary:{Colors.RESET}")
        for p in patterns:
            print(f"  {Colors.WHITE}• {p.upper():8}: {stats.get(p, 0)}{Colors.RESET}")

        print(f"{Colors.GREEN}[✔] GF results saved under: {gf_dir}{Colors.RESET}")
        

    def run_screenshot_capture(self):
        """Take screenshots of alive hosts using Gowitness"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('gowitness', {}).get('installed'):
            print(f"{Colors.RED}[!] Gowitness not installed! Install with: go install github.com/sensepost/gowitness@latest{Colors.RESET}")
            return

        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found. Run Alive Hosts Check first.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Screenshot Capture (Gowitness)...{Colors.RESET}\n")

        shots_dir = f"{self.output_dir}/screenshots"
        Path(shots_dir).mkdir(exist_ok=True)

        gowitness_bin = self.get_tool('gowitness')
        cmd = f"{gowitness_bin} file -f '{alive_file}' -P '{shots_dir}'"

        if self.run_command(cmd, timeout=1800):
            print(f"{Colors.GREEN}[✔] Screenshot capture completed{Colors.RESET}")
            print(f"{Colors.GREEN}[✔] Screenshots saved in: {shots_dir}{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] Gowitness failed to capture screenshots{Colors.RESET}")

    def run_dns_bruteforce(self):
        """Bruteforce DNS using MassDNS and merge into subdomains list"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('massdns', {}).get('installed'):
            print(f"{Colors.RED}[!] MassDNS not installed or not configured in tools_status.{Colors.RESET}")
            print(f"{Colors.YELLOW}    Make sure massdns binary is in /usr/local/bin/massdns or PATH.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting DNS Bruteforce (MassDNS)...{Colors.RESET}\n")

        dns_dir = f"{self.output_dir}/dns_bruteforce"
        Path(dns_dir).mkdir(exist_ok=True)

        # Wordlist (common subdomains)
        wordlist_candidates = [
            "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
            "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-110000.txt",
            "/usr/share/wordlists/dnsmap.txt"
        ]
        wordlist = None
        for wl in wordlist_candidates:
            if os.path.exists(wl):
                wordlist = wl
                break

        if not wordlist:
            print(f"{Colors.RED}[!] No DNS wordlist found. Please install seclists or provide a wordlist manually.{Colors.RESET}")
            return

        # Resolvers
        resolvers_candidates = [
            "/opt/recontools/massdns/resolvers.txt",
            "/usr/share/massdns/lists/resolvers.txt",
            "/etc/massdns/resolvers.txt"
        ]
        resolvers = None
        for r in resolvers_candidates:
            if os.path.exists(r):
                resolvers = r
                break

        if not resolvers:
            print(f"{Colors.RED}[!] No resolvers.txt found for MassDNS.{Colors.RESET}")
            print(f"{Colors.YELLOW}    Make sure you have a resolvers file, e.g. /usr/share/massdns/lists/resolvers.txt{Colors.RESET}")
            return

        # Build input list: word.domain
        input_file = f"{dns_dir}/massdns_input.txt"
        try:
            with open(wordlist) as wl, open(input_file, "w") as out:
                for line in wl:
                    sub = line.strip()
                    if not sub:
                        continue
                    out.write(f"{sub}.{self.domain}\n")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to build MassDNS input: {e}{Colors.RESET}")
            return

        massdns_output = f"{dns_dir}/massdns_raw.txt"
        massdns_bin = self.get_tool('massdns')
        cmd = (
            f"{massdns_bin} -r '{resolvers}' -t A -o S -w '{massdns_output}' '{input_file}'"
        )          


        if not self.run_command(cmd, timeout=1800):
            print(f"{Colors.RED}[!] MassDNS bruteforce failed{Colors.RESET}")
            return

        print(f"{Colors.GREEN}[✔] MassDNS bruteforce completed{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Parsing MassDNS output and merging subdomains...{Colors.RESET}")

        bruteforce_subs_file = f"{dns_dir}/bruteforced_subdomains.txt"
        found_subs = set()

        try:
            with open(massdns_output) as f:
                for line in f:
                    line = line.strip()
                    # Example S-format: sub.example.com. A 1.2.3.4
                    if not line or line.startswith(";"):
                        continue
                    parts = line.split()
                    if len(parts) >= 1:
                        host = parts[0].rstrip(".").lower()
                        if self.domain in host:
                            found_subs.add(host)

            with open(bruteforce_subs_file, "w") as out:
                for s in sorted(found_subs):
                    out.write(s + "\n")

            print(f"{Colors.GREEN}[✔] Bruteforced subdomains: {len(found_subs)}{Colors.RESET}")
            print(f"{Colors.GREEN}[✔] Saved to: {bruteforce_subs_file}{Colors.RESET}")

            # Merge into main subdomains.txt
            main_subs = f"{self.output_dir}/subdomains.txt"
            # Proper merge (MassDNS + previous subdomains)
            all_subs = set()

            # Add bruteforced results
            if os.path.exists(bruteforce_subs_file):
                all_subs.update([s.strip() for s in open(bruteforce_subs_file) if s.strip()])

            # Add previous results
            if os.path.exists(main_subs):
                all_subs.update([s.strip() for s in open(main_subs) if s.strip()])

            # Write safely
            with open(main_subs, "w") as out:
                for s in sorted(all_subs):
                    out.write(s + "\n")

            merged_count = len(all_subs)

            print(f"{Colors.GREEN}[✔] Total subdomains after merge: {merged_count}{Colors.RESET}")
            self.results['subdomains'] = merged_count
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to process MassDNS output: {e}{Colors.RESET}")

    def run_tech_scan(self):
        """Fingerprint technologies using WhatWeb"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        if not self.tools_status.get('whatweb', {}).get('installed'):
            print(f"{Colors.RED}[!] WhatWeb not installed! Install with: sudo apt install whatweb{Colors.RESET}")
            return

        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found. Run Alive Hosts Check first.{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Technology Fingerprinting (WhatWeb)...{Colors.RESET}\n")

        tech_dir = f"{self.output_dir}/tech_scan"
        Path(tech_dir).mkdir(exist_ok=True)

        output_file = f"{tech_dir}/whatweb_results.json"

        cmd = f"whatweb -i {alive_file} --log-json={output_file}"

        if self.run_command(cmd, timeout=1200):
            print(f"{Colors.GREEN}[✔] WhatWeb scan completed{Colors.RESET}")
            # FIX: avoid crash if output file missing or empty
            if not os.path.exists(output_file) or os.path.getsize(output_file) == 0:
                print(f"{Colors.RED}[!] WhatWeb produced no output (timeout or empty scan){Colors.RESET}")
                self.results['tech_scan'] = 0
                return
            try:
                lines = open(output_file).read().strip().split("\n")
                print(f"{Colors.GREEN}[✔] Total scanned: {len(lines)}{Colors.RESET}")
                print(f"{Colors.GREEN}[✔] Results saved to: {output_file}{Colors.RESET}")
                self.results['tech_scan'] = len(lines)
            except:
                print(f"{Colors.RED}[!] Error reading WhatWeb output{Colors.RESET}")
        else:
            print(f"{Colors.RED}[!] WhatWeb scan failed{Colors.RESET}")


    def run_sqlmap_scan(self):
        """Auto SQL Injection scan using SQLMap on URLs with parameters"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        urls_file = f"{self.output_dir}/urls_final.txt"
        if not os.path.exists(urls_file):
            urls_file = f"{self.output_dir}/urls.txt"

        if not os.path.exists(urls_file):
            print(f"{Colors.RED}[!] No URLs found! Run URL Collection first.{Colors.RESET}")
            return

        if not self.tools_status.get('sqlmap', {}).get('installed'):
            print(f"{Colors.RED}[!] SQLMap not installed! Install with: sudo apt install sqlmap{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting SQL Injection Scan (SQLMap)...{Colors.RESET}\n")

        sql_dir = f"{self.output_dir}/sqlmap"
        Path(sql_dir).mkdir(exist_ok=True)

        # Filter only URLs containing parameters
        param_urls = []
        try:
            with open(urls_file) as f:
                for line in f:
                    url = line.strip()
                    if "=" in url:
                        param_urls.append(url)
        except:
            pass

        if not param_urls:
            print(f"{Colors.YELLOW}[!] No parameterized URLs found. Nothing to scan.{Colors.RESET}")
            return

        print(f"{Colors.YELLOW}[*] Found {len(param_urls)} URLs with parameters{Colors.RESET}")

        results_total = 0

        for url in param_urls:
            clean_name = re.sub(r'[^A-Za-z0-9._-]', '_', url)
            output_file = f"{sql_dir}/{clean_name}.txt"

            cmd = (
                f"sqlmap -u '{url}' "
                f"--batch --level=3 --risk=2 "
                f"--random-agent --smart "
                f"--flush-session "
                f"--output-dir={sql_dir} "   # FIX  place BEFORE redirect
                f" > '{output_file}' 2>&1"    # FIX     ensure redirection at the end
            )
  


            print(f"{Colors.CYAN}[*] Scanning: {url}{Colors.RESET}")

            if self.run_command(cmd, timeout=900):
                if os.path.exists(output_file) and os.path.getsize(output_file) < 15:
                    os.remove(output_file)
                    print(f"{Colors.YELLOW}[!] Removed empty SQLMap output for {url}{Colors.RESET}")
                    continue
                results_total += 1

        print(f"\n{Colors.GREEN}[✔] SQLMap Scan Completed{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Total URLs tested: {results_total}{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Output saved to: {sql_dir}{Colors.RESET}")
        # Save total scanned URLs for summary
        self.results['sqlmap'] = results_total
        


    def run_deep_recon_mode(self):
        """Deep Recon Mode: advanced recon chain (URLs, JS, params, fuzzing, screenshots, etc.)"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] DEEP RECON MODE INITIATED...{Colors.RESET}\n")
        print(f"{Colors.YELLOW}[!] This will run multiple advanced modules back-to-back.{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Recommended: do basic recon (1–8) once before running this.{Colors.RESET}\n")

        confirm = input(f"{Colors.YELLOW}[?] Continue with Deep Recon Mode? (y/n): {Colors.RESET}").lower().strip()
        if confirm != 'y':
            print(f"{Colors.YELLOW}[!] Deep Recon Mode cancelled by user.{Colors.RESET}")
            return

        start_time = time.time()

        # 1) URL Collection + Advanced URL Enum
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 1: URL Collection + Advanced Crawling{Colors.RESET}")
        self.run_url_collection()
        self.run_advanced_url_enum()
        self.merge_all_urls() 

        # 2) JS Endpoints + Secrets
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 2: JS Endpoint Extraction & Secrets{Colors.RESET}")
        self.run_js_endpoint_extraction()

        # 3) Parameter Discovery
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 3: Parameter Discovery (ParamSpider + Arjun){Colors.RESET}")
        self.merge_all_urls() 
        self.run_parameter_discovery()

        # 4) Directory Fuzzing
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 4: Directory Fuzzing (FFUF){Colors.RESET}")
        self.run_directory_fuzzing()

        # 5) API Fuzzing
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 5: API Fuzzing (Kiterunner){Colors.RESET}")
        self.run_api_fuzzing()

        # 6) Subdomain Takeover
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 6: Subdomain Takeover Checks{Colors.RESET}")
        self.run_subdomain_takeover_check()

        # 7) GF Filters on final URL list
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 7: GF Filtering (XSS / SQLi / LFI / SSRF / Redirect / RCE){Colors.RESET}")
        self.run_gf_filters()

        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 8: Technology Fingerprinting (WhatWeb){Colors.RESET}")
        self.run_tech_scan()

        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 9: SQL Injection Scan (SQLMap){Colors.RESET}")
        self.run_sqlmap_scan()

        # 10) Screenshots (visual recon)
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 10: Screenshot Capture (Gowitness){Colors.RESET}")
        self.run_screenshot_capture()

        # 11) DNS Bruteforce (extra subs)
        print(f"\n{Colors.CYAN}{Colors.BOLD}► STEP 11: DNS Bruteforce (MassDNS){Colors.RESET}")
        self.run_dns_bruteforce()

        end_time = time.time()
        duration = int(end_time - start_time)

        print(f"\n{Colors.GREEN}{Colors.BOLD}[✔] Deep Recon Mode completed in ~{duration} seconds{Colors.RESET}")

        print(f"{Colors.GREEN}[✔] Results saved under:{Colors.RESET}")
        print(f"    {self.output_dir}/urls_final.txt")
        print(f"    {self.output_dir}/js_endpoints/")
        print(f"    {self.output_dir}/parameters/")
        print(f"    {self.output_dir}/fuzzing/")
        print(f"    {self.output_dir}/api_fuzzing/")
        print(f"    {self.output_dir}/takeover/")
        print(f"    {self.output_dir}/screenshots/")
        print(f"    {self.output_dir}/dns_bruteforce/")
        print(f"    {self.output_dir}/gf/")


    def run_api_fuzzing(self):
        """Fuzz API endpoints using Kiterunner (KR)"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting API Fuzzing with Kiterunner...{Colors.RESET}\n")

        # Check KR installation
        if not self.tools_status.get('kr', {}).get('installed'):
            print(f"{Colors.RED}[!] Kiterunner (kr) not installed! Install using:{Colors.RESET}")
            print(f"{Colors.YELLOW}go install github.com/assetnote/kiterunner/cmd/kr@latest{Colors.RESET}")
            return

        # Check alive hosts
        alive_file = f"{self.output_dir}/alive.txt"
        if not os.path.exists(alive_file):
            print(f"{Colors.RED}[!] No alive hosts found. Run Alive Hosts Check first.{Colors.RESET}")
            return

        # Prepare output directory
        api_dir = f"{self.output_dir}/api_fuzzing"
        Path(api_dir).mkdir(exist_ok=True)

        # Default wordlist (can be swapped to large lists)
        assetnote_wordlist = "/opt/recontools/kiterunner_wordlists/routes-large.kite"

        # Fallback lists if Assetnote list is missing
        fallback_lists = [
            "/usr/share/wordlists/kiterunner/routes-large.kite",
            "/usr/share/wordlists/kiterunner/routes-small.kite",
        ]
        # Select the best available list
        if os.path.exists(assetnote_wordlist):
            wordlist = assetnote_wordlist
        elif any(os.path.exists(w) for w in fallback_lists):
            wordlist = next(w for w in fallback_lists if os.path.exists(w))
        else:
            print(f"{Colors.RED}[!] No valid API wordlist found for Kiterunner!{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Creating minimal fallback (very weak results).{Colors.RESET}")
            fallback = f"{self.output_dir}/fallback_kiterunner.kite"
            with open(fallback, "w") as f:
                f.write("/api/v1/users\n/api/v1/login\n/api/v1/admin\n/internal\n/config\n")
            wordlist = fallback

        print(f"{Colors.YELLOW}[*] Using wordlist:{Colors.RESET} {wordlist}")

        # Load alive hosts
        with open(alive_file) as f:
            hosts = [h.strip() for h in f if h.strip()]

        print(f"{Colors.YELLOW}[*] Targets loaded: {len(hosts)}{Colors.RESET}")

        results_total = 0

        # Run KR on each host
        for host in hosts:
            if not host.strip():
                continue
            if not host.startswith("http://") and not host.startswith("https://"):
                host = "https://" + host
            clean_host = host.replace("https://", "").replace("http://", "").strip("/")
            output_file = f"{api_dir}/{clean_host}_kr_results.txt"

            kr_bin = self.get_tool('kr')
            cmd = (
                f"{kr_bin} brute {host} "
                f"-w {wordlist} "
                f"-o {output_file} "
                f"--silent"
            )

            print(f"{Colors.CYAN}[*] Fuzzing: {host}{Colors.RESET}")

            if self.run_command(cmd, timeout=900):  # 15 minutes max
                print(f"{Colors.GREEN}[✔] KR completed for {host}{Colors.RESET}")

                try:
                    if not os.path.exists(output_file):
                        print(f"{Colors.RED}[!] No KR output for {clean_host}{Colors.RESET}")
                        continue
                    with open(output_file) as f:
                        lines = {l.strip() for l in f if l.strip()}

                    count = len(lines)
                    results_total += count

                    print(f"{Colors.GREEN}  → Found {count} endpoints{Colors.RESET}")
                except:
                    print(f"{Colors.RED}[!] Failed reading KR results for {host}{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] KR failed for {host}{Colors.RESET}")

        print(f"\n{Colors.GREEN}[✔] API Fuzzing Completed{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Total endpoints discovered: {results_total}{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Results saved to: {api_dir}{Colors.RESET}")

        self.results['api_fuzz'] = results_total
        self.merge_all_urls()

    def run_subdomain_takeover_check(self):
        """Detect potential subdomain takeover vulnerabilities using Subzy + CNAME validation"""
        if not self.setup_complete:
            print(f"{Colors.RED}[!] Please set up domain first!{Colors.RESET}")
            return

        print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Starting Subdomain Takeover Check...{Colors.RESET}")

        subdomains_file = f"{self.output_dir}/subdomains.txt"
        if not os.path.exists(subdomains_file):
            print(f"{Colors.RED}[!] No subdomains found! Run Subdomain Enumeration first.{Colors.RESET}")
            return

        takeover_dir = f"{self.output_dir}/takeover"
        Path(takeover_dir).mkdir(exist_ok=True)

        output_file = f"{takeover_dir}/subzy_results.txt"

        #  PART 1 — SUBZY SCAN
        if self.tools_status.get('subzy', {}).get('installed'):
            print(f"{Colors.YELLOW}[*] Running Subzy...{Colors.RESET}")

            subzy_bin = self.get_tool('subzy')
            cmd = (
                f"{subzy_bin} run "
                f"--targets {subdomains_file} "
                f"--concurrency 50 "
                f"--hide_fails "
                f"--output {output_file}"
            )


            if self.run_command(cmd, timeout=900):
                print(f"{Colors.GREEN}[✔] Subzy completed{Colors.RESET}")
            else:
                print(f"{Colors.RED}[!] Subzy failed — continuing with fallback detection{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[!] Subzy not installed — skipping direct scan{Colors.RESET}")


        #  PART 2 — FALLBACK CNAME TAKEOVER CHECK

        print(f"{Colors.YELLOW}[*] Running fallback CNAME-based scan...{Colors.RESET}")

        fallback_file = f"{takeover_dir}/cname_fallback.txt"

        with open(subdomains_file) as f:
            subs = [s.strip() for s in f if s.strip()]

        takeover_keywords = [
            "herokuapp", "github.io", "amazonaws.com", "cloudfront.net",
            "azurewebsites.net", "trafficmanager.net", "fastly.net",
            "readme.io", "bitbucket.io", "s3.amazonaws.com",
            "digitaloceanspaces.com", "surge.sh", "zendesk.com",
            "cname.vercel-dns.com",
            "io.zeit.co",
            "myshopify.com",
            "wordpress.com",
            "ghs.google.com",
            "unbouncepages.com",
        ]

        findings = []

        for sub in subs:
            cmd = f"dig +short CNAME {sub}"
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                cname = result.stdout.strip()

                if cname:
                    for key in takeover_keywords:
                        if key in cname.lower():
                            findings.append(f"{sub} → {cname}")
                            print(f"{Colors.RED}[!] Potential Takeover: {sub} → {cname}{Colors.RESET}")
            except:
                continue

        with open(fallback_file, "w") as f:
            for entry in findings:
                f.write(entry + "\n")


        #   FINAL SUMMARY

        total = 0

        if os.path.isfile(output_file) and os.path.getsize(output_file) > 0:
            try:
                lines = open(output_file).read().strip().split("\n")
                subzy_hits = [l for l in lines if "VULNERABLE" in l.upper()]
                total += len(subzy_hits)
            except:
                pass

        total += len(findings)

        print(f"\n{Colors.GREEN}[✔] Subdomain Takeover Scan Completed{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Total potential vulnerabilities: {total}{Colors.RESET}")
        print(f"{Colors.GREEN}[✔] Results saved to: {takeover_dir}{Colors.RESET}")

        self.results['takeover'] = total


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
                
                # JS Endpoints
                js_count = self.results.get('js_endpoints', 0)
                f.write(f"JS Endpoints Extracted: {js_count}\n")
                if js_count > 0:
                    f.write(f"  • File: {self.output_dir}/js_endpoints/endpoints.txt\n")

                #  Parameters
                param_count = self.results.get('parameters', 0)
                f.write(f"Parameters Discovered: {param_count}\n")
                if param_count > 0:
                    f.write(f"  • File: {self.output_dir}/parameters/parameters_final.txt\n")
                # GF Filters
                gf_dir = f"{self.output_dir}/gf"
                patterns = ['xss','sqli','lfi','ssrf','redirect','rce']
                gf_stats = {}

                for p in patterns:
                    file_path = f"{gf_dir}/{p}.txt"
                    if os.path.isfile(file_path):
                        try:
                            gf_stats[p] = len([l for l in open(file_path).read().split("\n") if l.strip()])
                        except:
                            gf_stats[p] = 0
                    else:
                        gf_stats[p] = 0 
                f.write(f"GF Findings:\n")
                for k,v in gf_stats.items():
                    f.write(f"  • {k.upper()}: {v}\n")

                # API fuzzing
                api_fuzz = self.results.get('api_fuzz', 0)
                f.write(f"API Endpoints Fuzzed: {api_fuzz}\n")
                if api_fuzz > 0:
                    f.write(f"  • Directory: {self.output_dir}/api_fuzzing/\n")

                # Tech Scan
                tech = self.results.get('tech_scan', 0)
                f.write(f"Technologies Identified: {tech}\n")
                if tech > 0:
                    f.write(f"  • File: {self.output_dir}/tech_scan/whatweb_results.txt\n")
                # SQL Injection
                sqlmap = self.results.get('sqlmap', 0)
                f.write(f"SQLMap Scanned URLs: {sqlmap}\n")
                if sqlmap > 0:
                    f.write(f"  • Directory: {self.output_dir}/sqlmap/\n")
                # Subdomain Takeover
                takeover = self.results.get('takeover', 0)
                f.write(f"Subdomain Takeover Findings: {takeover}\n")
                if takeover > 0:
                    f.write(f"  • Directory: {self.output_dir}/takeover/\n")
                
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
            elif choice == '10':
                self.run_parameter_discovery()
            elif choice == '11':
                self.run_js_endpoint_extraction()
            elif choice == '12':
                self.run_directory_fuzzing()
            elif choice == '13':
                self.run_api_fuzzing()
            elif choice == '14':
                self.run_subdomain_takeover_check()
            elif choice == '15':
                self.run_advanced_url_enum()
            elif choice == '16':
                self.run_screenshot_capture()
            elif choice == '17':
                self.run_dns_bruteforce()
            elif choice == '18':
                self.run_gf_filters()
            elif choice == '19':
                self.run_tech_scan()
            elif choice == '20':
                self.run_sqlmap_scan()


            elif choice == 'D':
                self.run_deep_recon_mode()


            
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