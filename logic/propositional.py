"""
Propositional Logic Knowledge Base for Wumpus World
命題邏輯知識庫

Integrates concepts from Lab 8:
- Truth tables and logical operations
- CNF conversion
- Propositional inference rules
- Knowledge representation

Author: Mei Hsien Hsu
Course: CS4 Introduction to AI
"""

from typing import Dict, List, Set, Tuple, Optional


class PropositionalKB:
    """
    Propositional Logic Knowledge Base
    命題邏輯知識庫
    
    Stores facts and rules in propositional logic form.
    Supports queries and basic inference.
    """
    
    def __init__(self):
        """Initialize empty knowledge base"""
        self.facts: Dict[str, bool] = {}  # Known facts: fact_name -> True/False
        self.clauses: Set[str] = set()    # CNF clauses for inference
        self.rules: List[Tuple[List[str], str]] = []  # (antecedent, consequent)
        
        print("📚 Propositional KB initialized")
    
    def tell(self, fact: str, value: bool = True):
        """
        Add a fact to the knowledge base
        向知識庫添加事實
        
        Args:
            fact: Fact name (e.g., "Safe(1,1)")
            value: Truth value (True/False)
        """
        self.facts[fact] = value
        
    def tell_clause(self, clause: str):
        """
        Add a CNF clause to the knowledge base
        添加 CNF 子句
        
        Args:
            clause: CNF clause string (e.g., "¬P ∨ Q")
        """
        self.clauses.add(clause)
    
    def add_rule(self, antecedent: List[str], consequent: str):
        """
        Add an inference rule: antecedent → consequent
        添加推理規則
        
        Args:
            antecedent: List of preconditions
            consequent: Conclusion
        """
        self.rules.append((antecedent, consequent))
    
    def ask(self, query: str) -> Optional[bool]:
        """
        Query the knowledge base
        查詢知識庫
        
        Args:
            query: Fact to query
            
        Returns:
            True/False if known, None if unknown
        """
        return self.facts.get(query)
    
    def forward_chain(self) -> bool:
        """
        Apply forward chaining inference
        前向鏈接推理
        
        Returns:
            True if new facts were derived
        """
        derived_new = False
        
        for antecedent, consequent in self.rules:
            # Check if all antecedents are true
            if all(self.ask(ante) is True for ante in antecedent):
                # Check if consequent is not already known
                if self.ask(consequent) is None:
                    self.tell(consequent, True)
                    derived_new = True
                    print(f"   ⚡ Derived: {consequent}")
        
        return derived_new
    
    def add_wumpus_rules(self, position: Tuple[int, int], 
                        percept, 
                        adjacent: List[Tuple[int, int]]):
        """
        Add Wumpus World specific propositional logic rules
        添加 Wumpus World 特定的命題邏輯規則
        
        Rules implemented:
        1. ¬Breeze(x,y) ⇒ ¬Pit(adjacent cells)
        2. ¬Stench(x,y) ⇒ ¬Wumpus(adjacent cells)
        3. Breeze(x,y) ⇒ Pit(at least one adjacent)
        4. Stench(x,y) ⇒ Wumpus(at least one adjacent)
        
        Args:
            position: Current position (x, y)
            percept: Percept object with breeze, stench, etc.
            adjacent: List of adjacent cell positions
        """
        x, y = position
        
        # Current cell is safe (we're standing on it)
        self.tell(f"Safe({x},{y})", True)
        self.tell(f"Visited({x},{y})", True)
        
        # Rule 1 & 2: No percept → No danger nearby
        if not percept.breeze:
            # No breeze → No pits in adjacent cells
            for ax, ay in adjacent:
                self.tell(f"¬Pit({ax},{ay})", True)
                self.tell(f"Safe({ax},{ay})", True)
                
                # Add rule for inference
                self.add_rule(
                    [f"¬Breeze({x},{y})"],
                    f"¬Pit({ax},{ay})"
                )
        
        if not percept.stench:
            # No stench → No Wumpus in adjacent cells
            for ax, ay in adjacent:
                self.tell(f"¬Wumpus({ax},{ay})", True)
                self.tell(f"Safe({ax},{ay})", True)
                
                # Add rule for inference
                self.add_rule(
                    [f"¬Stench({x},{y})"],
                    f"¬Wumpus({ax},{ay})"
                )
        
        # Rule 3: Breeze detected
        if percept.breeze:
            self.tell(f"Breeze({x},{y})", True)
            # At least one adjacent cell has a pit
            pit_disjunction = " ∨ ".join([f"Pit({ax},{ay})" for ax, ay in adjacent])
            self.tell_clause(f"Breeze({x},{y}) ⇒ ({pit_disjunction})")
        else:
            self.tell(f"¬Breeze({x},{y})", True)
        
        # Rule 4: Stench detected
        if percept.stench:
            self.tell(f"Stench({x},{y})", True)
            # At least one adjacent cell has Wumpus
            wumpus_disjunction = " ∨ ".join([f"Wumpus({ax},{ay})" for ax, ay in adjacent])
            self.tell_clause(f"Stench({x},{y}) ⇒ ({wumpus_disjunction})")
        else:
            self.tell(f"¬Stench({x},{y})", True)
    
    def prove_safe(self, position: Tuple[int, int]) -> bool:
        """
        Prove that a position is safe using propositional inference
        使用命題推理證明位置安全
        
        Args:
            position: Position to check (x, y)
            
        Returns:
            True if proven safe, False otherwise
        """
        x, y = position
        
        # Direct check
        if self.ask(f"Safe({x},{y})") is True:
            return True
        
        # Check if we know there's no pit and no Wumpus
        no_pit = self.ask(f"¬Pit({x},{y})")
        no_wumpus = self.ask(f"¬Wumpus({x},{y})")
        
        if no_pit is True and no_wumpus is True:
            # Can infer safety
            self.tell(f"Safe({x},{y})", True)
            return True
        
        return False
    
    def display(self):
        """Display knowledge base contents"""
        print("\n" + "="*60)
        print("📚 Propositional Knowledge Base")
        print("="*60)
        
        print(f"\n✓ Known Facts ({len(self.facts)}):")
        for fact, value in sorted(self.facts.items()):
            if value:
                print(f"   {fact}")
        
        if self.clauses:
            print(f"\n📋 CNF Clauses ({len(self.clauses)}):")
            for clause in list(self.clauses)[:5]:  # Show first 5
                print(f"   {clause}")
            if len(self.clauses) > 5:
                print(f"   ... and {len(self.clauses)-5} more")
        
        if self.rules:
            print(f"\n⚡ Inference Rules ({len(self.rules)}):")
            for ante, cons in self.rules[:5]:  # Show first 5
                print(f"   {' ∧ '.join(ante)} → {cons}")
            if len(self.rules) > 5:
                print(f"   ... and {len(self.rules)-5} more")
    
    def get_safe_cells(self) -> Set[Tuple[int, int]]:
        """
        Get all cells proven to be safe
        獲取所有已證明安全的方格
        
        Returns:
            Set of (x, y) positions
        """
        safe_cells = set()
        
        for fact, value in self.facts.items():
            if value and fact.startswith("Safe(") and fact.endswith(")"):
                # Parse "Safe(x,y)" to get (x, y)
                try:
                    coords = fact[5:-1].split(",")
                    x, y = int(coords[0]), int(coords[1])
                    safe_cells.add((x, y))
                except:
                    continue
        
        return safe_cells


# Example usage and testing
if __name__ == "__main__":
    print("Testing Propositional Logic KB...")
    
    # Create KB
    kb = PropositionalKB()
    
    # Test basic operations
    kb.tell("Safe(0,0)", True)
    kb.tell("¬Pit(0,1)", True)
    kb.tell("¬Wumpus(1,0)", True)
    
    print(f"\nQuery Safe(0,0): {kb.ask('Safe(0,0)')}")
    print(f"Query ¬Pit(0,1): {kb.ask('¬Pit(0,1)')}")
    
    # Test rules
    kb.add_rule(["¬Pit(0,1)", "¬Wumpus(0,1)"], "Safe(0,1)")
    kb.tell("¬Wumpus(0,1)", True)
    
    print("\nApplying forward chaining...")
    kb.forward_chain()
    
    print(f"\nQuery Safe(0,1): {kb.ask('Safe(0,1)')}")
    
    kb.display()
    
    print("\n✅ Propositional Logic module test complete!")