#!/bin/bash

# ReconMaster Installation Script


set -e
INSTALL_DIR="$(pwd)"

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
        python3-venv \
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
        dnsutils \
        whois
    
    echo -e "${GREEN}[✔] Dependencies installed${NC}"
}

# Install Go tools
install_go_tools() {
    echo -e "${CYAN}[*] Installing Go-based security tools...${NC}"
    
    # Set GOPATH if not set
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    
    # Create go directory if it doesn't exist
    mkdir -p "$GOPATH/bin"
    
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
        "github.com/tomnomnom/gf@latest"
        # Extra recon & fuzzing
        "github.com/hakluke/hakrawler@latest"
        "github.com/ffuf/ffuf@latest"
        "github.com/assetnote/kiterunner/cmd/kr@latest"
        "github.com/hahwul/dalfox/v2@latest"
        "github.com/sensepost/gowitness@latest"
        "github.com/projectdiscovery/asnmap/cmd/asnmap@latest"
    )
    
    for tool in "${tools[@]}"; do
        echo -e "${YELLOW}[*] Installing $tool...${NC}"
        if go install "$tool"; then
            echo -e "${GREEN}[✔] $tool installed successfully${NC}"
        else
            echo -e "${RED}[!] Failed to install $tool${NC}"
        fi
    done
    
    # Add go/bin to PATH permanently (for interactive shells)
    # Add go/bin to PATH permanently (for both bash and zsh)
    echo 'export GOPATH=$HOME/go' >> ~/.zshrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.zshrc

    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc

    # Symlink important Go binaries so ReconMaster can use them under sudo/root
    local bins=(subfinder naabu httpx dnsx katana nuclei assetfinder waybackurls gau gf hakrawler ffuf kr dalfox gowitness asnmap)
    for bin in "${bins[@]}"; do
        if [[ -f "$GOPATH/bin/$bin" ]]; then
            ln -sf "$GOPATH/bin/$bin" "/usr/local/bin/$bin" 2>/dev/null || true
        fi
    done

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
        theharvester \
        chromium \
        testssl.sh || echo -e "${YELLOW}[!] Some additional apt tools failed to install (non-critical).${NC}"

    #install these separately and ignore failures
    apt install -y eyewitness photon 2>/dev/null || \
        echo -e "${YELLOW}[!] eyewitness or photon not found in repos (skipping).${NC}"

    echo -e "${YELLOW}[*] Installing additional tools from GitHub...${NC}"
    
    # Working directory for extra tools
    mkdir -p /opt/recontools
    cd /opt/recontools

    # Subdomain takeover (Subzy)
    if [[ ! -d "subzy" ]]; then
        echo -e "${YELLOW}[*] Cloning Subzy (subdomain takeover)...${NC}"
        git clone https://github.com/LukaSikic/subzy.git
        cd subzy
        go install ./... || true
        cd ..
        # Ensure subzy is globally available
        if [[ -n "$GOPATH" && -f "$GOPATH/bin/subzy" ]]; then
            ln -sf "$GOPATH/bin/subzy" /usr/local/bin/subzy 2>/dev/null || true
        fi
    fi

    # ParamSpider (parameter discovery)
    if [[ ! -d "ParamSpider" ]]; then
        echo -e "${YELLOW}[*] Cloning ParamSpider...${NC}"
        git clone https://github.com/devanshbatham/ParamSpider.git
        cd ParamSpider
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt || true
        cd ..
    fi

    # Arjun (hidden parameter discovery)
    if [[ ! -d "Arjun" ]]; then
        echo -e "${YELLOW}[*] Cloning Arjun...${NC}"
        git clone https://github.com/s0md3v/Arjun.git
        cd Arjun
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt || true
        cd ..
    fi

    # XSStrike (advanced XSS scanner)
    if [[ ! -d "XSStrike" ]]; then
        echo -e "${YELLOW}[*] Cloning XSStrike...${NC}"
        git clone https://github.com/s0md3v/XSStrike.git
        cd XSStrike
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt || true
        cd ..
    fi

    # Smuggler (HTTP request smuggling)
    if [[ ! -d "smuggler" ]]; then
        echo -e "${YELLOW}[*] Cloning Smuggler...${NC}"
        git clone https://github.com/defparam/smuggler.git
        # Python script, no build needed
    fi

    # MassDNS (fast DNS bruteforcer)
    if [[ ! -d "massdns" ]] ; then
        echo -e "${YELLOW}[*] Cloning MassDNS...${NC}"
        git clone https://github.com/blechschmidt/massdns.git
        cd massdns
        make
        ln -sf /opt/recontools/massdns/bin/massdns /usr/local/bin/massdns
        cd ..
        wget -q https://raw.githubusercontent.com/blechschmidt/massdns/master/lists/resolvers.txt \
            -O /opt/recontools/massdns/resolvers.txt
    fi

    # LinkFinder (JS endpoint finder) - must match /opt/recontools/LinkFinder/linkfinder.py
    if [[ ! -d "LinkFinder" ]]; then
        echo -e "${YELLOW}[*] Cloning LinkFinder...${NC}"
        git clone https://github.com/GerbenJavado/LinkFinder.git
        cd LinkFinder
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt || true
        cd ..
        ln -sf /opt/recontools/LinkFinder/linkfinder.py /usr/local/bin/linkfinder
        chmod +x /usr/local/bin/linkfinder
    fi

    # JS Beautifier (for JS analysis)
    if ! pip3 show jsbeautifier >/dev/null 2>&1; then
        echo -e "${YELLOW}[*] Installing jsbeautifier...${NC}"
        pip3 install jsbeautifier --break-system-packages 2>/dev/null \
            || pip3 install jsbeautifier \
            || true
    fi

    # S3Scanner (AWS S3 bucket scanner)
    if ! command -v s3scanner >/dev/null 2>&1; then
        echo -e "${YELLOW}[*] Installing S3Scanner...${NC}"
        pip3 install s3scanner --break-system-packages 2>/dev/null \
            || pip3 install s3scanner \
            || true
    else
        echo -e "${GREEN}[✔] S3Scanner already installed${NC}"
    fi

        # cloud_enum (cloud asset enumerator)
    if [[ ! -d "cloud_enum" ]]; then
        echo -e "${YELLOW}[*] Cloning cloud_enum...${NC}"
        git clone https://github.com/initstring/cloud_enum.git
        cd cloud_enum
        pip3 install -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -r requirements.txt || true
        cd ..
    else
        echo -e "${GREEN}[✔] cloud_enum already present in /opt/recontools/cloud_enum${NC}"
    fi

    echo -e "${YELLOW}[*] Ensuring GF patterns installed...${NC}"

    # Install for root (sudo mode)
    mkdir -p ~/.gf
    cp gf/examples/*.json ~/.gf/ 2>/dev/null || true
    cp Gf-Patterns/*.json ~/.gf/ 2>/dev/null || true

    # Install also for the normal user
    if [[ -n "$SUDO_USER" ]]; then
        USER_HOME="/home/$SUDO_USER"
        mkdir -p "$USER_HOME/.gf"
        cp ~/.gf/*.json "$USER_HOME/.gf/" 2>/dev/null || true
        chown -R "$SUDO_USER:$SUDO_USER" "$USER_HOME/.gf"
    fi

    # Kiterunner wordlists
    mkdir -p /opt/recontools/kiterunner_wordlists
    wget -q https://wordlists-cdn.assetnote.io/data/kiterunner/routes-large.kite \
        -O /opt/recontools/kiterunner_wordlists/routes-large.kite

    echo -e "${GREEN}[✔] Additional tools installed${NC}"
    cd "$INSTALL_DIR"
}

# Setup Python environment
setup_python_env() {
    echo -e "${CYAN}[*] Setting up Python environment...${NC}"
    
    # Install Python packages
    pip3 install --upgrade pip --break-system-packages || true
    pip3 install --break-system-packages -U --ignore-installed \
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
        dnspython

    pip3 install --break-system-packages pandas numpy || true
    
    echo -e "${GREEN}[✔] Python environment setup completed${NC}"
}

# Create ReconMaster directory structure
setup_reconmaster() {
    echo -e "${CYAN}[*] Setting up ReconMaster...${NC}"

    cd "$INSTALL_DIR"

    if [[ -f "$INSTALL_DIR/reconmaster.py" ]]; then
        ln -sf "$INSTALL_DIR/reconmaster.py" /usr/local/bin/reconmaster
        chmod +x /usr/local/bin/reconmaster
        echo -e "${GREEN}[✔] ReconMaster installed to /usr/local/bin/reconmaster${NC}"
    else
        echo -e "${RED}[!] reconmaster.py not found in: $INSTALL_DIR${NC}"
        exit 1
    fi

    mkdir -p /usr/share/wordlists/reconmaster

    echo -e "${YELLOW}[*] Downloading wordlists...${NC}"

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
    tools=(
        "subfinder"
        "amass"
        "assetfinder"
        "dnsx"
        "httpx"
        "naabu"
        "nmap"
        "katana"
        "gau"
        "waybackurls"
        "wafw00f"
        "nuclei"
        "hakrawler"
        "ffuf"
        "kr"
        "dalfox"
        "gf"
        "whatweb"
        "theharvester"
        "asnmap"
        "gowitness"
        "massdns"
        "subzy"
    )
    
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
    
    update_system
    install_dependencies
    install_go_tools
    install_additional_tools
    setup_python_env
    setup_reconmaster
    test_installation
    show_usage
}

main "$@"
