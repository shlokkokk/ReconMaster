#!/bin/bash

# =============================================================================
# ReconMaster Installation Script
# Professional Reconnaissance Framework for Kali Linux
# =============================================================================

set -e

# Colors for beautiful output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

# ASCII Banner
banner() {
    echo -e "${CYAN}"
echo "╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                                                      ║"
echo "║    ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗    ║"
echo "║    ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗   ║"
echo "║    ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝   ║"
echo "║    ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗   ║"
echo "║    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║   ║"
echo "║    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ║"
echo "║                                                                                                      ║"
echo "║                        Professional Reconnaissance Framework Installation                            ║"
echo "║                                                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}[!] This script must be run as root (use sudo)${NC}"
        exit 1
    fi
}

# Check system compatibility
check_system() {
    echo -e "${CYAN}[*] Checking system compatibility...${NC}"
    
    # Check if running on Kali Linux
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ ! "$NAME" =~ "Kali" ]]; then
            echo -e "${YELLOW}[!] Warning: This framework is optimized for Kali Linux${NC}"
            echo -e "${YELLOW}    It may work on other distributions but is not officially supported${NC}"
            read -p "Continue anyway? (y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
    fi
    
    # Check architecture
    ARCH=$(uname -m)
    if [[ "$ARCH" != "x86_64" ]]; then
        echo -e "${YELLOW}[!] Warning: Non-x86_64 architecture detected: $ARCH${NC}"
        echo -e "${YELLOW}    Some tools may not be available${NC}"
    fi
    
    echo -e "${GREEN}[✔] System check completed${NC}"
}

# Update system packages
update_system() {
    echo -e "${CYAN}[*] Updating system packages...${NC}"
    apt update -y
    apt upgrade -y
    echo -e "${GREEN}[✔] System updated${NC}"
}

# Install system dependencies
install_dependencies() {
    echo -e "${CYAN}[*] Installing system dependencies...${NC}"
    
    # Essential packages
    apt install -y \
        git \
        wget \
        curl \
        build-essential \
        python3 \
        python3-pip \
        python3-dev \
        libffi-dev \
        libssl-dev \
        libxml2-dev \
        libxslt1-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libpcap-dev \
        nmap \
        masscan \
        wafw00f \
        amass \
        jq \
        ruby \
        ruby-dev \
        golang-go \
        snapd
    
    echo -e "${GREEN}[✔] Dependencies installed${NC}"
}

# Install Go tools
install_go_tools() {
    echo -e "${CYAN}[*] Installing Go-based security tools...${NC}"
    
    # Set GOPATH if not set
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    
    # Create go directory if it doesn't exist
    mkdir -p $GOPATH/bin
    
    # Install tools using go install
    tools=(
        "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
        "github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
        "github.com/projectdiscovery/httpx/cmd/httpx@latest"
        "github.com/projectdiscovery/dnsx/cmd/dnsx@latest"
        "github.com/projectdiscovery/katana/cmd/katana@latest"
        "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
        "github.com/tomnomnom/assetfinder@latest"
        "github.com/tomnomnom/waybackurls@latest"
        "github.com/lc/gau@latest"
    )
    
    for tool in "${tools[@]}"; do
        echo -e "${YELLOW}[*] Installing $tool...${NC}"
        if go install "$tool"; then
            echo -e "${GREEN}[✔] $tool installed successfully${NC}"
        else
            echo -e "${RED}[!] Failed to install $tool${NC}"
        fi
    done
    
    # Add go/bin to PATH permanently
    echo 'export GOPATH=$HOME/go' >> ~/.zshrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc
    
    echo -e "${GREEN}[✔] Go tools installation completed${NC}"
}

# Install additional tools
install_additional_tools() {
    echo -e "${CYAN}[*] Installing additional reconnaissance tools...${NC}"
    
    # Install from apt
    apt install -y \
        dirb \
        gobuster \
        wfuzz \
        sqlmap \
        whatweb \
        eyewitness \
        photon \
        theharvester
    
    # Install from GitHub
    echo -e "${YELLOW}[*] Installing additional tools from GitHub...${NC}"
    
    # Clone and install some useful tools
    mkdir -p /opt/recontools
    cd /opt/recontools
    
    # Subdomain takeover tool
    if [[ ! -d "subzy" ]]; then
        git clone https://github.com/LukaSikic/subzy.git
        cd subzy
        go install
        cd ..
    fi
    
    # HTTPX is already installed via go install
    
    echo -e "${GREEN}[✔] Additional tools installed${NC}"
}

