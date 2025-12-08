# exo_8_solutions.py

from collections import defaultdict, deque

def reverse_graph(G):
    """
    Problem 1.1: Reverse a directed graph in O(V+E) time
    """
    rev_G = defaultdict(list)
    
    for u in G:
        for v in G[u]:
            rev_G[v].append(u)
    
    return rev_G

def prove_scc_properties():
    """
    Proofs for SCC properties (Problems 1.2-1.4)
    """
    proofs = """
    Problem 1.2: Proof that SCC(G) is acyclic:
    
    By contradiction: If SCC(G) had a cycle, then vertices in different
    SCCs could reach each other in both directions, meaning they should
    be in the same SCC. Contradiction.
    
    Problem 1.3: Proof that scc(rev(G)) = rev(scc(G)):
    
    Reversal preserves reachability relationships.
    If u→v in G, then v→u in rev(G).
    Strongly connected components remain the same after reversal.
    
    Problem 1.4: Proof of reachability equivalence:
    
    Forward: If u can reach v in G, then S(u) can reach S(v) in SCC(G)
    because edges between SCCs preserve reachability.
    
    Backward: If S(u) can reach S(v) in SCC(G), then there exists
    a path through SCCs, and within each SCC, vertices can reach each other.
    """
    return proofs

def has_euler_tour(graph):
    """
    Problem 2.1: Check if graph has Euler tour
    """
    for vertex in graph:
        if len(graph.get(vertex, [])) != len([v for v in graph if vertex in graph.get(v, [])]):
            return False
    return True

def find_euler_tour(graph):
    """
    Problem 2.2: Find Euler tour using Hierholzer's algorithm
    """
    if not has_euler_tour(graph):
        return None
    
    # Copy graph to avoid modifying original
    g = {u: deque(v) for u, v in graph.items()}
    stack = []
    circuit = []
    
    # Start from any vertex
    start = next(iter(g))
    stack.append(start)
    
    while stack:
        v = stack[-1]
        if g.get(v):
            u = g[v].popleft()
            stack.append(u)
        else:
            circuit.append(stack.pop())
    
    circuit.reverse()
    return circuit

def topological_sort(graph, start=None):
    """
    Problem 3: Topological Sort
    """
    from collections import deque
    
    # Calculate in-degrees
    in_degree = {v: 0 for v in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] = in_degree.get(v, 0) + 1
    
    # Initialize queue with vertices having 0 in-degree
    queue = deque([v for v in graph if in_degree[v] == 0])
    
    # If start is specified, begin from there if possible
    if start and in_degree.get(start, 0) == 0:
        queue = deque([start])
    
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        
        for v in graph.get(u, []):
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    
    if len(topo_order) != len(graph):
        print("Warning: Graph has a cycle!")
    
    return topo_order

def test_problems():
    """
    Test all problems
    """
    print("Problem 1: SCC and Reversal")
    print("=" * 50)
    
    # Example graph
    G = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['E'],
        'D': ['E', 'F'],
        'E': [],
        'F': [],
        'G': ['F', 'E']
    }
    
    print("Original graph edges:")
    for u in G:
        for v in G[u]:
            print(f"{u} → {v}")
    
    rev_G = reverse_graph(G)
    print("\nReversed graph edges:")
    for u in rev_G:
        for v in rev_G[u]:
            print(f"{u} → {v}")
    
    print("\n" + prove_scc_properties())
    
    print("\nProblem 2: Euler Tour")
    print("=" * 50)
    
    # Eulerian graph example
    euler_graph = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 3],
        3: [2, 0]
    }
    
    print(f"Graph has Euler tour: {has_euler_tour(euler_graph)}")
    tour = find_euler_tour(euler_graph)
    print(f"Euler tour: {tour}")
    
    print("\nProblem 3: Topological Sort")
    print("=" * 50)
    
    course_graph = {
        'A': ['B', 'C'],
        'B': ['C', 'D'],
        'C': ['E'],
        'D': ['E', 'F'],
        'E': [],
        'F': [],
        'G': ['F', 'E']
    }
    
    print("Starting from A:")
    order1 = topological_sort(course_graph, start='A')
    print(f"Topological order: {order1}")
    
    print("\nStarting from G:")
    order2 = topological_sort(course_graph, start='G')
    print(f"Topological order: {order2}")
    
    print("\nComplete topological sorts (all possible):")
    # Generate all topological orders
    from itertools import permutations
    
    vertices = list(course_graph.keys())
    valid_orders = []
    
    for perm in permutations(vertices):
        valid = True
        for i, u in enumerate(perm):
            for v in course_graph.get(u, []):
                if v in perm[:i]:  # v comes before u
                    valid = False
                    break
            if not valid:
                break
        if valid:
            valid_orders.append(perm)
    
    print(f"Number of valid topological orders: {len(valid_orders)}")
    print("First few orders:")
    for order in valid_orders[:3]:
        print(f"  {order}")

if __name__ == "__main__":
    test_problems()
