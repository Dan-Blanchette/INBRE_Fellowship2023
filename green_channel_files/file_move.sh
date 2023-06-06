#!/bin/bash

for i in {1..9}; do
   mv "*T0$i*" "frames_""$i"
done