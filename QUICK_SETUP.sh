#!/bin/bash
# 🚀 ZombieCoder Quick Setup Script
# Choose your setup based on use case

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🎯 $1${NC}"
}

# Function to check if port is in use
check_port() {
    if netstat -tlnp 2>/dev/null | grep -q ":$1 "; then
        return 0
    else
        return 1
    fi
}

# Function to start Ollama
start_ollama() {
    print_info "Starting Ollama..."
    if check_port 11434; then
        print_status "Ollama already running on port 11434"
    else
        ollama serve &
        sleep 3
        if check_port 11434; then
            print_status "Ollama started successfully"
        else
            print_error "Failed to start Ollama"
            exit 1
        fi
    fi
}

# Function to start Proxy
start_proxy() {
    print_info "Starting Proxy Interceptor..."
    if check_port 8080; then
        print_warning "Port 8080 already in use, stopping existing service..."
        pkill -f "cursor_proxy_interceptor.py" || true
        sleep 2
    fi
    
    cd /home/sahon/Desktop/zombiecoder
    source zombie_env/bin/activate
    python3 cursor_proxy_interceptor.py &
    sleep 3
    
    if check_port 8080; then
        print_status "Proxy started successfully on port 8080"
    else
        print_error "Failed to start Proxy"
        exit 1
    fi
}

# Function to start Agent System
start_agent_system() {
    print_info "Starting Agent System..."
    if check_port 8004; then
        print_status "Agent System already running on port 8004"
    else
        cd /home/sahon/Desktop/zombiecoder/core-server
        source ../zombie_env/bin/activate
        python3 advanced_agent_system.py &
        sleep 3
        
        if check_port 8004; then
            print_status "Agent System started successfully"
        else
            print_warning "Agent System failed to start (optional)"
        fi
    fi
}

# Function to start Truth Checker
start_truth_checker() {
    print_info "Starting Truth Checker..."
    if check_port 8002; then
        print_status "Truth Checker already running on port 8002"
    else
        cd /home/sahon/Desktop/zombiecoder/core-server
        source ../zombie_env/bin/activate
        python3 truth_checker.py &
        sleep 3
        
        if check_port 8002; then
            print_status "Truth Checker started successfully"
        else
            print_warning "Truth Checker failed to start (optional)"
        fi
    fi
}

# Function to start Editor Integration
start_editor_integration() {
    print_info "Starting Editor Integration..."
    if check_port 8003; then
        print_status "Editor Integration already running on port 8003"
    else
        cd /home/sahon/Desktop/zombiecoder/core-server
        source ../zombie_env/bin/activate
        python3 editor_integration.py &
        sleep 3
        
        if check_port 8003; then
            print_status "Editor Integration started successfully"
        else
            print_warning "Editor Integration failed to start (optional)"
        fi
    fi
}

# Function to start Multi-Project Manager
start_multi_project_manager() {
    print_info "Starting Multi-Project Manager..."
    if check_port 8001; then
        print_status "Multi-Project Manager already running on port 8001"
    else
        cd /home/sahon/Desktop/zombiecoder/core-server
        source ../zombie_env/bin/activate
        python3 multi_project_manager.py &
        sleep 3
        
        if check_port 8001; then
            print_status "Multi-Project Manager started successfully"
        else
            print_warning "Multi-Project Manager failed to start (optional)"
        fi
    fi
}

# Function to start Main Server
start_main_server() {
    print_info "Starting Main Server..."
    if check_port 12345; then
        print_status "Main Server already running on port 12345"
    else
        cd /home/sahon/Desktop/zombiecoder/core-server
        source ../zombie_env/bin/activate
        python3 main_server.py &
        sleep 3
        
        if check_port 12345; then
            print_status "Main Server started successfully"
        else
            print_warning "Main Server failed to start (optional)"
        fi
    fi
}

