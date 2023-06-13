#!/bin/bash

# author: Dan Blanchette
# date: 6-13-2023
# description: This script will separate files based on a channel of interest

# Read user input for the file name pattern
echo "Please enter the pattern for files to move:"
read -r pattern

# Specify an extension type for your data
echo "What file extension would you like to move?:"
echo "Ex: .png, .jpeg, .tiff, .tif"
read -r extension

# Name the new folder in which the data will be stored
echo "Please enter the destination name for files to move:"
read -r destination
mkdir -p "$destination"

# Enable nullglob to handle cases where no files match the pattern
shopt -s nullglob

# Current working directory path
cwd=$(pwd)

# Store the matching filenames in an array
# wild_cards are placed before and after the pattern
# NOTE: Adjust the path to the file folder as needed
files=(../tif_3chan/*"$pattern"*"$extension")

# Check if any files match the pattern
if [ ${#files[@]} -eq 0 ]; then
    echo "No files found matching the pattern: $pattern"
else
    # Move each file to the destination directory
    for file in "${files[@]}"; do
        mv "$file" "$cwd/$destination"
    done

    echo "Files moved successfully."
fi

# Disable nullglob
shopt -u nullglob


# SEPARATE FILES BY SPECIMEN
# Iterator for comparison logic
count=1

# You can change the max value of 6 to match the total number of recorded specimens from a concatenated time series.
for i in {1..6}; do
   # If the iterator (i) is equal to the counter (count), then make a folder called "specimen_n" where n is
   # the iterator number. Then move the specimens 1 - n into the folders.
   if [ $i -eq $count ]; then
      mkdir -p "$destination/spec_$i"
      mv "$destination"/*XY"$i"* "$destination/spec_$i/"
      ((count++))
   else
      # : means pass (do nothing) then give feedback
      :
      echo "Please adjust the maximum range to reflect the total number of specimens."
   fi
done

# FRAME SORT

cd "$destination"

for i in {1..6}; do
   cd "spec_$i/"
   for j in {1..97}; do
      mkdir -p "frame_$j/"
      if [ $j -lt 10 ]; then
         mv *T0"$j"* "frame_$j/"
      else
         mv *T"$j"* "frame_$j/"
      fi
   done
   cd ../
done