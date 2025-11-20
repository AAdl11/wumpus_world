# Wumpus World: Intelligent Agent System
## AI Knowledge-Based Reasoning in Uncertain Environments

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/Code%20Style-Professional-brightgreen.svg)]()

An advanced implementation of the classic Wumpus World problem, featuring knowledge-based reasoning, probabilistic inference, and strategic planning algorithms for autonomous decision-making in uncertain environments.

**Course Project:** CS4 Introduction to Artificial Intelligence  
**Institution:** Las Positas College  
**Semester:** Fall 2025  
**Instructor:** Professor An Lam  
**Completed:** November 2025

---

## 🎯 Project Overview

This project demonstrates practical integration of multiple AI techniques to create an intelligent agent capable of:

- **Logical Reasoning**: Using propositional and first-order logic for knowledge representation
- **Automated Inference**: Applying resolution-based theorem proving for safe navigation
- **Probabilistic Reasoning**: Handling uncertainty with Bayesian Networks
- **Strategic Planning**: Employing A* search and adversarial planning (Alpha-Beta pruning)
- **Goal-Directed Behavior**: Using backward chaining for plan generation

The system showcases how different AI paradigms work together to solve complex problems requiring perception, reasoning, and action under uncertainty.

---

## ✨ Core Features

### 🧠 Knowledge Representation & Reasoning

#### Propositional Logic Knowledge Base
- Rule-based representation of world knowledge
- Logical inference for deriving new facts
- CNF (Conjunctive Normal Form) conversion
- Efficient fact storage and retrieval

**Example Rules:**
```
¬Breeze(x,y) ⇒ ¬Pit(adjacent cells)
¬Stench(x,y) ⇒ ¬Wumpus(adjacent cells)
Safe(x,y) ← ¬Pit(x,y) ∧ ¬Wumpus(x,y)
```

#### First-Order Logic
- Quantified statements for expressive reasoning
- Universal (∀) and existential (∃) quantifiers
- Predicate logic for complex relationships
- Variable binding and unification

#### Automated Theorem Proving
- **Resolution Inference**: Proof by contradiction method
- **Forward Chaining**: Data-driven reasoning
- **Backward Chaining**: Goal-directed reasoning
- Efficient inference for real-time decision making

### 📊 Probabilistic Reasoning

#### Bayesian Networks
- Conditional probability tables (CPTs)
- Prior and posterior probability computation
- Belief propagation based on evidence
- Handles sensor uncertainty and incomplete information

**Network Structure:**
```
    Pit         Wumpus
     ↓             ↓
  Breeze       Stench
     ↓             ↓
  [Agent Perception]
```

**Use Case:** When agent perceives a breeze, Bayesian inference updates:
- Prior: P(Pit) = 0.2
- Posterior: P(Pit | Breeze) ≈ 0.73

### 🎮 Strategic Planning & Search

#### A* Search Algorithm
- Optimal pathfinding with admissible heuristics
- Manhattan distance heuristic for grid navigation
- Guarantees shortest safe path
- Efficient exploration strategy

#### Adversarial Search (Alpha-Beta Pruning)
- Game tree search with pruning optimization
- Handles moving opponents (dynamic Wumpus)
- Minimax decision making
- Reduces search space significantly

**Feature:** Agent can handle environments where the Wumpus actively moves, requiring strategic anticipation and counter-planning.

### ⚙️ Advanced Capabilities

#### Scalable World Sizes
- Configurable grid dimensions (4x4, 8x8, or custom)
- Performance optimization for larger spaces
- Adaptive exploration strategies

#### Resource Management
- Limited arrow resource for Wumpus elimination
- Strategic decision: when to eliminate vs. avoid
- Risk-reward calculation

#### Goal-Directed Planning
- Backward chaining from goals to actions
- Subgoal decomposition
- Plan generation and execution

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│               Wumpus World Environment                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   Grid   │  │ Wumpus   │  │   Pits   │             │
│  │  World   │  │  (Threat)│  │(Hazards) │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────────┬────────────────────────────────────┘
                     │ Percepts
                     ↓
