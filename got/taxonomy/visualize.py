""" Taxonomy visualization
"""

import argparse

from ete3 import TextFace, Tree, TreeStyle, \
    NodeStyle, RectFace, PieChartFace, TreeNode


def layout_lift(node: TreeNode, levels: int = 3) -> None:
    """Layout implementation for a tree node

    Parameters
    ----------
    node : TreeNode
        the root of the taxonomy tree / sub-tree
    levels : int
        a number of tree levels to draw

    Returns
    -------
    None
    """

    name = TextFace(node.name if (int(node.e) < levels or node.Hd == "1") else "", tight_text=True)
    name.rotation = 270
    node.add_face(name, column=0, position="branch-right")
    nst = NodeStyle()

    if .2 >= float(node.u) > 0:
        nst["fgcolor"] = "#90ee90"
    elif .4 >= float(node.u) > .2:
        nst["fgcolor"] = "green"
    elif float(node.u) > .4:
        nst["fgcolor"] = "#004000"
    else:
        nst["fgcolor"] = "red"

    if node.Hd == "0":
        nst["size"] = 20
        nst["shape"] = "square"
    else:
        if node.Ch == "1":
            nst["size"] = 40
            nst["shape"] = "circle"
        else:
            nst["size"] = 40
            nst["shape"] = "circle"

    if node.Sq == "1":
        nst["shape"] = "circle"

    node.set_style(nst)


def layout_raw(node: TreeNode, tight_mode: bool = True) -> None:
    """Layout implementation for a tree node

    Parameters
    ----------
    node : TreeNode
        the root of the taxonomy tree / sub-tree
    tight_mode : bool, default=True
        a mode to print node names more tightly

    Returns
    -------
    None
    """

    if tight_mode:
        name_segments = node.name.split(' ')
        for i, name_segment in enumerate(name_segments):
            name_face = TextFace(name_segment, tight_text=True)
            name_face.rotation = 270
            node.add_face(name_face, column=i, position="branch-right")
    else:
        name_face = TextFace(node.name, tight_text=True)
        name_face.rotation = 270
        node.add_face(name_face, column=0, position="branch-right")

    nst = NodeStyle()

    nst["fgcolor"] = "black"
    nst["size"] = 20
    nst["shape"] = "circle"

    node.set_style(nst)


def read_ete3_from_file(filename: str) -> str:
    """Reads ete3 representation from the file

    Parameters
    ----------
    filename : str
        a name of the file

    Returns
    -------
    str
        content of the file
    """
    with open(filename, 'r') as file_opened:
        return file_opened.read()


def draw_lifting_tree(filename: str) -> None:
    """Draws a tree from ete3 representation
    stored in a file

    Parameters
    ----------
    filename : str
        a name of the file

    Returns
    -------
    None
    """

    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = layout_lift
    ts.rotation = 90
    ts.branch_vertical_margin = 10
    ts.show_scale = False
    ts.scale = 50
    ts.title.add_face(TextFace(" ", fsize=20), column=0)

    ts.legend.add_face(TextFace("  "), column=0)
    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=2)
    ts.legend.add_face(TextFace("  "), column=3)

    ts.legend.add_face(TextFace("              "), column=0)
    ts.legend.add_face(TextFace("Node shape and size:"), column=1)
    ts.legend.add_face(TextFace("              "), column=2)
    ts.legend.add_face(TextFace("Node color - membership value:"), column=3)

    ts.legend.add_face(TextFace("  "), column=0)
    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=2)
    ts.legend.add_face(TextFace("  "), column=3)

    ts.legend.add_face(PieChartFace([100], 20, 20, colors=['white'], line_color='black'), column=0)
    ts.legend.add_face(TextFace("  topic that relates to the cluster"), column=1)

    ts.legend.add_face(RectFace(30, 10, "#90ee90", "#90ee90"), column=2)
    ts.legend.add_face(TextFace("  topic with minor membership 0<u(t)<=0.2"), column=3)

    ts.legend.add_face(TextFace("  "), column=0)
    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=2)
    ts.legend.add_face(TextFace("  "), column=3)

    ts.legend.add_face(PieChartFace([100], 40, 40, colors=['white'], line_color='black'), column=0)
    ts.legend.add_face(TextFace("  head subject"), column=1)

    ts.legend.add_face(RectFace(30, 10, "green", "green"), column=2)
    ts.legend.add_face(TextFace(u"  topic with medium membership 0.2<u(t)<=0.4   "), column=3)

    ts.legend.add_face(TextFace("  "), column=0)
    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=2)
    ts.legend.add_face(TextFace("  "), column=3)

    ts.legend.add_face(RectFace(20, 20, "black", "white"), column=0)
    ts.legend.add_face(TextFace("  topic that doesn't relate to cluster                     "), \
                       column=1)

    ts.legend.add_face(RectFace(30, 10, "#004000", "#004000"), column=2)
    ts.legend.add_face(TextFace("  topic with high membership u(t)>0.4"), column=3)

    ts.legend.add_face(TextFace("  "), column=0)
    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=2)
    ts.legend.add_face(TextFace("  "), column=3)

    ts.legend.add_face(TextFace("  "), column=1)
    ts.legend.add_face(TextFace("  "), column=1)

    ts.legend.add_face(RectFace(30, 10, "red", "red"), column=2)
    ts.legend.add_face(TextFace("  topic with no membership (u(t)=0)"), column=3)

    ts.legend_position = 3

    ete3_desc = read_ete3_from_file(filename)
    tree = Tree(ete3_desc, format=1)

    tree.show(tree_style=ts)


def draw_raw_tree(filename: str) -> None:
    """Draws a raw tree from ete3 representation
    stored in a file

    Parameters
    ----------
    filename : str
        a name of the file

    Returns
    -------
    None
    """

    ts = TreeStyle()
    ts.show_leaf_name = False
    ts.layout_fn = layout_raw
    ts.rotation = 90
    ts.branch_vertical_margin = 10
    ts.show_scale = False
    ts.scale = 50
    ts.title.add_face(TextFace(" ", fsize=20), column=0)

    ete3_desc = read_ete3_from_file(filename)
    tree = Tree(ete3_desc, format=1)

    tree.show(tree_style=ts)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Visualization of lifting.")
    parser.add_argument("ete3_file", type=str,
                        help="lifting results description in *.ete format")

    args = parser.parse_args()

    draw_lifting_tree(args.ete3_file)
