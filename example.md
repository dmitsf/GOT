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

We can see our collection contains 26823 samples. For the sake of simplisity, lets's use a subcollection from 500 samples. To make the subcollection:

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

for a in sampled['abstract']:
    if a.startswith('Abstract '):
        abstracts.append(a[ln:])

print(abstracts[:3])

# Outputs:
#
# ['In Data Mining, during the preprocessing step, there is a considerable diversity ... 
```


To construct text-to-topic relevance matrix, we will follow Annotated Suffix Tree (AST) approach. [This approach](https://bijournal.hse.ru/en/2012--3(21)/63370530.html) relies on fragment text representation and shows excellent results on many text analysis and retrieval problems.

We will use AST implementation from [EAST package](https://github.com/dmitsf/AST-text-analysis), developed by M.Dubov and improved by A.Vlasov and D.Frolov.



```

```

