""" ParGenFS algorithm with accessory functions
"""

import argparse
from operator import itemgetter
from math import sqrt
from typing import Dict, List, Set, Union

try:
    from got.taxonomies.taxonomy import Taxonomy, Node
    from got.taxonomies.ete3_functions import make_ete3_lifted, save_ete3
except ImportError as e:
    from taxonomy import Taxonomy, Node
    from ete3_functions import make_ete3_lifted, save_ete3


LIMIT = .15
GAMMA = .9
LAMBDA = .2


def enumerate_tree_layers(node: Node, current_layer: int = 0) -> None:
    """Assigns a corresponding layer numbers to the all nodes of the taxonomy

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    current_layer : int, default=0
        a layer number (nodes' level) to assign

    Returns
    -------
    None
    """
    node.e = current_layer
    for child in node:
        enumerate_tree_layers(child, current_layer=current_layer+1)


def get_cluster_k(tree_leaves: List[Node], node_names: List[str], \
                  membership_matrix: List[List[float]], k: int) -> Dict[str, float]:
    """Return a membership vector corresponding to a k-th cluster

    Parameters
    ----------
    tree_leaves : List[Node]
        all the leaves of the taxonomy
    node_names : List[str]
        string names of nodes
    membership_matrix : List[List[float]]
        membership matrix, size: (number_of_clusters x number_of_node_names)
    k : int
        index of a cluster
    Returns
    -------
    Dict[str, float]
        membership dictionary corresponding to a k-th cluster
    """
    node_to_weight = dict(zip(node_names, (c[k] for c in membership_matrix)))
    cluster = {t.name: node_to_weight.get(t.name, 0) for t in tree_leaves}

    return cluster


def annotate_with_sum(node: Node, cluster: Dict[str, float]) -> float:
    """Annotates a tree with the cluster weights

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    cluster : Dict[str, float]
        the cluster

    Returns
    -------
    float
        a not-normalized sum of squared weights
    """
    summ = .0

    if node.is_leaf:
        membership = cluster.get(node.name, .0)
        node.score = membership
        node.u = membership
        summ += membership ** 2
    else:
        node.score = .0
        node.u = .0

    for i in node:
        summ += annotate_with_sum(i, cluster)

    return summ


def normalize_and_return_leaf_weights(node: Node, summ: float) -> List[List[Union[str, float]]]:
    """Normalizes leaves' weights (annotations)

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    summ : float
        sum of weights value

    Returns
    -------
    List[List[Union[str, float]]]
        a list of weights normalized
    """
    leaf_weights: List[List[Union[str, float]]] = []

    if node.is_leaf:
        node.u /= sqrt(summ)
        leaf_weights.append([node.u, node.name])

    for i in node:
        leaf_weights.extend(normalize_and_return_leaf_weights(i, summ))

    return leaf_weights


def truncate_weights(node: Node, threshold: float) -> float:
    """Truncates (sets to zero) leaves' weights (annotations)
    what are less than the threshold

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    threshold : float
        the threshold value

    Returns
    -------
    float
        summ of the resulting squared weights
    """
    summ = .0
    if node.is_leaf:
        if node.u < threshold:
            node.u = 0
        else:
            summ += node.u ** 2

    for child in node:
        summ += truncate_weights(child, threshold)

    return summ


def set_internal_weights(node: Node) -> float:
    """Sets weights for internal nodes

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    float
        summ of the resulting squared weights
    """
    if node.is_leaf:
        return node.u ** 2

    summ = .0
    for child in node:
        summ += set_internal_weights(child)
        node.u = sqrt(summ)
    return summ


def prune_tree(node: Node) -> None:
    """Prunes the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    None
    """
    if node.is_internal:
        for child in node:
            prune_tree(child)

        if not node.u:
            g_label = 0
            if node.is_internal and not any([t.children for t in node]):
                g_label = 1
            node.children = []

            if g_label:
                node.G = [node]


def set_gaps_for_tree(node: Node) -> None:
    """Sets gaps for the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    None
    """
    gaps = [child for child in node if child.u == 0]
    if not node.G:
        node.G = gaps

    for child in node:
        set_gaps_for_tree(child)


