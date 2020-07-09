""" Functions for dealing with ete3 for taxonomy representations
"""

from typing import Union

try:
    from got.taxonomies.taxonomy import Taxonomy, Node
except ImportError as e:
    from taxonomy import Taxonomy, Node


def make_ete3_lifted(taxonomy_tree: Union[Node, Taxonomy], print_all: bool = True) -> str:
    """Returns ete3 representation of a taxonomy tree
       after lifting procedure completed

    Parameters
    ----------
    taxonomy_tree : Union[Node, Taxonomy]
        the root of the taxonomy tree / sub-tree or taxonomy
    print_all : bool, default=True
        label for printing all the parameters

    Returns
    -------
    str
        resulting ete3 representation
    """
    if isinstance(taxonomy_tree, Taxonomy):
        taxonomy_tree = taxonomy_tree.root

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
                           ("1" if node.is_internal else "0"), ":Sq=", ("1" if head_subject \
                                                                        else "0"), "]"])

        return output

    output = rec_ete3(taxonomy_tree)
    output.append(";")
    return "".join(output)


def make_ete3_raw(taxonomy_tree: Union[Node, Taxonomy]) -> str:
    """Returns ete3 representation of a taxonomy tree
       for raw taxonomy

    Parameters
    ----------
    taxonomy_tree : Union[Node, Taxonomy]
        the root of the taxonomy tree / sub-tree or taxonomy

    Returns
    -------
    str
        resulting ete3 representation
    """
    if isinstance(taxonomy_tree, Taxonomy):
        taxonomy_tree = taxonomy_tree.root

    def rec_ete3(node):
        output = []

        if node.is_internal:
            output.append("(")

            children_len = len(node.children)

            for k, child in enumerate(node.children):
                output.extend(rec_ete3(child))
                if k < children_len - 1:
                    output.append(",")

            output.append(")")
        output.append(node.name)

        return output

    output = rec_ete3(taxonomy_tree)
    output.append(";")
    return "".join(output)


def save_ete3(ete3_desc: str, filename: str = "taxonomy_tree_lifted.ete") -> None:
    """Writes resulting ete3 in a file

    Parameters
    ----------
    ete3_desc : str
        ete3 representation in a string
    filename : str, default="taxonomy_tree_lifted.ete"
        name of the file for writing

    Returns
    -------
    None
    """

    with open(filename, 'w') as file_opened:
        file_opened.write(ete3_desc)

    print(f"ete representation saved in the file: {filename}")


if __name__ == '__main__':

    taxonomy_file = "test_files/taxonomy_iab_fragment.fvtr"
    taxonomy_tree = Taxonomy(taxonomy_file)
    print(make_ete3_raw(taxonomy_tree))
