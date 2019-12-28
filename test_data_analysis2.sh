path="analysis/tester_results/NK"
in_path="data"

ALG="DPWeight"

IN_NAME="NK"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="Correlation"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="GranularityHeavy"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="GranularityLight"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="MaxCost"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="MaxWeight"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50

IN_NAME="WeightCapRation"
OUT_DIR=$path"/"$IN_NAME
run_tester -s $ALG --check-time True -p KnapsackParser --input-dir $in_path"/"$IN_NAME --output-dir $OUT_DIR --init-temperature 2500 --min-temperature 1 --cooling 0.99 --cycles 50