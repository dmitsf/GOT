# Calculating string-to-text relevance matrix using annotated suffix tree (AST).

To calculate string-to-text relevance matrix, we should:

1. Construct an annotated suffix tree (AST) for the text splitted using class constructor `AST()`.
2. Call method `score()`.

Let's consider an example.


```
>>> import ast
>>> a = ast.AST("xabxac hi")
>>> a.score('dsaasddffd')
0.04444444444444447
>>> 
```

