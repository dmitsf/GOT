from operator import itemgetter
from math import sqrt

from taxonomy import leaves_from_tree, get_taxonomy_tree

LIMIT = .2
GAMMA = .4
LAMBDA = .1


def get(tree):
    return leaves_from_tree(tree)


def enumerate_tree_layers(node, e=0):
    node["e"] = e
    for i in node["children"]:
        enumerate_tree_layers(i, e=e+1)


def get_cluster_k(tree_leaves, node_names, membership_matrix, k):

    node_to_weight = dict(zip(node_names, (c[k] for c in membership_matrix)))
    cluster = {t["name"]: node_to_weight.get(t["name"], 0) for t in tree_leaves}

    return cluster


def annotate_with_sum(node, cluster):
    summ = 0

    if not node["children"]:
        node["score"] = cluster.get(node["name"], 0)
        node["u"] = node["score"]
        summ += node["score"] ** 2
    else:
        node["score"] = 0
        node["u"] = node["score"]

    for i in node["children"]:
        summ += annotate_with_sum(i, cluster)

    return summ


def normalize_and_return_leaf_weights(node, summ):

    leaf_weights = []

    if not node["children"]:
        node["u"] /= sqrt(summ)
        leaf_weights.append([node["u"], node["name"]])

    for i in node["children"]:
        leaf_weights.extend(normalize_and_return_leaf_weights(i, summ))

    return leaf_weights


def truncate_weights(node, threshold):
    summ = 0
    if not node["children"]:
        if node["u"] < threshold:
            node["u"] = 0
        else:
            summ += node["u"] ** 2

    for t in node["children"]:
        summ += truncate_weights(t, threshold)

    return summ


def set_internal_weights(node):
    if not node["children"]:
        return node["u"] ** 2

    summ = 0
    for t in node["children"]:
        summ += set_internal_weights(t)
        node["u"] = sqrt(summ)
    return summ


def prune_tree(node):
    if node["children"]:
        for t in node["children"]:
            prune_tree(t)

        if not node["u"]:
            g_label = 0
            if node["children"] and not any([t["children"] for t in node["children"]]):
                g_label = 1
            node["children"] = []

            if g_label:
                node["G"] = [node]


def set_gaps_for_tree(node):
    g = [t for t in node.get("children", []) if t["u"] == 0]
    if not node.get("G"):
        node["G"] = g

    for t in node["children"]:
        set_gaps_for_tree(t)


def set_parameters(node):

    for t in node["children"]:
        set_parameters(t)

    g_set = sum([t["G"] for t in node["children"]], node.get("G", []))
    added = set()
    g_result = []
    for t in g_set:
        if t["name"] not in added:
            g_result.append(t)
            added |= {t["name"]}

    node["G"] = g_result
    node["v"] = (node.get("parent") or {}).get("u", 1)
    node["V"] = sum(x.get("v", 0) for x in node["G"])


def reduce_edges(node):
    if len(node["children"]) == 1:
        h = node["children"][0]["children"]
        node["children"] = h

        def update_layer_number(n):
            n["e"] -= 1
            for t in n["children"]:
                update_layer_number(t)

        for t in node["children"]:
            update_layer_number(t)

    for t in node["children"]:
        reduce_edges(t)


def make_init_step(node, gamma_v):
    if node["children"]:
        for t in node["children"]:
            make_init_step(t, gamma_v)
    else:
        if node["u"] > 0:
            node["H"] = [node]
            node["L"] = []
            node["p"] = gamma_v * node["u"]
        else:
            node["H"] = []
            node["L"] = []
            node["p"] = 0

        node["o"] = True


def make_recursive_step(node, gamma_v, lambda_v):

    if node["children"]:
        for t in node["children"]:
            make_recursive_step(t, gamma_v, lambda_v)

        if not node.get("o"):
            sum_penalty = sum([t.get("p", 0) for t in node["children"]])

            if node["u"] + lambda_v * node.get("V") < sum_penalty:
                node["H"] = [node]
                node["L"] = node.get("G")
                node["p"] = node["u"] + lambda_v * node.get("V")
            else:
                node["H"] = sum([t.get("H", []) for t in node["children"]], [])
                node["L"] = sum([t.get("L", []) for t in node["children"]], [])
                node["p"] = sum([t.get("p", 0) for t in node["children"]], 0)


def indicate_offshoots(node):
    if node["children"]:
        for t in node["children"]:
            indicate_offshoots(t)
    else:
        heads = [t["name"] for t in node["parent"].get("H", [])]
        if not heads:
            node["of"] = 1


def make_result_table(node):

    table = []

    if node["children"]:
        for t in node["children"]:
            table.extend(make_result_table(t))

    table.append([node["index"].rstrip(".") or "", node["name"], str(round(node["u"], 3)),
                  str(round(node["p"], 3)), str(round(node["V"], 3)),
                  "; ".join([s["index"] + " " + s["name"] for s in node.get("H", [])]),
                  "; ".join([s["index"] + " " + s["name"] for s in node.get("G", [])]),
                  "; ".join([s["index"] + " " + s["name"] for s in node.get("L", [])])])

    return table