┌─────────────────────────────────────────────────────────┐
│              Intelligent Agent System                   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │         Knowledge Representation Layer          │   │
│  │  ┌────────────────┐  ┌─────────────────────┐   │   │
│  │  │ Propositional  │  │  First-Order Logic  │   │   │
│  │  │   Logic KB     │  │   Representation    │   │   │
│  │  └────────────────┘  └─────────────────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │            Reasoning Engine Layer               │   │
│  │  ┌────────────┐  ┌──────────┐  ┌────────────┐  │   │
│  │  │ Resolution │  │ Forward  │  │ Backward   │  │   │
│  │  │ Inference  │  │ Chaining │  │ Chaining   │  │   │
│  │  └────────────┘  └──────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │       Probabilistic Reasoning Layer             │   │
│  │  ┌────────────────────────────────────────┐     │   │
│  │  │      Bayesian Network                  │     │   │
│  │  │  (Conditional Probability Tables)      │     │   │
│  │  └────────────────────────────────────────┘     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │         Planning & Search Layer                 │   │
│  │  ┌──────────┐  ┌────────────┐  ┌────────────┐  │   │
│  │  │ A* Search│  │ Alpha-Beta │  │  Decision  │  │   │
│  │  │          │  │  Pruning   │  │   Theory   │  │   │
│  │  └──────────┘  └────────────┘  └────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ Actions
                     ↓
┌─────────────────────────────────────────────────────────┐
│               Actuators (Movement, Arrow)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- No external dependencies (uses Python standard library only)

### Installation

```bash
# Clone the repository
git clone https://github.com/AAdl11/wumpus_world.git
cd wumpus_world

# Run the main program
python main.py
```

### Basic Usage

#### CLI Mode
```bash
# Start interactive CLI
python main.py

# Options in menu:
# 1. Propositional Logic Demo
# 2. Resolution Inference Demo
# 3. Bayesian Networks Demo
# 4. Backward Chaining Demo
# 5. Basic Simulation (4x4)
# 6. Large World Simulation (8x8)
# 7. Adversarial Mode (Moving Wumpus)
```

#### GUI Mode
```bash
# Launch graphical interface
python gui.py
```

### Running Specific Configurations

```bash
# 4x4 world with static Wumpus
python main.py --size 4 --static

# 8x8 world with moving Wumpus
python main.py --size 8 --moving-wumpus

# Custom pit probability
python main.py --size 6 --pit-prob 0.3
```

---

## 📊 Technical Specifications

### Performance Metrics
| Metric | Value |
|--------|-------|
| Lines of Code | ~2,500+ |
| Number of Classes | 15+ |
| Algorithms Implemented | 8+ |
| Supported World Sizes | 4x4 to 8x8+ |
| Average Solve Time (4x4) | < 2 seconds |
| Average Solve Time (8x8) | < 10 seconds |

### Code Quality
- **Architecture**: Modular, object-oriented design
- **Documentation**: Comprehensive inline comments
- **Testing**: Unit tests and integration tests
- **Code Style**: PEP 8 compliant
- **Maintainability**: Clean separation of concerns

### Algorithm Complexity
- **A* Search**: O((V+E) log V) with priority queue
- **Resolution**: Exponential worst case, polynomial average case
- **Bayesian Inference**: O(n) for simple queries, exponential for complex networks
- **Alpha-Beta Pruning**: O(b^(d/2)) with good ordering

---

## 📖 Course Integration

### Concepts Demonstrated

This project integrates concepts from CS4 curriculum:

**Lab 8: Propositional Logic**
- Truth tables and logical equivalence
- Knowledge base implementation
- Inference rules

**Lab 9: First-Order Logic & Resolution**
- Predicate logic with quantifiers
- Resolution theorem proving
- Unification algorithms

**Chapter 13: Probabilistic Reasoning**
- Bayesian Networks
- Conditional probability
- Belief propagation

**Chapter 6: Adversarial Search**
- Minimax algorithm
- Alpha-Beta pruning optimization
- Game tree search

**Chapter 3: Search Algorithms**
- A* pathfinding
- Heuristic functions
- Optimal search strategies

---

## 🎓 Educational Value

### Learning Outcomes

This project demonstrates:

1. **Knowledge Representation**
   - How to represent world knowledge formally
   - Trade-offs between different representation schemes

2. **Logical Reasoning**
   - Automated inference techniques
   - Proof methods and their applications

3. **Uncertainty Handling**
   - When and how to use probabilistic methods
   - Bayesian reasoning principles

4. **Strategic Planning**
   - Heuristic search algorithms
   - Game-theoretic decision making

5. **System Integration**
   - Combining multiple AI techniques
   - Designing modular, extensible systems

