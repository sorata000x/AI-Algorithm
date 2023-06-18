# NOTE: do not modify this file
from __future__ import absolute_import, division, print_function
import argparse
from game import Game, WHITE, BLACK, EMPTY, GRID_COUNT
from test import deterministic_test, win_test
from ai import AI

gen_tests = False

GRID_SIZE = 46
RADIUS = GRID_SIZE // 2
BOARD_START_X = 38
BOARD_START_Y = 55
EDGE_SIZE = GRID_SIZE//2
TEXT_POS = (10, 8)

HELP_TEXT = "{0} Click to place piece. Press Enter for rand/AI play and [m] for user/{1} play."

WHITE_COLOR = [255]*3
BLACK_COLOR = [0]*3

BORDER_COLOR = [0] * 3

BOARD_COLOR = [153,118,103]

TEXT_COLOR = [0] * 3
INACTIVE_COLOR = [70]*3
ACTIVE_COLOR = [0]*3

class Gomoku():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((530, 550))
        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("ariel",18)

        self.going = True
        self.game = Game(BLACK) # Initialize with 'b' since the first player to go is BLACK
        self.auto = False
        self.semiauto = True
        self.ai_play = False

    def loop(self):
        while self.going:
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

    def save_prob_arr(self, dictionary, filename="savedata_actions"):
        f = open(filename, "w")
        for key in dictionary:
            line = " ".join([str(key[0]), str(key[1]), str(dictionary[key])])
            f.write(line + "\n")
        f.close()

    def update(self):
        if self.ai_play:
            if not self.game.game_over:
                ai_player = AI(self.game.state())
                (r,c), win_rates = ai_player.mcts_search()
                if gen_tests:
                    self.game.save_state()
                    self.save_prob_arr(win_rates)
                self.game.place(r, c)
            self.ai_play = False
        else:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.going = False
                if e.type == MOUSEBUTTONDOWN:
                    self.auto = False
                    if self.semiauto:
                        if self.handle_key_event(e):
                            self.ai_play = True
                    else:
                        self.handle_key_event(e)
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        self.game.save_state()
                    if e.key == K_l:
                        self.game.load_state()
                    if e.key == K_RETURN:
                        self.auto = not self.auto
                    if e.key == K_SPACE:
                        self.auto = False
                        self.game.reset()
                    if e.key == K_m:
                        self.semiauto = not self.semiauto
            if self.auto:
                if not self.game.game_over:
                    r, c = self.game.rand_move()
                    self.game.place(r, c)
                    self.ai_play = True

    def draw(self):
        self.screen.fill((255, 255, 255))

        pygame.draw.rect(self.screen, BOARD_COLOR,
                         [BOARD_START_X - EDGE_SIZE, BOARD_START_Y - EDGE_SIZE,
                          (GRID_COUNT - 1) * GRID_SIZE + EDGE_SIZE * 2,
                          (GRID_COUNT - 1) * GRID_SIZE + EDGE_SIZE * 2], 0)
        # draw horizontal line
        for r in range(GRID_COUNT):
            y = BOARD_START_Y + r * GRID_SIZE
            pygame.draw.line(self.screen, INACTIVE_COLOR, [BOARD_START_X, y],
                             [BOARD_START_X + GRID_SIZE * (GRID_COUNT - 1), y], 2)

            if r in range(self.game.min_r, self.game.max_r + 1):
                x_start = BOARD_START_X + self.game.min_c * GRID_SIZE
                x_end = BOARD_START_X + self.game.max_c * GRID_SIZE
                pygame.draw.line(self.screen, ACTIVE_COLOR, [x_start, y],
                                 [x_end, y], 2)
        # draw vertical line
        for c in range(GRID_COUNT):
            x = BOARD_START_X + c * GRID_SIZE
            pygame.draw.line(self.screen, INACTIVE_COLOR, [x, BOARD_START_Y],
                             [x, BOARD_START_Y + GRID_SIZE * (GRID_COUNT - 1)], 2)
            if c in range(self.game.min_c, self.game.max_c + 1):
                y_start = BOARD_START_Y + self.game.min_r * GRID_SIZE
                y_end = BOARD_START_Y + self.game.max_r * GRID_SIZE
                pygame.draw.line(self.screen, ACTIVE_COLOR, [x, y_start],
                                 [x, y_end], 2)
        # draw pieces
        for r in range(GRID_COUNT):
            for c in range(GRID_COUNT):
                player = self.game.grid[r][c]
                if player != EMPTY:
                    piece_color = BLACK_COLOR if player == BLACK else WHITE_COLOR
                    x = BOARD_START_X + c * GRID_SIZE
                    y = BOARD_START_Y + r * GRID_SIZE
                    specs = [(0, RADIUS, piece_color)]
                    for width, radius, color in specs:
                        pygame.draw.circle(self.screen, color, [x, y], radius, width)
        # draw the winning line of five pieces
        if self.game.game_over:
            win_start, win_end = self.game.winning_pos
            start_pos = [BOARD_START_X + win_start[1] * GRID_SIZE,
                         BOARD_START_Y + win_start[0] * GRID_SIZE]
            end_pos = [BOARD_START_X + win_end[1] * GRID_SIZE,
                       BOARD_START_Y + win_end[0] * GRID_SIZE]
            pygame.draw.line(self.screen, (0, 200, 0), start_pos, end_pos, 6)

        if self.ai_play:
            self.screen.blit(self.font.render("AI Calculating...", True, (0, 0, 0)), TEXT_POS)                        
        elif self.game.game_over:
            self.screen.blit(self.font.render("{0} has won. Press [space] to restart".format("Black" if self.game.winner == 'b' else "White"), True, (0, 0, 0)), TEXT_POS)
        elif self.auto:
            self.screen.blit(self.font.render("rand/AI play.", True, (0, 0, 0)), TEXT_POS)                        
        elif self.semiauto:
            self.screen.blit(self.font.render(HELP_TEXT.format("User vs AI.", "user"), True, (0, 0, 0)), TEXT_POS)
        else:
            MANUAL_TEXT = "{0} Click to place piece. Press [m] to stop manual play."
            self.screen.blit(self.font.render(MANUAL_TEXT.format("Next to play: {0}.".format("Black" if self.game.player == BLACK else "White"), "AI"), True, (0, 0, 0)), TEXT_POS)
        pygame.display.update()

    def handle_key_event(self, e):
        #left-up corner coordinate
        origin_x = BOARD_START_X - EDGE_SIZE
        origin_y = BOARD_START_Y - EDGE_SIZE
        size = (GRID_COUNT - 1) * GRID_SIZE + EDGE_SIZE * 2
        pos = e.pos
        #Check the coordinates are in valid range
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            if not self.game.game_over:
                x = pos[0] - origin_x
                y = pos[1] - origin_y
                r = int(y // GRID_SIZE)
                c = int(x // GRID_SIZE)
                return self.game.place(r, c)

        return False

parser = argparse.ArgumentParser(description='Gomoku')
parser.add_argument('--test', '-t', dest="test", type=int, default=0, help='1: Test UCB values. 2: Test against random play.')
args = parser.parse_args()

if __name__ == '__main__':
    if args.test == 1:
        deterministic_test()
    elif args.test == 2:
        win_test()
    else:
        import pygame
        from pygame.locals import *
        game_runner = Gomoku()
        game_runner.loop()
