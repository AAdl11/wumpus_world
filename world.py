"""
world.py - Wumpus World Environment Simulation
Author: Mei Hsien Hsu
Course: CS4 - Intro AI
Fall 2025  
"""

from typing import Tuple, Set, Dict, List

Coord = Tuple[int, int]
DIRS = [(1,0), (0,1), (-1,0), (0,-1)]  # E, N, W, S

class World:
    """
    Represents the 4x4 Wumpus World grid environment.
    Tracks hazards (pits, wumpus), gold location, and agent state.
    """
    
    def __init__(self, size: Tuple[int,int] = (4,4), 
                 pits: Set[Coord] = None, 
                 wumpus: Coord = None, 
                 gold: Coord = None):
        """
        Initialize the Wumpus World.
        
        Args:
            size: Grid dimensions (width, height)
            pits: Set of coordinates containing pits
            wumpus: Coordinate of the wumpus
            gold: Coordinate of the gold
        """
        self.width, self.height = size
        
        # Default configuration (Russell & Norvig textbook example)
        self.pits = pits if pits else {(3,1), (3,3), (4,4)}
        self.wumpus = wumpus if wumpus else (1,3)
        self.gold = gold if gold else (2,3)
        
        # Agent state
        self.agent_pos: Coord = (1,1)
        self.agent_dir_idx: int = 0  # 0=E, 1=N, 2=W, 3=S
        self.alive = True
        self.has_gold = False
        self.out = False
        
    def in_bounds(self, coord: Coord) -> bool:
        """Check if coordinate is within grid boundaries."""
        x, y = coord
        return 1 <= x <= self.width and 1 <= y <= self.height
    
    def neighbors(self, coord: Coord) -> List[Coord]:
        """
        Get valid neighboring coordinates.
        
        Args:
            coord: The coordinate to find neighbors for
            
        Returns:
            List of valid neighbor coordinates
        """
        x, y = coord
        candidates = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        return [c for c in candidates if self.in_bounds(c)]
    
    def percepts_at(self, coord: Coord) -> Dict[str, bool]:
        """
        Generate percepts for a given coordinate.
        
        Percepts:
            - Breeze: Adjacent to a pit
            - Stench: Adjacent to the wumpus
            - Glitter: Same cell as gold (if not yet grabbed)
            
        Args:
            coord: The coordinate to sense
            
        Returns:
            Dictionary of percepts
        """
        neighbors = self.neighbors(coord)
        
        breeze = any(n in self.pits for n in neighbors)
        stench = any(n == self.wumpus for n in neighbors)
        glitter = (coord == self.gold and not self.has_gold)
        
        return {
            "Breeze": breeze,
            "Stench": stench,
            "Glitter": glitter
        }
    
    def forward(self):
        """Move agent forward one step in current direction."""
        dx, dy = DIRS[self.agent_dir_idx]
        new_x = self.agent_pos[0] + dx
        new_y = self.agent_pos[1] + dy
        new_pos = (new_x, new_y)
        
        if self.in_bounds(new_pos):
            self.agent_pos = new_pos
            # Check for death
            if new_pos in self.pits or new_pos == self.wumpus:
                self.alive = False
    
    def turn_left(self):
        """Rotate agent 90 degrees counter-clockwise."""
        self.agent_dir_idx = (self.agent_dir_idx + 1) % 4
    
    def turn_right(self):
        """Rotate agent 90 degrees clockwise."""
        self.agent_dir_idx = (self.agent_dir_idx - 1) % 4
    
    def grab(self):
        """Grab gold if in same cell."""
        if self.agent_pos == self.gold and not self.has_gold:
            self.has_gold = True
    
    def climb(self):
        """Climb out of cave if at (1,1)."""
        if self.agent_pos == (1,1):
            self.out = True
    
    def get_state(self) -> Dict:
        """Return current world state."""
        return {
            "position": self.agent_pos,
            "direction": ["East", "North", "West", "South"][self.agent_dir_idx],
            "alive": self.alive,
            "has_gold": self.has_gold,
            "escaped": self.out
        }
    
    def display_grid(self, visited: Set[Coord] = None, safe: Set[Coord] = None):
        """
        Display the current grid state with clear formatting.
        
        Args:
            visited: Set of visited coordinates
            safe: Set of known safe coordinates
        """
        visited = visited or set()
        safe = safe or set()
        
        print("\n" + "="*50)
        print("           WUMPUS WORLD GRID")
        print("="*50)
        
        # Print grid from top to bottom (y=4 down to y=1)
        for y in range(self.height, 0, -1):
            # Start row
            row = f"y={y} |"
            
            # Add each cell
            for x in range(1, self.width + 1):
                cell_content = " . "
                
                # Priority order: Agent > Hazards > Gold > Visited > Safe
                if (x, y) == self.agent_pos:
                    cell_content = " A "
                elif (x, y) in self.pits:
                    cell_content = " P "
                elif (x, y) == self.wumpus:
                    cell_content = " W "
                elif (x, y) == self.gold and not self.has_gold:
                    cell_content = " G "
                elif (x, y) in visited:
                    cell_content = " ✓ "
                elif (x, y) in safe:
                    cell_content = " ? "
                
                row += cell_content + "|"
            
            print(row)
        
        # Print bottom border and x-axis
        print("    +" + "---+"*self.width)
        print("      " + "   ".join([f"x={i}" for i in range(1, self.width+1)]))
        
        # Legend
        print("\n🔹 Legend:")
        print("   A=Agent  P=Pit  W=Wumpus  G=Gold  ✓=Visited  ?=Safe")
        
        # Agent status
        state = self.get_state()
        print(f"\n🤖 Agent Status:")
        print(f"   Position: {state['position']}")
        print(f"   Direction: {state['direction']}")
        print(f"   Alive: {state['alive']}")
        print(f"   Has Gold: {state['has_gold']}")
        print(f"   Escaped: {state['escaped']}")
        
        print("="*50 + "\n")


if __name__ == "__main__":
    # Test the World class
    world = World()
    
    print("Testing World class...")
    print(f"Initial state: {world.get_state()}")
    
    print(f"\nPercepts at (1,1): {world.percepts_at((1,1))}")
    print(f"Percepts at (2,1): {world.percepts_at((2,1))}")
    print(f"Percepts at (1,2): {world.percepts_at((1,2))}")
    
    world.display_grid()
    
    print("\nMoving forward...")
    world.forward()
    print(f"New position: {world.agent_pos}")
    
    print("\nTest complete!")