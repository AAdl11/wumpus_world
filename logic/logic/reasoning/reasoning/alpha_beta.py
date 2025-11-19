"""
Alpha-Beta Pruning for Adversarial Search in Wumpus World

Implements game tree search with alpha-beta pruning for scenarios
where the Wumpus can move (adversarial setting).

Author: Mei Hsien Hsu
Course: CS4 Introduction AI
"""

from typing import List, Tuple, Optional, Any, Dict
import copy


class GameState:
    """
    Represents a game state for adversarial search
    """
    
    def __init__(self, agent_pos: Tuple[int, int], wumpus_pos: Tuple[int, int],
                 world_size: int, gold_pos: Tuple[int, int] = None,
                 agent_has_arrow: bool = True, wumpus_alive: bool = True):
        """
        Initialize game state
        
        Args:
            agent_pos: Agent position (x, y)
            wumpus_pos: Wumpus position (x, y)
            world_size: Size of world
            gold_pos: Gold position
            agent_has_arrow: Whether agent has arrow
            wumpus_alive: Whether Wumpus is alive
        """
        self.agent_pos = agent_pos
        self.wumpus_pos = wumpus_pos
        self.world_size = world_size
        self.gold_pos = gold_pos or (world_size-1, world_size-1)
        self.agent_has_arrow = agent_has_arrow
        self.wumpus_alive = wumpus_alive
        self.gold_collected = False
    
    def is_terminal(self) -> bool:
        """Check if this is a terminal state"""
        # Terminal if:
        # 1. Agent collected gold
        # 2. Agent is eaten by Wumpus
        # 3. Agent reached starting position with gold
        
        if self.agent_pos == self.wumpus_pos and self.wumpus_alive:
            return True  # Agent eaten
        
        if self.agent_pos == self.gold_pos:
            self.gold_collected = True
        
        if self.gold_collected and self.agent_pos == (0, 0):
            return True  # Won!
        
        return False
    
    def evaluate(self) -> float:
        """
        Evaluate the current state from agent's perspective
        
        Returns:
            Utility value (higher is better for agent)
        """
        # If agent is eaten, very bad
        if self.agent_pos == self.wumpus_pos and self.wumpus_alive:
            return -1000
        
        # If gold collected and at start, win!
        if self.gold_collected and self.agent_pos == (0, 0):
            return 1000
        
        # Otherwise, calculate heuristic
        score = 0
        
        # Reward for collecting gold
        if self.gold_collected:
            score += 500
            # Reward for being close to exit
            dist_to_exit = abs(self.agent_pos[0]) + abs(self.agent_pos[1])
            score += 100 - dist_to_exit * 10
        else:
            # Reward for being close to gold
            dist_to_gold = (abs(self.agent_pos[0] - self.gold_pos[0]) +
                          abs(self.agent_pos[1] - self.gold_pos[1]))
            score += 100 - dist_to_gold * 10
        
        # Penalty for being close to Wumpus
        if self.wumpus_alive:
            dist_to_wumpus = (abs(self.agent_pos[0] - self.wumpus_pos[0]) +
                            abs(self.agent_pos[1] - self.wumpus_pos[1]))
            if dist_to_wumpus == 0:
                score -= 1000
            elif dist_to_wumpus == 1:
                score -= 200
            elif dist_to_wumpus == 2:
                score -= 50
        
        return score
    
    def get_adjacent(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid adjacent positions"""
        x, y = pos
        adjacent = []
        
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.world_size and 0 <= ny < self.world_size:
                adjacent.append((nx, ny))
        
        return adjacent
    
    def get_agent_actions(self) -> List[str]:
        """Get legal actions for agent"""
        actions = []
        
        # Can always try to move in four directions
        if self.agent_pos[0] > 0:
            actions.append('MOVE_WEST')
        if self.agent_pos[0] < self.world_size - 1:
            actions.append('MOVE_EAST')
        if self.agent_pos[1] > 0:
            actions.append('MOVE_SOUTH')
        if self.agent_pos[1] < self.world_size - 1:
            actions.append('MOVE_NORTH')
        
        # Can grab gold if at gold location
        if self.agent_pos == self.gold_pos and not self.gold_collected:
            actions.append('GRAB')
        
        # Can shoot if has arrow and Wumpus alive
        if self.agent_has_arrow and self.wumpus_alive:
            actions.append('SHOOT')
        
        return actions
    
    def get_wumpus_actions(self) -> List[str]:
        """Get legal actions for Wumpus"""
        if not self.wumpus_alive:
            return ['STAY']
        
        actions = ['STAY']
        
        # Wumpus can move to adjacent cells
        adjacent = self.get_adjacent(self.wumpus_pos)
        for adj in adjacent:
            if adj == (self.wumpus_pos[0] + 1, self.wumpus_pos[1]):
                actions.append('MOVE_EAST')
            elif adj == (self.wumpus_pos[0] - 1, self.wumpus_pos[1]):
                actions.append('MOVE_WEST')
            elif adj == (self.wumpus_pos[0], self.wumpus_pos[1] + 1):
                actions.append('MOVE_NORTH')
            elif adj == (self.wumpus_pos[0], self.wumpus_pos[1] - 1):
                actions.append('MOVE_SOUTH')
        
        return actions
    
    def apply_agent_action(self, action: str) -> 'GameState':
        """Apply agent action and return new state"""
        new_state = copy.deepcopy(self)
        
        if action == 'MOVE_NORTH':
            new_state.agent_pos = (self.agent_pos[0], self.agent_pos[1] + 1)
        elif action == 'MOVE_SOUTH':
            new_state.agent_pos = (self.agent_pos[0], self.agent_pos[1] - 1)
        elif action == 'MOVE_EAST':
            new_state.agent_pos = (self.agent_pos[0] + 1, self.agent_pos[1])
        elif action == 'MOVE_WEST':
            new_state.agent_pos = (self.agent_pos[0] - 1, self.agent_pos[1])
        elif action == 'GRAB':
            if self.agent_pos == self.gold_pos:
                new_state.gold_collected = True
        elif action == 'SHOOT':
            new_state.agent_has_arrow = False
            # Simple shooting: kills Wumpus if in same row/column
            if (self.agent_pos[0] == self.wumpus_pos[0] or
                self.agent_pos[1] == self.wumpus_pos[1]):
                new_state.wumpus_alive = False
        
        return new_state
    
    def apply_wumpus_action(self, action: str) -> 'GameState':
        """Apply Wumpus action and return new state"""
        new_state = copy.deepcopy(self)
        
        if action == 'MOVE_NORTH':
            new_state.wumpus_pos = (self.wumpus_pos[0], self.wumpus_pos[1] + 1)
        elif action == 'MOVE_SOUTH':
            new_state.wumpus_pos = (self.wumpus_pos[0], self.wumpus_pos[1] - 1)
        elif action == 'MOVE_EAST':
            new_state.wumpus_pos = (self.wumpus_pos[0] + 1, self.wumpus_pos[1])
        elif action == 'MOVE_WEST':
            new_state.wumpus_pos = (self.wumpus_pos[0] - 1, self.wumpus_pos[1])
        # STAY does nothing
        
        return new_state


class AlphaBetaSearch:
    """
    Alpha-Beta Pruning Search Algorithm
    
    Implements minimax with alpha-beta pruning for efficient
    game tree search in adversarial settings.
    """
    
    def __init__(self, initial_state: GameState):
        """
        Initialize Alpha-Beta search
        
        Args:
            initial_state: Starting game state
        """
        self.initial_state = initial_state
        self.nodes_explored = 0
        self.pruned_branches = 0
        
        print("🎮 Alpha-Beta Search initialized")
    
    def alpha_beta(self, state: GameState, depth: int, 
                  alpha: float, beta: float, 
                  maximizing: bool) -> Tuple[float, Optional[str]]:
        """
        Alpha-Beta pruning algorithm
        
        Args:
            state: Current game state
            depth: Remaining search depth
            alpha: Alpha value (best for MAX)
            beta: Beta value (best for MIN)
            maximizing: True if maximizing player (agent)
            
        Returns:
            (best_value, best_action)
        """
        self.nodes_explored += 1
        
        # Terminal test or depth limit
        if depth == 0 or state.is_terminal():
            return state.evaluate(), None
        
        if maximizing:
            # Agent's turn (maximize)
            max_value = float('-inf')
            best_action = None
            
            for action in state.get_agent_actions():
                new_state = state.apply_agent_action(action)
                value, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, False)
                
                if value > max_value:
                    max_value = value
                    best_action = action
                
                alpha = max(alpha, value)
                
                # Beta cutoff (pruning)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break
            
            return max_value, best_action
        
        else:
            # Wumpus's turn (minimize)
            min_value = float('inf')
            best_action = None
            
            for action in state.get_wumpus_actions():
                new_state = state.apply_wumpus_action(action)
                value, _ = self.alpha_beta(new_state, depth - 1, alpha, beta, True)
                
                if value < min_value:
                    min_value = value
                    best_action = action
                
                beta = min(beta, value)
                
                # Alpha cutoff (pruning)
                if beta <= alpha:
                    self.pruned_branches += 1
                    break
            
            return min_value, best_action
    
    def get_best_move(self, depth: int = 3) -> Tuple[str, float]:
        """
        Get best move for agent using alpha-beta search
        
        Args:
            depth: Search depth (default 3)
            
        Returns:
            (best_action, expected_value)
        """
        self.nodes_explored = 0
        self.pruned_branches = 0
        
        value, action = self.alpha_beta(
            self.initial_state,
            depth,
            float('-inf'),
            float('inf'),
            True
        )
        
        return action, value
    
    def get_statistics(self) -> Dict[str, int]:
        """Get search statistics"""
        return {
            'nodes_explored': self.nodes_explored,
            'branches_pruned': self.pruned_branches
        }


# Demonstration
def demo_alpha_beta():
    """Demonstrate Alpha-Beta pruning"""
    print("\n" + "="*70)
    print("DEMONSTRATION: Alpha-Beta Pruning")
    print("="*70)
    
    # Create initial state
    print("\n📋 Initial State:")
    print("   Agent at (0, 0)")
    print("   Wumpus at (2, 2)")
    print("   Gold at (3, 3)")
    
    state = GameState(
        agent_pos=(0, 0),
        wumpus_pos=(2, 2),
        world_size=4,
        gold_pos=(3, 3)
    )
    
    # Create search
    search = AlphaBetaSearch(state)
    
    # Get best move
    print("\n🔍 Running Alpha-Beta search (depth=3)...")
    best_action, expected_value = search.get_best_move(depth=3)
    
    stats = search.get_statistics()
    
    print(f"\n✅ Search Complete!")
    print(f"   Best Action: {best_action}")
    print(f"   Expected Value: {expected_value:.1f}")
    print(f"   Nodes Explored: {stats['nodes_explored']}")
    print(f"   Branches Pruned: {stats['branches_pruned']}")
    
    pruning_efficiency = (stats['branches_pruned'] / stats['nodes_explored'] * 100
                         if stats['nodes_explored'] > 0 else 0)
    print(f"   Pruning Efficiency: {pruning_efficiency:.1f}%")


if __name__ == "__main__":
    print("Testing Alpha-Beta Pruning...")
    
    demo_alpha_beta()
    
    print("\n✅ Alpha-Beta module test complete!")