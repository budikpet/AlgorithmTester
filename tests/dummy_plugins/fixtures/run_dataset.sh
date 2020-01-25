ALG="DummyAlgorithm"
CONC="instances"
fixtures="tests/dummy_plugins/fixtures"

run_tester --input-dir $fixtures/"data" --output-dir $fixtures/"tester_results" -s $ALG -r $CONC --check-time True -p "DummyParser"