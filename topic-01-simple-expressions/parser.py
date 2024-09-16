"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""
"""
    simple_expression = number | "(" expression ")" | "-" simple_expression
    factor = simple_expression
    term = factor { "*"|"/" factor }
    expression = term { "+"|"-" term }
"""

from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens


def parse_expression(tokens):
    return parse_simple_expression(tokens)

def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
    }
    # pprint(ast)

def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))

    # Added test cases
    for s in ["4", "20", "6061234123458912748917498237947981239479138749817489137"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    for s in ["(4)", "(20)", "(990099)"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    for s in ["-3", "-10000", "-4009725892348950"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    for s in ["-(3)"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))



def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")
    tokens = tokenize("2*3")
    ast, tokens = parse_term(tokens)
    assert ast == {'left': {'position': 0, 'tag': 'number', 'value': 2},'right': {'position': 2, 'tag': 'number', 'value': 3},'tag': '*'}    
    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "*",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "/",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "*",
    }

     # Added test cases
    tokens = tokenize("1*2*3/4*5/6*7*8/9")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {
            'left': {
                'left': {
                    'left': {
                        'left': {
                            'left': {
                                'left': {
                                    'left': {'position': 0, 'tag': 'number', 'value': 1},
                                    'right': {'position': 2, 'tag': 'number','value': 2},
                                    'tag': '*'},
                                'right': {'position': 4, 'tag': 'number', 'value': 3},
                                'tag': '*'},
                            'right': {'position': 6, 'tag': 'number', 'value': 4},
                            'tag': '/'},
                        'right': {'position': 8, 'tag': 'number', 'value': 5},
                        'tag': '*'},
                    'right': {'position': 10, 'tag': 'number', 'value': 6},
                    'tag': '/'},
                'right': {'position': 12, 'tag': 'number', 'value': 7},
                'tag': '*'},
            'right': {'position': 14, 'tag': 'number', 'value': 8},
            'tag': '*'},
        'right': {'position': 16, 'tag': 'number', 'value': 9},
        'tag': '/'
    }
    tokens = tokenize("(2)/(3)")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {'position': 1, 'tag': 'number', 'value': 2},
        'right': {'position': 5, 'tag': 'number', 'value': 3},
        'tag': '/'
    }
    tokens = tokenize("2*3*2*1")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {
            'left': {
                'left': {
                    'position': 0, 'tag': 'number', 'value': 2},
                'right': {'position': 2, 'tag': 'number', 'value': 3},
                'tag': '*'},
            'right': {'position': 4, 'tag': 'number', 'value': 2},
            'tag': '*'},
        'right': {'position': 6, 'tag': 'number', 'value': 1},
        'tag': '*'
    }
    tokens = tokenize("-(2*3)/(60*3)")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {
            'tag': 'negate',
            'value': {'left': {
                        'position': 2, 'tag': 'number', 'value': 2},
                        'right': {'position': 4, 'tag': 'number', 'value': 3},
                        'tag': '*'}
                },
        'right': {
            'left': {'position': 8, 'tag': 'number', 'value': 60},
            'right': {'position': 11, 'tag': 'number', 'value': 3},
            'tag': '*'
            },
        'tag': '/'
    }
    tokens = tokenize("-10/-20")
    ast, tokens = parse_term(tokens)
    assert ast == {
        'left': {
            'tag': 'negate',
            'value': {'position': 1, 'tag': 'number', 'value': 10}
            },
        'right': {
            'tag': 'negate',
            'value': {'position': 5, 'tag': 'number', 'value': 20}
            },
        'tag': '/'
    }


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression")
    tokens = tokenize("2+3")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {"position": 0, "tag": "number", "value": 2},
        "right": {"position": 2, "tag": "number", "value": 3},
        "tag": "+",
    }
    tokens = tokenize("2+3-4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "+",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "-",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }
    tokens = tokenize("2+3*4+5")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        "left": {
            "left": {"position": 0, "tag": "number", "value": 2},
            "right": {
                "left": {"position": 2, "tag": "number", "value": 3},
                "right": {"position": 4, "tag": "number", "value": 4},
                "tag": "*",
            },
            "tag": "+",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "+",
    }

    # added test cases
    tokens = tokenize("2*3+4*2")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {'position': 0, 'tag': 'number', 'value': 2},
            'right': {'position': 2, 'tag': 'number', 'value': 3},
            'tag': '*'},
        'right': {
            'left': {'position': 4, 'tag': 'number', 'value': 4},
            'right': {'position': 6, 'tag': 'number', 'value': 2},
            'tag': '*'},
        'tag': '+'
    }
    tokens = tokenize("(1000)*-99-(32)*(1)")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {'position': 1, 'tag': 'number', 'value': 1000},
            'right': {
                'tag': 'negate',
                'value': {'position': 8, 'tag': 'number', 'value': 99}},
            'tag': '*'},
        'right': {
            'left': {'position': 12, 'tag': 'number', 'value': 32},
            'right': {'position': 17, 'tag': 'number', 'value': 1},
            'tag': '*'},
        'tag': '-'
    }
    tokens = tokenize("(10+-5)+(2*10)")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {'position': 1, 'tag': 'number', 'value': 10},
            'right': {
                'tag': 'negate',
                'value': {'position': 5, 'tag': 'number', 'value': 5}},
            'tag': '+'},
        'right': {
            'left': {'position': 9, 'tag': 'number', 'value': 2},
            'right': {'position': 11, 'tag': 'number', 'value': 10},
            'tag': '*'},
        'tag': '+'
    }
    tokens = tokenize("(10*2)-(2/2)+(100*9)")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {
                'left': {'position': 1, 'tag': 'number', 'value': 10},
                'right': {'position': 4, 'tag': 'number', 'value': 2},
                'tag': '*'},
            'right': {
                'left': {
                    'position': 8, 'tag': 'number', 'value': 2},
                    'right': {'position': 10, 'tag': 'number', 'value': 2},
                    'tag': '/'},
            'tag': '-'},
        'right': {
            'left': {'position': 14, 'tag': 'number', 'value': 100},
           'right': {'position': 18, 'tag': 'number', 'value': 9},
           'tag': '*'},
        'tag': '+'
    }
    tokens = tokenize("10+2+3-2+3+2+10*3+2+1+5+10+30-10")
    ast, tokens = parse_expression(tokens)
    assert ast == {
        'left': {
            'left': {
                'left': {
                    'left': {
                        'left': {
                            'left': {
                                'left': {
                                    'left': {
                                        'left': {
                                            'left': {
                                                'left': {
                                                    'left': {'position': 0, 'tag': 'number', 'value': 10},
                                                    'right': {'position': 3, 'tag': 'number', 'value': 2},
                                                    'tag': '+'},
                                                'right': {'position': 5, 'tag': 'number', 'value': 3},
                                                'tag': '+'},
                                            'right': {'position': 7, 'tag': 'number', 'value': 2},
                                            'tag': '-'},
                                        'right': {'position': 9, 'tag': 'number', 'value': 3},
                                        'tag': '+'},
                                    'right': {'position': 11, 'tag': 'number', 'value': 2},
                                    'tag': '+'},
                                'right': {
                                    'left': {'position': 13, 'tag': 'number', 'value': 10},
                                    'right': {'position': 16,'tag': 'number', 'value': 3},
                                    'tag': '*'},
                                'tag': '+'},
                            'right': {'position': 18, 'tag': 'number', 'value': 2},
                            'tag': '+'},
                        'right': {'position': 20, 'tag': 'number', 'value': 1},
                        'tag': '+'},
                    'right': {'position': 22, 'tag': 'number', 'value': 5},
                    'tag': '+'},
                'right': {'position': 24, 'tag': 'number', 'value': 10},
                'tag': '+'},
            'right': {'position': 27, 'tag': 'number', 'value': 30},
            'tag': '+'},
        'right': {'position': 30, 'tag': 'number', 'value': 10},
        'tag': '-'
    }


def parse(tokens):
        return parse_expression(tokens)
    
def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    assert parse(tokens) == parse_expression(tokens)

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    print("done")
