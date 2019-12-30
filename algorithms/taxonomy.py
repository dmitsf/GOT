""" A class for taxonomy representing
"""

import re

from collections.abc import Collection
from typing import List, Generator, Union


class Node(Collection):
    """
    A class used to represent a Tree node with the all descendants.
    This is a basic data structure for a taxonomy representing.

    Initial attributes
    ----------
    index : str
        a string representing the node index, for example 1.2.3.
    name : str
        the name of the node
    parent : Node or None
        the parent of the node
    children : List['Node']
        a list of the all direct descendants (children) of the node

    Main methods
    -------
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

    is_internal (property)
        checks whether the node is an internal node (i.e., is
        not a leaf)
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
        children : List['Node']
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

    def __setattr__(self, name: str, value: Union[list, dict, str, bool]) -> None:
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


class Taxonomy:
    """
    A class for taxonomy representation
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
        self.built_from = filename
        self.root = get_taxonomy_tree(filename)

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

    def get_taxonomy_tree(filename: str) -> Node:
        """Builds the taxonomy from its description in the file

            Parameters
            ----------
            filename : str
                the file with the taxonomy description in tab-separated
                taxonomy description (TSTD) format

            Returns
            -------
            Node
                the root of the taxonomy built
        """

        tree = Node("", "root", None)
        curr_parent = tree

        with open(filename, 'r') as file_opened:
            for line in file_opened:
                index_s = re.search(r"(^[\.\d]+)[*, ]", line)
                name_s = re.search(r",([A-Za-z 102\-']+),?", line)

                if index_s and name_s:
                    index, name = index_s.group(0)[:-1], \
                                  name_s.group(0)[1:].lower() \
                                  if (name_s.group(0)[-1].isalpha() or \
                                      name_s.group(0)[-1] == "'") \
                                      else name_s.group(0)[1:-1].lower()
                    while curr_parent.index not in index:
                        if curr_parent.parent is not None:
                            curr_parent = curr_parent.parent

                    current_node = Node(index, name, curr_parent)
                    curr_parent.children.append(current_node)
                    curr_parent = current_node

        return tree


def leaves_from_tree(tree: Node) -> List[Node]:
    """Returns all the leaves of the taxonomy

        Parameters
        ----------
        tree : Node
            the root of the taxonomy

        Returns
        -------
        List[Node]
            a list of the taxonomy leaves
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


if __name__ == '__main__':

    TAXONOMY_GOT = Taxonomy("test_files/latin_taxonomy_rest.csv") # get_taxonomy_tree()
    print(('\n'.join([i.index +' ' + i.name for i in leaves_from_tree(TAXONOMY_GOT)])))