def set_parameters(node: Node) -> None:
    """Sets parameters G, v, V for the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    None
    """
    for child in node:
        set_parameters(child)

    g_set = sum([child.G for child in node], node.G or [])
    added: Set[str] = set()
    g_result = []
    for gap in g_set:
        if gap.name not in added:
            g_result.append(gap)
            added |= {gap.name}

    node.G = g_result
    node.v = node.parent.u if node.parent else 1.
    node.V = sum(g.v if g.v is not None else 0 for g in node.G)


def reduce_edges(node: Node) -> None:
    """Reduces tree edges for the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    None
    """
    if len(node) == 1:
        temp = node.children[0].children
        node.children = temp

        def update_layer_number(t_node):
            t_node.e -= 1
            for child in t_node:
                update_layer_number(child)

        for child in node:
            update_layer_number(child)

    for child in node:
        reduce_edges(child)


def make_init_step(node: Node, gamma_v: float) -> None:
    """Init step of ParGenFS algorithm

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    gamma_v : float
        gamma value

    Returns
    -------
    None
    """
    if node.is_internal:
        for child in node:
            make_init_step(child, gamma_v)
    else:
        if node.u > 0:
            node.H = [node]
            node.L = []
            node.p = gamma_v * node.u
        else:
            node.H = []
            node.L = []
            node.p = 0

        node.o = True


def make_recursive_step(node: Node, gamma_v: float, lambda_v: float) -> None:
    """Recursive step of ParGenFS algorithm

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree
    gamma_v : float
        gamma value
    lambda_v : float
        lambda value

    Returns
    -------
    None
    """
    if node.is_internal:
        for child in node:
            make_recursive_step(child, gamma_v, lambda_v)

        if not node.o:
            sum_penalty = sum([t.p if t.p is not None else 0 for t in node], .0)

            if node.u + lambda_v * node.V < sum_penalty:
                node.H = [node]
                node.L = node.G
                node.p = node.u + lambda_v * node.V
            else:
                node.H = sum((t.H if t.H is not None else [] for t in node), [])
                node.L = sum((t.L if t.L is not None else [] for t in node), [])
                node.p = sum((t.p if t.p is not None else 0 for t in node), .0)


def indicate_offshoots(node: Node) -> None:
    """Indicates all the offshoots in the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    None
    """

    if node.is_internal:
        for child in node:
            indicate_offshoots(child)
    else:
        if node.parent:
            heads = [t.name for t in node.parent.H]
            if not heads:
                node.of = 1


def make_result_table(node: Node) -> List[List[str]]:
    """Indicates all the offshoots in the tree / sub-tree

    Parameters
    ----------
    node : Node
        the root of the taxonomy tree / sub-tree

    Returns
    -------
    List[List[str]]
        resulting table for printing / saving in a file
    """

    table = []

    if node.is_internal:
        for child in node:
            table.extend(make_result_table(child))

    table.append([node.index.rstrip(".") or "", node.name, str(round(node.u, 3)),
                  str(round(node.p, 3)), str(round(node.V, 3)),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.G or [])]),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.H or [])]),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.L or [])])])

    return table


def save_result_table(result_table: List[List[str]], filename: str = "table.csv") -> None:
    """Writes resulting table in a file

    Parameters
    ----------
    result_table : List[List[str]]
        table for saving
    filename : str, default="table.csv"
        name of the file for writing

    Returns
    -------
    None
    """

    result_table = sorted(result_table, key=lambda x: (len(x), x))
    result_table = [["index", "name", "u", "p", "V", "G", "H", "L"]] + result_table

    with open(filename, 'w') as file_opened:
        for table_row in result_table:
            file_opened.write('\t'.join(table_row) + '\n')

    print(f"Table saved in the file: {filename}")


