Assignment 5: Sudoku
=========
DO NOT FORK

Due date
-----
Jun-11 (Sunday) 11:59pm. Again only submit the `ai.py` file. 

Task
-----
Implement a constraint solver for Sudoku puzzles using backtracking search. Pseudocode is given in `pseudocode.pdf`. 

When making decisions, we recommend using the heuristic of **choosing an unassigned variable with the smallest domain**. You can see the difference with and without this heuristic. But as long as you pass the following tests, you do not have to use this heuristic. 

For testing, there are four options you can use with "python main.py -t ...":
- 0: "Propagation only" test. A really simple test case that can be solved without search.
- 1: "Propagation and search" test. A hard test case that requires both propagation and search.
- 2: Provides 50 easy test cases. 
- 3: Provides 50 hard test cases. 

We are setting a 20 seconds timeout on each instance. To pass the tests, you can timeout on 2 instances in the easy class ('-t 2') and up to 30 instances in the hard class ('-t 3'), because the runtime may have large variance based on your branching methods.

For this assignment, you get full score as long as you pass the given tests, with the allowed timeout cases. 

Extra credit (5 Points)
-----
This EC part is designed to be a bit "research-oriented" and encourages you to explore more on the topic of SAT solving. It is completely optional. 

The course staff will NOT answer questions regarding the EC part of this assignment.

The EC task is to implement an encoding of Sudoku as propositional logic formulas in conjunctive normal forms, and use a state-of-the-art SAT solver to solve. Read the `cnf-notes.pdf` file for more details on the format of the encoding. The `example.cnf` file shows an example of the file format. 

You need to solve the same puzzles but through generating CNF files. In the `ai.py` file there are function templates you can use. Pass the encodings to a SAT solver (see below) to solve, and then parse the output from the SAT solver and plug them back into the original problem, and put the solutions in the same format (pass them as domains to the test scripts). You can run "python main.py -e" with the same "-t" options as above, to test the results using SAT solvers. 

If you have done things correctly, you should see that all hard puzzles will be solved quickly (most of the time is spent on creating the CNF file). You get full EC if all hard instances ("-t 3") pass the test. 

SAT Solvers to Use: The source code of the popular picosat solver [PicoSAT](http://fmv.jku.at/picosat/) is already included as a directory. In that directory, simply do `./configure.sh` and then `make` to build the tool, and then the binary `picosat` can take the CNF files you produce (always use extension `.cnf`). Try the example.cnf file with it (first move the picosat executable to the top directory and then `./picosat example.cnf`). Note that the test script also assumes that `picosat` is in the same directory of as the `main.py` file, so make sure to move it to the right place after you've built it. 

We highly recommend using linux/mac machine to compile and run picosat. If you have to use windows, this [note](https://gist.github.com/ConstantineLignos/4601835) may be helpful but I haven't tried. If you have difficulty in getting PicoSAT to work, try [cryptominisat](https://github.com/msoos/cryptominisat) which has more instructions about making things work on windows. If you want to know about more SAT solvers, check the [page](http://www.satcompetition.org/) for the annual SAT solver competition. 