---

## 🔬 Technical Implementation

### Key Algorithms Implemented

1. **Propositional Logic KB** (`logic/propositional.py`)
   - Fact storage and retrieval
   - Rule-based inference
   - Safety proofs

2. **Resolution Inference** (`logic/resolution.py`)
   - CNF conversion
   - Resolution proof method
   - Automated theorem proving

3. **Bayesian Networks** (`reasoning/bayesian.py`)
   - Prior probability maintenance
   - Bayes' theorem application
   - Posterior probability calculation

4. **A* Search** (`search.py`)
   - Priority queue implementation
   - Manhattan distance heuristic
   - Path reconstruction

5. **Alpha-Beta Pruning** (`reasoning/alpha_beta.py`)
   - Game tree search
   - Pruning optimization
   - Move ordering

---

## 🎯 Real-World Applications

### Analogous Problems

1. **Autonomous Navigation**
   - Self-driving cars avoiding obstacles
   - Drone navigation in unknown environments

2. **Medical Diagnosis**
   - Symptom-based disease inference
   - Treatment planning under uncertainty

3. **Cybersecurity**
   - Threat detection in networks
   - Intrusion response planning

4. **Resource Management**
   - Supply chain optimization
   - Emergency response coordination

---

## 🔮 Future Enhancements

### Potential Extensions

- [ ] **Machine Learning Integration**
  - Train agent using reinforcement learning
  - Compare learned vs. programmed strategies
  
- [ ] **Enhanced Visualization**
  - Real-time reasoning visualization
  - Knowledge base state display
  
- [ ] **Multi-Agent Scenarios**
  - Cooperative agents
  - Communication and coordination
  
- [ ] **Web Interface**
  - Browser-based UI
  - Online demonstrations

- [ ] **Performance Optimization**
  - Parallel processing for larger worlds
  - Caching and memoization

---

## 📈 Project Timeline

| Phase | Status | Description |
|-------|--------|-------------|
| **Phase 1** | ✅ Complete | Core Wumpus World environment |
| **Phase 2** | ✅ Complete | Propositional logic KB |
| **Phase 3** | ✅ Complete | First-order logic & Resolution |
| **Phase 4** | ✅ Complete | Bayesian Networks |
| **Phase 5** | ✅ Complete | Advanced search (A*, Alpha-Beta) |
| **Phase 6** | ✅ Complete | GUI and visualization |
| **Phase 7** | ✅ Complete | Documentation and testing |
| **Phase 8** | 📋 Future | ML integration |

---

## 👤 Author

**Mei Hsien Hsu**

- 🎓 Computer Science Student at Las Positas College
- 🎯 Transfer Goal: UC Berkeley / Stanford
- 📚 Focus: Artificial Intelligence, Logic, Probabilistic Reasoning
- 💼 16 years of volunteer service with Tzu Chi Foundation

### Connect
- GitHub: [@AAdl11](https://github.com/AAdl11)
- Project Repository: [wumpus_world](https://github.com/AAdl11/wumpus_world)

---

## 🙏 Acknowledgments

This project builds upon foundational AI concepts from:

- **Russell, S. & Norvig, P.** - *Artificial Intelligence: A Modern Approach* (4th Edition)
- **Course**: CS4 Introduction to AI - Las Positas College
- **Instructor**: Professor An Lam

Special thanks to the AI education community for excellent resources and support.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Academic Use

If you use this code for academic work, please cite:

```
Hsu, M. H. (2025). Wumpus World: Intelligent Agent System with Knowledge-Based 
Reasoning and Probabilistic Inference. CS4 Final Project, Las Positas College. 
https://github.com/AAdl11/wumpus_world
```

---

## 📞 Support

- 📧 Issues: [GitHub Issues](https://github.com/AAdl11/wumpus_world/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/AAdl11/wumpus_world/discussions)
- 📖 Wiki: [Project Wiki](https://github.com/AAdl11/wumpus_world/wiki)

---

## 🌟 Project Stats

If you find this project useful for learning AI concepts, please consider giving it a star ⭐!

---

**Last Updated:** November 19, 2025  
**Version:** 2.0.0  
**Status:** Active Development 🚀

---

> *"In a world of uncertainty, intelligent agents must reason logically, infer probabilistically, and act strategically."*  
> — CS4 Introduction to Artificial Intelligence