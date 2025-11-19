"""
agent.py - Knowledge-Based Agent for Wumpus World
Author: Mei Hsien Hsu
Course: CS4 - Introduction to AI 
Fall 2025  
"""

from typing import Set, List, Optional
from world import World, Coord
from knowledge_base import KnowledgeBase
from search import bfs_search

class Agent:
    """
    Knowledge-Based Agent that explores Wumpus World safely.
    Uses logical inference to determine safe moves and search for planning.
    """
    
    def __init__(self, world: World):
        """
        Initialize agent with world reference.
        
        Args:
            world: The Wumpus World environment
        """
        self.world = world
        self.kb = KnowledgeBase()
        self.visited: Set[Coord] = set()
        self.returning = False  # Flag for return-to-start mode
        self.plan: List[Coord] = []  # Current path plan
        
    def step(self) -> str:
        """
        Execute one decision-making step.
        
        Returns:
            String description of action taken
        """
        # Get current state
        pos = self.world.agent_pos
        percepts = self.world.percepts_at(pos)
        neighbors = self.world.neighbors(pos)
        
        # Update knowledge base
        self.kb.update_from_percepts(pos, neighbors, percepts)
        self.visited.add(pos)
        
        # === DECISION LOGIC ===
        
        # 1. Found gold? Grab it!
        if percepts["Glitter"]:
            self.world.grab()
            self.returning = True
            return f"💰 GRAB gold at {pos}!"
        
        # 2. Have gold and back at start? Climb out!
        if self.returning and pos == (1, 1):
            self.world.climb()
            return f"🏆 CLIMB out - MISSION SUCCESS!"
        
        # 3. If returning, follow path back to (1,1)
        if self.returning:
            return self._return_home()
        
        # 4. Look for safe unvisited neighbors
        safe_unvisited = self._get_safe_unvisited_neighbors()
        
        if safe_unvisited:
            next_cell = safe_unvisited[0]
            self._move_to(next_cell)
            return f"➡️  Move to {next_cell} (safe neighbor)"
        
        # 5. No direct safe neighbor - use search to find path
        path = self._find_path_to_unvisited_safe()
        
        if path and len(path) > 1:
            next_cell = path[1]  # path[0] is current position
            self._move_to(next_cell)
            return f"🔍 Follow path to {next_cell}"
        
        # 6. Explored everything reachable - return home
        if not self.returning:
            self.returning = True
            return "🔄 All safe cells explored - returning home"
        
        # 7. No moves available
        return "⚠️  STUCK - No safe moves available"
    
    def _get_safe_unvisited_neighbors(self) -> List[Coord]:
        """Get neighboring cells that are safe and unvisited."""
        neighbors = self.world.neighbors(self.world.agent_pos)
        safe_unvisited = []
        
        for neighbor in neighbors:
            x, y = neighbor
            is_safe = self.kb.ask(f"Safe({x},{y})")
            is_unvisited = neighbor not in self.visited
            
            if is_safe and is_unvisited:
                safe_unvisited.append(neighbor)
        
        return safe_unvisited
    
    def _find_path_to_unvisited_safe(self) -> Optional[List[Coord]]:
        """
        Use BFS to find path to any unvisited safe cell.
        
        Returns:
            List of coordinates forming the path, or None
        """
        def is_goal(coord: Coord) -> bool:
            x, y = coord
            return (self.kb.ask(f"Safe({x},{y})") and 
                    coord not in self.visited)
        
        def is_traversable(coord: Coord) -> bool:
            x, y = coord
            return self.kb.ask(f"Safe({x},{y})")
        
        path = bfs_search(
            start=self.world.agent_pos,
            goal_test=is_goal,
            get_neighbors=self.world.neighbors,
            is_valid=is_traversable
        )
        
        return path
    
    def _return_home(self) -> str:
        """Navigate back to (1,1) using BFS."""
        if self.world.agent_pos == (1, 1):
            return "🏠 Already at home position"
        
        def is_goal(coord: Coord) -> bool:
            return coord == (1, 1)
        
        def is_traversable(coord: Coord) -> bool:
            x, y = coord
            # Can traverse visited cells (known to be safe)
            return coord in self.visited or self.kb.ask(f"Safe({x},{y})")
        
        path = bfs_search(
            start=self.world.agent_pos,
            goal_test=is_goal,
            get_neighbors=self.world.neighbors,
            is_valid=is_traversable
        )
        
        if path and len(path) > 1:
            next_cell = path[1]
            self._move_to(next_cell)
            return f"🏠 Returning home via {next_cell}"
        
        return "⚠️  Cannot find path home!"
    
    def _move_to(self, target: Coord):
        """
        Move agent to target cell (assumes adjacent).
        Handles direction turning and forward movement.
        
        Args:
            target: Adjacent coordinate to move to
        """
        current = self.world.agent_pos
        
        # Calculate direction needed
        dx = target[0] - current[0]
        dy = target[1] - current[1]
        
        # Map direction to index: E=0, N=1, W=2, S=3
        target_dir = None
        if dx == 1 and dy == 0:
            target_dir = 0  # East
        elif dx == 0 and dy == 1:
            target_dir = 1  # North
        elif dx == -1 and dy == 0:
            target_dir = 2  # West
        elif dx == 0 and dy == -1:
            target_dir = 3  # South
        
        if target_dir is not None:
            # Turn to face target direction
            while self.world.agent_dir_idx != target_dir:
                self.world.turn_right()
            
            # Move forward
            self.world.forward()
    
    def get_stats(self) -> dict:
        """Return agent statistics."""
        return {
            "visited_count": len(self.visited),
            "kb_facts": len(self.kb.facts),
            "returning": self.returning,
            "safe_cells_known": len(self.kb.get_safe_cells())
        }


if __name__ == "__main__":
    # Test agent behavior
    print("Testing Agent class...")
    
    world = World()
    agent = Agent(world)
    
    print(f"Initial state: {world.get_state()}")
    print(f"\nAgent stats: {agent.get_stats()}")
    
    # Run a few steps
    for i in range(8):
        print(f"\n{'='*50}")
        print(f"STEP {i+1}")
        print(f"{'='*50}")
        
        action = agent.step()
        print(f"🎯 Action: {action}")
        print(f"📍 Position: {world.agent_pos}")
        print(f"📊 Stats: {agent.get_stats()}")
        
        if not world.alive:
            print("\n💀 Agent died!")
            break
        if world.out:
            print("\n🏆 Agent escaped!")
            break
    
    print("\n✅ Test complete!")