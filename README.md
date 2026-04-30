# EC327-FinalProject-FenwayTetris


Fenway Tetris is a Tetris-style game built in Python using pygame. It follows the core mechanics of Tetris while adding a Boston/Fenway theme through custom colors, images, and layout design.

Description: The player controls falling blocks and must arrange them to complete full rows. When a row is filled, it is cleared and the score increases. As more lines are cleared, the game gradually speeds up, making it more challenging over time.
The entire implementation is contained in a single Python file.

Features:
- Tetris movement and rotation
- Hard drop functionality
- Score tracking system
- Increasing difficulty based on rounds
- Pause and game over states
- Start screen and sidebar with instructions

Controls
- Left / Right arrows: move piece
- Down arrow: move piece down
- Up arrow: rotate piece
- Space: hard drop
- Enter: start game
- P: pause
- Esc: exit
  
Setup and Execution:

Install Python (version 3 recommended)
Install pygame:

 pip install pygame


Ensure the following files are in the same directory:

- Python game file
- fenwaypark.png
- redsoxplayer.png
- Jersey10-Regular.ttf

Run the program:

 python filename.py




Implementation Notes:

The board is represented as a 2D list
Block shapes are defined using nested lists
A main class (TetrisEngine) manages game logic, rendering, and input handling
Movement and rotation are validated before being applied
Line clearing updates both the board and the score
Additional Notes
The game runs in fullscreen mode
Speed increases after clearing a set number of lines
The game ends when no new pieces can be placed

Authors:
Tatiana Boothe and Camila Bautista 
developed this as part of an academic project.
