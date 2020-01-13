from package_parsers.sat_parser import SATParser

def test_get_next_instance():
    parser = SATParser()
    fixture_path: str = "tests/test_parsers/fixtures"

    with open(f"{fixture_path}/instance_files/wuf20-014-A.mwcnf") as input_file:
        instance = parser.get_next_instance(input_file)

    assert instance["num_of_vars"] is not None
    assert instance["num_of_clauses"] is not None
    assert instance["clauses"] is not None
    assert instance["weights"] is not None
    assert instance["output_filename"] is not None

    assert len(instance["clauses"]) == instance["num_of_clauses"]
    
    max_var: int = 0
    for clause in instance["clauses"]:
        curr_max_var = max(clause.max(), abs(clause.min()))
        if max_var < curr_max_var:
            max_var = curr_max_var

    assert instance["num_of_vars"] == max_var

    print