# Usage and examples

## __relevance.py__: obtaining string-to-text relevance matrix using Annotated Suffix Tree approach.

Let's construct string-to-text relevance matrix. We will use a collection of scientific papers' abstracts as texts and Data Science Taxonomy topics as strings.

At first, we should extract all the leaves from a taxonomy. To do this, we can use _taxonomy.py_ module from GoT:

```
$ python3 taxonomy.py Data_Science_taxonomy.csv
```

Now all the leaves are saved in _taxonomy\_leaves.txt_ file. We can ensure this fact using _less_ command:

```
$ less taxonomy_leaves.txt

sample complexity and generalization bounds
boolean function learning
unsupervised learning and clustering
support vector machines
gaussian processes
modelling
boosting
bayesian analysis
inductive inference
online learning theory
```

Our text collection is stored in a large _.csv_ file. Let's deal the file using [pandas](https://pandas.pydata.org/):

```
import pandas as pd

df = pd.read_csv("papers_parsed_relevant.csv")
print(df.columns)

# Outputs: Index(['Unnamed: 0', 'title', 'authors', 'abstract', 'highlights',
#                 'publication', 'keywords', 'query', 'link', 'journal', 'volume', 'date',
#                 'date_parsed'], dtype='object')

print(df.shape)

# Outputs: (26823, 13)
```

We can see our collection contains 26823 samples. For the sake of simplicity, let's create a subcollection contains 500 samples. To make the subcollection:

```
sub_df = df.sample(500)
```

We want to use the "abstract" column. Let's take a look:

```
print(sub_df['abstract'])

# Outputs:
#
# 21933    Abstract The goal of this paper is to handle t...
# 13858    Abstract This paper deals with the modelling o...
# 9960     Abstract We investigate to what extent the sol...
# 15796    Abstract In this paper, we propose a novel 3D ...
# 5347     Abstract The classification and prediction acc...
#                               ...                        
# 12936    Abstract Slack variables are utilized in optim...
# 20234    Abstract Selecting relevant features for suppo...
# 23438    Abstract Crowd density estimation, which aims ...
# 7124     Abstract Given a graph  G = ( V , E )  and a t...
# 15784    Abstract In this paper, we propose a new schem...
# Name: abstract, Length: 500, dtype: object
```

We see we should trim "Abstract" words from the beginning of each abstract. Let's do this:

```
abstracts = []
ln = len('Abstract ')

for a in sub_df['abstract']:
    if a.startswith('Abstract '):
        abstracts.append(a[ln:])

print(abstracts[:2])

# Outputs:
#
# ['In Data Mining, during the preprocessing step, there is a considerable diversity ... 
```

