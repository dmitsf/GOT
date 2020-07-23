__GOT__ (__G__ eneralization __O__ ver __T__ axonomies) software package.

The repository includes ParGenFS and related algorithms implementations.

Read more about the algorithm and the related definitions in the recent article: https://doi.org/10.1016/j.ins.2019.09.082

See a technical documentation here: https://got-docs.readthedocs.io/


# Installation

For basic usage you may skip the installation: it will be sufficient to clone the repository and run programs form the repository folder.

If you would like to import GOT modules in your Python code, you may install the package.
To install, you should run from the repository folder:

```
$ [sudo] python3 setup.py install 
```

The install command may be slightly different - this depends on your Python interpreter setup.


# Requirements

For visualization you should install ete3 package (http://etetoolkit.org/download/):

```
$ [sudo] pip3 install --upgrade ete3
```

These modules may be needed also:

```
$ [sudo] apt-get install python3-pyqt5.qtsvg
$ [sudo] apt-get install python3-pyqt5.qtopengl
```

# Taxonomy format: _.fvtr_

We use _.fvtr_ (flat-view taxonomy representation) format. It relies on a representation of ACM CCS taxonomy (https://www.acm.org/publications/class-2012). You can see examples of files in [test_files/](https://github.com/dmitsf/GOT/blob/master/got/test_files/) folder.

# Usage

## Working with a taxonomy

__taxonomy.py__: parses a taxonomy file in _.fvtr_ format, prepares a basic data structure for working with the taxonomy tree.

```
$ python3 taxonomy.py taxonomy_file
```

positional arguments:
*  taxonomy_file:  taxonomy description in *.fvtr format

optional arguments:
*  -h, --help:     show help message and exit


## Generalization

__pargenfs.py__: lifts the leaf cluster over a taxonomy tree. Produces two files:
* _table.csv_: table with all the variables' values
* _taxonomy\_tree.ete_: lifting result on the taxonomy tree in ete3 format.

### Usage

```
$ python3 pargenfs.py taxonomy_file taxonomy_leaves clusters cluster_number

```

positional arguments:
*  taxonomy_file:    taxonomy description in *.fvtr format
*  taxonomy_leaves:  taxonomy leaves in *.txt format
*  clusters:         clusters' membership table in *.dat format
*  cluster_number:   number of cluster for lifting

optional arguments:
*  -h, --help:       show help message and exit

## Visualization

__visualize.py__: draws lifting results from _taxonomy_tree.ete_ on taxonomy tree.

```
$ python3 visualize.py ete3_file
```

positional arguments:
*  ete3_file:   lifting results description in *.ete format

optional arguments:
 * -h, --help:  show help message and exit


# Tutorial

Let us consider working with IAB taxonomy fragment [test_files/taxonomy_iab_fragment.fvtr](https://github.com/dmitsf/GOT/blob/master/got/test_files/taxonomy_iab_fragment.fvtr).

![Taxonomy fragment](https://raw.githubusercontent.com/dmitsf/GOT/master/got/relevance_analysis/got_results/iab_fragment.png)

Fig. 1: Taxonomy fragment

## Working with a taxonomy

```
$ python3 taxonomy.py test_files/taxonomy_iab_fragment.fvtr

Taxonomy leaves for test_files/taxonomy_iab_fragment.fvtr:
579.580.581. men's jewelry and watches
579.582.583. men's business wear
579.582.584. men's casual wear
579.582.585. men's formal wear
579.582.586. men's outerwear style
579.582.587. men's sportswear
579.582.588. men's underwear and sleepwear
579.589. men's shoes and footwear

```

## Generalization

```
$ python3 pargensf.py test_files/taxonomy_iab_fragment.fvtr test_files/taxonomy_leaves_iab_fragment.txt test_files/clusters_ds_modified.dat 0

Number of leaves: 8
All positive weights:
men's jewelry and watches                                    0.66164
men's business wear                                          0.51372
men's casual wear                                            0.44276
men's outerwear style                                        0.31983
After transformation:
men's jewelry and watches                                    0.66164
men's business wear                                          0.51372
men's casual wear                                            0.44276
men's outerwear style                                        0.31983
Setting weights for internal nodes
Membership in root: 1.00000
Pruning tree
Setting gaps
Other parameters setting
ParGenFS main steps
(men's shoes and footwear[&&NHX:p=0:e=1:H={}:u=0.0:v=1.0:G={}:L={}:Hd=0:Ch=0:Sq=0],men's accessories[&&NHX:p=0.265:e=1:H=
{men's accessories}:u=0.662:v=1.0:G={}:L={}:Hd=1:Ch=0:Sq=1],(men's formal wear...men's underwear and sleepwear 3 
items[&&NHX:p=0:e=2:H={}:u=0.0:v=0.75:G={}:L={}:Hd=0:Ch=0:Sq=0],men's outerwear style[&&NHX:p=0.128:e=2:H={men's outerwear 
style}:u=0.32:v=0.75:G={}:L={}:Hd=1:Ch=0:Sq=1],men's casual wear[&&NHX:p=0.177:e=2:H={men's casual wear}:u=0.443:v=0.75:G=
{}:L={}:Hd=1:Ch=0:Sq=1],men's business wear[&&NHX:p=0.205:e=2:H={men's business wear}:u=0.514:v=0.75:G={}:L=
{}:Hd=1:Ch=0:Sq=1])men's clothing style[&&NHX:p=0.511:e=1:H={men's business wear;...;men's outerwear style}:u=0.75:v=1.0:G=
{men's formal wear;...;men's underwear and sleepwear}:L={}:Hd=0:Ch=1:Sq=0])root[&&NHX:p=0.775:e=0:H={men's 
accessories;...;men's outerwear style}:u=1.0:v=1.0:G={men's shoes and footwear;...;men's underwear and sleepwear}:L=
{}:Hd=0:Ch=1:Sq=0];
Done
```

## Visualization

```
$ python3 visualize.py
```

![Visualization result](https://raw.githubusercontent.com/dmitsf/GOT/master/got/relevance_analysis/got_results/result_iab_fragment.png)

Fig. 2: Visualization result


# Example: using a taxonomy to analyse a text collection

Let us consider the analysis of a text collection with the help of GoT software package. We will consider Data Science Taxonomy (DST, published, for example, in [this preprint](https://wp.hse.ru/data/2019/01/13/1146987922/WP7_2018_04_______.pdf)) and collection of abstracts of research papers on Data Science (may be downloaded from the [webpage of "Concept" research group, HSE University](https://cs.hse.ru/concept/taxonomies)). The collection under consideration was obtained from 80 Elsevier and Springer journals related to Data Science. The collection is available at the [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets).

Our final aim here is to obtain and visualize the main research directions in the Data Science area that we can extract using the collection and the taxonomy.

We will follow the steps below:

0. Downloading and preparing the text collection and the taxonomy.
1. Obtaining text-to-topic relevance matrix using Annotated Suffix Tree approach.
2. Obtaining fuzzy thematic clusters using FADDIS algorithm.
3. Generalizing the clusters and visualizing them with the help of GoT.

Let's start.

## 0. Downloading and preparing the text collection and the taxonomy.

We can download the collection via browser from the [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets)
or via command line:

```
$ wget https://cs.hse.ru/data/2019/05/19/1506729559/papers_parsed_relevant.zip
```

After that, we should unzip the archive downloaded:

```
$ unzip papers_parsed_relevant.zip
```

We can download the DST taxonomy via browser from the [webpage of "Concept" research group](https://cs.hse.ru/concept/taxonomies)
or via command line:

```
$ wget https://cs.hse.ru/data/2019/12/18/1523118089/Data_Science_taxonomy.xlsx
```

Since the taxonomy has _.xlsx_ format, we should transform the taxonomy to _.csv_. One may do this using Microsoft Excel, OpenOffice/LibreOffice Calc, or via command line:

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

All the fuzzy clusters are saved in _clusters.dat_ file. We are ready to generalize them with GoT.

## 3. Generalizing the clusters and visualizing them with the help of GoT.

Let's generalize the 0-th obtained cluster with the parameters LIMIT = 0.12 (cluster's membership threshold), GAMMA = 0.9, LAMBDA = 0.075. We will use _pargenfs.py_ module from GoT:

```
$ python3 pargenfs.py Data_Science_taxonomy.csv taxonomy_leaves.txt clusters.dat 0

Number of leaves: 351
All positive weights:
instance-based learning                                      0.24283
content analysis and feature selection                       0.22174
database interoperability                                    0.20913
fuzzy representation                                         0.18784
ontologies                                                   0.17688
neuro-fuzzy approach                                         0.17494
structured text search                                       0.16406
robust regression                                            0.16056
decision diagrams                                            0.15770
multidimensional range search                                0.15517
relevance assessment                                         0.15021
bayesian analysis                                            0.14260
graph embedding                                              0.13755
q-learning                                                   0.12964
knowledge discovery                                          0.12467
thesauri                                                     0.12376
learning under covariate shift                               0.12285
critical nodes detection                                     0.11745
bayesian networks                                            0.11663
contingency table analysis                                   0.11658
image search                                                 0.11466
integrity checking                                           0.11460
markov network models                                        0.11249
entity relationship models                                   0.11231
scalable                                                     0.11186
process mining                                               0.10558
data encoding and canonicalization                           0.10427
online learning theory                                       0.10281
data modeling                                                0.10260
graph drawings                                               0.10236
...
After transformation:
instance-based learning                                      0.35224
content analysis and feature selection                       0.32165
database interoperability                                    0.30336
fuzzy representation                                         0.27247
ontologies                                                   0.25658
neuro-fuzzy approach                                         0.25376
structured text search                                       0.23797
robust regression                                            0.23290
decision diagrams                                            0.22876
multidimensional range search                                0.22508
relevance assessment                                         0.21789
bayesian analysis                                            0.20684
graph embedding                                              0.19953
q-learning                                                   0.18804
knowledge discovery                                          0.18083
thesauri                                                     0.17952
learning under covariate shift                               0.17820
Setting weights for internal nodes
Membership in root: 1.00000
Pruning tree...
Setting gaps...
Other parameters setting...
ParGenFS main steps...
Done. Saving...
Table saved in the file: table.csv
ete representation saved in the file: taxonomy_tree_lifted.ete
Done.
```

All the variables' values ware saved in _table.csv_ file. The table contains all the penalty values, gaps, offshoots, and head subjects for all the steps of the algorithm's execution. Let's take a look. As a result of algorithm's execution, we can see 11 head subjects, devoted mainly to Machine Learning and Information Systems: 

```
1.1.1.6. bayesian analysis; 
1.1.2.6. database interoperability; 
2.1.1.4. decision diagrams; 
2.1.5.3. regression analysis; 
3. information systems; 
5.2.1.2.7.1 graph embedding; 
5.2.1.4.3. learning under covariate shift; 
5.2.3.3.3.2 fuzzy representation; 
5.2.3.8. rule learning; 
5.2.3.9. instance-based learning; 
5.2.4.1.2. q-learning
```

A Ete representation of the cluster generalization in the taxonomy was saved in _taxonomy_tree_lifted.ete_ file. Let's visualize the result using _visualize.py_ module.

```
$ python3 visualize.py taxonomy_tree_lifted.ete
```

We can see the figure - the same as posted below. To look in details, you can click on the figure and open full-size.

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/relevance_analysis/got_results/cluster_0.png "Cluster 0 generalization visualization.")

Fig. 3: Cluster 0 generalization.


For cluster 2, we obtainded the following fugure.

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/relevance_analysis/got_results/cluster_1.png "Cluster 1 generalization visualization.")

Fig. 4: Cluster 1 generalization.

The 15 head subjects were obtained here, which is devoted mainly to Databases, Visualization and Implementation:

```
1.1.1.15. semi-supervised learning; 
1.1.2.9. data integration; 
2.1.3.2. loopy belief propagation; 
3.1.1.4. physical data models; 
3.1.3.3.3. database recovery; 
3.1.4.4. call level interfaces; 
3.1.5.5. wrappers; 
3.2.1.7 graph mining; 
3.3.1.3.2. surfacing; 
3.4.5.8. clustering and classification; 
4.1.3.1. scientific visualization; 
4.1.4. visualization systems and tools; 
5.2.3.1.1 parallel implementation; 
5.2.3.7.6. latent dirichlet allocation; 
5.2.4.3. spectral methods
```

We can complete the same steps for all the clusters obtained.
