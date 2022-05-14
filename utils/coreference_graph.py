import pandas as pd
import networkx as nx
from pyvis.network import Network


def coreference_graph(groups):
    """
    function to plot coreference aspects as a graph.
    """
    d = pd.DataFrame(columns=["source", "target"])
    net = Network(width=1000)
    net.add_node("root", label="root", color="#F53D3D")

    for parent in groups.keys():
        net.add_node(parent, label=parent, color= "#3D2E28" if len(groups[parent]) == 1 else "#57C21D")
        d = d.append({"source":"root", "target": parent},ignore_index=True)
        for child in groups[parent]:
            if child != parent:
                net.add_node(child, label=child, color="#C24D1D")
                d = d.append({"source":parent, "target":child}, ignore_index=True)
    graph = nx.from_pandas_edgelist(d, source="source", target = "target")
    net.add_edges(graph.edges)
    net.show("temp_html.html")
    return net
