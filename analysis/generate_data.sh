
# Init temperature
echo "Initial temperature"
OUT_DIR="analysis/tester_results/ParamAnalysis/InitTemperature"
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/100 --init-temperature 100 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/300 --init-temperature 300 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/500 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/700 --init-temperature 700 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/900 --init-temperature 900 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/1000 --init-temperature 1000 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/2500 --init-temperature 2500 --min-temperature 1 --cooling 0.995 --cycles 50

# Cycles
echo "Cycles"
OUT_DIR="analysis/tester_results/ParamAnalysis/Cycles"
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/50 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/100 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 100
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/150 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 150
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/200 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 200
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/250 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 250

# Cooling
echo "Cooling"
OUT_DIR="analysis/tester_results/ParamAnalysis/Cooling"
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/50 --init-temperature 500 --min-temperature 1 --cooling 0.875 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/100 --init-temperature 500 --min-temperature 1 --cooling 0.900 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/150 --init-temperature 500 --min-temperature 1 --cooling 0.925 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/200 --init-temperature 500 --min-temperature 1 --cooling 0.950 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/ParamAnalysis --output-dir $OUT_DIR/250 --init-temperature 500 --min-temperature 1 --cooling 0.975 --cycles 50

