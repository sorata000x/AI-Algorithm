# NOTE: do not modify this file
from game import Game, WHITE, BLACK
from ai import AI

TOL = 0.01

def load_UCB_arr(text):
    action_win_UCB_sol = {}
    for line in text.split("\n"):
        tokens = line.strip().split(" ")
        action_win_UCB_sol[(int(tokens[0]), int(tokens[1]))] = float(tokens[2])
    return action_win_UCB_sol


def deterministic_test():
    sols = []
    states = []

    with open("test_sols") as file:
        text = file.read()

        sols_text = text.split("\n\n")[:-1]
        
        for sol_text in sols_text:
            sols.append(load_UCB_arr(sol_text))
            
    with open("test_states") as file:
        states = file.readlines()

    states = [state[:-1] for state in states]

    assert(len(states) == len(sols))
    num_tests = len(states)
    test_num = 1
    for state, sol in zip(states, sols):
        print("test {}/{}".format(test_num, num_tests))
        game = Game()
        game.load_state_text(state)

        ai_player = AI(game.state())
        _, UCBs = ai_player.mcts_search()

        incorrect_cnt = 0
        for key in sol:
            if (UCBs[key] - sol[key] <= TOL and 
                UCBs[key] - sol[key] >= -TOL):
                pass
            else:
                print("Incorrect UCB for action:", key)
                print("yours/correct: {}/{}".format(UCBs[key], sol[key]))
                incorrect_cnt += 1
    
        

        print()
        if incorrect_cnt == 0:
            print("PASSED")
        else:
            print("FAILED")
        print()

        test_num += 1

MIN_WINS = 9
NUM_PLAYS = 10
def win_test():
    simulator = Game()
    wins = 0
    for play_i in range(NUM_PLAYS):
        print("play {}/{}".format(play_i + 1, NUM_PLAYS))
        simulator.reset(BLACK)
        ai_play = False
        while not simulator.game_over:
            if ai_play:
                ai_player = AI(simulator.state())
                (r,c), _ = ai_player.mcts_search()
            else:
                (r,c) = simulator.rand_move()

            simulator.place(r, c)
            ai_play = not ai_play

        if simulator.winner == WHITE:
            print("AI won.")
            wins += 1
        else:
            print("Random player won.")
        print()

    if wins < MIN_WINS:
        print("FAILED")
    else:
        print("PASSED")
