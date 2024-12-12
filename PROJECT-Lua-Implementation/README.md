### EXAPLANATION ###

For my project, I decided I wanted to allow Trivial to interact with Lua using Lupa, a Python library package. This involved allowing the language to be able to import functions as well as send code to a Lua runtime instance. Recently I had discovered Lua and was interested in how it was able to interact with C and expanding its functionality as a embeddable language. I wanted to figure out a way to embed Lua to Trivial in order to expand its functionality. I was met with several issues however, mainly due to how statements are handled and how it appears you can not run two statements one after the other if you are running a file (you can see this by making an "example.t" file with two 'print "hello"' statements). However, simply running runner.py by itself and running each line appears to work well. So far testing as really only been done with doing math and sending strings to Lua. 

### CONTRIBUTIONS ###

I (Sam Markus) did all the work for the project. Any additions I have made to the parser and evaluator have a "ADDED" comment near it to show which parts are mine and which are part of DeLozier's original code. The trivialLua.py is all my work related to adding Lua functionality, Lupa on the other hand is an external library package used for the program in order too allow Python to interact with Lua. 

The github link for Lupa and full credit to Scodor: https://github.com/scoder/lupa

### HOW TO RUN ###

Make sure you have Lupa installed prior as it is not included with Python by default.

- Run this command in terminal: pip install lupa

Running evaluator.py by itself will run the test for import as well as the tests for trivialLua, making it an easy way to show if the package is working properly as well as showing that imports work as well. 

Alternatively, running runner.py and entering the command to import the package works as well. You will know the package has been imported when "trivialLua imported successfully!" is printed to the console.

- Run this command in runner.py to import trivialLua: import "trivialLua"

Afterwords, you can use the keyword "luaEval" with your lua command as a trivial string surrounded by paranthesis will run the code and have it output in lua. Note that you must use apostrophe quotes (example: 'test') when writing strings to be given to Lua due to how Trivial identifies strings by looking for quotation marks and not apostrophes.

Following are examples of code that will run in runner.py (after importing trivialLua): 

- luaEval ("1+1")
- luaEval ("'abc'")
- luaEval ("2*2")