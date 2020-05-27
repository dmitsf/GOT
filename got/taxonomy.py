""" A class for taxonomy representing
"""

import re
import argparse

from collections.abc import Collection
from typing import List, Generator, Union, Tuple


class Node(Collection):
    """
    A class used to represent a Tree node with the all descendants.
    This is a basic data structure for a taxonomy representing.

    Initial attributes
    ------------------
    index : str
        a string representing the node index, for example 1.2.3.
    name : str
        the name of the node
    parent : Node or None
        the parent of the node
    children : List['Node']
        a list of the all direct descendants (children) of the node
    u : float
        membership value (normalized)
    score : float
        membership value (non-normalized)
    v : float
        node's gap importance
    V : float
        node's cumulative gap importance
    G : List['Node']
        node's set of gaps
    L : List['Node']
        node's set of losses
    p : float
        node's ParGenFS penalty
    H : List['Node']
        node's head subjects

    Main methods
    ------------
    __init__(index, name, parent, children)
        constructor

    __contains__(item)
        checks whether the item is a direct decsendant of the node,
        one may use "in" operator to check the property above

    __iter__()
        iterates over all descendants of the node, this is a
        syntactic sugar for iteration over "node.children"

    __len__()
        returns the outgoing degree of the node, i.e., the
        number of node's children

    __setattr__(name, value)
        allows to set any custom attribute, this is useful for
        ParGenFS algorithm

    __getattr__(name)
        allows to get a custom attribute. If there is no such
        attrubute, returns "None"

    is_leaf() (property)
        checks whether the node is a leaf node

    is_internal() (property)
        checks whether the node is an internal node (i.e., is
        not a leaf)

    is_root() (property)
        checks whether the node is a root of the tree

    """
    def __init__(self, index: str, name: str, parent: Union['Node', None], \
                 children: List['Node'] = None) -> None:
        """Constructor

        Parameters
        ----------
        index : str
            a string representing the node index, for example 1.2.3.
        name : str
            the name of the node
        parent : Union['Node', None]
            the parent of the node
        children : List['Node'], default=None
            a list of the all direct descendants (children) of the node

        Returns
        -------
        None
        """
        self.index = index
        self.name = name
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children

        self.u: float = .0
        self.score: float = .0
        self.G: List['Node'] = []
        self.L: List['Node'] = []
        self.V: float = .0
        self.v: float = .0
        self.p: float = .0
        self.H: List['Node'] = []

    def __contains__(self, item: Union['Node', object]) -> bool:
        """Checks whether the item is a direct descendant of the node

        Parameters
        ----------
        item : Union['Node', object]
            a node to check

        Returns
        -------
        bool
            "True" if the item is a direct descendant of the node,
            else "False"
        """
        return item in self.children

    def __iter__(self) -> Generator['Node', None, None]:
        """Iterates over all the descendants of the node

        Returns
        -------
        Generator['Node', None, None]
            generator over all the descendants
        """
        for item in self.children:
            yield item

    def __len__(self) -> int:
        """Returns an outgoing degree of the node, i.e., a
        number of node's children

        Returns
        -------
        int
            an outgoing degree of the node
        """
        return len(self.children)

    def __setattr__(self, name: str, value: Union[list, dict, str, bool, int, \
                                                  float]) -> None:
        """Allows to set any custom attribute, this is useful for
        ParGenFS algorithm

        Parameters
        ----------
        name: str
            a name of the attribute
        value: Union[list, dict, str, bool]
            a value of the attribute
        Returns
        -------
        None
        """
        self.__dict__[name] = value

    def __getattr__(self, name: str) -> Union[list, dict, str, bool, None]:
        """Allows to get a custom attribute. If there is no such
        attrubute, returns "None"

        Parameters
        ----------
        name: str
            a name of the attribute

        Returns
        -------
        Union[list, dict, str, bool, None]
            a value of the attribute or "None", if there is no such
            an attibute
        """
        if name not in self.__dict__:
            return None
        return self.__dict__[name]

    @property
    def is_leaf(self) -> bool:
        """Checks whether the node is a leaf node

        Returns
        -------
        bool
            "True" if the node is a leaf node,
            else "False"
        """
        return not self.children

    @property
    def is_internal(self) -> bool:
        """Checks whether the node is an internal node (i.e., is
        not a leaf)

        Returns
        -------
        bool
            "True" if the node is an internal node,
            else "False"
        """
        return bool(self.children)

    @property
    def is_root(self) -> bool:
        """Checks whether the node is a root of the tree

        Returns
        -------
        bool
            "True" if the node is a root node,
            else "False"
        """
        return self.parent is None


