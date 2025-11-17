"""
knowledge_base.py - Logical Inference Engine for Wumpus World
Implements propositional logic reasoning with forward chaining
Author: Mei Hsien Hsu
Course: CS4 - Intro AI
Fall 2025
"""

from typing import Set, List, Tuple

Coord = Tuple[int, int]

class KnowledgeBase:
    """
    Maintains logical knowledge about the world and performs inference.
    Uses propositional logic with Modus Ponens and constraint propagation.
    """
    
    def __init__(self):
        """Initialize empty knowledge base."""
        self.facts: Set[str] = set()
        self.pit_clauses: List[Set[str]] = []
        self.wumpus_clauses: List[Set[str]] = []
        
    def tell(self, fact: str):
        """Add a fact to the knowledge base."""
        self.facts.add(fact)
    
    def ask(self, query: str) -> bool:
        """Query the knowledge base."""
        return query in self.facts
    
    def update_from_percepts(self, position: Coord, neighbors: List[Coord], 
                            percepts: dict):
        """Update KB based on percepts at current position."""
        x, y = position
        
        self.tell(f"Visited({x},{y})")
        self.tell(f"Safe({x},{y})")
        self.tell(f"NotPit({x},{y})")
        self.tell(f"NotWumpus({x},{y})")
        
        if percepts["Breeze"]:
            self.tell(f"Breeze({x},{y})")
            clause = {f"Pit({nx},{ny})" for nx, ny in neighbors}
            self.pit_clauses.append(clause)
        else:
            self.tell(f"NoBreeze({x},{y})")
            for nx, ny in neighbors:
                self.tell(f"NotPit({nx},{ny})")
        
        if percepts["Stench"]:
            self.tell(f"Stench({x},{y})")
            clause = {f"Wumpus({nx},{ny})" for nx, ny in neighbors}
            self.wumpus_clauses.append(clause)
        else:
            self.tell(f"NoStench({x},{y})")
            for nx, ny in neighbors:
                self.tell(f"NotWumpus({nx},{ny})")
        
        if percepts["Glitter"]:
            self.tell(f"Glitter({x},{y})")
            self.tell(f"Gold({x},{y})")
        
        self.propagate()
    
    def propagate(self):
        """Perform forward chaining inference."""
        changed = True
        iterations = 0
        max_iterations = 100
        
        while changed and iterations < max_iterations:
            changed = False
            iterations += 1
            
            for clause in self.pit_clauses[:]:
                original_size = len(clause)
                clause -= {f for f in clause if f"Not{f}" in self.facts}
                
                if len(clause) < original_size:
                    changed = True
                
                if len(clause) == 1:
                    pit_fact = list(clause)[0]
                    if pit_fact not in self.facts:
                        self.tell(pit_fact)
                        changed = True
                
                if len(clause) == 0:
                    self.pit_clauses.remove(clause)
            
            for clause in self.wumpus_clauses[:]:
                original_size = len(clause)
                clause -= {f for f in clause if f"Not{f}" in self.facts}
                
                if len(clause) < original_size:
                    changed = True
                
                if len(clause) == 1:
                    wumpus_fact = list(clause)[0]
                    if wumpus_fact not in self.facts:
                        self.tell(wumpus_fact)
                        changed = True
                
                if len(clause) == 0:
                    self.wumpus_clauses.remove(clause)
            
            for x in range(1, 5):
                for y in range(1, 5):
                    not_pit = f"NotPit({x},{y})" in self.facts
                    not_wumpus = f"NotWumpus({x},{y})" in self.facts
                    safe_fact = f"Safe({x},{y})"
                    
                    if not_pit and not_wumpus and safe_fact not in self.facts:
                        self.tell(safe_fact)
                        changed = True
    
    def get_safe_cells(self) -> Set[Coord]:
        """Return set of all cells known to be safe."""
        safe_cells = set()
        for fact in self.facts:
            if fact.startswith("Safe("):
                coords = fact[5:-1].split(",")
                safe_cells.add((int(coords[0]), int(coords[1])))
        return safe_cells
    
    def get_visited_cells(self) -> Set[Coord]:
        """Return set of all visited cells."""
        visited = set()
        for fact in self.facts:
            if fact.startswith("Visited("):
                coords = fact[8:-1].split(",")
                visited.add((int(coords[0]), int(coords[1])))
        return visited
    
    def display_knowledge(self):
        """Display current knowledge state (for debugging)."""
        print("\n" + "="*40)
        print("KNOWLEDGE BASE STATE")
        print("="*40)
        
        print(f"\n🔹 Known Facts ({len(self.facts)}):")
        for fact in sorted(list(self.facts)[:10]):  # Show first 10
            print(f"  - {fact}")
        if len(self.facts) > 10:
            print(f"  ... and {len(self.facts) - 10} more facts")
        
        print(f"\n🔹 Pit Clauses ({len(self.pit_clauses)}):")
        for i, clause in enumerate(self.pit_clauses[:3], 1):
            print(f"  {i}. {' OR '.join(list(clause)[:3])}")
        
        print(f"\n🔹 Wumpus Clauses ({len(self.wumpus_clauses)}):")
        for i, clause in enumerate(self.wumpus_clauses[:3], 1):
            print(f"  {i}. {' OR '.join(list(clause)[:3])}")
        
        print("\n" + "="*40 + "\n")


if __name__ == "__main__":
    kb = KnowledgeBase()
    print("Testing Knowledge Base...")
    
    kb.update_from_percepts(
        position=(2, 1),
        neighbors=[(1,1), (3,1), (2,2)],
        percepts={"Breeze": True, "Stench": False, "Glitter": False}
    )
    
    print(f"\n✅ After visiting (2,1) with Breeze:")
    kb.display_knowledge()
    
    kb.update_from_percepts(
        position=(1, 1),
        neighbors=[(2,1), (1,2)],
        percepts={"Breeze": False, "Stench": False, "Glitter": False}
    )
    
    print(f"✅ After visiting (1,1) with no percepts:")
    kb.display_knowledge()
    
    print(f"Safe cells known: {kb.get_safe_cells()}")
    print("\nTest complete!")