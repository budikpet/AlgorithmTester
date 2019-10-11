#!/bin/bash

source ../venv/bin/activate

startWithFile=$1	# Which file should we start from (for example N4_inst
algorithmToRun=$2	# 0 == BruteForce, 1 == UnsortedBranchBound, 2 == BranchBound
endWithFile=$3""

echo $algorithmToRun

srcPath="./src"
dataPath="./data"
outputPath="./analysisOutput"
MODE="Decision"

dataFiles=$(python $srcPath/helpers.py get-test-files $dataPath"/NR")

mkdir $outputPath

startFileFound=0
for f in $dataFiles
do
    name=$(basename "$f" ".dat")
    echo $name
    
    if [ $startWithFile != $name ]  && [ $startFileFound -eq 0 ]
    then
    	continue
    else
    	startFileFound=1
    fi
    
    if [ $endWithFile"_" = $name"_" ]
    then
    	break
    fi
    
    if [ $algorithmToRun -eq 0 ]
    then
    	python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "BruteForce" >> $outputPath/$name"_BruteForce.dat"
    elif [ $algorithmToRun -eq 1 ]
    then
    	python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "UnsortedBranchBound" >> $outputPath/$name"_UnsortedBranchBound.dat"
    elif [ $algorithmToRun -eq 2 ]
    then
    	python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "BranchBound" >> $outputPath/$name"_BranchBound.dat"
    fi
done
