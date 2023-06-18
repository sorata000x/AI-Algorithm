# NOTE: do not modify this file
from __future__ import print_function
import copy

GRID_COUNT = 11

WHITE = 'w'
BLACK = 'b'
EMPTY = '.'

ROLLOUT_RNG_MAX = 1000;

class Game:
    def __init__(self, player=BLACK, grid=None):
        self.rollout_rng = 0
        self.reset(player, grid)

    # resets the board to the specified state;
    # randomly initalizes if no state provided
    def reset(self, player=BLACK, init_grid=None):
        self.winning_pos = None
        self.winner = None
        self.game_over = False
        self.player = player
        self.actions = []
        self.maxrc = (len(init_grid) - 1) if init_grid is not None else (GRID_COUNT - 1)
        self.max_r = self.max_c = self.min_r = self.min_c = (self.maxrc)//2

        if init_grid is not None:
            self.grid = copy.deepcopy(init_grid)
            self.populate(False)
        else:
            self.grid = self.new_grid(GRID_COUNT)
            self.populate()
            self.place(*(self.get_actions()[0]))
            self.place(*self.rand_move())

    def reset_maxes(self, r, c, in_reset=True):
        old_max_r = self.max_r
        old_min_r = self.min_r
        old_max_c = self.max_c
        old_min_c = self.min_c

        self.max_r = min(self.maxrc, max(self.max_r, r + 1))
        self.max_c = min(self.maxrc, max(self.max_c, c + 1))
        self.min_r = max(0, min(self.min_r, r - 1))
        self.min_c = max(0, min(self.min_c, c - 1))

        if in_reset:
            new_rs = []
            if (self.max_r != old_max_r):
                new_rs.append(self.max_r)
            if (self.min_r != old_min_r):
                new_rs.append(self.min_r)

            for new_r in new_rs:
                for cp in range(self.min_c, self.max_c+1):
                    self.actions.append((new_r, cp))
                    
            new_cs = []
            if (self.max_c != old_max_c):
                new_cs.append(self.max_c)
            if (self.min_c != old_min_c):
                new_cs.append(self.min_c)
            for new_c in new_cs:
                for rp in range(old_min_r, old_max_r+1):
                    self.actions.append((rp, new_c))

    def populate(self, in_reset=True):
        for r in range(0, self.maxrc + 1):
            for c in range(0, self.maxrc + 1):
                if self.grid[r][c] != EMPTY:
                    self.reset_maxes(r, c, in_reset)
                    self.check_win(r, c)

        for i in range(self.min_r, self.max_r+1):
            for j in range(self.min_c, self.max_c+1):
                if self.grid[i][j] == EMPTY:
                    if (i, j) not in self.actions:
                        self.actions.append((i,j))

    # returns the current game state
    def state(self):
        return (self.player, self.grid)

    def new_grid(self, grid_length):
        new_grid = []
        for i in range(grid_length):
            new_grid.append(list("." * grid_length))
        return new_grid

    # places the current player's piece in the specified location
    # and swaps players
    def place(self, r, c):
        if (r, c) in self.get_actions():
            self.actions.remove((r, c))
            self.grid[r][c] = self.player
            self.reset_maxes(r, c, True)

            self.check_win(r, c)
            if len(self.get_actions()) == 0:
                self.game_over = True
                self.winner = WHITE

            self.player = WHITE if self.player == BLACK else BLACK
            return True
        return False

    def check_win(self, r, c):
        runs = [ self.continuous_count_both(r, c, -1, 0),
                 self.continuous_count_both(r, c, 0, 1),
                 self.continuous_count_both(r, c, 1, 1),
                 self.continuous_count_both(r, c, -1, 1) ]
        
        max_run = max(runs, key=lambda x: x[1])

        if max_run[1] >= 5:
            self.winner = self.grid[r][c]
            self.game_over = True
            self.winning_pos = max_run[0]

    def continuous_count_both(self, r, c, dr, dc):
        start, start_count = self.continuous_count(r, c, dr, dc)
        end, end_count = self.continuous_count(r, c, -dr, -dc)
        return ((start, end), 1 + start_count + end_count)

    def continuous_count(self, r, c, dr, dc):
        start = (r, c)
        player = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < GRID_COUNT and 0 <= new_c < GRID_COUNT:
                if self.grid[new_r][new_c] == player:
                    result += 1
                    start = (new_r, new_c)
                else:
                    break
            else:
                break
            i += 1
        return start, result

    def get_actions(self):
        return self.actions

    # returns a randomly selected move from the set of possible actions
    def rand_move(self):
        self.rollout_rng = (self.rollout_rng + 1) % ROLLOUT_RNG_MAX
        return self.get_actions()[(self.rollout_rng) % len(self.actions)]

    def save_state(self, filename="savedata"):
        f = open(filename, "w")
        line = " ".join([str(self.grid[int(x / GRID_COUNT)][x % GRID_COUNT]) for x in range(0, GRID_COUNT**2)])
        f.write(self.player + " " + line)
        f.close()

    def load_state_text(self, text):
        split = text.split(' ')
        player_to_go = str(split[0])
        new_grid = self.new_grid(GRID_COUNT)
        for i in range(0, GRID_COUNT**2):
            new_grid[int(i / GRID_COUNT)][i % GRID_COUNT] = str(split[1+i])
        self.reset(player_to_go, new_grid)

    def load_state(self, filename="savedata"):
        f = open(filename, "r")
        line = f.readline()
        self.load_state_text(line)
        f.close()
