#!/bin/bash

# Constants
seed="cpjohnson"
header="% 1. Title: Seven Segment LED Database <- Acquired from Sherine
% 
% 2. Sources:
%      (a) LED.c dataset generation code
% 
% 3. Relevant Information:
%    This dataset represent a 7 segment LED display for integer
%    numbers from 0 to 9. It is generated with 10% error, which
%    means that there is about 10% probablity that any of the
%    seven segments of LED might flip from ON to OFF or vice versa.
%        
% 
% 4. Number of Instances: 1000 (About 100 in each of ten classes)
% 
% 5. Number of Attributes: 7 nominal and class
% 
% 6. Attribute Information:
%    1. LED Segment 1 {0 - OFF, 1 - ON}
%    2. LED Segment 2 {0 - OFF, 1 - ON}
%    3. LED Segment 3 {0 - OFF, 1 - ON}
%    4. LED Segment 4 {0 - OFF, 1 - ON}
%    5. LED Segment 5 {0 - OFF, 1 - ON}
%    6. LED Segment 6 {0 - OFF, 1 - ON}
%    7. LED Segment 7 {0 - OFF, 1 - ON}
%    8. class: Number Dispaly {0,1,2,3,4,5,6,7,8,9}
% 
% 7. Missing Attribute Values: None
% 
% 8. Class Distribution: About 10% for each of 10 classes.

@relation SevenSegLED

@attribute seg1 {0, 1}
@attribute seg2 {0, 1}
@attribute seg3 {0, 1}
@attribute seg4 {0, 1}
@attribute seg5 {0, 1}
@attribute seg6 {0, 1}
@attribute seg7 {0, 1}

@attribute class {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

@data"

dir="LED_data"
mkdir $dir 2> /dev/null

for noise in {0..20} ; do
  file="./$dir/temp$noise.arff"
  rm $file 2> /dev/null
  ./LED 1000 $seed $file $noise >> /dev/null
  data="$(cat $file)"
  echo -e "$header\n$data" > $file
done
