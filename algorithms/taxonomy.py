import re

from collections.abc import Collection


class Node(Collection):
    def __init__(self, index, name, parent):
        self.index = index
        self.name = name
        self.parent = parent
        self.children = []

    def __contains__(self, item):
        return item in self.children

    def __iter__(self):
        for item in self.children:
            yield item

    def __len__(self):
        return len(self.children)

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            return None
        return self.__dict__[name]

    @property
    def is_leaf(self):
        return not self.children

    @property
    def is_internal(self):
        return bool(self.children)


def get_taxonomy_tree(file_name="latin_taxonomy_rest.csv"):

    tree = Node('', 'root', None)
    curr_parent = tree

    with open(file_name, 'r') as f:
        for line in f:
            index_s = re.search(r"(^[\.\d]+)[*, ]", line)
            name_s = re.search(r",([A-Za-z 102\-']+),?", line)

            if index_s and name_s:
                index, name = index_s.group(0)[:-1], \
                              name_s.group(0)[1:].lower() \
                              if (name_s.group(0)[-1].isalpha() or \
                                  name_s.group(0)[-1] == "'") \
                                  else name_s.group(0)[1:-1].lower()
                while curr_parent.index not in index:
                    curr_parent = curr_parent.parent

                current_node = Node(index, name, curr_parent)
                curr_parent.children.append(current_node)
                curr_parent = current_node

    return tree


def leaves_from_tree(tree):

    leaves = []

    def find_leaves(node):
        if node.is_internal:
            for t in node:
                find_leaves(t)
        else:
            leaves.append(node)

    find_leaves(tree)

    return leaves


if __name__ == '__main__':

    t = get_taxonomy_tree()
    print(('\n'.join([i.index +' ' + i.name for i in leaves_from_tree(t)])))
