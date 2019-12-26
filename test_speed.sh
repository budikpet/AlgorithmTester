OUT_DIR="analysis/tester_results/TestSpeed"
run_tester -s SA,SAPenalty --check-time True -p KnapsackParser --input-dir data/TestSpeed --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.995 --cycles 50
