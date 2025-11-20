"""
Resolution Inference Engine for Wumpus World

Integrates concepts from Lab 9:
- First-order logic representation
- Resolution-based theorem proving
- Similar to Colonel West example
- Proof by contradiction

Author: Mei Hsien Hsu
Course: CS4 Introduction to AI
"""

from typing import List, Set, Tuple, Optional
from logic.propositional import PropositionalKB


class Clause:
    """
    Represents a clause in CNF (Conjunctive Normal Form)
    表示 CNF 形式的子句
    
    A clause is a disjunction of literals: L1 ∨ L2 ∨ ... ∨ Ln
    """
    
    def __init__(self, literals: Set[str]):
        """
        Initialize a clause
        
        Args:
            literals: Set of literal strings (e.g., {"P", "¬Q", "R"})
        """
        self.literals = literals
    
    def __repr__(self):
        if not self.literals:
            return "⊥"  # Empty clause (contradiction)
        return " ∨ ".join(sorted(self.literals))
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))
    
    def is_empty(self) -> bool:
        """Check if this is the empty clause (contradiction)"""
        return len(self.literals) == 0
    
    def contains_complementary(self) -> bool:
        """Check if clause contains both P and ¬P"""
        for lit in self.literals:
            complement = self._complement(lit)
            if complement in self.literals:
                return True
        return False
    
    @staticmethod
    def _complement(literal: str) -> str:
        """Get the complement of a literal"""
        if literal.startswith('¬'):
            return literal[1:]
        else:
            return '¬' + literal


class ResolutionEngine:
    """
    Resolution Inference Engine
    
    Implements resolution-based theorem proving, similar to
    the Colonel West example from Lab 9.
    """
    
    def __init__(self, kb: PropositionalKB = None):
        """
        Initialize resolution engine
        
        Args:
            kb: Optional PropositionalKB to use as base knowledge
        """
        self.kb = kb
        self.clauses: Set[Clause] = set()
        
        # Convert KB facts to clauses if provided
        if kb:
            self._convert_kb_to_clauses()
        
        print("🔍 Resolution Engine initialized")
    
    def _convert_kb_to_clauses(self):
        """
        Convert PropositionalKB facts to CNF clauses
        """
        for fact, value in self.kb.facts.items():
            if value:
                # Positive fact
                self.clauses.add(Clause({fact}))
            else:
                # Negative fact
                self.clauses.add(Clause({f"¬{fact}"}))
    
    def add_clause(self, literals: Set[str]):
        """Add a clause to the knowledge base"""
        clause = Clause(literals)
        if not clause.contains_complementary():
            self.clauses.add(clause)
    
    def resolve(self, c1: Clause, c2: Clause) -> Optional[Clause]:
        """
        Resolve two clauses
        
        Resolution rule:
        If C1 contains literal L and C2 contains ¬L,
        then we can derive C1-{L} ∪ C2-{¬L}
        
        Args:
            c1: First clause
            c2: Second clause
            
        Returns:
            Resolvent clause, or None if no resolution possible
        """
        # Find complementary literals
        for lit1 in c1.literals:
            complement = Clause._complement(lit1)
            
            if complement in c2.literals:
                # Can resolve on this literal
                new_literals = (c1.literals - {lit1}) | (c2.literals - {complement})
                
                # Check for tautology (contains both P and ¬P)
                resolvent = Clause(new_literals)
                if resolvent.contains_complementary():
                    return None
                
                return resolvent
        
        return None
    
    def prove_by_resolution(self, goal: str, max_iterations: int = 1000) -> bool:
        """
        Prove a goal using resolution (proof by contradiction)
        
        Similar to Lab 9 Colonel West example:
        1. Add negation of goal to KB
        2. Apply resolution repeatedly
        3. If we derive empty clause (⊥), goal is proven
        
        Args:
            goal: Goal to prove (e.g., "Safe(1,1)")
            max_iterations: Maximum resolution steps
            
        Returns:
            True if proven, False otherwise
        """
        print(f"\n🔍 Proving: {goal}")
        print("="*60)
        
        # Step 1: Add negation of goal
        negated_goal = Clause._complement(goal)
        working_clauses = self.clauses.copy()
        working_clauses.add(Clause({negated_goal}))
        
        print(f"Step 1: Add ¬{goal} to KB")
        print(f"Total clauses: {len(working_clauses)}")
        
        # Step 2: Apply resolution
        iteration = 0
        new_clauses = set()
        
        while iteration < max_iterations:
            iteration += 1
            
            # Try to resolve all pairs of clauses
            clause_list = list(working_clauses)
            n = len(clause_list)
            
            for i in range(n):
                for j in range(i + 1, n):
                    resolvent = self.resolve(clause_list[i], clause_list[j])
                    
                    if resolvent is not None:
                        # Check for empty clause (contradiction found!)
                        if resolvent.is_empty():
                            print(f"\n✅ Proof found in {iteration} iterations!")
                            print(f"Resolved {clause_list[i]} and {clause_list[j]}")
                            print(f"Derived: ⊥ (empty clause)")
                            print(f"∴ {goal} is PROVEN")
                            return True
                        
                        # Add new resolvent
                        if resolvent not in working_clauses:
                            new_clauses.add(resolvent)
            
            # No new clauses generated
            if not new_clauses:
                print(f"\n❌ Cannot prove {goal}")
                print(f"No new clauses after {iteration} iterations")
                return False
            
            # Add new clauses and continue
            working_clauses.update(new_clauses)
            new_clauses.clear()
            
            if iteration % 100 == 0:
                print(f"Iteration {iteration}: {len(working_clauses)} clauses")
        
        print(f"\n⚠️  Max iterations ({max_iterations}) reached")
        return False
    
    def prove_safe(self, position: Tuple[int, int]) -> bool:
        """
        Prove that a position is safe using resolution
        
        Safe(x,y) is true if:
        - We can prove ¬Pit(x,y) AND ¬Wumpus(x,y)
        
        Args:
            position: Position to check (x, y)
            
        Returns:
            True if proven safe
        """
        x, y = position
        
        # Try to prove no pit
        no_pit = self.prove_by_resolution(f"¬Pit({x},{y})")
        
        # Try to prove no Wumpus
        no_wumpus = self.prove_by_resolution(f"¬Wumpus({x},{y})")
        
        # Safe if both proven
        if no_pit and no_wumpus:
            print(f"\n✅ Position ({x},{y}) is SAFE")
            return True
        
        return False
    
    def display_clauses(self, max_show: int = 10):
        """Display current clauses in the KB"""
        print("\n" + "="*60)
        print("📋 Resolution Engine - Current Clauses")
        print("="*60)
        
        clause_list = list(self.clauses)[:max_show]
        for i, clause in enumerate(clause_list, 1):
            print(f"{i}. {clause}")
        
        if len(self.clauses) > max_show:
            print(f"... and {len(self.clauses) - max_show} more clauses")
        
        print(f"\nTotal: {len(self.clauses)} clauses")


