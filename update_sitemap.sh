#!/bin/bash

# Sitemap Auto Update Service - Optimized Version

# Set script directory and enter it
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR" || { echo "Error: Failed to change to script directory"; exit 1; }

# Log function for better output formatting
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check if required files exist
check_requirements() {
    if [ ! -f "auto_update_sitemap.py" ]; then
        log "Error: auto_update_sitemap.py not found!"
        exit 1
    fi
    
    if ! command -v python3 &> /dev/null; then
        log "Error: python3 is required but not installed!"
        exit 1
    fi
}

# Display help information
display_help() {
    echo "========================================"
    echo "  Sitemap Auto Update Service"
    echo "========================================"
    echo ""
    echo "Options:"
    echo "  1) Update sitemap manually once"
    echo "  2) Start auto-monitoring service (hourly updates)"
    echo "  3) Start auto-monitoring service (custom interval)"
    echo "  4) View sitemap content"
    echo "  h) Display this help message"
    echo ""
}

# Handle manual sitemap update
handle_manual_update() {
    log "Starting manual sitemap update..."
    if python3 auto_update_sitemap.py --manual; then
        log "Sitemap update completed successfully!"
        return 0
    else
        log "Error: Sitemap update failed!"
        return 1
    fi
}

# Handle custom interval input
get_valid_interval() {
    local interval
    while true; do
        read -p "Please enter check interval (seconds, minimum 60): " interval
        if [[ "$interval" =~ ^[0-9]+$ ]] && [ "$interval" -ge 60 ]; then
            echo "$interval"
            return 0
        else
            log "Invalid input. Please enter an integer greater than or equal to 60."
        fi
    done
}

# Main function
main() {
    check_requirements
    display_help
    
    # Get user selection with validation
    while true; do
        read -p "Please enter option [1-4, h]: " choice
        
        case "$choice" in
            1)
                echo ""
                handle_manual_update
                break
                ;;
            2)
                echo ""
                log "Starting auto-monitoring service (checking file changes hourly)..."
                log "Press Ctrl+C to stop the service"
                python3 auto_update_sitemap.py
                break
                ;;
            3)
                echo ""
                local interval=$(get_valid_interval)
                log "Starting auto-monitoring service (checking every $interval seconds)..."
                log "Press Ctrl+C to stop the service"
                python3 auto_update_sitemap.py --interval "$interval"
                break
                ;;
            4)
                echo ""
                log "Viewing sitemap content (last 20 entries)..."
                if [ -f "sitemap.xml" ]; then
                    head -n 100 sitemap.xml | tail -n 20
                    echo ""
                    log "Full file location: $SCRIPT_DIR/sitemap.xml"
                else
                    log "Error: sitemap.xml not found!"
                fi
                break
                ;;
            h|H)
                display_help
                ;;
            *)
                log "Invalid option. Please select 1-4 or h for help."
                ;;
        esac
    done
}

# Run the main function
main

exit $?