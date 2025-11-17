"""
search.py - Path planning algorithms for Wumpus World
Implements BFS and optionally DFS/A*
Author: Mei Hsien Hsu
Course: CS4 - Intro AI
Fall 2025
"""

from typing import List, Set, Callable, Optional
from collections import deque

Coord = tuple[int, int]

def bfs_search(start: Coord, 
               goal_test: Callable[[Coord], bool],
               get_neighbors: Callable[[Coord], List[Coord]],
               is_valid: Callable[[Coord], bool]) -> Optional[List[Coord]]:
    """
    Breadth-First Search to find path to any goal cell.
    
    Args:
        start: Starting coordinate
        goal_test: Function that returns True if coord is a goal
        get_neighbors: Function that returns valid neighbors
        is_valid: Function that returns True if cell can be traversed
        
    Returns:
        List of coordinates forming path from start to goal, or None
    """
    if goal_test(start):
        return [start]
    
    frontier = deque([(start, [start])])
    explored = {start}
    
    while frontier:
        current, path = frontier.popleft()
        
        for neighbor in get_neighbors(current):
            if neighbor in explored or not is_valid(neighbor):
                continue
            
            new_path = path + [neighbor]
            
            if goal_test(neighbor):
                return new_path
            
            frontier.append((neighbor, new_path))
            explored.add(neighbor)
    
    return None  # No path found


def dfs_search(start: Coord, 
               goal_test: Callable[[Coord], bool],
               get_neighbors: Callable[[Coord], List[Coord]],
               is_valid: Callable[[Coord], bool],
               max_depth: int = 50) -> Optional[List[Coord]]:
    """
    Depth-First Search (for comparison, not recommended for this problem).
    
    Args:
        start: Starting coordinate
        goal_test: Function that returns True if coord is a goal
        get_neighbors: Function that returns valid neighbors
        is_valid: Function that returns True if cell can be traversed
        max_depth: Maximum search depth
        
    Returns:
        List of coordinates forming path, or None
    """
    stack = [(start, [start], 0)]
    explored = {start}
    
    while stack:
        current, path, depth = stack.pop()
        
        if depth > max_depth:
            continue
        
        if goal_test(current):
            return path
        
        for neighbor in get_neighbors(current):
            if neighbor not in explored and is_valid(neighbor):
                stack.append((neighbor, path + [neighbor], depth + 1))
                explored.add(neighbor)
    
    return None


if __name__ == "__main__":
    print("Testing BFS Search...")
    
    # Simple 4x4 grid test
    def simple_neighbors(coord):
        x, y = coord
        candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        return [c for c in candidates if in_bounds(c)]
    
    def in_bounds(coord):
        x, y = coord
        return 1 <= x <= 4 and 1 <= y <= 4
    
    # Test 1: Find path from (1,1) to (4,4)
    print("\nTest 1: Path from (1,1) to (4,4)")
    path = bfs_search(
        start=(1, 1),
        goal_test=lambda c: c == (4, 4),
        get_neighbors=simple_neighbors,
        is_valid=in_bounds
    )
    print(f"Path found: {path}")
    print(f"Path length: {len(path) if path else 0}")
    
    # Test 2: Find path with obstacle
    print("\nTest 2: Path avoiding (2,2)")
    obstacles = {(2, 2)}
    
    def is_valid_with_obstacles(coord):
        return in_bounds(coord) and coord not in obstacles
    
    path = bfs_search(
        start=(1, 1),
        goal_test=lambda c: c == (3, 3),
        get_neighbors=simple_neighbors,
        is_valid=is_valid_with_obstacles
    )
    print(f"Path found: {path}")
    
    # Test 3: No path exists
    print("\nTest 3: Impossible path (blocked)")
    obstacles = {(2,1), (1,2)}  # Block all exits from (1,1)
    
    path = bfs_search(
        start=(1, 1),
        goal_test=lambda c: c == (4, 4),
        get_neighbors=simple_neighbors,
        is_valid=is_valid_with_obstacles
    )
    print(f"Path found: {path}")
    
    print("\n✅ All tests complete!")