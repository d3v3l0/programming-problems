"""
Statement

Given the head of a graph, return a deep copy (clone) of the graph.
Each node in the graph contains a label (int) and a list (List[UndirectedGraphNode])
of its neighbors. There is an edge between the given node and each of the nodes in its neighbors.

Input: graph node
Output: graph node in an identical but deep-copied graph
-----------------
Understand / Plan

- For this problem, we must copy an undirected graph
- In order to do this, we must visit each node in the graph at least once
- Cycles may occur
- Since each node has a list of references to other nodes in the graph,
those nodes must exist for us to add them to the list, so it seems like
the most straightforward thing to do is create all of the nodes and then fixup
the references
- we can do this in two passes:
  - dfs the original graph
  - during dfs, create every node for the new graph, but store  array as a list of labels (not nodes)
    - as we create each node, keep it in a dictionary mapping labels to nodes
  - once dfs is complete, go through keys of dictionary and swap labels for nodes
  - this will be O(n) for time (although it will take two passes through the graph) and O(n) for space

-----------------
Execute

See code below
-----------------
Review

Looked at the following discussion posts:
-
"""
import collections


class UndirectedGraphNode:
    def __init__(self, x):
        self.label = x
        self.neighbors = []


def deserialize_graph(serialized_str):
    """
    Convert a graph string in the given format to
    an in-memory representation
    """
    serialized_str = serialized_str.strip('{').strip('}')
    serialized_nodes = serialized_str.split('#')
    nodes = {}

    # Create nodes in dictionary
    for serialized_node in serialized_nodes:
        node_ids = serialized_node.split(',')
        print("Evaluated node " + node_ids[0])
        node = UndirectedGraphNode(node_ids[0])
        node.neighbors = node_ids[1:]
        print(node_ids, node.neighbors)
        nodes[node_ids[0]] = node

    # Fix up labels
    for node_id in nodes.keys():
        node = nodes[node_id]
        neighbors = []
        for label in node.neighbors:
            neighbors.append(nodes[label])
        node.neighbors = neighbors

    # Return a single node
    return nodes[list(nodes.keys())[0]]


def serialize_graph(node):
    """
    Convert an in-memory graph to a serialized
    string representation by BFSing entire graph
    """
    visited = []
    nodestrings = []
    q = collections.deque([node])
    while q:
        current = q.popleft()
        if current in visited:
            continue
        else:
            visited.append(current)

        nodestring = str(current.label)
        for neighbor in current.neighbors:
            nodestring += "," + str(neighbor.label)
            q.append(neighbor)
        nodestrings.append(nodestring)

    return '{' + ("#".join(nodestrings)) + '}'


class Solution:
    # @param node, a undirected graph node
    # @return a undirected graph node
    def cloneGraph(self, node):
        """
        Clone graph via BFS and fixup
        """
        if node == None:
            return

        # BFS to produce dict of new nodes
        visited = []
        new_graph = {}
        q = collections.deque([node])
        while q:
            current = q.popleft()
            if current in visited:
                continue
            else:
                visited.append(current)
                for neighbor in current.neighbors:
                    q.append(neighbor)

            new_graph[current.label] = UndirectedGraphNode(current.label)
            new_graph[current.label].neighbors = [
                neighbor.label for neighbor in current.neighbors]

        # Fix up neighbors
        for node_id in new_graph.keys():
            current = new_graph[node_id]
            actual_neighbors = []
            for neighbor_id in current.neighbors:
                actual_neighbors.append(new_graph[neighbor_id])
            current.neighbors = actual_neighbors

        # Return the copy of the original node
        return new_graph[node.label]


if __name__ == '__main__':
    s = Solution()
    # expected = "{0,1,2#1,2#2,2}"
    expected = '{-1,1#1}'
    actual = serialize_graph(deserialize_graph(expected))
    print(actual)
    assert actual == expected

    graph1 = deserialize_graph(expected)
    graph2 = s.cloneGraph(graph1)
    s_graph2 = serialize_graph(graph2)
    print(s_graph2)
    assert s_graph2 == expected
