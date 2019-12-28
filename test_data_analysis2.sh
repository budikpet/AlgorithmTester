path="analysis/tester_results"
ALG="SA"

# Init temperature
echo "Initial temperature"
OUT_DIR=$path"/ParamAnalysis/InitTemperature"

step=100
start=3500
end=4000

for i in `seq $start $step $end`; do 
    echo $i
    run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/$i --init-temperature $i --min-temperature 1 --cooling 0.995 --cycles 50
done