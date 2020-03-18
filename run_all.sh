#!/bin/bash

datafile="/home/notclaytonjohnson/projects/ds/hw2/LED_data/temp"
outfile="./ib1-3_output"
export CLASSPATH="/home/notclaytonjohnson/projects/ds/weka-3.8/weka/weka.jar"

for noise in {0..20} ; do
  for rand in {1..10}; do
    echo "Running classifiers for $noise% noise on seed of $rand on datafile: $datafile$noise.arff" >> $outfile
    java weka.Run weka.classifiers.lazy.IB1 -t $datafile$noise.arff -s $rand 2>/dev/null | grep -E "Correctly Classified Instances|IB1 Classifier" >> $outfile
    java weka.Run weka.classifiers.lazy.IB2 -t $datafile$noise.arff -s $rand 2>/dev/null | grep -E "Correctly Classified Instances|IB2 Classifier" >> $outfile
    java weka.Run weka.classifiers.lazy.IB3 -t $datafile$noise.arff -s $rand 2>/dev/null | grep -E "Correctly Classified Instances|IB3 Classifier" >> $outfile
  done
done
