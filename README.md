# ReconMaster 🎯

**Professional Reconnaissance Framework for Kali Linux**

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
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

---

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
output-domain.com/
├── subdomains_raw.txt      # Raw enumeration results
├── subdomains.txt          # Cleaned subdomain list
├── dns_resolved.txt        # DNS resolution results
├── alive.txt               # Live HTTP servers
├── ports_fast.txt          # Quick port scan results
├── ports_full.txt          # Detailed Nmap results
├── urls.txt                # Collected endpoints
├── waf_summary.txt         # WAF detection results
├── nuclei_output.txt       # Vulnerability findings
├── summary.txt             # Executive summary
└── logs/                   # Execution logs
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

---
