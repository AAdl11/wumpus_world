"""
main.py - Wumpus World Simulation Runner
Complete game loop with visualization and logging
Author: Mei Hsien Hsu
Course: CS4 - Intro AI, Professor An Lam
Institution: Las Positas College
Fall 2025
"""

from world import World
from agent import Agent
import time

def print_header():
    """Print welcome banner."""
    print("\n" + "="*60)
    print("🎮  WUMPUS WORLD - KNOWLEDGE-BASED AGENT SIMULATION")
    print("="*60)
    print("Author: Mei Hsien Hsu")
    print("Course: CS4 - Introduction to Artificial Intelligence")
    print("Instructor: Professor An Lam, Las Positas College")
    print("="*60 + "\n")

def print_step_divider(step_num: int):
    """Print step separator."""
    print("\n" + "─"*60)
    print(f"📍 STEP {step_num}")
    print("─"*60)

def run_simulation(world: World, agent: Agent, 
                  max_steps: int = 100, 
                  step_delay: float = 0.5,
                  verbose: bool = True):
    """
    Run the Wumpus World simulation.
    
    Args:
        world: The world environment
        agent: The knowledge-based agent
        max_steps: Maximum steps before timeout
        step_delay: Delay between steps (seconds)
        verbose: Whether to print detailed output
    
    Returns:
        Dictionary with simulation results
    """
    step_count = 0
    action_history = []
    
    while world.alive and not world.out and step_count < max_steps:
        step_count += 1
        
        if verbose:
            print_step_divider(step_count)
            
            # Show current state
            pos = world.agent_pos
            percepts = world.percepts_at(pos)
            
            print(f"📍 Position: {pos}")
            print(f"👁️  Percepts: {percepts}")
            print(f"🧠 KB has {len(agent.kb.facts)} facts")
            print(f"✓  Visited {len(agent.visited)} cells")
        
        # Agent makes decision
        action = agent.step()
        action_history.append(action)
        
        if verbose:
            print(f"🎯 Action: {action}")
            
            # Show grid every few steps
            if step_count % 3 == 0 or not world.alive or world.out:
                safe_cells = agent.kb.get_safe_cells()
                world.display_grid(visited=agent.visited, safe=safe_cells)
        
        # Check termination conditions
        if not world.alive:
            if verbose:
                print("\n💀 AGENT DIED!")
            break
        
        if world.out:
            if verbose:
                print("\n🏆 AGENT ESCAPED SUCCESSFULLY!")
            break
        
        # Small delay for readability
        if verbose and step_delay > 0:
            time.sleep(step_delay)
    
    # Final summary
    results = {
        "success": world.out and world.has_gold,
        "alive": world.alive,
        "has_gold": world.has_gold,
        "steps": step_count,
        "cells_visited": len(agent.visited),
        "final_position": world.agent_pos,
        "actions": action_history
    }
    
    return results

def print_final_report(results: dict):
    """Print final simulation report."""
    print("\n" + "="*60)
    print("📊 FINAL REPORT")
    print("="*60)
    
    if results["success"]:
        print("✅ Result: SUCCESS - Agent retrieved gold and escaped!")
    elif not results["alive"]:
        print("❌ Result: FAILURE - Agent died")
    else:
        print("⚠️  Result: INCOMPLETE - Agent got stuck or timed out")
    
    print(f"\n📈 Statistics:")
    print(f"   • Total steps: {results['steps']}")
    print(f"   • Cells visited: {results['cells_visited']}")
    print(f"   • Final position: {results['final_position']}")
    print(f"   • Has gold: {'Yes' if results['has_gold'] else 'No'}")
    print(f"   • Survived: {'Yes' if results['alive'] else 'No'}")
    
    print(f"\n📜 Action History:")
    for i, action in enumerate(results['actions'][:10], 1):
        print(f"   {i}. {action}")
    if len(results['actions']) > 10:
        print(f"   ... and {len(results['actions']) - 10} more actions")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main entry point."""
    print_header()
    
    # Configuration
    print("⚙️  Configuration:")
    print("   • Grid size: 4×4")
    print("   • Pits: (3,1), (3,3), (4,4)")
    print("   • Wumpus: (1,3)")
    print("   • Gold: (2,3)")
    print("   • Start: (1,1), facing East")
    print()
    
    # Create world (using textbook example)
    world = World(
        size=(4, 4),
        pits={(3,1), (3,3), (4,4)},
        wumpus=(1,3),
        gold=(2,3)
    )
    
    # Create agent
    agent = Agent(world)
    
    # Show initial grid
    print("🗺️  Initial World State:")
    world.display_grid()
    
    input("Press ENTER to start simulation...")
    
    # Run simulation
    results = run_simulation(
        world=world,
        agent=agent,
        max_steps=100,
        step_delay=0.3,  # 0.3 seconds between steps
        verbose=True
    )
    
    # Print final report
    print_final_report(results)

if __name__ == "__main__":
    main()