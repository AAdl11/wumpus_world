"""
Bayesian Network for Probabilistic Reasoning in Wumpus World

Implements Bayesian inference for handling uncertainty:
- Prior and posterior probabilities
- Conditional probability tables (CPT)
- Bayes' Theorem applications
- Uncertainty in pit and Wumpus locations

Author: Mei Hsien Hsu
Course: CS4 Introduction AI
"""

from typing import Dict, List, Tuple, Set
import math


class BayesianNetwork:
    """
    Bayesian Network for Wumpus World
    
    Network structure:
        Pit         Wumpus
         ↓             ↓
      Breeze       Stench
         ↓             ↓
    [Agent Perception]
    """
    
    def __init__(self):
        """Initialize Bayesian Network with Wumpus World structure"""
        self.nodes = {}
        self.cpt = {}  # Conditional Probability Tables
        
        self._build_network()
        
        print("📊 Bayesian Network initialized")
    
    def _build_network(self):
        """Build the network structure for Wumpus World"""
        # Define nodes and their parents
        self.add_node('Pit', parents=[])
        self.add_node('Wumpus', parents=[])
        self.add_node('Breeze', parents=['Pit'])
        self.add_node('Stench', parents=['Wumpus'])
        
        # Set prior probabilities
        # P(Pit) - probability of pit in any cell
        self.set_cpt('Pit', {
            True: 0.2,   # 20% chance of pit
            False: 0.8
        })
        
        # P(Wumpus) - probability of Wumpus in any cell
        self.set_cpt('Wumpus', {
            True: 0.05,  # 5% chance (only one Wumpus)
            False: 0.95
        })
        
        # P(Breeze | Pit)
        # If pit exists, high probability of feeling breeze
        self.set_cpt('Breeze', {
            (True,): 0.90,   # P(Breeze | Pit) = 90%
            (False,): 0.10   # P(Breeze | ¬Pit) = 10% (false positive)
        })
        
        # P(Stench | Wumpus)
        # If Wumpus exists, high probability of smelling stench
        self.set_cpt('Stench', {
            (True,): 0.95,   # P(Stench | Wumpus) = 95%
            (False,): 0.05   # P(Stench | ¬Wumpus) = 5% (false positive)
        })
    
    def add_node(self, name: str, parents: List[str] = None):
        """
        Add a node to the network
        
        Args:
            name: Node name
            parents: List of parent node names
        """
        self.nodes[name] = {
            'parents': parents if parents else [],
            'children': []
        }
        
        # Update children for parents
        if parents:
            for parent in parents:
                if parent in self.nodes:
                    self.nodes[parent]['children'].append(name)
    
    def set_cpt(self, node: str, cpt: Dict):
        """
        Set Conditional Probability Table for a node
        
        Args:
            node: Node name
            cpt: CPT dictionary
        """
        self.cpt[node] = cpt
    
    def get_prior(self, node: str, value: bool) -> float:
        """
        Get prior probability of a node
        
        Args:
            node: Node name
            value: True/False
            
        Returns:
            Prior probability
        """
        return self.cpt[node].get(value, 0.5)
    
    def get_conditional(self, node: str, parent_values: Tuple) -> float:
        """
        Get conditional probability given parent values
        
        Args:
            node: Node name
            parent_values: Tuple of parent values
            
        Returns:
            Conditional probability
        """
        return self.cpt[node].get(parent_values, 0.5)
    
    def bayes_theorem(self, hypothesis: bool, evidence: bool, 
                     p_h: float, p_e_given_h: float, p_e_given_not_h: float) -> float:
        """
        Apply Bayes' Theorem
        
        P(H|E) = P(E|H) * P(H) / P(E)
        where P(E) = P(E|H)*P(H) + P(E|¬H)*P(¬H)
        
        Args:
            hypothesis: True/False
            evidence: True/False
            p_h: P(H)
            p_e_given_h: P(E|H)
            p_e_given_not_h: P(E|¬H)
            
        Returns:
            P(H|E)
        """
        # Calculate P(E) using total probability
        p_e = p_e_given_h * p_h + p_e_given_not_h * (1 - p_h)
        
        if p_e == 0:
            return 0
        
        # Apply Bayes' Theorem
        if evidence:
            p_h_given_e = (p_e_given_h * p_h) / p_e
        else:
            # P(H|¬E)
            p_not_e = 1 - p_e
            if p_not_e == 0:
                return 0
            p_h_given_e = ((1 - p_e_given_h) * p_h) / p_not_e
        
        return p_h_given_e
    
    def infer_pit_probability(self, has_breeze: bool) -> float:
        """
        Infer probability of pit given breeze observation
        
        Uses Bayes' Theorem:
        P(Pit | Breeze) = P(Breeze | Pit) * P(Pit) / P(Breeze)
        
        Args:
            has_breeze: True if breeze detected
            
        Returns:
            P(Pit | evidence)
        """
        # Get probabilities from CPT
        p_pit = self.get_prior('Pit', True)
        p_breeze_given_pit = self.get_conditional('Breeze', (True,))
        p_breeze_given_no_pit = self.get_conditional('Breeze', (False,))
        
        # Apply Bayes' Theorem
        posterior = self.bayes_theorem(
            hypothesis=True,
            evidence=has_breeze,
            p_h=p_pit,
            p_e_given_h=p_breeze_given_pit,
            p_e_given_not_h=p_breeze_given_no_pit
        )
        
        return posterior
    
    def infer_wumpus_probability(self, has_stench: bool) -> float:
        """
        Infer probability of Wumpus given stench observation
        
        P(Wumpus | Stench) = P(Stench | Wumpus) * P(Wumpus) / P(Stench)
        
        Args:
            has_stench: True if stench detected
            
        Returns:
            P(Wumpus | evidence)
        """
        # Get probabilities from CPT
        p_wumpus = self.get_prior('Wumpus', True)
        p_stench_given_wumpus = self.get_conditional('Stench', (True,))
        p_stench_given_no_wumpus = self.get_conditional('Stench', (False,))
        
        # Apply Bayes' Theorem
        posterior = self.bayes_theorem(
            hypothesis=True,
            evidence=has_stench,
            p_h=p_wumpus,
            p_e_given_h=p_stench_given_wumpus,
            p_e_given_not_h=p_stench_given_no_wumpus
        )
        
        return posterior
    
    def infer_danger_probability(self, has_breeze: bool, has_stench: bool) -> float:
        """
        Infer combined danger probability
        
        P(Danger) = P(Pit ∨ Wumpus)
        = P(Pit) + P(Wumpus) - P(Pit ∧ Wumpus)
        
        Assuming independence:
        P(Pit ∧ Wumpus) ≈ P(Pit) * P(Wumpus)
        
        Args:
            has_breeze: Breeze detected
            has_stench: Stench detected
            
        Returns:
            P(Danger | evidence)
        """
        p_pit = self.infer_pit_probability(has_breeze)
        p_wumpus = self.infer_wumpus_probability(has_stench)
        
        # Union probability (assuming near-independence)
        p_danger = p_pit + p_wumpus - (p_pit * p_wumpus)
        
        return p_danger
    
    def is_safe_enough(self, has_breeze: bool, has_stench: bool, 
                      threshold: float = 0.7) -> bool:
        """
        Determine if a location is safe enough to visit
        
        Args:
            has_breeze: Breeze detected
            has_stench: Stench detected
            threshold: Safety threshold (default 70%)
            
        Returns:
            True if P(Safe) > threshold
        """
        p_danger = self.infer_danger_probability(has_breeze, has_stench)
        p_safe = 1 - p_danger
        
        return p_safe > threshold
    
    def explain_inference(self, has_breeze: bool, has_stench: bool):
        """
        Explain the Bayesian inference process
        """
        print("\n" + "="*60)
        print("📊 Bayesian Inference Explanation")
        print("="*60)
        
        # Prior probabilities
        print("\n1️⃣  Prior Probabilities (before evidence):")
        p_pit_prior = self.get_prior('Pit', True)
        p_wumpus_prior = self.get_prior('Wumpus', True)
        print(f"   P(Pit) = {p_pit_prior:.1%}")
        print(f"   P(Wumpus) = {p_wumpus_prior:.1%}")
        
        # Evidence
        print("\n2️⃣  Evidence Observed:")
        print(f"   Breeze: {has_breeze}")
        print(f"   Stench: {has_stench}")
        
        # Likelihoods
        print("\n3️⃣  Likelihoods (sensor accuracy):")
        print(f"   P(Breeze | Pit) = {self.get_conditional('Breeze', (True,)):.1%}")
        print(f"   P(Stench | Wumpus) = {self.get_conditional('Stench', (True,)):.1%}")
        
        # Posterior probabilities
        print("\n4️⃣  Posterior Probabilities (after evidence):")
        p_pit_post = self.infer_pit_probability(has_breeze)
        p_wumpus_post = self.infer_wumpus_probability(has_stench)
        print(f"   P(Pit | Evidence) = {p_pit_post:.1%}")
        print(f"   P(Wumpus | Evidence) = {p_wumpus_post:.1%}")
        
        # Decision
        print("\n5️⃣  Decision Analysis:")
        p_danger = self.infer_danger_probability(has_breeze, has_stench)
        p_safe = 1 - p_danger
        print(f"   P(Danger) = {p_danger:.1%}")
        print(f"   P(Safe) = {p_safe:.1%}")
        
        if self.is_safe_enough(has_breeze, has_stench):
            print(f"   ✅ DECISION: Location is safe enough to explore")
        else:
            print(f"   ⚠️  DECISION: Location is too dangerous")
    
    def display_cpt(self):
        """Display all Conditional Probability Tables"""
        print("\n" + "="*60)
        print("📋 Conditional Probability Tables (CPT)")
        print("="*60)
        
        for node, table in self.cpt.items():
            print(f"\n{node}:")
            parents = self.nodes[node]['parents']
            
            if not parents:
                print("  (Prior probability)")
            else:
                print(f"  (Given: {', '.join(parents)})")
            
            for condition, prob in table.items():
                print(f"  {condition} → {prob:.2%}")


