# Example: using a taxonomy to analyse a text collection

Let us consider analysis of a text collection with a help of GoT software package. We will consider Data Science Taxonomy (DST, published in [this preprint](https://wp.hse.ru/data/2019/01/13/1146987922/WP7_2018_04_______.pdf)) and collection of abstracts of research papers on Data Science (may be downloaded from a [webpage of "Concept" research group, HSE University](https://cs.hse.ru/concept/taxonomies)). The collection under consideration was obtained from 80 Elsevier and Springer journals related to Data Science. The collection is available at a [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets).

Our final aim is to extract and understand the main research directions in the Data Science area.

We will follow the steps below:

0. Downloading and preparing the text collection and the taxonomy.
1. Obtaining text-to-topic relevance matrix using Annotated Suffix Tree approach.
2. Obtaining fuzzy thematic clusters using FADDIS algorithm.
3. Generalizing the clusters and visualizing them with the help of GoT.

Let's start.

## 0. Downloading and preparing the text collection and the taxonomy.

We can download the collection via browser from a [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets)
or via commandline:

```
$ wget https://cs.hse.ru/data/2019/05/19/1506729559/papers_parsed_relevant.zip
```

After that, we should unzip the archive:

```
$ unzip papers_parsed_relevant.zip
```

We can download the DST taxonomy via browser from a [webpage of "Concept" research group](https://cs.hse.ru/concept/taxonomies)
or via commandline:

```
$ wget https://cs.hse.ru/data/2019/12/18/1523118089/Data_Science_taxonomy.xlsx
```

Since the taxonomy have _.xlsx_ format, we should transform the taxonomy to _.csv_. One may do this using Miscrosoft Excel, OpenOffice/LibreOffice Calc or via commandline:

```
$ libreoffice --headless --convert-to csv Data_Science_taxonomy.xlsx
```

Now we have all the files prepared.


## 1. Obtaining text-to-topic relevance matrix using Annotated Suffix Tree approach.

To construct text-to-taxonomy\_topic relevance matrix, we should extract all the leaves from a taxonomy. To do this, we can use _taxonomy.py_ module from GoT:

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

# Ouputs: (26823, 13)
```

We can see our collection contains 26823 samples. For the sake of simplisity, lets's use a subcollection constains 500 samples. To make the subcollection:

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

We see we should trim "Abstract" word from the beginning of each abstract. Let's do this:

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

To construct text-to-topic relevance matrix, we will follow Annotated Suffix Tree (AST) approach. [This approach](https://bijournal.hse.ru/en/2012--3(21)/63370530.html) relies on fragment text representation and shows excellent results on many text analysis and retrieval problems.

We will use AST implementation from [EAST package](https://github.com/dmitsf/AST-text-analysis), developed by M.Dubov and improved by A.Vlasov and D.Frolov. In the code snippet below, we use a common text processing pipeline from [this example](https://github.com/dmitsf/AST-text-analysis/blob/master/examples/relevances.py). For a subcollection consisting of 500 samples calculations may take several minutes, it depends on your computer.

```
import re

import numpy as np

from east.asts import base


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
        ast = base.AST.get_ast(list(make_substrings(text_tokens)))
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

## 2. Obtaining fuzzy thematic clusters using FADDIS algorithm.

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
# [('gaussian processes', 0.5797048882008996), ('boosting', 0.5481740449484693), 
# ('online learning theory', 0.49649238052543937), ('query learning', 0.29972568516128634), 
# ('modelling', 0.16035911816266413), ('sample complexity and generalization bounds', 0.028083528546619597), 
# ('bayesian analysis', 0.02456740568435398), ('boolean function learning', 0.0),
# ('unsupervised learning and clustering', 0.0), ('support vector machines', 0.0), ('inductive inference', 0.0),
# ('multi-agent learning', 0.0), ('models of learning', 0.0)]
# [('inductive inference', 0.7036691642201909), ('boolean function learning', 0.4708936191239057), 
# ('unsupervised learning and clustering', 0.4271583918603897), ('multi-agent learning', 0.3105183398625311),
# ('models of learning', 0.06434838666427031), ('support vector machines', 0.009069773978266147),
# ('sample complexity and generalization bounds', 0.0), ('gaussian processes', 0.0), ('modelling', 0.0),
# ('boosting', 0.0), ('bayesian analysis', 0.0), ('online learning theory', 0.0), ('query learning', 0.0)]
# ...
# (9 clusters)
```

