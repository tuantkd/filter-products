#!/bin/bash

# Activate the virtual environment using bash
source ./venv/Scripts/activate

# Run the commission.py script using Python
python ./commission_calculation/commission.py

# Additional message after script completion
echo "The script has finished running."

# Ping google.com using its IP address
ping -c 100 8.8.8.8

# Keep the terminal open after execution (if needed)
read -p "Press [Enter] to continue..."
