#!/bin/bash

source ../venv/bin/activate

srcPath="./src"
dataPath="./data"
outputPath="./analysisOutput"
MODE="Decision"

dataFiles=$(python $srcPath/helpers.py $dataPath"/NR")

mkdir $outputPath

counter=0
for f in $dataFiles
do
    name=$(basename "$f" ".dat")
    echo $name
    if [ $counter -le 5 ]
    then
        python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "BruteForce" >> $outputPath/$name"_BruteForce.dat"
        echo $counter
    fi

    counter=$((counter+1))
    
    python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "BranchBound" >> $outputPath/$name"_BranchBound.dat"
    python $srcPath/knapsackSolver.py --dataFile $f --mode $MODE -s "UnsortedBranchBound" >> $outputPath/$name"_UnsortedBranchBound.dat"
done