class FirstOrderLogic:
    """
    First-Order Logic representation
    
    Supports quantifiers (∀, ∃) and predicates
    """
    
    @staticmethod
    def universal_instantiation(formula: str, constant: str) -> str:
        """
        Universal Instantiation: ∀x P(x) → P(c)
        
        Args:
            formula: Universal formula (e.g., "∀x Safe(x)")
            constant: Constant to instantiate with
            
        Returns:
            Instantiated formula
        """
        # Simple string replacement (real implementation would parse)
        if formula.startswith("∀x "):
            predicate = formula[3:]
            return predicate.replace("x", constant)
        return formula
    
    @staticmethod
    def existential_instantiation(formula: str, skolem_constant: str) -> str:
        """
        Existential Instantiation: ∃x P(x) → P(c)
        存在例示
        
        Args:
            formula: Existential formula
            skolem_constant: Skolem constant
            
        Returns:
            Instantiated formula
        """
        if formula.startswith("∃x "):
            predicate = formula[3:]
            return predicate.replace("x", skolem_constant)
        return formula


# Example usage demonstrating Lab 9 concepts
def demo_colonel_west_style():
    """
    Demonstration similar to Lab 9 Colonel West example
    """
    print("\n" + "="*70)
    print("DEMONSTRATION: Resolution Inference (Colonel West Style)")
    print("="*70)
    
    # Create knowledge base
    kb = PropositionalKB()
    
    # Add facts (similar to Colonel West scenario)
    print("\n📝 Given Facts:")
    print("1. American(West)")
    print("2. Weapon(M1)")
    print("3. Sells(West, M1, Nono)")
    print("4. Hostile(Nono)")
    print("5. ∀x,y,z (American(x) ∧ Weapon(y) ∧ Sells(x,y,z) ∧ Hostile(z)) → Criminal(x)")
    
    kb.tell("American(West)", True)
    kb.tell("Weapon(M1)", True)
    kb.tell("Sells(West,M1,Nono)", True)
    kb.tell("Hostile(Nono)", True)
    
    # Create resolution engine
    engine = ResolutionEngine(kb)
    
    # Add the implication rule as clauses
    # ¬American(x) ∨ ¬Weapon(y) ∨ ¬Sells(x,y,z) ∨ ¬Hostile(z) ∨ Criminal(x)
    engine.add_clause({
        "¬American(West)",
        "¬Weapon(M1)",
        "¬Sells(West,M1,Nono)",
        "¬Hostile(Nono)",
        "Criminal(West)"
    })
    
    print("\n🎯 Goal: Prove Criminal(West)")
    
    # Prove using resolution
    result = engine.prove_by_resolution("Criminal(West)")
    
    if result:
        print("\n✅ Successfully proven: West is a criminal")
    else:
        print("\n❌ Could not prove")


if __name__ == "__main__":
    print("Testing Resolution Engine...")
    
    demo_colonel_west_style()
    
    print("\n✅ Resolution module test complete!")