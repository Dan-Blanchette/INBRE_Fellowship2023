#!/bin/bash

cd green1/


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
