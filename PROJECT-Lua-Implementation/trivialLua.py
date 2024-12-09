# Basic imports
import re
from pprint import pprint

# Trivial imports
from tokenizer import patterns, tokenize
from parser import parse_expression, parse
from evaluator import evaluate, equals

# Lupa import
from lupa import LuaRuntime                      # import Lupa upon program startup
lua = LuaRuntime(unpack_returned_tuples=True)    # Create variable for lua to run on

"""
TOKENIZER ADDITIONS
- Add patterns related to Lua into the Tokenizer's patterns list
- Compile each new addition so they can succeed in a test
"""
luaPatterns = [
    [r"luaRuntime", "luaRuntime"],
    [r"luaEval", "luaEval"]
]

for pattern in luaPatterns:
    patterns.insert(0, pattern)
    pattern[0] = re.compile(pattern[0])



"""
PARSER ADDITIONS
- Define parse luaEval
- Rewrite parse_statement to include luaEval
"""

def parse_luaEval_statement(tokens):
    """
    print_statement = "print" [ expression ] ;
    """
    assert tokens[0]["tag"] == "luaEval"
    tokens = tokens[1:]
    if tokens[0]["tag"] in ["}", ";", None]:
        # no expression
        return {"tag": "luaEval", "value": None}, tokens
    else:
        value, tokens = parse_expression(tokens)
        return {"tag": "luaEval", "value": value}, tokens


"""
EVALUATOR ADDITIONS
- null
"""
def evaluateLuaEval(ast, environment):
    if ast["tag"] == "luaEval":
        if ast["value"]:
            value, _ = evaluate(ast["value"], environment)
            lua.eval(value)
        else:
            lua.eval()
        return None, False

"""
TEST FUNCTIONS
- Runs when library is run by itself to ensure all features are working properly
"""
def testLuaTokens():
    print("testing luaKeywords...")
    for keyword in [
        "luaRuntime",
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
    ast = parse_luaEval_statement(tokenize('luaEval "1+1"'))[0]
    assert ast == {'tag': 'luaEval', 'value': {'tag': 'string', 'value': '1+1'}}
    pprint(ast)

def test_evaluate_luaEval():
    print("test evaluate_luaEval_statement")
    #pprint(tokenize("luaEval 1+1"))
    #equals("luaEval 77", {}, None, {})
    #equals("luaEval", {}, None, {})
    #equals("luaEval 50+7", {}, None, {})
    #equals("luaEval 50+8", {}, None, {})

if __name__ == "__main__":
    testLuaTokens()
    test_parse_luaEval_statement()
    test_evaluate_luaEval()