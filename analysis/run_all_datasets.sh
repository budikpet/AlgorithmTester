ALG="SA_SAT_V1"
CONC="FILES"

init_temp=1000
min_temp=0.5
cycles=55
cooling=0.9995

# wufA

PARENT="wuf-A"
DATASET="wuf20-88-A"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

DATASET="wuf20-91-A"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# DATASET="wuf100-430-A"
# run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# wufM

PARENT="wuf-M"
DATASET="wuf20-78-M"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

DATASET="wuf50-201-M"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# DATASET="wuf75-310-M"
# run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# wufN

PARENT="wuf-N"
DATASET="wuf20-78-N"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

DATASET="wuf50-201-N"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# DATASET="wuf75-310-N"
# run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# wufQ

PARENT="wuf-Q"
DATASET="wuf20-78-Q"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

DATASET="wuf50-201-Q"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# DATASET="wuf75-310-Q"
# run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# wufR

PARENT="wuf-R"
DATASET="wuf20-78-R"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

DATASET="wuf50-201-R"
run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

# DATASET="wuf75-310-R"
# run_tester --input-dir data/$PARENT/$DATASET --output-dir analysis/tester_results/$PARENT/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling

