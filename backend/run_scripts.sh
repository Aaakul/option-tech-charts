#!/bin/bash
for script in get_csv.py get_current_month.py get_summary.py get_filtered.py get_json.py; do
    echo "Running $script..."
    python "$script"
    if [ $? -ne 0 ]; then
        echo "An error occurred while running $script."
        exit 1
    fi
done
echo "All scripts have been executed successfully."