# ReconMaster 🎯

> [!IMPORTANT]
> ### 🚀 ReconMaster is now **Oculus v3.0**!
> The development of this tool has migrated to a new, dedicated repository: **[Oculus](https://github.com/shlokkokk/Oculus)**.
> 
> **Why upgrade to v3.0 (Oculus)?**
> - **Blazing Speed:** Full concurrency engine using `ThreadPoolExecutor`.
> - **Extreme Resilience:** Hardened command execution with automatic retries and SSL-failure handling.
> - **State Management:** Persistent sessions with auto-resume capability.
> - **Advanced Analysis:** New logic for deep CORS, XSS, and CNAME takeover detection.
> - **Stunning UI:** Enhanced real-time output and professional HTML reporting.
> 
> This repository (v2.0) remains here as a stable legacy version. For the latest features and security updates, please move to the new home.

**Professional Reconnaissance Framework for Kali Linux**

![Version](https://img.shields.io/badge/version-2.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.6+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-orange.svg)

---

## 🔥 Overview

ReconMaster is the most advanced, beautiful, and intelligent reconnaissance framework ever created for bug bounty hunters and penetration testers. It combines multiple industry-leading security tools into a single, cohesive interface with stunning visual design and intelligent automation.

### ✨ Key Features

- **🎨 Beautiful Interface** - Professional ASCII art and color-coded output
- **🤖 Intelligent Automation** - Smart workflow suggestions and automated sequences
- **🔧 Multi-Tool Integration** - Seamlessly combines 12+ reconnaissance tools
- **📊 Comprehensive Reporting** - Detailed summaries with actionable insights
- **🛡️ Smart Error Handling** - Graceful fallbacks and helpful guidance
- **⚡ Performance Optimized** - Parallel processing and intelligent timeouts
- **🎯 Beginner-Friendly** - Clear menus and helpful hints throughout

### 🆕 New in ReconMaster v2

- **🔍 JS Endpoint Extraction** (LinkFinder + custom JS parser + secret finder)
- **🧩 Parameter Discovery** (ParamSpider + Arjun merging engine)
- **🗂️ Advanced Directory Fuzzing** (FFUF with recursion + smart extensions)
- **🛰️ API Fuzzing** (Kiterunner with automatic wordlist selection)
- **📸 Screenshot Capture** (Gowitness automation)
- **🔬 Tech Stack Fingerprinting** (WhatWeb JSON output)
- **💣 SQLi Auto-Exploitation** (SQLMap batch scanning)
- **⚠️ Subdomain Takeover Check** (Subzy + CNAME fallback engine)
- **🌐 Deep URL Enumeration** (Hakrawler deep crawl)
- **🧠 Deep Recon Mode** (11-step chained modules)


---
## 🚀 Deep Recon Mode (v2)

Deep Recon Mode executes **11 modules automatically**, including:

1. URL Collection  
2. Advanced URL Enum  
3. JS Endpoint Extraction  
4. Parameter Discovery  
5. Directory Fuzzing  
6. API Fuzzing  
7. Subdomain Takeover Check  
8. GF Filters  
9. Tech Scan  
10. SQLMap Scan  
11. DNS Bruteforce  
12. Screenshot Capture  
 

Run it with:


sudo reconmaster
Select: D


## 🚀 Quick Start

### Installation

```bash
# Download and run installation script
git clone https://github.com/shlokkokk/ReconMaster
cd ReconMaster
sudo chmod +x install.sh
sudo ./install.sh
```

### Basic Usage

```bash
# Start ReconMaster
sudo reconmaster

# Quick workflow
1. Select option 'C' to set domain
2. Enter your target (e.g., example.com)
3. Select option '9' for full automated recon
4. Review results in output-domain.com/
```

---

## 📋 Features & Menu Options

### Core Reconnaissance Modules

| Option | Module | Description | Tools Used |
|--------|--------|-------------|------------|
| **1** | Subdomain Enumeration | Discover subdomains using multiple sources | Subfinder, Amass, Assetfinder |
| **2** | DNS Resolution | Resolve DNS records for subdomains | DNSx |
| **3** | Alive Hosts Check | Identify live web servers | HTTPx |
| **4** | Fast Port Scan | Quick port discovery | Naabu (fallback to Nmap) |
| **5** | Full Port Scan | Comprehensive service detection | Nmap |
| **6** | URL Collection | Gather endpoints from multiple sources | Katana, Gau, Waybackurls |
| **7** | WAF Detection | Identify Web Application Firewalls | Wafw00f |
| **8** | Vulnerability Scan | Automated vulnerability assessment | Nuclei |

### Automation & Utilities

| Option | Function | Description |
|--------|----------|-------------|
| **9** | Full Automated Recon | Complete reconnaissance sequence with progress tracking |
| **C** | Change Domain | Switch to a different target domain |
| **I** | Initialize Tools | Check and install required tools |
| **H** | Help System | Comprehensive help and usage guide |
| **Q** | Quit | Exit ReconMaster |
### Advanced Modules (ReconMaster v2)

| Option | Module                     | Description                                    | Tools Used                    |
|--------|----------------------------|------------------------------------------------|-------------------------------|
| **10** | Parameter Discovery        | Find hidden GET/POST parameters                | ParamSpider, Arjun            |
| **11** | JS Endpoint Extraction     | Extract JS endpoints + secrets                 | LinkFinder, custom parser     |
| **12** | Directory Fuzzing          | Recursive fuzzing with smart extensions        | FFUF                          |
| **13** | API Fuzzing                | Bruteforce API endpoints                       | Kiterunner (kr)               |
| **14** | Subdomain Takeover Check   | Detect takeover risks using CNAME + Subzy      | Subzy, dig                    |
| **15** | Advanced URL Enumeration   | Deep crawling beyond base URL                  | Hakrawler                     |
| **16** | Screenshot Capture         | Take screenshots of alive hosts                | Gowitness                     |
| **17** | DNS Bruteforce             | High-speed subdomain bruteforce                | MassDNS                       |
| **18** | GF Filters                 | Extract XSS/SQLi/LFI/SSRF/etc. patterns        | gf                            |
| **19** | Technology Scan            | Fingerprint tech stack details                 | WhatWeb                       |
| **20** | SQL Injection Scan         | Auto SQLMap exploitation                       | SQLMap                        |
| **D**  | Deep Recon Mode            | Runs 11 advanced modules back-to-back          | ALL tools                     |


---

## 🏗️ Architecture

### Tool Integration

ReconMaster intelligently integrates industry-standard tools:

- **Subdomain Discovery**: Subfinder, Amass, Assetfinder
- **DNS Resolution**: DNSx with comprehensive record types
- **HTTP Probing**: HTTPx with multiple port support
- **Port Scanning**: Naabu for speed, Nmap for detailed analysis
- **URL Discovery**: Katana crawler, Gau, Waybackurls
- **WAF Detection**: Wafw00f with detailed fingerprinting
- **Vulnerability Scanning**: Nuclei with customizable templates

### Output Structure

```
output-example.com/
├── subdomains.txt
├── dns_resolved.txt
├── alive.txt
├── ports_fast.txt
├── ports_full.txt
├── urls.txt
├── urls_final.txt
│
├── js_endpoints/
│   ├── js_raw_urls.txt
│   ├── js_files/
│   ├── endpoints_raw.txt
│   ├── endpoints.txt
│   └── secrets.txt
│
├── parameters/
│   ├── paramspider_raw.txt
│   ├── arjun_raw.txt
│   └── parameters_final.txt
│
├── fuzzing/
│   └── <host>/ffuf_results.txt
│
├── api_fuzzing/
│   └── <host>_kr_results.txt
│
├── takeover/
│   ├── subzy_results.txt
│   └── cname_fallback.txt
│
├── advanced_urls/
│   └── advanced_urls.txt
│
├── dns_bruteforce/
│   ├── massdns_input.txt
│   ├── massdns_raw.txt
│   └── bruteforced_subdomains.txt
│
├── screenshots/
│   └── *.png
│
├── gf/
│   ├── xss.txt
│   ├── sqli.txt
│   ├── lfi.txt
│   ├── ssrf.txt
│   ├── redirect.txt
│   └── rce.txt
│
├── sqlmap/
│   └── *.txt
│
├── tech_scan/
│   └── whatweb_results.json
│
└── summary.txt
```

---

## 🎯 Workflow Examples

### Basic Reconnaissance

```bash
# Start ReconMaster
sudo reconmaster

# Set target domain
[+] Enter target domain (e.g., example.com): hackerone.com

# Run subdomain enumeration
[*] Starting Subdomain Enumeration...
[✔] Found 247 unique subdomains

# Check alive hosts
[*] Checking Alive Hosts...
[✔] Found 89 alive hosts

# Run vulnerability scan
[*] Starting Vulnerability Scan...
[✔] Found 23 vulnerabilities (Critical: 2, High: 8)
```

### Full Automated Mode

```bash
# Run complete reconnaissance
[*] Starting FULL AUTOMATED RECON...

Phase 1: Subdomain Enumeration ✔
Phase 2: DNS Resolution ✔
Phase 3: Alive Hosts Check ✔
Phase 4: Port Scanning ✔
Phase 5: URL Collection ✔
Phase 6: WAF Detection ✔
Phase 7: Vulnerability Scanning ✔

[✔] Recon completed in 847 seconds
[✔] Results saved to: output-hackerone.com/
```

---

## 🔧 Tool Requirements

### Automatically Installed

- **Subfinder** - Subdomain discovery
- **Amass** - Passive enumeration
- **Assetfinder** - Alternative subdomain finder
- **DNSx** - DNS resolution
- **HTTPx** - HTTP probing
- **Naabu** - Fast port scanner
- **Nmap** - Network mapper
- **Katana** - Web crawler
- **Gau** - Get All URLs
- **Waybackurls** - Archive URLs
- **Wafw00f** - WAF detection
- **Nuclei** - Vulnerability scanner
- **ParamSpider** – Parameter discovery  
- **Arjun** – Hidden parameter discovery  
- **LinkFinder** – JS endpoint extraction  
- **FFUF** – Directory fuzzing  
- **Kiterunner (kr)** – API fuzzing  
- **Gowitness** – Web screenshots  
- **WhatWeb** – Tech fingerprinting  
- **SQLMap** – SQL injection detection  
- **Subzy** – Subdomain takeover detection  
- **Hakrawler** – Deep crawling  
- **MassDNS** – DNS bruteforce  

### Installation Commands

If any tools are missing, ReconMaster provides exact installation commands:

```bash
# Go tools
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/projectdiscovery/httpx/cmd/httpx@latest

# APT packages
sudo apt install naabu nuclei amass
```

---

## 🎨 Interface Design

### Color Scheme

- **Cyan** - Headers and primary information
- **Green** - Success states and positive results
- **Red** - Errors and critical findings
- **Yellow** - Warnings and pending actions
- **Blue** - Information and progress indicators
- **Magenta** - Special highlights
- **White** - Standard text and results

### Interactive Elements

- **✔ Checkmarks** - Completed operations
- **✘ Crosses** - Failed or missing items
- **→ Arrows** - Navigation and suggestions
- **• Bullets** - Lists and enumerations
- **[!] Alerts** - Important information
- **[?] Questions** - User prompts
- **[*] Progress** - Ongoing operations

---

## 🧠 Intelligence Features

### Smart Suggestions

After each operation, ReconMaster suggests logical next steps:

```
[*] Recommended Next Steps:
  → DNS Resolution (Option 2)
  → Alive Check (Option 3)
  → Full Recon (Option 9)
```

### Error Handling

- **Missing Tools** - Automatic detection with install guidance
- **Empty Results** - Graceful handling with helpful messages
- **Network Issues** - Timeout management and retry logic
- **Permission Errors** - Clear guidance on required privileges

### Progress Tracking

- **Real-time Updates** - Live progress indicators
- **Time Estimates** - Expected completion times
- **Phase Completion** - Clear milestone tracking

---

## 📈 Sample Results

### Executive Summary

```
RECONMASTER SUMMARY REPORT
========================================================================

Target Domain: hackerone.com
Scan Date: 2025-11-29 14:32:18
Total Duration: 847 seconds
Output Directory: output-hackerone.com/

------------------------------------------------------------------------
                           DISCOVERY RESULTS
------------------------------------------------------------------------

Subdomains Discovered: 247
  • File: output-hackerone.com/subdomains.txt

DNS Records Resolved: 189
  • File: output-hackerone.com/dns_resolved.txt

Alive Hosts Found: 89
  • File: output-hackerone.com/alive.txt

Open Ports (Fast Scan): 156
  • File: output-hackerone.com/ports_fast.txt

Service Details (Full Scan): 23
  • File: output-hackerone.com/ports_full.txt

URLs Collected: 1,247
  • File: output-hackerone.com/urls.txt

WAF Detection Results: 67/89 hosts protected
  • File: output-hackerone.com/waf_summary.txt

Vulnerabilities Found: 23
  • Critical: 2
  • High: 8
  • File: output-hackerone.com/nuclei_output.txt
```

---

## 🛡️ Security Considerations

### Responsible Usage

- **Legal Authorization** - Only scan targets you own or have permission to test
- **Rate Limiting** - Built-in delays and timeouts to avoid overwhelming targets
- **Data Protection** - All results stored locally, no external transmission
- **Privacy** - No telemetry or analytics collection

### Best Practices

- **Target Validation** - Verify domain ownership before scanning
- **Gradual Approach** - Start with passive enumeration
- **Rate Control** - Use appropriate timeouts for target infrastructure
- **Documentation** - Keep detailed records of authorized testing

---

## 🔍 Troubleshooting


### KR (Kiterunner) fails or exits instantly
Ensure kr is symlinked:

ls /usr/local/bin/kr

If missing, reinstall:
go install github.com/assetnote/kiterunner/cmd/kr@latest

### JS Module shows 0 endpoints
Ensure LinkFinder path exists:
ls /opt/recontools/LinkFinder/linkfinder.py

### Subzy not running
Verify binary:
ls /usr/local/bin/subzy


### Common Issues

**Q: ReconMaster won't start**
```bash
# Check permissions
sudo chmod +x /usr/local/bin/reconmaster

# Verify Python installation
python3 --version
```

**Q: Missing tools after installation**
```bash
# Re-run tool initialization
sudo reconmaster
# Select option 'I' to check and install tools
```

**Q: Scan results are empty**
```bash
# Check network connectivity
ping 8.8.8.8

# Verify target is reachable
nslookup example.com
```

**Q: Installation fails on non-Kali systems**
```bash
# Manual installation for other distributions
# Install Go: https://golang.org/doc/install
# Install tools individually using go install commands
```

---

## 📚 Advanced Usage

### Custom Configuration

Create custom configuration files for tool optimization:

```bash
# Custom wordlists
mkdir -p ~/.config/reconmaster/
echo "custom.subdomains" > ~/.config/reconmaster/wordlists.txt

# Tool configurations
export DNSX_THREADS=100
export HTTPX_TIMEOUT=15
```

### Integration with Other Tools

```bash
# Export results for other tools
cat output-domain.com/alive.txt | xargs -I {} nikto -h {}

# Use with Burp Suite
cat output-domain.com/urls.txt | while read url; do
    curl -x http://127.0.0.1:8080 "$url"
done
```

---

## 🚀 Performance Optimization

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for tools and results
- **Network**: Stable internet connection for tool downloads
- **CPU**: Multi-core processor recommended for parallel operations

### Optimization Tips

1. **Increase Timeouts** - For slow networks or large targets
2. **Use Thread Control** - Adjust based on system capabilities
3. **Selective Scanning** - Focus on specific reconnaissance phases
4. **Result Filtering** - Use grep and awk for result analysis

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/reconmaster.git
cd reconmaster

# Install development dependencies
pip3 install -r requirements-dev.txt

# Run tests
python3 -m pytest tests/
```

ReconMaster v2 performs **high-intensity active recon modules** such as:

- FFUF fuzzing  
- SQLMap exploitation  
- MassDNS bruteforce  
- Kiterunner API fuzzing  

Use ONLY on targets you have permission to test.


---
