# ReconMaster Quick Start Guide

Get up and running with ReconMaster in 5 minutes! 🚀

---

## ⚡ Ultra-Fast Setup

### 1. Install (2 minutes)

```bash
# Download and install
git clone https://github.com/shlokkokk/ReconMaster
cd ReconMaster
sudo chmod +x install.sh && sudo ./install.sh
```

### 2. Run (1 minute)

```bash
# Start ReconMaster
sudo reconmaster

# Set your target
[+] Select option: C
[+] Enter target domain: example.com

# Run full reconnaissance
[+] Select option: 9
[?] Continue with full automated recon? (y/n): y
```

### 3. Results (2 minutes)

```bash
# Check your results
ls output-example.com/
cat output-example.com/summary.txt
```

---

## 🎯 Essential Workflow

### For Bug Bounty Hunters

```bash
# Quick target assessment
1. Set domain (C)
2. Subdomain enumeration (1)
3. Alive hosts check (3)
4. Vulnerability scan (8)

# Comprehensive reconnaissance
1. Set domain (C)
2. Full automated recon (9)
3. Review summary.txt
4. Focus on critical findings
```

### For Penetration Testers

```bash
# Methodical approach
1. Set domain (C)
2. Subdomain enumeration (1)
3. DNS resolution (2)
4. Alive hosts check (3)
5. Port scanning (4/5)
6. URL collection (6)
7. WAF detection (7)
8. Vulnerability scan (8)
```

---

## 📋 Menu Cheat Sheet

| Key | Action | When to Use |
|-----|--------|-------------|
| **C** | Change Domain | Start every session |
| **1** | Subdomain Enum | Discover attack surface |
| **2** | DNS Resolution | Map infrastructure |
| **3** | Alive Check | Find live targets |
| **4** | Fast Port Scan | Quick service discovery |
| **5** | Full Port Scan | Detailed analysis |
| **6** | URL Collection | Endpoint discovery |
| **7** | WAF Detection | Identify protection |
| **8** | Vulnerability Scan | Security assessment |
| **9** | Full Auto Recon | Complete workflow |
| **I** | Initialize Tools | Fix missing tools |
| **H** | Help | Get assistance |
| **Q** | Quit | Exit session |

---

## 🏃‍♂️ Common Scenarios

### Scenario 1: New Bug Bounty Program

```bash
# Target: newprogram.com
sudo reconmaster
C → newprogram.com
9 → y (full recon)
# Wait 15-45 minutes
# Review output-newprogram.com/summary.txt
```

### Scenario 2: Quick Target Check

```bash
# Target: client.com
sudo reconmaster
C → client.com
1 → y (subdomains)
3 → y (alive check)
8 → y (vulnerability scan)
# Focus on critical findings
```

### Scenario 3: Deep Investigation

```bash
# Target: scope.com
sudo reconmaster
C → scope.com
1 → y (subdomains)
2 → y (DNS resolution)
3 → y (alive check)
5 → y (full port scan)
6 → y (URL collection)
7 → y (WAF detection)
8 → y (vulnerability scan)
```

---

## 🎨 Pro Tips

### Efficiency Hacks

1. **Start with Full Auto**: Option 9 gives complete coverage
2. **Focus on WAF-less Targets**: Check results for "No WAF" entries
3. **Prioritize Critical Findings**: Always review high/critical vulnerabilities
4. **Use Results Immediately**: Files are ready for other tools

### Time Management

- **Quick Scan**: 5-10 minutes (subdomains + alive + vulns)
- **Standard Scan**: 15-30 minutes (full auto recon)
- **Deep Scan**: 30-60 minutes (all options individually)

### Output Organization

```bash
# Create workspace
mkdir -p ~/recon/targets/
cd ~/recon/targets/

# Run reconmaster
sudo reconmaster

# Results automatically organized
ls output-target.com/
```

---

## 🐛 Quick Troubleshooting

### "Command not found"
```bash
sudo ln -s ~/go/bin/subfinder /usr/local/bin/subfinder
# Repeat for other missing tools
```

### "Permission denied"
```bash
sudo reconmaster
# Always run as root for network operations
```

### Tools not installed
```bash
sudo ./install.sh
# Or manually: go install github.com/projectdiscovery/subfinder@latest
```

---

## 🚀 Power User Commands

### Batch Processing

```bash
# Multiple targets from file
while read domain; do
    echo "Scanning $domain..."
    mkdir -p output-$domain
    # Run reconmaster non-interactive mode
    echo -e "C\n$domain\n9\ny\n" | sudo reconmaster
done < targets.txt
```

### Integration with Other Tools

```bash
# Use ReconMaster output with other tools
cat output-target.com/alive.txt | xargs -I {} nikto -h {}
cat output-target.com/urls.txt | grep login | xargs -I {} sqlmap -u {}
```

### Automated Reporting

```bash
# Generate daily reports
date=$(date +%Y-%m-%d)
sudo reconmaster
# Select target and run full recon
cp output-target.com/summary.txt reports/target-$date.txt
```

---

## 📊 Understanding Results

### Key Files

- **`subdomains.txt`** - All discovered subdomains
- **`alive.txt`** - Live web servers
- **`urls.txt`** - Collected endpoints
- **`nuclei_output.txt`** - Security vulnerabilities
- **`summary.txt`** - Executive summary

### Reading the Summary

```
Subdomains: 201          # Total attack surface
Alive Hosts: 67          # Live targets
Open Ports: 245          # Service opportunities
URLs Found: 3,456        # Endpoint discovery
WAF Protected: 45/67     # Protection analysis
Vulnerabilities: 88      # Security findings
```

### Priority Matrix

1. **Critical**: Immediate attention required
2. **High**: Address within 24 hours
3. **Medium**: Schedule for next sprint
4. **Low**: Monitor and review

---

## 🎯 Next Steps

### For Beginners

1. **Practice on Safe Targets**
   - Use `example.com` for testing
   - Try `httpbin.org` for API testing
   - Practice with `owasp.org` targets

2. **Learn the Tools**
   - Research each integrated tool
   - Understand what each phase does
   - Read tool documentation

3. **Join the Community**
   - Bug bounty platforms
   - Security forums
   - ReconMaster discussions

### For Professionals

1. **Customize Workflows**
   - Create custom tool sequences
   - Integrate with existing tools
   - Automate reporting

2. **Advanced Techniques**
   - Bypass WAF detection
   - Rate limiting strategies
   - Stealth scanning methods

3. **Contribution**
   - Report bugs and issues
   - Suggest new features
   - Contribute code

---

## 📚 Additional Resources

### Learning Materials

- [ ] Read the full README.md
- [ ] Review sample_run.md
- [ ] Check installation.md for troubleshooting
- [ ] Join community discussions

### External Resources

- **Bug Bounty Platforms**: HackerOne, Bugcrowd, Synack
- **Security Tools**: ProjectDiscovery suite, OWASP tools
- **Learning**: PortSwigger Web Security Academy, HackTheBox

---

## 🎉 Success Metrics

You'll know you're successful when:

- [ ] ReconMaster starts without errors
- [ ] You can set a target domain
- [ ] Subdomain enumeration finds results
- [ ] Summary report is generated
- [ ] You understand the basic workflow

---

**Ready to start your reconnaissance journey?** 🎯

Run `sudo reconmaster` and discover your first target!