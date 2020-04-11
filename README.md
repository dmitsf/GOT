__GOT__ (__G__ eneralization __O__ ver __T__ axonomies) software package.

The repository includes ParGenFS and related algorithms implementations.

Read more about the algorithm and the related definitions in the recent article: https://doi.org/10.1016/j.ins.2019.09.082

See a technical documentation here: https://got-docs.readthedocs.io/


# Installation

For basic usage you may skip the installation: it will be sufficient to clone the repository and run programs form the repository folder.

If you would like to import GOT modules in your Python code, you may install the package.
To install, you should run from the repository folder:

```
[sudo] python3 setup.py install 
```

The install command may be slightly different - this depends on your Python interpreter setup.


# Requirements

For visualization you should install ete3 package (http://etetoolkit.org/download/):

```
[sudo] pip3 install --upgrade ete3
```

These modules may be needed also:

```
[sudo] apt-get install python3-pyqt5.qtsvg
[sudo] apt-get install python3-pyqt5.qtopengl
```

# Taxonomy format: _.fvtr_

We use _.fvtr_ (flat-view taxonomy representation) format. It relies on a representation of ACM CCS taxonomy (https://www.acm.org/publications/class-2012). You can see examples of files in [test_files/](https://github.com/dmitsf/GOT/blob/master/got/test_files/) folder.

# Usage

## Working with a taxonomy

__taxonomy.py__: parses a taxonomy file in _.fvtr_ format, prepares a basic data structure for working with the taxonomy tree.

```
python3 taxonomy.py taxonomy_file
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
python3 pargenfs.py taxonomy_file taxonomy_leaves clusters cluster_number

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
python3 visualize.py ete3_file
```

positional arguments:
*  ete3_file:   lifting results description in *.ete format

optional arguments:
 * -h, --help:  show help message and exit


# Tutorial

Let us consider working with IAB taxonomy fragment [test_files/taxonomy_iab_fragment.fvtr](https://github.com/dmitsf/GOT/blob/master/got/test_files/taxonomy_iab_fragment.fvtr).

![Taxonomy fragment](https://raw.githubusercontent.com/dmitsf/GOT/master/got/got_results/iab_fragment.png)

Fig. 1: Taxonomy fragment

## Working with a taxonomy

```
python3 taxonomy.py test_files/taxonomy_iab_fragment.fvtr

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
python3 pargensf.py test_files/taxonomy_iab_fragment.fvtr test_files/taxonomy_leaves_iab_fragment.txt test_files/clusters_ds_modified.dat 0

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
python3 visualize.py
```

![Visualization result](https://raw.githubusercontent.com/dmitsf/GOT/master/got/got_results/result_iab_fragment.png)

Fig. 2: Visualization result
