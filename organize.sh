#!/bin/bash

# Create archive directory if it doesn't exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Create timestamp
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# Archive the file if it exists
if [ -f "grades.csv" ]; then
    NEW_NAME="grades_${TIMESTAMP}.csv"
    mv "grades.csv" "archive/${NEW_NAME}"
    echo "$(date) - Archived grades.csv to ${NEW_NAME}" >> organizer.log
    echo "Archived: grades.csv -> archive/${NEW_NAME}"
else
    echo "grades.csv not found"
fi

# Create new empty grades.csv
touch grades.csv
echo "Created new empty grades.csv"
