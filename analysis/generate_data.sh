
# Init temperature
OUT_DIR="analysis/tester_results/PARAM_ANALYSIS/INIT_TEMPERATURE"
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/100 --init-temperature 100 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/300 --init-temperature 300 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/500 --init-temperature 500 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/700 --init-temperature 700 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/900 --init-temperature 900 --min-temperature 1 --cooling 0.995 --cycles 50
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/PARAM_ANALYSIS --output-dir $OUT_DIR/1000 --init-temperature 1000 --min-temperature 1 --cooling 0.995 --cycles 50