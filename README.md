# ♟️ Python Chess Engine

A fully functional, object-oriented chess engine built from scratch in Python using Pygame. 

This project goes beyond a simple 2D board game by implementing a highly efficient, mathematically rigorous rules engine. It calculates absolute pins, restricts paralyzed pieces, and seamlessly manages complex board states and edge cases like En Passant and Castling.

## 🚀 Technical Highlights

Building the rules of chess requires handling massive amounts of edge cases and state memory. Here is how this engine solves them:

* **Advanced Move Generation:** Instead of a naive approach that simulates every possible move to check for legality, this engine uses mathematical algorithms (ray-casting style) to identify absolute pins, checks, and sliding trajectories (Queens, Rooks, Bishops) instantly.
* **Robust State Management:** Implemented a chronological state timeline (History Logs) to track transient game states. This guarantees flawless execution of the "Undo" function without corrupting castling rights or En Passant ghost squares.
* **Complex Edge Cases Solved:**
  * **Castling:** Verifies intermediate squares are completely empty and untouched by enemy attack rays before permitting the King and Rook to swap.
  * **En Passant:** Tracks a 1-turn "ghost square" memory that correctly expires if not immediately acted upon.
  * **Pawn Promotion:** Automatically detects final-rank advancement.

## 🧠 Architecture

The codebase is strictly separated into two main components following standard MVC (Model-View-Controller) design principles:

* `ChessEngine.py` **(The Model):** The brain of the operation. It stores the `GameState`, determines valid moves, keeps a move log, and handles all board logic. Completely independent of the UI.
* `ChessMain.py` **(The View & Controller):** Handles the Pygame GUI, captures user mouse clicks, renders graphics (featuring a classic green and white tournament board), and updates the display based on the engine's current state.

## 💻 Installation and Usage

To run this project locally on your machine, you will need Python 3 and Pygame installed.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/HarshitSRIVASTAVA00/CHESS-ENGINE.git](https://github.com/HarshitSRIVASTAVA00/CHESS-ENGINE.git)
   cd CHESS-ENGINE
