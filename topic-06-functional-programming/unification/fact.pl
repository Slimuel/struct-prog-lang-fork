person(greg).
person(susan).

son(greg, david). 
son(david, jack).

daughter(kim, david).
daughter(steph, david).

child(X, Y) :- son(X, Y). 
child(X, Y) :- daughter(X, Y).

grandchild(X, Y) :- child(X, Z), child(Z, Y). 