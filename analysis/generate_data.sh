path="analysis/tester_results"
ALG="SA"

# Init temperature
echo "Initial temperature"
OUT_DIR=$path"/ParamAnalysis/InitTemperature"
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 100 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 300 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 700 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 900 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 1000 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.995 --cycles 50

# Cycles
echo "Cycles"
OUT_DIR=$path"/ParamAnalysis/Cycles"
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 100
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 150
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 200
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 250

# Cooling
echo "Cooling"
OUT_DIR=$path"/ParamAnalysis/Cooling"
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.875 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.900 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.925 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.950 --cycles 50
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR --init-temperature 500 --min-temperature 1 --cooling 0.975 --cycles 50

