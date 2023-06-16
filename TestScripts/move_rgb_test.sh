#!/bin/bash

# Read user input for the pattern
echo "Please enter the pattern for files to move:"
read -r pattern

echo "What file extension would you like to move?:"
echo "Ex: .png, .jpeg, .tiff, .tif"
read -r extension

echo "Please enter the destination name for files to move:"
read -r destination
mkdir -p "$destination"

# Enable nullglob to handle cases where no files match the pattern
shopt -s nullglob

# Store the matching filenames in an array
# wild_cards are placed before and after the pattern
files=(pngimgs/*"$pattern"*"$extension")

# Check if any files match the pattern
if [ ${#files[@]} -eq 0 ]; then
    echo "No files found matching the pattern: $pattern"
else
    # Move each file to the destination directory
    for file in "${files[@]}"; do
        mv "$file" "$destination"
    done

    echo "Files moved successfully."
fi

# Disable nullglob
shopt -u nullglob

cd "$dir_name" || exit
touch frame_sort.sh