ALG="SA_SAT_V1,SA_SAT_V2,SA_SAT_V3"
CONC="Files"
RESULTS_DIR="tester_results_evo"

init_temp=1000
min_temp=0.5
cycles=50
cooling=0.95

# Simple
DATASET="simple"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

# init_temperature
init_temp=5000
DATASET="init_temp/5000"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

init_temp=10000
DATASET="init_temp/10000"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

init_temp=1000

# cycles
cycles=100
DATASET="cycles/100"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

cycles=200
DATASET="cycles/200"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

cycles=50

# cooling
cooling=0.995
DATASET="cooling/0995"
run_tester --input-dir data/evo_files --output-dir analysis/$RESULTS_DIR/$DATASET -s $ALG -r $CONC --check-time True -p "SATParser" --init-temperature $init_temp --min-temperature $min_temp --cycles $cycles --cooling $cooling --max-retry-attempts 3 --create-evo-file True

cooling=0.95