# Description
2048 is a very simple game. This is a very simple implementation of it.
For a better implementation, [check out this link](https://gabrielecirulli.github.io/2048/)

# Intent
The purpose of me creating this is that I want to implement an AI, or rather multiple AIs to solve it.
For one AI, I want to have it beat the game using as few moves as possible.
For the other AI, I want to have it beat the game with the highest score possible.

For my initial attempt, I will make an AI using a minimax algorithm, using 4 different branches representing the 4 cardinal directions. The branch that has the highest merges will be the one selected.

# To use
The program uses the [curses library](https://docs.python.org/3/howto/curses.html) for input/output. I am not sure if this is os agnostic.
