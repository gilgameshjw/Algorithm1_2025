# exo_5_solutions.py

"""
Problem 1: Equivalent Definitions of a Tree
Proof sketch for each equivalence:

1. ↔ 2: A tree is connected and acyclic. A forest is a collection of acyclic components.
   A tree is just a forest with exactly one component.
   
2. ↔ 3: A tree with V vertices has exactly V-1 edges (can be proved by induction).
   Connectedness ensures it's exactly V-1, not less.
   
3. ↔ 4: Minimal connectivity means removing any edge disconnects it.
   Connected graph with V-1 edges has this property.
   
4. ↔ 5: Minimally connected ⇒ acyclic (otherwise could remove cycle edge).
   Acyclic with V-1 edges ⇒ connected and minimal.
   
5. ↔ 6: Maximally acyclic means adding any edge creates a cycle.
   Acyclic with V-1 edges is maximal (adding edge would create cycle).
   
6. ↔ 7: Unique paths between vertices ⇔ acyclic and connected.
   Cycle would give two paths between vertices.
"""

def reconstruct_graphs():
    """
    Problem 2: Sparse Graph Representation
    """
    # Graph 1 (undirected)
    print("Graph 1 (Undirected):")
    print("col_pointers = [0, 2, 5, 8, 11, 12]")
    print("row_indices = [1, 2, 0, 2, 3, 0, 1, 3, 1, 2, 4, 3]")
    print("values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]")
    
    # Adjacency matrix for Graph 1
    adj_matrix1 = [
        [0, 1, 1, 0, 0],  # A: connected to B, C
        [1, 0, 1, 1, 0],  # B: connected to A, C, D
        [1, 1, 0, 1, 0],  # C: connected to A, B, D
        [0, 1, 1, 0, 1],  # D: connected to B, C, E
        [0, 0, 0, 1, 0]   # E: connected to D
    ]
    
    print("\nAdjacency Matrix (Graph 1):")
    for row in adj_matrix1:
        print(row)
    
    print("\nEdges (Graph 1): A-B, A-C, B-C, B-D, C-D, D-E")
    
    # Graph 2 (directed)
    print("\n\nGraph 2 (Directed):")
    print("col_pointers = [0, 0, 2, 4, 5, 7]")
    print("row_indices = [0, 3, 0, 1, 2, 1, 3]")
    print("values = [1, 1, 1, 1, 1, 1, 1]")
    
    # Adjacency matrix for Graph 2
    adj_matrix2 = [
        [0, 0, 0, 0, 0],  # A: no outgoing edges
        [1, 0, 0, 1, 0],  # B: A→B, D→B
        [0, 1, 0, 0, 0],  # C: B→C
        [1, 0, 1, 0, 0],  # D: A→D, C→D
        [0, 0, 0, 0, 0]   # E: no outgoing edges
    ]
    
    print("\nAdjacency Matrix (Graph 2):")
    for row in adj_matrix2:
        print(row)
    
    print("\nEdges (Graph 2): A→B, D→B, B→C, A→D, C→D")
    print("Unique cycle: A→B→C→D→A (A→B, B→C, C→D, D→A)")
    
    return adj_matrix1, adj_matrix2

if __name__ == "__main__":
    reconstruct_graphs()