def pargenfs(cluster: Dict[str, float], taxonomy_tree: Taxonomy, \
             gamma_v: float = .2, lambda_v: float = .2) -> None:
    """Runs ParGenFS algorithm over a taxonomy tree

    Parameters
    ----------
    cluster : List[float]
        the cluster to generalize
    taxonomy_tree : Taxonomy
        the taxonomy tree
    gamma_v : float, default=.2
        gamma penalty value
    lambda_v : float, default=.2
        lambda penalty value

    Returns
    -------
    None
    """

    enumerate_tree_layers(taxonomy_tree.root)

    summ = annotate_with_sum(taxonomy_tree.root, cluster)
    leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree.root, summ)
    print(f"Number of leaves: {len(leaf_weights)}")
    print("All positive weights:")

    for weight, i in sorted(leaf_weights, key=itemgetter(0), reverse=True):
        if not weight:
            break
        print(f"{i:<60} {weight:.5f}")

    summ_after_trunc = truncate_weights(taxonomy_tree.root, LIMIT)

    if summ_after_trunc == 0:
        print("The threshold is too large. Try a smaller one.")
        return

    updated_leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree.root, summ_after_trunc)
    print("After transformation:")
    for weight, i in sorted(updated_leaf_weights, key=itemgetter(0), reverse=True):
        if not weight:
            break
        print(f"{i:<60} {weight:.5f}")

    print("Setting weights for internal nodes")
    root_u = set_internal_weights(taxonomy_tree.root)
    print(f"Membership in root: {root_u:.5f}")
    print("Pruning tree...")
    prune_tree(taxonomy_tree.root)

    print("Setting gaps...")
    set_gaps_for_tree(taxonomy_tree.root)

    print("Other parameters setting...")
    set_parameters(taxonomy_tree.root)
    reduce_edges(taxonomy_tree.root)

    print("ParGenFS main steps...")
    make_init_step(taxonomy_tree.root, gamma_v)
    make_recursive_step(taxonomy_tree.root, gamma_v, lambda_v)

    indicate_offshoots(taxonomy_tree.root)

    print("Done. Saving...")
    result_table = make_result_table(taxonomy_tree.root)
    save_result_table(result_table)

    ete3_desc = make_ete3_lifted(taxonomy_tree.root)
    save_ete3(ete3_desc)
    print("ete representation saved.")
    #print(ete3_desc)
    print("Done.")


def run(taxonomy_file: str, taxonomy_leaves: str, clusters: str, cluster_number: int) -> None:
    """Obtains cluster and runs ParGenFS algorithm over a taxonomy tree

    Parameters
    ----------
    taxonomy_file : str
        taxonomy description in *.fvtr format
    taxonomy_leaves : str
        taxonomy leaves in *.txt format
    clusters : str
        clusters' membership table in *.dat format
    cluster_number : int
        number of cluster for lifting

    Returns
    -------
    None
    """

    gamma_val = GAMMA
    lambda_val = LAMBDA
    taxonomy_tree = Taxonomy(taxonomy_file)

    node_names = []
    with open(taxonomy_leaves, 'r') as file_opened:
        for i in file_opened.readlines():
            splitted = i.split('\t')
            if len(splitted) > 1:
                node_names.append(splitted[1].strip())
            else:
                node_names.append(splitted[0].strip())

    membership_matrix = []
    with open(clusters, 'r') as file_opened:
        for line in file_opened.readlines():
            try:
                membership_vector = list(map(float, line.split('\t')))
            except ValueError:
                membership_vector = list(map(float, line.split(' ')))
            membership_matrix.append(membership_vector)

    tree_leaves = taxonomy_tree.leaves
    cluster = get_cluster_k(tree_leaves, node_names, membership_matrix, cluster_number)
    pargenfs(cluster, taxonomy_tree, gamma_v=gamma_val, lambda_v=lambda_val)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Lifting a cluster over a taxonomy.")
    parser.add_argument("taxonomy_file", type=str,
                        help="taxonomy description in *.fvtr format")
    parser.add_argument("taxonomy_leaves", type=str,
                        help="taxonomy leaves in *.txt format")
    parser.add_argument("clusters", type=str,
                        help="clusters' membership table in *.dat format")
    parser.add_argument("cluster_number", type=int,
                        help="number of cluster for lifting")

    args = parser.parse_args()

    run(args.taxonomy_file, args.taxonomy_leaves, args.clusters, args.cluster_number)
