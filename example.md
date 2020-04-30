Let us consider comprehensive analysis of a textual collection with a help of GoT software package. We will consider Data Science Taxonomy (published in []) and collection of research papers on Data Science []. The collection was obtained from Elsevier and Springer journals related to Data Science.

Our final aim is to extract and understand main research directions in the Data Science area.

We will follow the steps below:

0. Download and prepare the text collection and the taxonomy.
1. Obtain text-to-topic relevance matrix using Annotated Suffix Tree approach [].
2. Obtain fuzzy thematic clusters using FADDIS algorithm [].
3. Generalize the clusters and visualize them with the help of GoT.

Let's start.



You can download https://cs.hse.ru/concept/datasets

or via commandline:

wget https://cs.hse.ru/data/2019/05/19/1506729559/papers_parsed_relevant.zip

and unzip the archive:

unzip papers_parsed_relevant.zip