def save_result_table(result_table, file_name="table.csv"):
    result_table = sorted(result_table, key=lambda x: (len(x), x))
    result_table = [["index", "name", "u", "p", "V", "H", "G", "L"]] + result_table

    with open(file_name, 'w') as f:
        for t in result_table:
            f.write('\t'.join(t) + '\n')


def make_ete3(taxonomy_tree, print_all=True):
    heads = [t["index"] for t in taxonomy_tree["H"]]

    def rec_ete3(node, h=0):
        output = []

        if node["index"] in heads and not h:
            h = 1

        if node["children"]:
            output.append("(")
            sorted_children = sorted(node["children"], key=lambda x: x.get("u"))
            j = 0
            while not sorted_children[j].get("u"):
                j += 1

            sn = sorted_children[j - 1]["name"]
            if j == 2:
                sorted_children[j - 1]["name"] = sorted_children[0]["name"] + ". " \
                                                 + sorted_children[j - 1]["name"]
            if j > 2:
                sorted_children[j - 1]["name"] = sorted_children[0]["name"] + "..." \
                                                 + sorted_children[j - 1]["name"] + \
                                                 " " +  str(j) + " items"
            if j:
                output.extend(rec_ete3(sorted_children[j - 1], h=h))
                output.append(",")

            sorted_children[j - 1]["name"] = sn

            l = len(sorted_children[j:])
            for k, t in enumerate(sorted_children[j:]):
                output.extend(rec_ete3(t, h=h))
                if k < l - 1:
                    output.append(",")
            output.append(")")

        if node.get("u", 0) > 0 or print_all:
            output.append(node["name"])
            output.extend(["[&&NHX:", "p=", str(round(node["p"], 3)), ":", "e=", str(node["e"]), \
                           ":", "H={", ";".join([s["name"] for s in (node.get("H", []) if \
                                                                     len(node.get("H", [])) < 3 \
                                                                     else [node["H"][0], \
                                                                           {"name": "..."}, \
                                                                           node["H"][-1]])]), \
                           "}:u=", str(round(node["u"], 3)), ":", "v=", str(round(node["v"], 3)), \
                           ":G={", ";".join([s["name"] for s in (node.get("G", []) \
                                                                 if len(node.get("G", [])) < 3 \
                                                                 else [node["G"][0], {"name":
                                                                                      "..."},\
                                                                       node["G"][-1]])]), \
                           "}:L={", ";".join([s["name"] for s in (node.get("L", []) \
                                                                  if len(node.get("L", [])) < 3 \
                                                                  else [node["L"][0], {"name": \
                                                                                       "..."}, \
                                                                        node["L"][-1]])]), \
                           "}:Hd=", ("1" if node["index"] in heads else "0"), ":Ch=", \
                           ("1" if node.get("children") else "0"), ":Sq=", ("1" if h else "0"),\
                           "]"])

        return output

    output = rec_ete3(taxonomy_tree)
    output.append(";")
    return "".join(output)


def save_ete3(ete3_desc, file_name="taxonomy_tree.ete"):
    with open(file_name, 'w') as f:
        f.write(ete3_desc)


def pargenfs(cluster, taxonomy_tree, gamma_v=.2, lambda_v=.2):

    enumerate_tree_layers(taxonomy_tree)

    summ = annotate_with_sum(taxonomy_tree, cluster)
    leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree, summ)
    print("Number of leaves:", len(leaf_weights))
    print("All positive weights:")

    for w, i in sorted(leaf_weights, key=itemgetter(0), reverse=True):
        if not w:
            break
        print("%-50s %.5f" % (i, w))

    summ_after_trunc = truncate_weights(taxonomy_tree, LIMIT)
    updated_leaf_weights = normalize_and_return_leaf_weights(taxonomy_tree, summ_after_trunc)
    print("After transformation:")
    for w, i in sorted(updated_leaf_weights, key=itemgetter(0), reverse=True):
        if not w:
            break
        print("%-50s %.5f" % (i, w))

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
    taxonomy_tree = get_tree()

    node_names = []
    with open("latin_taxonomy_leaves.txt", 'r') as f:
        for i in f.readlines():
            node_names.append(i.split('\t')[1].strip().replace("ju", "yu").\
                              replace("ja", "ya").lower().replace("hor", "khor").\
                              replace("kuh", "kukh").replace("eha", "ekha").\
                              replace("hrom", "khrom").replace("yh", "ykh").\
                              replace("hol", "khol").replace("oh", "okh"))

    membership_matrix = []
    with open("mem2dat", 'r') as f:
        for l in f.readlines():
            line = list(map(float, l.split('\t')))
            membership_matrix.append(line)

    tree_leaves = leaves_from_tree(taxonomy_tree)
    cluster = get_cluster_k(tree_leaves, node_names, membership_matrix, 2)
    pargenfs(cluster, taxonomy_tree, gamma_v=gamma_val, lambda_v=lambda_val)


if __name__ == "__main__":

    run()
