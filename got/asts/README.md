# Usage and examples

## __ast.py__: calculating string-to-text relevance matrix using annotated suffix tree (AST).

To calculate string-to-text relevance matrix, we should:

1. Construct an annotated suffix tree (AST) for the text splitted using class constructor `AST()`.
2. Call method `score()`.

Let's consider an example.

```
>>> import ast
>>> a = ast.AST("xabxac hi")
>>> a.score('dsaasddffd')
0.04444444444444447 
```

If the text is too long, we can split the text into strings and pass them in the `AST()` constructor as a list:

```
>>> a = ast.AST(["xabxac hi", "hello ok"])
>>> a.score('dsaasddffd')
0.02352941176470589
```

## Data structures

Class `AST` (_ast.py_ file) - internal Python data structure for abstract suffix tree representation.

- constructor of the class allows to create . Syntax:

```
from ast import AST
a = AST(str)
```

for a single string, or

```
a = AST(list[str])
```

for a list of substrings.

- method `score` calculates relevance between the AST `a` and a given string `str`.

Syntax:

```
s = a.score(str)
```
