#!/bin/bash
# counter

#!/bin/bash

# first make the directories
for i in {1..97}; do
   if [ -d "frame_$i" ]; then
      :
   else
      mkdir "frame_$i"
   fi
done


count=1
# loop through 1 - 97 to be used as widcard identification for script
for file in {1..97}; do
   if [ $count -lt 10 ]; then
      find . -name "*T0$count*.tif" -exec mv {} "frame_$count/" \;
      ((count++))
   else
      find . -name "*T$count*.tif" -exec mv {} "frame_$count/" \;
      ((count++))
   fi
done 