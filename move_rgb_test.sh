#!/bin/bash
# create a new folder for the files to be stored
mkdir rgb_files
# move the files of interest into the new folder
mv tif_3chan/*RGB.tif rgb_files
# navigate to the new folder
cd rgb_files
touch frame_sort.sh