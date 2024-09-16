from tokenizer import tokenize 
from parser import parse

def evaluate(ast, environment):

    return 4, False

def equals(code, environment, expected_result, expected_environment=None):
    result, _ = evaluate(parse(tokenize(code)), environment)
    assert (result == expected_result), f"""ERROR: When executing 
    {[code]}
    -- expected --
    {[expected_result]}
    -- got --
    {[result]}."""
    if expected_environment:
        assert (environment == expected_environment), f"""ERROR: When executing 
        {[code]}
        -- expected --
        {[expected_result]}
        -- got --
        {[result]}."""

def test_evaluate_single_value():
    print("test evaluate single value")
    equals("4", {},4,{})

if __name__ == "__main__":
    test_evaluate_single_value()
    print("done.")