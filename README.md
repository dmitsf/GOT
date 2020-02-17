GOT (generalization over taxonomies) software package.

Includes ParGenFS and related algorithms implementation.

Read more in the recent article: https://doi.org/10.1016/j.ins.2019.09.082

See related documentation here: https://got-docs.readthedocs.io/


# Installation

Download the repository and run from the repository folder:

```
[sudo] python3 setup.py install 
```

For visualization you should install ete3 package (http://etetoolkit.org/download/):

```
[sudo] pip3 install --upgrade ete3
```


These modules may be needed also:

```
[sudo] apt-get install python3-pyqt5.qtsvg
[sudo] apt-get install python3-pyqt5.qtopengl
```

# Example

Let us consider GOT package and working with IAB taxonomy fragment.

## Working with taxonomy

__taxonomy.py__: parses a taxonomy file in _.fvtr_ format, prepares basic data structure for working with the taxonomy tree.

```
python3 taxonomy.py

Taxonomy leaves:
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

__pargensf.py__: lifts the leaf cluster over a taxonomy tree. Produces two files:
* _table.csv_: table with all the variables' values
* _taxonomy_tree.ete_: lifting result on the taxonomy tree in ete3 format.


```
python3 pargensf.py

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
(men's shoes and footwear[&&NHX:p=0:e=1:H={}:u=0.0:v=1.0:G={}:L={}:Hd=0:Ch=0:Sq=0],men's accessories[&&NHX:p=0.265:e=1:H={men's accessories}:u=0.662:v=1.0:G={}:L={}:Hd=1:Ch=0:Sq=1],(men's formal wear...men's underwear and sleepwear 3 items[&&NHX:p=0:e=2:H={}:u=0.0:v=0.75:G={}:L={}:Hd=0:Ch=0:Sq=0],men's outerwear style[&&NHX:p=0.128:e=2:H={men's outerwear style}:u=0.32:v=0.75:G={}:L={}:Hd=1:Ch=0:Sq=1],men's casual wear[&&NHX:p=0.177:e=2:H={men's casual wear}:u=0.443:v=0.75:G={}:L={}:Hd=1:Ch=0:Sq=1],men's business wear[&&NHX:p=0.205:e=2:H={men's business wear}:u=0.514:v=0.75:G={}:L={}:Hd=1:Ch=0:Sq=1])men's clothing style[&&NHX:p=0.511:e=1:H={men's business wear;...;men's outerwear style}:u=0.75:v=1.0:G={men's formal wear;...;men's underwear and sleepwear}:L={}:Hd=0:Ch=1:Sq=0])root[&&NHX:p=0.775:e=0:H={men's accessories;...;men's outerwear style}:u=1.0:v=1.0:G={men's shoes and footwear;...;men's underwear and sleepwear}:L={}:Hd=0:Ch=1:Sq=0];
Done
```

## Visualization

__visualize.py__: draws lifting results from _taxonomy_tree.ete_ on taxonomy tree.

```
python3 visualize.py
```

![Visualization result](https://github.com/dmitsf/GOT/blob/master/got/got_results/result_iab_fragment.png)

