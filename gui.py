"""
gui.py - Interactive GUI for Wumpus World
Author: Mei Hsien Hsu
Course: CS4 - Intro AI
Final Project - Fall 2025
Professor: An Lam, Las Positas College

This GUI provides a professional visualization of the Knowledge-Based Agent
navigating the Wumpus World using propositional logic and BFS search.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from world import World
from agent import Agent

class WumpusGUI:
    """
    Professional GUI for Wumpus World Knowledge-Based Agent simulation.
    Features visual grid, real-time stats, and interactive controls.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Wumpus World - Knowledge-Based Agent | Mei Hsien Hsu | CS4 Final Project")
        self.root.geometry("1400x850")
        self.root.configure(bg="#f5f5f5")
        
        # Initialize game components
        self.world = World()
        self.agent = Agent(self.world)
        self.step_count = 0
        self.game_over = False
        self.auto_running = False
        
        # Create all UI components
        self.create_widgets()
        self.update_display()
        
        # Bind keyboard shortcuts
        self.root.bind('<space>', lambda e: self.next_step())
        self.root.bind('r', lambda e: self.reset())
    
    def create_widgets(self):
        """Create all UI components with professional styling"""
        
        # ========== HEADER SECTION ==========
        header_frame = tk.Frame(self.root, bg="#1976D2", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🎮 WUMPUS WORLD",
            font=("Segoe UI", 48, "bold"),
            bg="#1976D2",
            fg="white"
        )
        title.pack(pady=5)
        
        subtitle = tk.Label(
            header_frame,
            text="Knowledge-Based Agent Simulation | CS4 Final Project | Mei Hsien Hsu",
            font=("Segoe UI", 11),
            bg="#1976D2",
            fg="#E3F2FD"
        )
        subtitle.pack()
        
        # ========== MAIN CONTAINER ==========
        main_container = tk.Frame(self.root, bg="#f5f5f5")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # ========== LEFT PANEL - GRID (60% WIDTH) ==========
        left_panel = tk.Frame(main_container, bg="#f5f5f5")
        left_panel.place(relx=0, rely=0, relwidth=0.6, relheight=1)  # 60% width!
        
        grid_title = tk.Label(
            left_panel,
            text="🗺️  World Grid (4×4)",
            font=("Segoe UI", 20, "bold"),
            bg="#f5f5f5",
            fg="#333"
        )
        grid_title.pack(pady=8)
        
        # Grid container with border
        grid_container = tk.Frame(
            left_panel,
            bg="#424242",
            relief="solid",
            borderwidth=4
        )
        grid_container.pack()
        
        self.grid_frame = tk.Frame(grid_container, bg="#424242")
        self.grid_frame.pack(padx=3, pady=3)
        
        # Create 4x4 grid cells - 60% OF SCREEN
        self.cells = {}
        for y in range(4, 0, -1):
            for x in range(1, 5):
                cell = tk.Label(
                    self.grid_frame,
                    text="",
                    width=7,    # SMALLER to fit 60%!
                    height=3,   # SMALLER!
                    relief="raised",
                    borderwidth=2,
                    font=("Arial", 55, "bold"),
                    bg="white",
                    fg="black"
                )
                cell.grid(row=5-y, column=x-1, padx=2, pady=2)
                self.cells[(x, y)] = cell
        
        # Coordinate labels
        coord_frame = tk.Frame(left_panel, bg="#f5f5f5")
        coord_frame.pack(pady=8)
        
        tk.Label(
            coord_frame,
            text="x →   1        2        3        4",
            font=("Consolas", 11),
            bg="#f5f5f5",
            fg="#666"
        ).pack()
        
        # ========== RIGHT PANEL - INFO (40% WIDTH) ==========
        right_panel = tk.Frame(main_container, bg="#f5f5f5")
        right_panel.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)  # 40% width!
        
        # ========== STATUS PANEL ==========
        status_frame = tk.LabelFrame(
            right_panel,
            text="📊 Agent Status",
            font=("Segoe UI", 16, "bold"),  # BIGGER!
            bg="white",
            fg="#1976D2",
            relief="solid",
            borderwidth=2,
            padx=20,
            pady=15
        )
        status_frame.pack(fill=tk.X, pady=10)
        
        self.step_label = tk.Label(
            status_frame,
            text="Step: 0",
            font=("Segoe UI", 18, "bold"),  # BIGGER!
            bg="white",
            fg="#D32F2F"
        )
        self.step_label.pack(anchor="w", pady=4)
        
        self.position_label = tk.Label(
            status_frame,
            text="📍 Position: (1, 1)",
            font=("Segoe UI", 15),  # BIGGER!
            bg="white",
            fg="#333"
        )
        self.position_label.pack(anchor="w", pady=3)
        
        self.direction_label = tk.Label(
            status_frame,
            text="🧭 Direction: East",
            font=("Segoe UI", 15),  # BIGGER!
            bg="white",
            fg="#333"
        )
        self.direction_label.pack(anchor="w", pady=3)
        
        self.status_label = tk.Label(
            status_frame,
            text="✅ Alive | ❌ No Gold | ❌ Not Escaped",
            font=("Segoe UI", 14),  # BIGGER!
            bg="white",
            fg="#666"
        )
        self.status_label.pack(anchor="w", pady=3)
        
        self.kb_label = tk.Label(
            status_frame,
            text="🧠 KB Facts: 0 | 🟢 Safe: 1 | 👣 Visited: 0",
            font=("Segoe UI", 13),  # BIGGER!
            bg="white",
            fg="#666"
        )
        self.kb_label.pack(anchor="w", pady=3)
        
        # ========== ACTION PANEL ==========
        action_frame = tk.LabelFrame(
            right_panel,
            text="🎯 Current Action",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#1976D2",
            relief="solid",
            borderwidth=2,
            padx=18,
            pady=12
        )
        action_frame.pack(fill=tk.X, pady=10)
        
        self.action_label = tk.Label(
            action_frame,
            text="⏸️  Ready to start simulation!",
            font=("Segoe UI", 12),
            bg="white",
            fg="#388E3C",
            wraplength=300,
            justify="left"
        )
        self.action_label.pack()
        
        # ========== LEGEND PANEL ==========
        legend_frame = tk.LabelFrame(
            right_panel,
            text="📖 Legend",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#1976D2",
            relief="solid",
            borderwidth=2,
            padx=18,
            pady=12
        )
        legend_frame.pack(fill=tk.X, pady=10)
        
        legends = [
            ("🚀", "Agent (You)"),
            ("⭐", "Gold (Goal)"),
            ("🐉", "Wumpus (Deadly)"),
            ("☠️", "Pit (Deadly)"),
            ("👟", "Visited"),
            ("✨", "Safe"),
            ("🟩", "Green = Visited"),
            ("🟨", "Yellow = Agent"),
        ]
        
        for emoji, desc in legends:
            legend_row = tk.Frame(legend_frame, bg="white")
            legend_row.pack(anchor="w", pady=2)
            
            tk.Label(
                legend_row,
                text=f"{emoji}",
                font=("Segoe UI", 13, "bold"),
                bg="white",
                width=3,
                anchor="w"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                legend_row,
                text=desc,
                font=("Segoe UI", 12),
                bg="white",
                fg="#666"
            ).pack(side=tk.LEFT)
        
        # ========== CONTROL BUTTONS - AT BOTTOM ==========
        button_container = tk.Frame(self.root, bg="#ecf0f1")
        button_container.pack(side=tk.BOTTOM, fill=tk.X, pady=12)
        
        button_style = {
            "font": ("Segoe UI", 14, "bold"),
            "relief": "raised",
            "borderwidth": 3,
            "cursor": "hand2",
            "padx": 30,
            "pady": 13
        }
        
        self.step_button = tk.Button(
            button_container,
            text="▶️  Next Step",
            command=self.next_step,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            **button_style
        )
        self.step_button.pack(side=tk.LEFT, padx=8)
        
        self.auto_button = tk.Button(
            button_container,
            text="⏩  Auto Run",
            command=self.auto_run,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            **button_style
        )
        self.auto_button.pack(side=tk.LEFT, padx=8)
        
        self.pause_button = tk.Button(
            button_container,
            text="⏸️  Pause",
            command=self.pause_auto,
            bg="#FF9800",
            fg="white",
            activebackground="#F57C00",
            state="disabled",
            **button_style
        )
        self.pause_button.pack(side=tk.LEFT, padx=8)
        
        self.reset_button = tk.Button(
            button_container,
            text="🔄  Reset",
            command=self.reset,
            bg="#f44336",
            fg="white",
            activebackground="#d32f2f",
            **button_style
        )
        self.reset_button.pack(side=tk.LEFT, padx=8)
        
        # ========== FOOTER ==========
        footer = tk.Label(
            self.root,
            text="CS4 - Introduction to AI | Professor An Lam | Las Positas College | Fall 2025",
            font=("Segoe UI", 9),
            bg="#ecf0f1",
            fg="#666"
        )
        footer.pack(side=tk.BOTTOM, pady=5)
    
    def update_display(self):
        """Update all visual elements with current game state"""
        
        # Update grid cells
        for y in range(4, 0, -1):
            for x in range(1, 5):
                cell = self.cells[(x, y)]
                text = ""
                bg_color = "white"
                fg_color = "black"
                
                # Draw world elements first
                if (x, y) in self.world.pits:
                    text = "☠️"
                    fg_color = "#D32F2F"
                    
                if (x, y) == self.world.wumpus:
                    text = "🐉"
                    fg_color = "#7B1FA2"
                    
                if (x, y) == self.world.gold and not self.world.has_gold:
                    text = "⭐"
                    fg_color = "#FFD700"
                
                # Agent position (override everything)
                if (x, y) == self.world.agent_pos:
                    text = "🚀"
                    bg_color = "#FFEB3B"
                    fg_color = "#1976D2"
                
                # Visited cells
                elif (x, y) in self.agent.visited:
                    bg_color = "#E0E0E0"
                    if not text:
                        text = "👟"
                        fg_color = "#9E9E9E"
                
                # Safe cells
                elif self.agent.kb.ask(f"Safe({x},{y})"):
                    bg_color = "#C8E6C9"
                    if not text:
                        text = "✨"
                        fg_color = "#4CAF50"
                
                cell.config(text=text, bg=bg_color, fg=fg_color)
        
        # Update status labels
        self.step_label.config(text=f"Step: {self.step_count}")
        
        pos = self.world.agent_pos
        self.position_label.config(text=f"📍 Position: {pos}")
        
        state = self.world.get_state()
        self.direction_label.config(text=f"🧭 Direction: {state['direction']}")
        
        alive = "✅ Alive" if state['alive'] else "💀 Dead"
        gold = "💎 Has Gold" if state['has_gold'] else "❌ No Gold"
        
        self.status_label.config(text=f"{alive} | {gold}")
        
        kb_facts = len(self.agent.kb.facts)
        safe_cells = len(self.agent.kb.get_safe_cells())
        visited = len(self.agent.visited)
        
        self.kb_label.config(
            text=f"🧠 KB: {kb_facts} | 🟢 Safe: {safe_cells} | 👣 Visit: {visited}"
        )
    
    def next_step(self):
        """Execute one step of agent reasoning and action"""
        
        if self.game_over:
            return
        
        if not self.world.alive:
            self.end_game(
                "💀 MISSION FAILED",
                f"The agent died!\n\nSteps survived: {self.step_count}",
                False
            )
            return
        
        if self.world.out:
            return
        
        # Execute agent decision
        action = self.agent.step()
        self.step_count += 1
        
        # Update action display
        self.action_label.config(
            text=f"Step {self.step_count}: {action}",
            fg="#1976D2"
        )
        
        # Refresh display
        self.update_display()
        
        # Check win/lose conditions
        if self.world.out and self.world.has_gold:
            self.end_game(
                "🏆 MISSION ACCOMPLISHED!",
                f"Agent successfully retrieved the gold and escaped!\n\n"
                f"📊 Performance:\n"
                f"  • Total Steps: {self.step_count}\n"
                f"  • Cells Explored: {len(self.agent.visited)}\n"
                f"  • KB Facts Learned: {len(self.agent.kb.facts)}",
                True
            )
        elif not self.world.alive:
            self.end_game(
                "💀 MISSION FAILED",
                f"Agent died!\n\nSteps survived: {self.step_count}",
                False
            )
    
    def auto_run(self):
        """Automatically run simulation until completion"""
        
        self.auto_running = True
        self.step_button.config(state="disabled")
        self.auto_button.config(state="disabled")
        self.pause_button.config(state="normal")
        
        self._auto_step()
    
    def _auto_step(self):
        """Recursive helper for auto-run"""
        
        if not self.auto_running:
            return
        
        if not self.game_over and self.world.alive and not self.world.out:
            self.next_step()
            self.root.after(600, self._auto_step)
        else:
            self.pause_auto()
    
    def pause_auto(self):
        """Pause auto-run"""
        
        self.auto_running = False
        self.step_button.config(state="normal")
        self.auto_button.config(state="normal")
        self.pause_button.config(state="disabled")
    
    def end_game(self, title, message, success):
        """Handle game end state"""
        
        self.game_over = True
        self.pause_auto()
        
        self.step_button.config(state="disabled")
        self.auto_button.config(state="disabled")
        
        if success:
            self.action_label.config(
                text="🏆 MISSION ACCOMPLISHED!",
                fg="#2E7D32",
                font=("Segoe UI", 14, "bold")
            )
        else:
            self.action_label.config(
                text="💀 MISSION FAILED",
                fg="#C62828",
                font=("Segoe UI", 14, "bold")
            )
        
        messagebox.showinfo(title, message)
    
    def reset(self):
        """Reset game to initial state"""
        
        self.world = World()
        self.agent = Agent(self.world)
        self.step_count = 0
        self.game_over = False
        self.auto_running = False
        
        self.step_button.config(state="normal")
        self.auto_button.config(state="normal")
        self.pause_button.config(state="disabled")
        
        self.action_label.config(
            text="⏸️  Ready to start simulation!",
            fg="#388E3C",
            font=("Segoe UI", 12)
        )
        
        self.update_display()


def main():
    """Launch the GUI application"""
    
    root = tk.Tk()
    app = WumpusGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🎮 Launching Wumpus World GUI...")
    print("="*60)
    print("Author: Mei Hsien Hsu")
    print("Course: CS4 - Introduction to Artificial Intelligence")
    print("Project: Final Project - Knowledge-Based Agent")
    print("Professor: An Lam")
    print("Institution: Las Positas College")
    print("="*60 + "\n")
    main()