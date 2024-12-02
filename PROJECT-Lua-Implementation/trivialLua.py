# Basic imports
import re

# Trivial imports
from tokenizer import patterns, tokenize
import parser
import evaluator 

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
- null
"""


"""
EVALUATOR ADDITIONS
- null
"""

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

if __name__ == "__main__":
    testLuaTokens()