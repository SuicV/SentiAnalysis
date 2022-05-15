import pandas as pd
import networkx as nx
from pyvis.network import Network


def coreference_graph(groups):
    """
    function to plot coreference aspects as a graph.
    """
    # create a dataframe to store connection between nodes
    d = pd.DataFrame(columns=["source", "target"])
    # create empty network
    net = Network(width=1000)
    # add root node with red color
    net.add_node("root", label="root", color="#F53D3D")

    for parent in groups.keys():
        # add group node with color green if it has similare aspects else black
        net.add_node(parent, label=parent, color= "#3D2E28" if len(groups[parent]) == 1 else "#57C21D")
        # link group node with parent
        d = d.append({"source":"root", "target": parent},ignore_index=True)
        for child in groups[parent]:
            # add similar aspects nodes to the group node with brown color
            if child != parent:
                net.add_node(child, label=child, color="#C24D1D")
                d = d.append({"source":parent, "target":child}, ignore_index=True)
    # connect graph nodes using created dataframe
    graph = nx.from_pandas_edgelist(d, source="source", target = "target")
    net.add_edges(graph.edges)
    # store graph as html file
    net.write_html("temp_html.html")
    return net
