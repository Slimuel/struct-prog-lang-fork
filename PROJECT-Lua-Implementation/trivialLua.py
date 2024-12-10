# Basic imports
import re
from pprint import pprint

# Trivial imports
from tokenizer import patterns, tokenize
from parser import statements, parse_expression, parse_statement, parse
from evaluator import evaluations, evaluate, equals

# Lupa import
from lupa import LuaRuntime                      # import Lupa upon program startup
lua = LuaRuntime(unpack_returned_tuples=True)    # Create variable for lua to run on

"""
TOKENIZER ADDITIONS
- Add patterns related to Lua into the Tokenizer's patterns list
- Compile each new addition into a regular expression
"""
luaPatterns = [
    [r"luaEval", "luaEval"]
]

for pattern in luaPatterns:
    patterns.insert(0, pattern)
    pattern[0] = re.compile(pattern[0])



"""
PARSER ADDITIONS
- Define parse_luaEval_statement
- Add to statements in parser.py
"""
    
def parse_luaEval_statement(tokens):
    """
    luaEval_statement = "luaEval" "(" [ expression ] ")";
    """
    assert tokens[0]["tag"] == "luaEval"
    tokens = tokens[1:]
    if tokens[0]["tag"] != "(":
        raise Exception(f"Expected '(': {tokens[0]}")
    value, tokens = parse_expression(tokens[1:])
    if tokens[0]["tag"] != ")":
        raise Exception(f"Expected ')': {tokens[0]}")
    tokens = tokens[1:]
    return {"tag": "luaEval", "value": value}, tokens

statements["luaEval"] = parse_luaEval_statement

"""
EVALUATOR ADDITIONS
- Define evaluateLuaEval function in order to execute lua commands
- Add to evaluations list to be ran inside of evaluate function in evaluator.py
"""
def evaluateLuaEval(ast, environment):
    if ast["tag"] == "luaEval":
        if ast["value"]:
            value, _ = evaluate(ast["value"], environment)
            object = lua.eval(value)
        else:
            object = lua.eval("")
        return object, False

evaluations["luaEval"] = evaluateLuaEval

"""
TEST FUNCTIONS
- Runs when library is run by itself to ensure all features are working properly
"""
def testLuaTokens():
    print("testing luaKeywords...")
    for keyword in [
        "luaEval"
    ]:
        t = tokenize(keyword)
        assert len(t) == 2
        assert t[0]["tag"] == keyword, f"expected {keyword}, got {t[0]}"
        assert "value" not in t



def test_parse_luaEval_statement():
    """
    luaEval_statement = "luaEval" [ expression ] ;
    """
    print("testing parse_luaEval_statement...")
    ast = parse_luaEval_statement(tokenize('luaEval ("1+1")'))[0]
    assert ast == {'tag': 'luaEval', 'value': {'tag': 'string', 'value': '1+1'}}
    
    ast = parse_statement(tokenize('luaEval ("2+2")'))[0]
    assert ast == {'tag': 'luaEval', 'value': {'tag': 'string', 'value': '2+2'}} 

    ast = parse_statement(tokenize('luaEval ("\'abc\'")'))[0]
    

def test_evaluate_luaEval():
    print("test evaluate_luaEval_statement...")
    equals('luaEval("1+1")', {}, 2, {})
    equals('luaEval("")', {}, None, {})
    equals('luaEval ("50*4")', {}, 200, {})
    equals('luaEval ("\'abc\'")', {}, "abc", {})


print("trivialLua imported successfully!")

def testFunctions():
    testLuaTokens()
    test_parse_luaEval_statement()
    test_evaluate_luaEval()

if __name__ == "__main__":
    testFunctions()