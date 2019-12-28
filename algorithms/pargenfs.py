""" ParGenFS algorithm with accessory functions
"""

from operator import itemgetter
from math import sqrt
from typing import List

from taxonomy import leaves_from_tree, get_taxonomy_tree, Node


LIMIT = .2
GAMMA = .4
LAMBDA = .1


def enumerate_tree_layers(node: None, current_layer: int = 0) -> None:
    """Assigns a corresponding layer numbers to the all nodes of the taxonomy

    Parameters
    ----------
    tree : Node
        the root of the taxonomy
    current_layer : int
        a layer number (nodes' level) to assign

    Returns
    -------
    None
    """

    node.e = current_layer
    for child in node:
        enumerate_tree_layers(child, current_layer=current_layer+1)


def get_cluster_k(tree_leaves: List[Node], node_names: List[str], \
                  membership_matrix: List[List[float]], k: int) -> List[float]:
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
    List[float]
        membership vector corresponding to a k-th cluster
    """

    node_to_weight = dict(zip(node_names, (c[k] for c in membership_matrix)))
    cluster = {t.name: node_to_weight.get(t.name, 0) for t in tree_leaves}

    return cluster


def annotate_with_sum(node, cluster):
    summ = 0

    if node.is_leaf:
        node.score = cluster.get(node.name, 0)
        node.u = node.score
        summ += node.score ** 2
    else:
        node.score = 0
        node.u = node.score

    for i in node:
        summ += annotate_with_sum(i, cluster)

    return summ


def normalize_and_return_leaf_weights(node, summ):

    leaf_weights = []

    if node.is_leaf:
        node.u /= sqrt(summ)
        leaf_weights.append([node.u, node.name])

    for i in node:
        leaf_weights.extend(normalize_and_return_leaf_weights(i, summ))

    return leaf_weights


def truncate_weights(node, threshold):
    summ = 0
    if node.is_leaf:
        if node.u < threshold:
            node.u = 0
        else:
            summ += node.u ** 2

    for child in node:
        summ += truncate_weights(child, threshold)

    return summ


def set_internal_weights(node):
    if node.is_leaf:
        return node.u ** 2

    summ = 0
    for child in node:
        summ += set_internal_weights(child)
        node.u = sqrt(summ)
    return summ


def prune_tree(node):
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


def set_gaps_for_tree(node):
    gaps = [child for child in node if child.u == 0]
    if not node.G:
        node.G = gaps

    for child in node:
        set_gaps_for_tree(child)


def set_parameters(node):

    for child in node:
        set_parameters(child)

    g_set = sum([child.G for child in node], node.G or [])
    added = set()
    g_result = []
    for gap in g_set:
        if gap.name not in added:
            g_result.append(gap)
            added |= {gap.name}

    node.G = g_result
    node.v = node.parent.u if node.parent else 1
    node.V = sum(g.v if g.v is not None else 0 for g in node.G)


def reduce_edges(node):
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


def make_init_step(node, gamma_v):
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


def make_recursive_step(node, gamma_v, lambda_v):

    if node.is_internal:
        for child in node:
            make_recursive_step(child, gamma_v, lambda_v)

        if not node.o:
            sum_penalty = sum([t.p if t.p is not None else 0 for t in node])

            if node.u + lambda_v * node.V < sum_penalty:
                node.H = [node]
                node.L = node.G
                node.p = node.u + lambda_v * node.V
            else:
                node.H = sum((t.H if t.H is not None else [] for t in node), [])
                node.L = sum((t.L if t.L is not None else [] for t in node), [])
                node.p = sum((t.p if t.p is not None else 0 for t in node), 0)


def indicate_offshoots(node):
    if node.is_internal:
        for child in node:
            indicate_offshoots(child)
    else:
        heads = [t.name for t in (node.parent.H or [])]
        if not heads:
            node.of = 1


def make_result_table(node):

    table = []

    if node.is_internal:
        for child in node:
            table.extend(make_result_table(child))

    table.append([node.index.rstrip(".") or "", node.name, str(round(node.u, 3)),
                  str(round(node.p, 3)), str(round(node.V, 3)),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.H or [])]),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.G or [])]),
                  "; ".join([" ".join([s.index, s.name]) for s in (node.L or [])])])

    return table


def save_result_table(result_table, filename="table.csv"):
    result_table = sorted(result_table, key=lambda x: (len(x), x))
    result_table = [["index", "name", "u", "p", "V", "H", "G", "L"]] + result_table

    with open(filename, 'w') as file_opened:
        for table_row in result_table:
            file_opened.write('\t'.join(table_row) + '\n')


def make_ete3(taxonomy_tree, print_all=True):
    head_subjects = set(t.index for t in taxonomy_tree.H)

    def rec_ete3(node, head_subject=0):
        output = []

        if node.index in head_subjects and not head_subject:
            head_subject = 1

        if node.is_internal:
            output.append("(")
            sorted_children = sorted(node.children, key=lambda x: x.u)
            j = 0
            while not sorted_children[j].u:
                j += 1

            last_sorted_name = sorted_children[j - 1].name
            if j == 2:
                sorted_children[j - 1].name = sorted_children[0].name + ". " \
                                                 + sorted_children[j - 1].name
            if j > 2:
                sorted_children[j - 1].name = sorted_children[0].name + "..." \
                                                 + sorted_children[j - 1].name + \
                                                 " " +  str(j) + " items"
            if j:
                output.extend(rec_ete3(sorted_children[j - 1], head_subject=head_subject))
                output.append(",")

            sorted_children[j - 1].name = last_sorted_name

            children_len = len(sorted_children[j:])
            for k, child in enumerate(sorted_children[j:]):
                output.extend(rec_ete3(child, head_subject=head_subject))
                if k < children_len - 1:
                    output.append(",")
            output.append(")")

        if node.u > 0 or print_all:
            output.append(node.name)
            output.extend(["[&&NHX:", "p=", str(round(node.p, 3)), ":", "e=", str(node.e), \
                           ":", "H={", ";".join([s.name for s in ((node.H or []) if \
                                                                  len(node.H or []) < 3 \
                                                                  else [node.H[0], \
                                                                        Node(None, "...", None), \
                                                                        node.H[-1]])]), \
                           "}:u=", str(round(node.u, 3)), ":", "v=", str(round(node.v, 3)), \
                           ":G={", ";".join([s.name for s in ((node.G or []) \
                                                              if len(node.G or []) < 3 \
                                                              else [node.G[0],
                                                                    Node(None, "...", None), \
                                                                    node.G[-1]])]), \
                           "}:L={", ";".join([s.name for s in ((node.L or []) \
                                                               if len(node.L or []) < 3 \
                                                               else [node.L[0], \
                                                                     Node(None, "...", None), \
                                                                     node.L[-1]])]), \
                           "}:Hd=", ("1" if node.index in head_subjects else "0"), ":Ch=", \
                           ("1" if node.is_internal else "0"), ":Sq=", ("1" if head_subject else "0"),\
                           "]"])

        return output

    output = rec_ete3(taxonomy_tree)
    output.append(";")
    return "".join(output)


def save_ete3(ete3_desc, filename="taxonomy_tree.ete"):
    with open(filename, 'w') as file_opened:
        file_opened.write(ete3_desc)


def pargenfs(cluster, taxonomy_tree, gamma_v=.2, lambda_v=.2):

    enumerate_tree_layers(taxonomy_tree)

    summ = annotate_with_sum(taxonomy_tree, cluster)
    leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree, summ)
    print("Number of leaves:", len(leaf_weights))
    print("All positive weights:")

    for weight, i in sorted(leaf_weights, key=itemgetter(0), reverse=True):
        if not weight:
            break
        print("%-50s %.5f" % (i, weight))

    summ_after_trunc = truncate_weights(taxonomy_tree, LIMIT)
    updated_leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree, summ_after_trunc)
    print("After transformation:")
    for weight, i in sorted(updated_leaf_weights, key=itemgetter(0), reverse=True):
        if not weight:
            break
        print("%-50s %.5f" % (i, weight))

    print("Setting weights for internal nodes")
    root_u = set_internal_weights(taxonomy_tree)
    print("Membership in root:", root_u)
    print("Pruning tree")
    prune_tree(taxonomy_tree)

    print("Setting gaps")
    set_gaps_for_tree(taxonomy_tree)

    print("Other parameters setting")
    set_parameters(taxonomy_tree)
    reduce_edges(taxonomy_tree)

    print("ParGenFS main steps")
    make_init_step(taxonomy_tree, gamma_v)
    make_recursive_step(taxonomy_tree, gamma_v, lambda_v)

    indicate_offshoots(taxonomy_tree)

    result_table = make_result_table(taxonomy_tree)
    save_result_table(result_table)

    ete3_desc = make_ete3(taxonomy_tree)
    save_ete3(ete3_desc)
    print(ete3_desc)
    print("Done")


def run():
    gamma_val = GAMMA
    lambda_val = LAMBDA
    taxonomy_tree = get_taxonomy_tree()

    node_names = []
    with open("test_files/latin_taxonomy_leaves.txt", 'r') as file_opened:
        for i in file_opened.readlines():
            node_names.append(i.split('\t')[1].strip().replace("ju", "yu").\
                              replace("ja", "ya").lower().replace("hor", "khor").\
                              replace("kuh", "kukh").replace("eha", "ekha").\
                              replace("hrom", "khrom").replace("yh", "ykh").\
                              replace("hol", "khol").replace("oh", "okh"))

    membership_matrix = []
    with open("test_files/clusters.dat", 'r') as file_opened:
        for line in file_opened.readlines():
            membership_vector = list(map(float, line.split('\t')))
            membership_matrix.append(membership_vector)

    tree_leaves = leaves_from_tree(taxonomy_tree)
    cluster = get_cluster_k(tree_leaves, node_names, membership_matrix, 2)
    pargenfs(cluster, taxonomy_tree, gamma_v=gamma_val, lambda_v=lambda_val)


if __name__ == "__main__":

    run()