To construct text-to-topic relevance matrix, we will follow the Annotated Suffix Tree (AST) approach. [This approach](https://bijournal.hse.ru/en/2012--3(21)/63370530.html) relies on fragment text representation and shows excellent results on many text analysis and retrieval problems.

In the code snippet below, we use a common text processing pipeline from [this example](https://github.com/dmitsf/AST-text-analysis/blob/master/examples/relevances.py). For a subcollection consisting of 500 samples calculations may take several minutes, it depends on your computer.

```
import re

import numpy as np

from asts import ast


def clear_text(text, lowerize=True):

    pat = re.compile(r'[^A-Za-z0-9 \-\n\r.,;!?А-Яа-я]+')
    cleared_text = re.sub(pat, ' ', text)

    if lowerize:
        cleared_text = cleared_text.lower()

    tokens = cleared_text.split()
    return tokens


def make_substrings(tokens, k=4):

    for i in range(max(len(tokens) - k + 1, 1)):
        yield ' '.join(tokens[i:i + k])


def get_relevance_matrix(texts, strings):

    matrix = np.empty((0, len(strings)), float)
    prepared_text_tokens = [clear_text(t) for t in texts]

    prepared_string_tokens = [clear_text(s) for s in strings]
    prepared_strings = [' '.join(t) for t in prepared_string_tokens]

    for text_tokens in prepared_text_tokens:
        ast = ast.AST(list(make_substrings(text_tokens)))
        row = np.array([ast.score(s) for s in prepared_strings])
        matrix = np.append(matrix, [row], axis=0)

    return matrix


def save_matrix(matrix):
    np.savetxt("relevance_matrix.txt", matrix)


if __name__ == "__main__":

    with open("taxonomy_leaves.txt") as f:
        strings = [l.strip() for l in f.readlines()]

    relevance_matrix = get_relevance_matrix(abstracts, strings)
    save_matrix(relevance_matrix)

```

The text-to-topic relevance matrix is saved in _relevance_matrix.txt_ file.


## __corelevance.py__: obtaining topic-to-topic co-relevance matrix.

To construct co-relevance matrix we should use __corelevance.py__ module:

```
if __name__ == "__main__":

    with open("taxonomy_leaves.txt") as f:
        strings = [l.strip() for l in f.readlines()]

    corelevance_matrix = get_corelevance_matrix(abstracts, strings)
    save_matrix(corelevance_matrix)

```

The topic-to-topic co-relevance matrix is saved in _corelevance_matrix.txt_ file.


## __lapin.py__: performs Laplacian preudo-inverse transform for matrices.

To obtain the transformed matrix. follow the example:

```
import numpy as np
from lapin import lapin


if __name__ == "__main__":
    relevance_matrix = np.loadtxt("relevance_matrix.txt")
    print(relevance_matrix.shape)
    tc = relevance_matrix.dot(relevance_matrix.T)
    print(tc.shape)

    tc_transformed = lapin(tc)

```


## __faddis.py__: obtaining fuzzy thematic clusters using FADDIS algorithm.

To obtain fuzzy thematic clusters we will use [FADDIS algorithm](https://www.sciencedirect.com/science/article/pii/S0020025511004592) and it's pythonic implementation [PyFADDIS](https://github.com/dmitsf/PyFADDIS). We will follow the pipeline with LAPIN transform from the [example](https://github.com/dmitsf/PyFADDIS/blob/master/example_clustering.py).

```
import numpy as np
from lapin import lapin
from faddis import faddis

from operator import itemgetter

NUM_EL = 15

if __name__ == "__main__":
    relevance_matrix = np.loadtxt("relevance_matrix.txt")
    print(relevance_matrix.shape)
    tc = relevance_matrix.dot(relevance_matrix.T)
    print(tc.shape)

    tc_transformed = lapin(tc)
    B, member, contrib, intensity, lat, tt = faddis(tc_transformed)
    np.savetxt("clusters.dat", member)

    with open("taxonomy_leaves.txt") as fn:
        annotations = [l.strip() for l in fn]

    for cluster in member.T:
        print(list(sorted(zip(annotations, cluster.flat),
                          key=itemgetter(1), reverse=True))[:NUM_EL])
                          
# Outputs:
# [('instance-based learning', 0.20771581404136386), ('content analysis and feature selection', 0.18967568803261997), 
# ('database interoperability', 0.1788892447738294), ('fuzzy representation', 0.16067391344470527),
# ('ontologies', 0.15130289387272605), ('neuro-fuzzy approach', 0.1496424373875215),
# ('structured text search', 0.1403321558987256), ('robust regression', 0.13734017658793016),
# ('decision diagrams', 0.13489637787773734), ('multidimensional range search', 0.13272601213805382),
# ('multi-agent reinforcement learning', 0.1297804717368329), ('relevance assessment', 0.12848786685817676),
# ('default reasoning and belief revision', 0.12342181824121827), ('bayesian analysis', 0.1219749038419412),
# ('apprenticeship learning', 0.12023676186324098)]
# [('database recovery', 0.19132381678822608), ('latent dirichlet allocation', 0.1767176922782787),
# ('clustering and classification', 0.14762655820331685), ('frequent graph mining', 0.1432865199559833),
# ('graph partitioning', 0.1405635466934665), ('scientific visualization', 0.1393156862863722),
# ('semi-supervised learning', 0.13404581869787371), ('parallel implementation', 0.12742329189956983),
# ('spectral clustering', 0.11767981069558497), ('physical data models', 0.11529847572171881),
# ('visualization toolkits', 0.1151370689138779), ('surfacing', 0.1150003615924787),
# ('data integration', 0.10885533917409053), ('call level interfaces', 0.1071431128087069),
# ('wrappers', 0.10551240594293687)]
# ...
# (5 clusters)
```

All the fuzzy clusters are saved in _clusters.dat_ file.


# Data structures

These modules don't introduce new data structures. All calculations use [Numpy matrices](https://numpy.org/doc/stable/reference/generated/numpy.matrix.html) and [Numpy arrays](https://numpy.org/doc/stable/reference/generated/numpy.array.html).