# Function to show setup options
show_options() {
    print_header "ZombieCoder Setup Options"
    echo ""
    echo "🔴 Basic Chat (Minimum)"
    echo "   - Ollama + Proxy"
    echo "   - Raw model responses"
    echo "   - Use: Quick testing"
    echo ""
    echo "🟡 Smart Chat (Recommended)"
    echo "   - Ollama + Proxy + Agent System"
    echo "   - Intelligent responses with memory"
    echo "   - Use: Daily coding"
    echo ""
    echo "🟢 Production (Factual)"
    echo "   - + Truth Checker"
    echo "   - Fact-checked responses"
    echo "   - Use: Production work"
    echo ""
    echo "🔵 Full IDE (Code Assistance)"
    echo "   - + Editor Integration"
    echo "   - IDE-aware responses"
    echo "   - Use: Code assistance"
    echo ""
    echo "🟣 Multi-Project (Project Management)"
    echo "   - + Multi-Project Manager"
    echo "   - Project-specific responses"
    echo "   - Use: Multi-project development"
    echo ""
    echo "⚡ Complete (Full Automation)"
    echo "   - All servers"
    echo "   - Production-ready"
    echo "   - Use: Enterprise automation"
    echo ""
}

# Function to show current status
show_status() {
    print_header "Current System Status"
    echo ""
    
    if check_port 11434; then
        print_status "Ollama (11434) - Running"
    else
        print_error "Ollama (11434) - Not running"
    fi
    
    if check_port 8080; then
        print_status "Proxy (8080) - Running"
    else
        print_error "Proxy (8080) - Not running"
    fi
    
    if check_port 8004; then
        print_status "Agent System (8004) - Running"
    else
        print_warning "Agent System (8004) - Not running"
    fi
    
    if check_port 8002; then
        print_status "Truth Checker (8002) - Running"
    else
        print_warning "Truth Checker (8002) - Not running"
    fi
    
    if check_port 8003; then
        print_status "Editor Integration (8003) - Running"
    else
        print_warning "Editor Integration (8003) - Not running"
    fi
    
    if check_port 8001; then
        print_status "Multi-Project Manager (8001) - Running"
    else
        print_warning "Multi-Project Manager (8001) - Not running"
    fi
    
    if check_port 12345; then
        print_status "Main Server (12345) - Running"
    else
        print_warning "Main Server (12345) - Not running"
    fi
    
    echo ""
}

# Function to stop all services
stop_all() {
    print_info "Stopping all ZombieCoder services..."
    pkill -f "cursor_proxy_interceptor.py" || true
    pkill -f "advanced_agent_system.py" || true
    pkill -f "truth_checker.py" || true
    pkill -f "editor_integration.py" || true
    pkill -f "multi_project_manager.py" || true
    pkill -f "main_server.py" || true
    pkill -f "ollama serve" || true
    sleep 2
    print_status "All services stopped"
}

# Main function
main() {
    case "$1" in
        "basic")
            print_header "Starting Basic Chat Setup"
            start_ollama
            start_proxy
            print_status "Basic Chat setup complete!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "smart")
            print_header "Starting Smart Chat Setup"
            start_ollama
            start_proxy
            start_agent_system
            print_status "Smart Chat setup complete!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "production")
            print_header "Starting Production Setup"
            start_ollama
            start_proxy
            start_agent_system
            start_truth_checker
            print_status "Production setup complete!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "full-ide")
            print_header "Starting Full IDE Setup"
            start_ollama
            start_proxy
            start_agent_system
            start_truth_checker
            start_editor_integration
            print_status "Full IDE setup complete!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "multi-project")
            print_header "Starting Multi-Project Setup"
            start_ollama
            start_proxy
            start_agent_system
            start_truth_checker
            start_editor_integration
            start_multi_project_manager
            print_status "Multi-Project setup complete!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "complete")
            print_header "Starting Complete Setup"
            start_ollama
            start_proxy
            start_agent_system
            start_truth_checker
            start_editor_integration
            start_multi_project_manager
            start_main_server
            print_status "Complete setup finished!"
            print_info "Configure Cursor to use localhost:8080 as proxy"
            ;;
        "status")
            show_status
            ;;
        "stop")
            stop_all
            ;;
        "help"|"")
            show_options
            echo ""
            print_info "Usage: $0 [basic|smart|production|full-ide|multi-project|complete|status|stop|help]"
            echo ""
            print_info "Examples:"
            echo "  $0 basic      # Start basic chat setup"
            echo "  $0 smart      # Start smart chat setup (recommended)"
            echo "  $0 production # Start production setup"
            echo "  $0 status     # Show current status"
            echo "  $0 stop       # Stop all services"
            ;;
        *)
            print_error "Unknown option: $1"
            print_info "Use '$0 help' to see available options"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