class Taxonomy:
    """
    A class for taxonomy representing

    Initial attributes
    ------------------
    built_from : str
        a string representing the filename using for taxonomy
        building
    _root : Node
        a root of the taxonomy tree
    leaves_extracted : bool
        label: whether leaves were extracted for the taxonomy or not
    _leaves : List[None]
        containts all the leaves of the taxonomy

    Main methods
    ------------
    __init__(filename)
        constructor

    __repr__()
        represents basic info about the taxonomy

    get_taxonomy_tree(filename)
        builds the taxonomy from the file

    leaves() (property)
        returns all the leaves of the taxonomy

    root() (property)
        returns the root of the taxonomy

    get_index_and_name(node_repr) (staticmethod)
        returns str representations for index and name of node

    """

    def __init__(self, filename: str) -> None:
        """Constructor

        Parameters
        ----------
        filename : str
            a string representing the name of the file for
            taxonomy constructing

        Returns
        -------
        None
        """
        self._root = self.get_taxonomy_tree(filename)
        self.leaves_extracted: bool = False
        self._leaves: List[Node] = []

    def _repr__(self) -> str:
        """Represents information about the taxonomy

        Parameters
        ----------

        Returns
        -------
        str
            string representing the information
        """
        return "Taxonomy built from {}".format(self.built_from)

    @property
    def root(self) -> Node:
        """returns the root of the taxonomy

        Parameters
        ----------

        Returns
        -------
        Node
            the root of the tree
        """
        return self._root

    @staticmethod
    def get_index_and_name(node_repr: Tuple[re.Match, re.Match]) \
        -> Tuple[str, str]:
        """returns str representations of index and name

        Parameters
        ----------
        node : Tuple[re.Match, re.Match]
            index and name found by regexp

        Returns
        -------
        Union[str, str]
            node index and name
        """
        index_s, name_s = node_repr
        return index_s.group(0)[:-1], \
            name_s.group(0)[1:].lower() \
            if (name_s.group(0)[-1].isalpha() or \
                name_s.group(0)[-1] == "'") \
                else name_s.group(0)[1:-1].lower()

    def get_taxonomy_tree(self, filename: str) -> Node:
        """Builds the taxonomy from its description in the file

        Parameters
        ----------
        filename : str
            the file with the taxonomy representation in flat-view
            taxonomy representation (FVTR) format

        Returns
        -------
        Node
            the root of the taxonomy built
        """
        nodes = []
        with open(filename, 'r') as file_opened:
            for line in file_opened:
                index_s = re.search(r"(^[\.\d]+)[*, ]", line)
                name_s = re.search(r",([A-Za-zА-Яа-я 102\-']+),?", line)
                if not index_s:
                    index_s = re.search(r"([\.\d]+.?) ", line)
                    name_s = re.search(r" ([A-Za-zА-Яа-я 102\-']+),?", line)
                if index_s and name_s:
                    nodes.append((index_s, name_s))

        root_found = True
        root_index = nodes[0][0].group(0)[:-1]

        for index_s, _ in nodes[1:]:
            if not index_s.group(0)[:-1].startswith(root_index):
                root_found = False
                break

        if root_found:
            index, name = self.get_index_and_name(nodes[0])
            tree = Node(index, name, None)
            nodes = nodes[1:]
        else:
            tree = Node("", "root", None)

        curr_parent = tree

        for node in nodes:
            index, name = self.get_index_and_name(node)
            while curr_parent.index not in index:
                if curr_parent.parent is not None:
                    curr_parent = curr_parent.parent

            current_node = Node(index, name, curr_parent)
            curr_parent.children.append(current_node)
            curr_parent = current_node

        self.built_from = filename
        self.leaves_extracted = False
        return tree

    @property
    def leaves(self) -> List[Node]:
        """Containts all the leaves of the taxonomy

           Parameters
           ----------
           tree : Node
               the root of the taxonomy

           Returns
           -------
           List[Node]
               a list of the taxonomy leaves
        """
        if self.leaves_extracted:
            return self._leaves

        leaves = extract_leaves(self._root)
        self._leaves = leaves
        self.leaves_extracted = True

        return leaves

    @leaves.setter
    def leaves(self, leaves_list: List[Node]) -> None:
        """Property setter for leaves

           Parameters
           ----------
           leaves_list : List[Node]
               a list of the taxonomy leaves to set

           Returns
           -------
           None
        """
        self._leaves = leaves_list


def extract_leaves(tree: Node) -> List[Node]:
    """Returns all the leaves of the tree / sub-tree

       Parameters
       ----------
       tree : Node
           the root of the tree / sub-tree

       Returns
       -------
       List[Node]
           a list of the tree / sub-tree leaves
    """
    leaves = []

    def find_leaves(node):
        if node.is_internal:
            for child in node:
                find_leaves(child)
        else:
            leaves.append(node)

    find_leaves(tree)

    return leaves

def save_leaves(leaves: List[Node], filename: str = "taxonomy_leaves.txt") -> None:
    """Saves all the leaves of the tree / sub-tree

       Parameters
       ----------
       leaves : List[Node]
           the list of leaves

       Returns
       -------
       None
    """

    with open(filename, "w") as file_opened:
        for node in leaves:
            file_opened.write(node.name)
            file_opened.write("\n")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Working with taxonomy.")
    parser.add_argument("taxonomy_file", type=str,
                        help="taxonomy description in *.fvtr format")

    args = parser.parse_args()

    TAXONOMY_GOT = Taxonomy(args.taxonomy_file)
    print(f"Taxonomy was built from file: {args.taxonomy_file}.")
    print(f"Taxonomy leaves for {args.taxonomy_file}:")
    print(('\n'.join([' '.join([i.index, i.name]) for i in TAXONOMY_GOT.leaves])))
    print("Number of leaves:", len(TAXONOMY_GOT.leaves))
    save_leaves(TAXONOMY_GOT.leaves)
