# Example: using a taxonomy to analyse a text collection

Let us consider analysis of a text collection with a help of GoT software package. We will consider Data Science Taxonomy (DST, published in [this preprint](https://wp.hse.ru/data/2019/01/13/1146987922/WP7_2018_04_______.pdf)) and collection of abstracts of research papers on Data Science (may be downloaded from a [webpage of "Concept" research group, HSE University](https://cs.hse.ru/concept/taxonomies)). The collection under consideration was obtained from 80 Elsevier and Springer journals related to Data Science. The collection is available at a [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets).

Our final aim is to extract and understand the main research directions in the Data Science area.

We will follow the steps below:

0. Downloading and preparing the text collection and the taxonomy.
1. Obtaining text-to-topic relevance matrix using Annotated Suffix Tree approach [].
2. Obtaining fuzzy thematic clusters using FADDIS algorithm [].
3. Generalizing the clusters and visualizing them with the help of GoT.

Let's start.

## 0. Downloading and preparing the text collection and the taxonomy.

We can download the collection via browser from a [webpage of "Concept" research group](https://cs.hse.ru/concept/datasets)
or via commandline:

```wget https://cs.hse.ru/data/2019/05/19/1506729559/papers_parsed_relevant.zip```

After that, we should unzip the archive:

```unzip papers_parsed_relevant.zip```

We can download the DST taxonomy via browser from a [webpage of "Concept" research group](https://cs.hse.ru/concept/taxonomies)
or via commandline:

```wget https://cs.hse.ru/data/2019/12/18/1523118089/Data_Science_taxonomy.xlsx```

Since the taxonomy have .xlsx format, we should transform the taxonomy to .csv. One may do this using Miscrosoft Excel, OpenOffice/LibreOffice Calc or via commandline:

```libreoffice --headless --convert-to csv Data_Science_taxonomy.xlsx```

Now we have all the files prepared.

.
