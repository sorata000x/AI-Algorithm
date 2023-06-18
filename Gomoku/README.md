# Assignment 4: Gomoku with Monte Carlo Tree Search

Your task is to implement MCTS for playing Gomoku. The base game engine is from [here](https://github.com/HackerSir/PygameTutorials/tree/master/Lesson04/Gomoku). 

Again, DO NOT publicly fork this repositiory. 

## Due date

May-28 Sunday 11:59pm. 

As usual, only submit the `ai.py` file on Gradescope. 


## The Game

Gomoku is a popular game played on the Go board, following much simpler rules. 

- There are two players, one placing black pieces and the other white pieces, at the grid intersections of the board. 
- The two players take turns to place one piece each time. Pieces are never moved or removed from the board. 
- The players' goal is to have five pieces of their own color to form an unbroken line horizontally (`examples/ex1.png`), vertically (`examples/ex2.png`), or diagonally (`examples/ex3.png`). Of course, these are unlikely realistic games between reasonable players. A real game is more like `examples/ex4.png` (black is still very lame at the end).  
- The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

Here's a youtube video of a competitive Gomoku game (in case you're interested, or want to procrastinate): https://www.youtube.com/watch?v=siYgHaEwmZU&ab_channel=SandraJones

## Tasks

Implement MCTS in `ai.py`. Read the comments carefully.

Note that the starter code makes it clear that your MCTS should return more than just one action in the end, but also the table of winning rates for all actions for the root node (number of wins divided by total number of samples, i.e., the X-bar term in the best child formula). The tests compare these values that you compute with the correct ones for a few predefined states. 

In MCTS, the search exits when the "computation budget" is reached. The current default value is 1000, which will be used for testing. You can increase or decrease it to see the different behaviors of AI. For instance, with a budget over 6000, a correctly implemented MCTS AI should be able to play a fairly interesting game against you (although it may still make some obvious mistakes when the number of next actions to consider gets larger). 

Check the MCTS-1000.mov and MCTS-6000.mov files in the repo for a demo of the correctly implemented MCTS with 1000 and 6000 budgets respectively. There is randomness, so the behavior of your implementation does not need to exactly match the video. 

It is easy to see that good moves should be pretty close to the pieces already on the board. Thus, to accelerate search, we have limited the search to a small "active" area around existing pieces (this area uses black lines on the board, compared to grey lines in the inactive area). 

## Usage

To run the program, do:
```
python main.py
```

To run tests for the winning rate table in several predefined states, do:
```
python main.py -t 1
```

To run AI against random policy, do:
```
python main.py -t 2
```

The game engine starts with human against a random-play agent. Click any grid intersections and see what the computer does. Press enter to see a random game between two random-play agents (also press enter to pause autoplay and switch back to human vs random). Press 'm' to switch to manually playing both sides.  

More details can be found in `Tests` section below.

## Tests

- `python main.py -t 1` runs tests for the winning rate table in several predefined states. Note that a budget of 1000 runs and parameter c=1 in the `best_child` function is used in the test cases. Note that the order in the table is important. To pass the tests, make sure to follow the instructions in the `ai.py` starter code. 

- `python main.py -t 2` runs your AI against a random policy. Your AI should always win. 

Because the -t 1 tests rely on how the random states are generated, you may have a correct implementation that fails it. Still, the test should be valuable for you to debug. We will mostly check the -t 2 tests to see if you are close to getting things right. As usual, the overall correctness is determined by manual grading, and the tests are just heuristics. 


## Optional: Competition

The game gives you an opportunity for testing out many approaches that have been covered in the class. For instance, what kind of heuristic evaluation function can you use to improve the performance? Can you run some form of reinforcement learning to automatically come up with value estimates that can help the MCTS agent? 

You can spend time to try out any strategies you like, to maximize the strength of your AI agent within given computational budget. We will run a small tournament during Week 10. There will be a separate, completely optional, assignment in Gradescope named "EC: Gomoku Competition" for you to submit to, if you would like to participate in the competition. The submission deadline is the same as the due date of the PA. Implement all you need still only in ai.py and do not use any imports that fail to compile on the autograder. 

Only work on this part if you are really interested and have the time. We will not specify a fixed amount of extra credits so that you feel the need of doing it just for the points, but submissions that perform well and implement interesting ideas will receive additional credits. In fact, if you are aiming for A+ in the class (which will be determined by soft rules when we give grades at the end), participating in this competition can be useful. 

## Tips/FAQ

- You can check this [survey article](http://www.incompleteideas.net/609%20dropbox/other%20readings%20and%20resources/MCTS-survey.pdf) for more info on MCTS. 

- If you aren't already, check out `pdb` to help you debug!
