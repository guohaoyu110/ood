# create a package manager/ package dependency system 
from collections import defaultdict, deque 
class PackageManager:
    def __init__(self):
        self.result = []
        self.graph = defaultdict(list)
        self.visiting = set() # mark a node as visiting when the node is being visited in the graph path 
        self.visited = set() # mark as visited when a node is dealt with 
    def build_graph(self, dependencies):  # dependencies include the src node and dst node 
        # build graph using the dependencies 
        for src, dst in dependencies:
            self.graph[src].append(dst) 
    def install(self, package):  # this works as the main function 
        # start from package and install recursively to install all the packages that this package is reliant on 
        # run dfs to get the topological sort result 
        if not self.dfs(package):
            return []
        else:
            return self.result[::-1] 
    def dfs(self, package):
        if package in self.visiting: # if yes, means cycle detected 
            return False 
        if package in self.visited: # if yes, means already dealt with this node 
            return True  
        self.visiting.add(package) 
        for neighbor in self.graph[package]:
            if not self.dfs(neighbor):
                return False
        self.visiting.remove(package)
        self.visited.add(package)
        self.result.append(package)  
        return True 
        

# use this as a dfs function to perform topological sort 
def test_package_manager():
    pm = PackageManager()

    # Example 1: Simple dependency graph with no cycles
    dependencies = [
        ("A", "B"),
        ("A", "C"),
        ("B", "D"),
        ("C", "E"),
        ("D", "F")
    ]
    
    pm.build_graph(dependencies)
    try:
        result = pm.install("A")
        print("Installation order:", result)
    except ValueError as e:
        print(e)

    # Example 2: Cyclic dependency graph
    pm = PackageManager()  # Create a new instance to reset everything
    dependencies_with_cycle = [
        ("A", "B"),
        ("B", "C"),
        ("C", "A")
    ]

    pm.build_graph(dependencies_with_cycle)
    try:
        result = pm.install("A")
        print("Installation order:", result)
    except ValueError as e:
        print(e)

# Run the tests
test_package_manager()
