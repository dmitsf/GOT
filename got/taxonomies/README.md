# Generalizing the clusters and visualizing them with the help of GoT.

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

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/cluster_0.png "Cluster 0 generalization visualization.")

Fig. 3: Cluster 0 generalization.


For cluster 2, we obtainded the following fugure.

![](https://raw.githubusercontent.com/dmitsf/GOT/master/got/taxonomies/got_results/cluster_1.png "Cluster 1 generalization visualization.")

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

# Data structures

## fvtr format

tab-separated (tsv)-like format to store taxonomies.

example:




## ete3

##

##