# Setup Python environment
setup_python_env() {
    echo -e "${CYAN}[*] Setting up Python environment...${NC}"

    echo -e "${YELLOW}[!] Installing Python packages in safe mode...${NC}"

    pip3 install --upgrade pip --break-system-packages || true

    pip3 install \
        requests \
        urllib3 \
        beautifulsoup4 \
        lxml \
        selenium \
        tldextract \
        colorama \
        termcolor \
        pyfiglet \
        dnslib \
        dnspython \
        --break-system-packages || true

    echo -e "${GREEN}[✔] Python environment setup completed${NC}"
}

# Create ReconMaster directory structure
setup_reconmaster() {
    echo -e "${CYAN}[*] Setting up ReconMaster...${NC}"

    if [[ -f "reconmaster.py" ]]; then
        ln -sf "$(pwd)/reconmaster.py" /usr/local/bin/reconmaster
        chmod +x /usr/local/bin/reconmaster
        echo -e "${GREEN}[✔] Launcher installed at /usr/local/bin/reconmaster${NC}"
    else
        echo -e "${RED}[!] reconmaster.py not found in current directory${NC}"
        exit 1
    fi

    mkdir -p /usr/share/wordlists/reconmaster

    if [[ ! -d "/usr/share/seclists" ]]; then
        apt install seclists -y
    fi

    echo -e "${GREEN}[✔] ReconMaster setup completed${NC}"
}


# Test installation
test_installation() {
    echo -e "${CYAN}[*] Testing installation...${NC}"
    
    # Test ReconMaster
    if command -v reconmaster &> /dev/null; then
        echo -e "${GREEN}[✔] ReconMaster is accessible${NC}"
    else
        echo -e "${RED}[!] ReconMaster not found in PATH${NC}"
    fi
    
    # Test key tools
    tools=("subfinder" "httpx" "naabu" "nuclei" "amass" "nmap")
    
    for tool in "${tools[@]}"; do
        if command -v "$tool" &> /dev/null; then
            echo -e "${GREEN}[✔] $tool is installed${NC}"
        else
            echo -e "${RED}[!] $tool is not installed${NC}"
        fi
    done
    
    echo -e "${GREEN}[✔] Installation test completed${NC}"
}

# Display usage instructions
show_usage() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                           INSTALLATION COMPLETED!                            ║"
    echo "╠══════════════════════════════════════════════════════════════════════════════╣"
    echo "║                                                                              ║"
    echo "║  To start using ReconMaster:                                                 ║"
    echo "║    sudo reconmaster                                                          ║"
    echo "║                                                                              ║"
    echo "║  Basic workflow:                                                             ║"
    echo "║    1. Set your target domain (Option C)                                      ║"
    echo "║    2. Run subdomain enumeration (Option 1)                                   ║"
    echo "║    3. Check alive hosts (Option 3)                                           ║"
    echo "║    4. Run full automated recon (Option 9)                                    ║"
    echo "║                                                                              ║"
    echo "║  For quick start:                                                            ║"
    echo "║    sudo reconmaster → C → example.com → 9                                    ║"
    echo "║                                                                              ║"
    echo "║  Output will be saved in: output-domain.com/                                 ║"
    echo "║  Check summary.txt for detailed results                                      ║"
    echo "║                                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Main installation function
main() {
    banner
    check_root
    check_system
    
    echo -e "${YELLOW}"
    echo "This script will install:"
    echo "  • System dependencies and development tools"
    echo "  • Go programming language and Go-based security tools"
    echo "  • Python environment and packages"
    echo "  • ReconMaster framework"
    echo "  • Additional reconnaissance tools"
    echo -e "${NC}"
    
    read -p "Continue with installation? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}[!] Installation cancelled by user${NC}"
        exit 0
    fi
    
    # Execute installation steps
    update_system
    install_dependencies
    install_go_tools
    install_additional_tools
    setup_python_env
    setup_reconmaster
    test_installation
    show_usage
}

# Run main function
main "$@"