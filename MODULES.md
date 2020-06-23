# MODULE LIST

## 1. __pargenfs.py__

__pargenfs.py__: lifts the leaf cluster over a taxonomy tree. Produces two files:
* _table.csv_: table with all the variables' values
* _taxonomy\_tree.ete_: lifting result on the taxonomy tree in _*.ete3_ format.

### Usage

```
$ python3 pargenfs.py taxonomy_file taxonomy_leaves clusters cluster_number
```

positional arguments:
*  taxonomy_file:    taxonomy description in _*.fvtr_ format
*  taxonomy_leaves:  taxonomy leaves in _*.txt_ format
*  clusters:         clusters' membership table in _*.dat_ format
*  cluster_number:   number of cluster for lifting

optional arguments:
*  -h, --help:       show help message and exit

## 2. __taxonomy.py__

__taxonomy.py__: parses a taxonomy file in _*.fvtr_ format, prepares a basic data structure for working with the taxonomy tree.

```
$ python3 taxonomy.py taxonomy_file
```

positional arguments:
*  taxonomy_file:  taxonomy description in _*.fvtr_ format

optional arguments:
*  -h, --help:     show help message and exit

## 3. __visualize.py__

__visualize.py__: draws lifting results from _taxonomy_tree.ete_ on taxonomy tree. After the start, shows an image than can be saved as _*.pdf_ file from the image menu.

```
$ python3 visualize.py ete3_file
```

positional arguments:
*  ete3_file:   lifting results description in _*.ete_ format

optional arguments:
 * -h, --help:  show help message and exit

## 4. __ete3_functions.py__

__ete3_functions.py__: contains auxiliary functions for working with ete3 format.

## 5. __util/__

__util/__: a folder containing utility modules

### 5.1. __lapin.py__

__lapin.py__: LAPIN transform implementation. Produces a file:
* _transformed_matrix.dat_: a matrix transformed by the program.

#### Usage

```
$ python3 lapin.py matrix_file
```

positional arguments:
*  matrix_file:      a matrix to transform in _*.dat_ format

optional arguments:
*  -h, --help:       show help message and exit

### 5.2. __faddis.py__

__faddis.py__: FADDIS clustering implementation in Python. Produces a file:
* _clusters.dat_: fuzzy clusters obtained by the program.

#### Usage

```
$ python3 faddis.py matrix_file
```

positional arguments:
*  matrix_file:      a matrix to cluster in _*.dat_ format

optional arguments:
*  -h, --help:       show help message and exit

### 5.3. __relevances.py__

__relevances.py__: calculates relevance and co-relevance matrices for a given text collection and taxonomy. Produces a file:
* _relevance_matrix.dat_/_corelevance_matrix.dat_: relevance/corelevance matrices (dependsing on chosen mode).

#### Usage

```
$ python3 relevances.py mode text_collection taxonomy_leaves
```

positional arguments:
* mode:      a mode: either `relevance` or `corelevance`
* text_collection: a text collection as a double-blank line separated _*.txt_ file (double-blank lines between texts of the collection)
* taxonomy_leaves: taxonomy leaves as _*.txt_ file, one taxonomy topic per a line.

optional arguments:
*  -h, --help:       show help message and exit

## 6. __ast/__

__ast/__: a folder containing AST implementation.

### 6.1. __base_ast.py__

__base_ast.py__: annotated suffix tree implementation. Used by the _relevance.py_ program.
