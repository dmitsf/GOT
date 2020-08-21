# Usage and examples

## __taxonomy.py__: working with a taxonomy

__taxonomy.py__: parses a taxonomy file in _.fvtr_ format, prepares a basic data structure for working with the taxonomy tree. Prints all the leaves and saves them into _taxonomy_leaves.csv_ file.

### Usage

```
$ python3 taxonomy.py taxonomy_file
```

positional arguments:
*  taxonomy_file:  taxonomy description in *.fvtr format

optional arguments:
*  -h, --help:     show help message and exit

### Example 1

Let us consider working with IAB taxonomy fragment [test_files/taxonomy_iab_fragment.fvtr](https://github.com/dmitsf/GOT/blob/master/got/taxonomies/test_files/taxonomy_iab_fragment.fvtr).

![Taxonomy fragment](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/iab_fragment.png)

Fig. 1: Taxonomy fragment

Let's obtain all the leaves for the taxonomy. 

```
$ python3 taxonomy.py test_files/taxonomy_iab_fragment.fvtr
```

The command produces this output:

```
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

### Example 2

We will consider Data Science Taxonomy (DST, published, for example, in [this preprint](https://wp.hse.ru/data/2019/01/13/1146987922/WP7_2018_04_______.pdf)). We can download the DST taxonomy via browser from the [webpage of "Concept" research group](https://cs.hse.ru/concept/taxonomies)
or via command line:

```
$ wget https://cs.hse.ru/data/2019/12/18/1523118089/Data_Science_taxonomy.xlsx
```

Since the taxonomy has _.xlsx_ format, we should transform the taxonomy to _.csv_. One may do this using Microsoft Excel, OpenOffice/LibreOffice Calc, or via command line:

```
$ libreoffice --headless --convert-to csv Data_Science_taxonomy.xlsx
```

Assume we should extract all the leaves from a taxonomy. To do this, we can use _taxonomy.py_ module from GoT:

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

## __pargenfs.py__: generalization

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

### Example

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

A Ete representation of the cluster generalization in the taxonomy was saved in _taxonomy_tree_lifted.ete_ file.


## __visualize.py__: Visualization

__visualize.py__: draws lifting results from _taxonomy_tree.ete_ on taxonomy tree.

### Usage

```
$ python3 visualize.py ete3_file
```

positional arguments:
*  ete3_file:   lifting results description in *.ete format

optional arguments:
 * -h, --help:  show help message and exit


### Example


Let's visualize the result using _visualize.py_ module.

```
$ python3 visualize.py taxonomy_tree_lifted.ete
```

We can see the figure - the same as posted below. To look in details, you can click on the figure and open full-size.

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/cluster_0.png "Cluster 0 generalization visualization.")

Fig. 2: Cluster 0 generalization.


For cluster 2, we obtainded the following fugure.

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/cluster_1.png "Cluster 1 generalization visualization.")

Fig. 3: Cluster 1 generalization.

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

# Data structures

## fvtr format

_.fvtr_ (flat-view taxonomy representation) format is a comma-separated (csv)-like format to store taxonomies. It relies on a representation of ACM CCS taxonomy (https://www.acm.org/publications/class-2012). You can see examples of files in [test_files/](https://github.com/dmitsf/GOT/blob/master/got/test_files/) folder.

Example -  IAB taxonomy fragment:

```
579.,Men's Fashion,
579.580.,,Men's Accessories,
579.580.581.,,,Men's Jewelry and Watches,
579.582.,,Men's Clothing Style,
579.582.583.,,,Men's Business Wear,
579.582.584.,,,Men's Casual Wear,
579.582.585.,,,Men's Formal Wear,
579.582.586.,,,Men's Outerwear Style,
579.582.587.,,,Men's Sportswear,
579.582.588.,,,Men's Underwear and Sleepwear,
579.589.,,Men's Shoes and Footwear,
```

represents the taxonomy shown at Fig. 4.

![Taxonomy fragment](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/iab_fragment.png)

Fig. 4: IAB taxonomy fragment

## ete3

A format for taxonomy tree storing used in [ETE toolkit](http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#understanding-ete-trees) and other tools. Allows to define a tree topology alongside with the tree nodes' attributes.

Some examples from [ETE toolkit docs](http://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html):

```
"(A,B,(C,D));"

#
#     /-A
#    |
#----|--B
#    |
#    |     /-C
#     \---|
#          \-D

"((A,B),(C,D));"

#
#          /-A
#     /---|
#    |     \-B
#----|
#    |     /-C
#     \---|
#          \-D

```

## Tree

A class representing a taxonomy tree.

    A class for taxonomy representing

    Initial attributes
    ------------------
    built_from : str
        a string representing the filename using for taxonomy
        building
    _root : Node
        a root of the taxonomy tree
    leaves_extracted : bool
        label: whether leaves were extracted for the taxonomy or not
    _leaves : List[None]
        containts all the leaves of the taxonomy

    Main methods
    ------------
    __init__(filename)
        constructor

    __repr__()
        represents basic info about the taxonomy

    get_taxonomy_tree(filename)
        builds the taxonomy from the file

    leaves() (property)
        returns all the leaves of the taxonomy

    root() (property)
        returns the root of the taxonomy

    get_index_and_name(node_repr) (staticmethod)
        returns str representations for index and name of node

## Node

A class representing a taxonomy tree node.


    A class used to represent a Tree node with the all descendants.
    This is a basic data structure for a taxonomy representing.

    Initial attributes
    ------------------
    index : str
        a string representing the node index, for example 1.2.3.
    name : str
        the name of the node
    parent : Node or None
        the parent of the node
    children : List['Node']
        a list of the all direct descendants (children) of the node
    u : float
        membership value (normalized)
    score : float
        membership value (non-normalized)
    v : float
        node's gap importance
    V : float
        node's cumulative gap importance
    G : List['Node']
        node's set of gaps
    L : List['Node']
        node's set of losses
    p : float
        node's ParGenFS penalty
    H : List['Node']
        node's head subjects

    Main methods
    ------------
    __init__(index, name, parent, children)
        constructor

    __contains__(item)
        checks whether the item is a direct decsendant of the node,
        one may use "in" operator to check the property above

    __iter__()
        iterates over all descendants of the node, this is a
        syntactic sugar for iteration over "node.children"

    __len__()
        returns the outgoing degree of the node, i.e., the
        number of node's children

    __setattr__(name, value)
        allows to set any custom attribute, this is useful for
        ParGenFS algorithm

    __getattr__(name)
        allows to get a custom attribute. If there is no such
        attrubute, returns "None"

    is_leaf() (property)
        checks whether the node is a leaf node

    is_internal() (property)
        checks whether the node is an internal node (i.e., is
        not a leaf)

    is_root() (property)
        checks whether the node is a root of the tree


## result table

A table with the result of the lifting obtaing during __pargenfs.py__ execution. The table is a comma-separated (_*.csv_) file with the following columns:

```
"index", "name", "u", "p", "V", "G", "H", "L"
```

The columns contain values obtained for each node of the taxonomy tree.
