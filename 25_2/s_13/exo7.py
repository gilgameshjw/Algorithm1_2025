# exo_7_solutions.py

import networkx as nx
import matplotlib.pyplot as plt

def create_graph_examples():
    """
    Problem 1: Graph Examples
    """
    # 1. Directed graphs and their transposed graphs
    print("1. Directed Graphs and Transpose:")
    
    # Example 1
    G1 = nx.DiGraph()
    G1.add_edges_from([(1, 2), (2, 3), (3, 1)])
    G1_transpose = G1.reverse()
    
    print("Original G1 edges:", list(G1.edges()))
    print("Transpose G1 edges:", list(G1_transpose.edges()))
    
    # 2. Undirected graphs and their complements
    print("\n2. Undirected Graphs and Complements:")
    
    G2 = nx.Graph()
    G2.add_edges_from([(1, 2), (2, 3), (3, 1)])
    G2_complement = nx.complement(G2)
    
    print("Original G2 edges:", list(G2.edges()))
    print("Complement G2 edges:", list(G2_complement.edges()))
    
    # 3. Dense graph complement
    print("\n3. Dense Graph Complement:")
    
    # Complete graph K5
    K5 = nx.complete_graph(5)
    K5_complement = nx.complement(K5)
    
    print("K5 edges:", len(K5.edges()), "density:", nx.density(K5))
    print("K5 complement edges:", len(K5_complement.edges()), "density:", nx.density(K5_complement))
    print("For dense graphs, the complement is sparse.")
    
    # 4. Dual graphs (simplified planar examples)
    print("\n4. Dual Graphs (Planar Examples):")
    
    # Simple planar graph: a triangle
    planar_G = nx.Graph()
    planar_G.add_edges_from([(0, 1), (1, 2), (2, 0)])
    
    print("Simple planar graph (triangle)")
    print("Dual would have one vertex inside the triangle")
    
    # 5. Why dual only for planar graphs
    print("\n5. Why Dual Only for Planar Graphs:")
    explanation = """
    The dual graph is only well-defined for planar graphs because:
    
    1. Definition: The dual is constructed by placing a vertex in each face
       and connecting vertices across shared edges.
       
    2. Non-planar Example: K5 (complete graph with 5 vertices)
       - K5 is non-planar (Kuratowski's theorem)
       - It cannot be drawn without edge crossings
       - Without well-defined faces, we cannot construct a dual
       
    3. Geometric Requirement: The dual relies on the embedding of the graph
       in the plane with distinct faces. Non-planar graphs cannot have such
       an embedding without crossings.
       
    4. Topological Constraint: The concept of 'inside' and 'outside'
       requires a planar embedding to be meaningful.
    """
    print(explanation)
    
    return G1, G1_transpose, G2, G2_complement

def bron_kerbosch_no_pivot(R, P, X, graph, cliques):
    """
    Bron-Kerbosch algorithm without pivoting
    """
    if not P and not X:
        cliques.append(R.copy())
        return
    
    for v in list(P):
        # New recursive call
        bron_kerbosch_no_pivot(
            R.union({v}),
            P.intersection(set(graph[v])),
            X.intersection(set(graph[v])),
            graph,
            cliques
        )
        P.remove(v)
        X.add(v)

def find_maximal_cliques():
    """
    Problem 2: Bron-Kerbosch Algorithm Execution
    """
    # Graph representation
    graph = {
        "A": ["B", "C"],
        "B": ["A", "C"],
        "C": ["A", "B", "D"],
        "D": ["C"]
    }
    
    print("Graph adjacency list:")
    for vertex, neighbors in graph.items():
        print(f"{vertex}: {neighbors}")
    
    # Initial call
    R = set()
    P = set(graph.keys())  # All vertices
    X = set()
    
    cliques = []
    
    print("\nInitial call: R = {}, P = {A,B,C,D}, X = {}")
    
    # Trace first two recursive calls
    print("\nTrace of first two calls:")
    
    # Call 1: Start with vertex A
    print("\n1. Starting with vertex A:")
    print("   R = {A}, P = {B,C} (neighbors of A), X = {}")
    
    # From A, explore B
    print("\n2. From A, exploring B:")
    print("   R = {A,B}, P = {C} (neighbors of A∩B), X = {}")
    print("   → Maximal clique found: {A, B, C}")
    
    # Find all maximal cliques
    bron_kerbosch_no_pivot(R, P, X, graph, cliques)
    
    print("\nAll maximal cliques:")
    for i, clique in enumerate(cliques, 1):
        print(f"{i}. {clique}")
    
    # Find maximum cliques
    max_size = max(len(c) for c in cliques) if cliques else 0
    maximum_cliques = [c for c in cliques if len(c) == max_size]
    
    print(f"\nMaximum clique(s) (size {max_size}):")
    for clique in maximum_cliques:
        print(f"  {clique}")
    
    return cliques, maximum_cliques

if __name__ == "__main__":
    create_graph_examples()
    print("\n" + "=" * 50)
    find_maximal_cliques()