# Demonstration and testing
def demo_bayesian_inference():
    """Demonstrate Bayesian inference for Wumpus World"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Bayesian Network Inference")
    print("="*70)
    
    # Create network
    bn = BayesianNetwork()
    
    # Display CPTs
    bn.display_cpt()
    
    # Scenario 1: Breeze detected, no stench
    print("\n" + "="*70)
    print("SCENARIO 1: Breeze detected, no stench")
    print("="*70)
    bn.explain_inference(has_breeze=True, has_stench=False)
    
    # Scenario 2: Stench detected, no breeze
    print("\n" + "="*70)
    print("SCENARIO 2: Stench detected, no breeze")
    print("="*70)
    bn.explain_inference(has_breeze=False, has_stench=True)
    
    # Scenario 3: Both breeze and stench
    print("\n" + "="*70)
    print("SCENARIO 3: Both breeze and stench detected")
    print("="*70)
    bn.explain_inference(has_breeze=True, has_stench=True)
    
    # Scenario 4: Neither detected
    print("\n" + "="*70)
    print("SCENARIO 4: No breeze, no stench")
    print("="*70)
    bn.explain_inference(has_breeze=False, has_stench=False)


if __name__ == "__main__":
    print("Testing Bayesian Network...")
    
    demo_bayesian_inference()
    
    print("\n✅ Bayesian Network module test complete!")