#!/usr/bin/env python3
"""
Check for loops (cycles) in a vis-network learning graph JSON file.

This script reads a learning graph in vis-network JSON format and detects
any cycles in the directed graph. If cycles are found, it reports the
nodes involved in each cycle.

Usage:
    python check-loops.py <path-to-learning-graph.json>
"""

import json
import sys
from collections import defaultdict


def load_graph(filepath):
    """Load a vis-network JSON file and return nodes and edges."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    nodes = {node['id']: node.get('label', str(node['id'])) for node in data.get('nodes', [])}
    edges = data.get('edges', [])

    return nodes, edges


def build_adjacency_list(edges):
    """Build an adjacency list from edges."""
    adj = defaultdict(list)
    for edge in edges:
        from_node = edge['from']
        to_node = edge['to']
        adj[from_node].append(to_node)
    return adj


def find_cycles(nodes, adj):
    """
    Find all cycles in a directed graph using DFS.

    Returns a list of cycles, where each cycle is a list of node IDs.
    """
    WHITE = 0  # Not visited
    GRAY = 1   # Currently in recursion stack
    BLACK = 2  # Completely processed

    color = {node_id: WHITE for node_id in nodes}
    parent = {node_id: None for node_id in nodes}
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)

        for neighbor in adj.get(node, []):
            if neighbor not in color:
                # Node exists in edges but not in nodes list
                continue

            if color[neighbor] == GRAY:
                # Found a cycle - extract the cycle from path
                cycle_start_idx = path.index(neighbor)
                cycle = path[cycle_start_idx:]
                cycles.append(cycle)
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)

        path.pop()
        color[node] = BLACK

    for node_id in nodes:
        if color[node_id] == WHITE:
            dfs(node_id, [])

    return cycles


def main():
    if len(sys.argv) < 2:
        print("Usage: python check-loops.py <path-to-learning-graph.json>")
        sys.exit(1)

    filepath = sys.argv[1]

    try:
        nodes, edges = load_graph(filepath)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}")
        sys.exit(1)

    if not nodes:
        print("Warning: No nodes found in the graph.")
        sys.exit(0)

    adj = build_adjacency_list(edges)
    cycles = find_cycles(nodes, adj)

    if not cycles:
        print(f'No Loops Found in file {filepath}.')
    else:
        print(f"Found {len(cycles)} loop(s) in the graph:\n")
        for i, cycle in enumerate(cycles, 1):
            print(f"Loop {i}:")
            cycle_labels = [f"  {node_id}: {nodes.get(node_id, 'Unknown')}" for node_id in cycle]
            print("\n".join(cycle_labels))
            # Show the cycle path
            path_labels = [nodes.get(node_id, str(node_id)) for node_id in cycle]
            path_labels.append(path_labels[0])  # Close the loop for display
            print(f"  Path: {' -> '.join(path_labels)}")
            print()
        sys.exit(1)


if __name__ == "__main__":
    main()
