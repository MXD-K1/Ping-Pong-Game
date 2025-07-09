# Ping Pong Game
A simple two-player Pong game where players compete to keep the ball in play and score points.
The main purpose of making this game is to enhance my skills further and to practice programming.
I started this project from scratch to simulate the process of understanding the requested tasks to make a project.

## Features
1. Basic classic Pong mechanics.
2. Player vs Player mode.
3. Basic UI for score display.
4. Simple menu setting to change colors.

## How to Run
1. Clone this repository to your local machine.
2. Ensure Python is installed (Python version >= 3.6 is required).  
   *You can verify your Python version with:*
   ```bash
   python --version
   ```
3. Install the required dependencies:
   ```bash
   pip install pygame
   ```
4. If you are not in code file write this into the terminal:
    ```bash
   cd code
   ```
5. Run the main script:
   ```bash
   python main.py
   ```

## Controls
1. To move the first paddle use the keys w, s.
2. To move the second paddle use the up and down arrow keys.
3. To get out use k the reason is that it is far form the first player movement keys.

## Problems
1. The colors system is somehow complex.
2. the box color in the settings is yellow , so when changing an item color to yellow they become one.
   To understand what I mean see the [image](images/matching color problem.png)
3. Calling `level.reinit()` continuously without the need to do so.
4. The ball move weirdly sometimes when meeting the paddle or the two horizontal edges.

## Contributing
Contributions to this project are welcome and encouraged!
Whether it's improving the code, fixing problems, suggesting new features, or sharing ideas, feel free to get involved.
    
---
*To contribute:*
- Fork the project.
- Make your changes.
- Create a pull request!

## License
This project is open-source and available under the MIT License. Feel free to use, modify, and distribute the code,
provided proper attribution is given. For more information see the included [license](LICENSE).

## Contact
For any questions, issues, or feedback, don't hesitate to open an issue on GitHub or email me at hmdoonwork71@gmail.com.
