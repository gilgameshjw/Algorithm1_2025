# exo_6_solutions.py

class WeightedTreeNode:
    """
    Problem 1: Weighted Tree Class
    Each child has weight 1/n of parent's weight
    """
    def __init__(self, weight=1.0, children=None):
        self.weight = weight
        self.children = children if children is not None else []
    
    def add_child(self, child):
        self.children.append(child)

def generate_tree(N=3, n=2):
    """
    Generate a tree of depth N where each node has n children
    Children weights are 1/n of parent's weight
    """
    def build_tree(depth, current_weight):
        if depth == 0:
            return None
        
        node = WeightedTreeNode(weight=current_weight)
        if depth > 1:
            child_weight = current_weight / n
            for _ in range(n):
                child = build_tree(depth - 1, child_weight)
                if child:
                    node.add_child(child)
        return node
    
    return build_tree(N, 1.0)

def dfs_sum(node, flip=False):
    """
    Depth-first search summing weights
    """
    if not node:
        return 0
    
    weight = -node.weight if flip else node.weight
    total = weight
    
    for child in node.children:
        total += dfs_sum(child, flip)
    
    return total

def bfs_sum(root, flip=False):
    """
    Breadth-first search summing weights
    """
    if not root:
        return 0
    
    from collections import deque
    
    total = 0
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        total += -node.weight if flip else node.weight
        
        for child in node.children:
            queue.append(child)
    
    return total

def bfs_recursive(nodes, flip=False, total=0):
    """
    Recursive BFS implementation (not recommended)
    """
    if not nodes:
        return total
    
    next_level = []
    for node in nodes:
        total += -node.weight if flip else node.weight
        next_level.extend(node.children)
    
    return bfs_recursive(next_level, flip, total)

def test_tree_operations():
    """Test all tree operations"""
    print("Testing Tree Operations:")
    print("=" * 50)
    
    # Test with different n values
    for n in [2, 3, 4]:
        print(f"\nn = {n}:")
        tree = generate_tree(N=3, n=n)
        
        # DFS sum
        dfs_result = dfs_sum(tree)
        print(f"DFS Sum: {dfs_result} (Expected: 1.0)")
        
        # BFS sum
        bfs_result = bfs_sum(tree)
        print(f"BFS Sum: {bfs_result} (Expected: 1.0)")
        
        # DFS with flip
        dfs_flip = dfs_sum(tree, flip=True)
        print(f"DFS with flip: {dfs_flip} (Expected: 1.0 or -1.0 depending on depth)")
        
        # BFS with flip
        bfs_flip = bfs_sum(tree, flip=True)
        print(f"BFS with flip: {bfs_flip}")
        
        # Recursive BFS
        bfs_rec_result = bfs_recursive([tree])
        print(f"Recursive BFS Sum: {bfs_rec_result}")

def why_not_recursive_bfs():
    """
    Problem 1.7: Why BFS is not recommended to implement recursively
    """
    explanation = """
    Why BFS is not recommended to implement recursively:
    
    1. Memory Usage: Recursive BFS requires storing all nodes at each level,
       which can lead to excessive memory usage for wide trees.
       
    2. Stack Overflow: Deep recursion can cause stack overflow errors.
       BFS naturally works level by level, which doesn't map well to recursion.
       
    3. Inefficiency: Recursive BFS requires passing the entire frontier
       as a parameter, leading to unnecessary copying and overhead.
       
    4. Natural Iterative Solution: BFS is naturally iterative using a queue.
       Forcing it into recursion adds complexity without benefits.
       
    5. Tail Recursion: Most languages don't optimize tail recursion for BFS
       since it's not a simple tail-recursive pattern.
       
    Iterative BFS with a queue is simpler, more efficient, and easier to understand.
    """
    return explanation

if __name__ == "__main__":
    test_tree_operations()
    print("\n" + "=" * 50)
    print(why_not_recursive_bfs())
