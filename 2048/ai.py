from __future__ import absolute_import, division, print_function
import copy, random
from inspect import getframeinfo, currentframe

from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MOVES_EC = {0: 'up', 1: 'left', 3: 'right', 2: 'down'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1
MOVE_CHANCE = 1/len(MOVES)

# debug
frameinfo = getframeinfo(currentframe())

def print_line():
    print(f'print line: {frameinfo.lineno}')

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])   # tile_state, score

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return not bool(self.children)

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    # root_state = (tile_state, score)
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)
        self.ec = False

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: Test the function
    # build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0):
        if not node or depth == 0:  # base case
            return
        if node.player_type == MAX_PLAYER:
            if not self.ec:     # normal tree
                for move in MOVES:
                    self.simulator.set_state(node.state[0], node.state[1])  # reset the state
                    self.simulator.move(move)
                    if self.simulator.current_state() != node.state:  # only add valid move
                        node.children.append((move, Node(self.simulator.current_state(), CHANCE_PLAYER)))
            else:   # extra smart tree
                for move in MOVES_EC:
                    self.simulator.set_state(node.state[0], node.state[1])  # reset the state
                    self.simulator.move(move)
                    if self.simulator.current_state() != node.state:
                        # focus on up and left
                        if move != MOVES_EC[3] or node.is_terminal():  # only go right if can't go up or left
                            node.children.append((move, Node(self.simulator.current_state(), CHANCE_PLAYER)))
                        if move != MOVES_EC[2] or node.is_terminal():  # only go down if no other choice
                            node.children.append((move, Node(self.simulator.current_state(), CHANCE_PLAYER)))
        elif node.player_type == CHANCE_PLAYER:
            # simulate for each tile place for each child
            for i in range(0, self.simulator.board_size):
                for j in range(0, self.simulator.board_size):
                    self.simulator.set_state(node.state[0], node.state[1])  # reset the state
                    if self.simulator.tile_matrix[i][j] == 0:
                        new_tile_matrix = copy.deepcopy(self.simulator.tile_matrix)
                        new_tile_matrix[i][j] = 2
                        self.simulator.set_state(new_tile_matrix, self.simulator.score)
                        node.children.append((None, Node(self.simulator.current_state(), MAX_PLAYER)))
        self.simulator.set_state(node.state[0], node.state[1])  # reset the state
        # build subtree recursively
        for i in range(len(node.children)):
            self.build_tree(node.children[i][1], depth-1)

    def shape_score(self, tile_matrix):
        ADJACENT_SCORE = 10
        score = 0

        sorted_tiles = sorted([item for sublist in tile_matrix for item in sublist], reverse=True)

        col_num = range(0, self.simulator.board_size)
        # prioritize 'locked' row
        for c in col_num:
            if c == self.simulator.board_size-1:
                score *= 2
            elif tile_matrix[c][0] > tile_matrix[c+1][0] and tile_matrix[c][0] == sorted_tiles[c]:
                score += tile_matrix[c][0] * 2
            else:
                break
        """
        # tile propagation (not sure how useful it actually is)
        for i in range(0, self.simulator.board_size-1):
            for j in range(0, self.simulator.board_size-1):
                if tile_matrix[i][j] > tile_matrix[i+1][j] or tile_matrix[i][j] > tile_matrix[i][j+1]:
                    score += tile_matrix[i][j]
                else:
                    break
        """

        # want adjacent tiles
        DIRECTION = [(1,0), (-1,0), (0,1), (0,-1)]
        for i in range(0, self.simulator.board_size):
            for j in range(0, self.simulator.board_size):
                for d in DIRECTION:
                    if 0 <= i+d[0] < self.simulator.board_size and 0 <= j+d[1] < self.simulator.board_size:
                        if tile_matrix[i][j] == tile_matrix[i+d[0]][j+d[1]]:
                            score += tile_matrix[i][j]
                            break
        return score

    # TODO: Test the function
    # Calculate expectimax
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        if node.is_terminal():
            if not self.ec:
                return None, node.state[1]
            else:
                return None, node.state[1] + self.shape_score(node.state[0])
        if node.player_type == MAX_PLAYER:
            value = float('-inf')
            direction = None
            for n in node.children:
                exp = self.expectimax(n[1])[1]
                if value < exp:
                    value = exp
                    direction = int(n[0])
            return direction, value
        if node.player_type == CHANCE_PLAYER:
            value = 0
            for n in node.children:
                value = value + self.expectimax(n[1])[1] * 1/len(node.children)
            return None, value
        print(f'ERROR: Unexpected line reached: {frameinfo.filename}: {frameinfo.lineno}')
        return None, -1

    def print_tree(self, node, level=0):
        #print(f"level: {level} | node: {node.state}")
        for n in node.children:
            #print(f'd: {n[0]}', end=' | ')
            self.print_tree(n[1], level+1)

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        self.print_tree(self.root)
        direction, _ = self.expectimax(self.root)
        #print(f'direction: {MOVES[direction]}')
        return direction

    # TODO (optional): implement method for extra credits
    # Reference: https://www.gameskinny.com/lnagr/2048-game-strategy-how-to-always-win-at-2048
    def compute_decision_ec(self):
        self.ec = True
        self.build_tree(self.root, self.search_depth)
        self.print_tree(self.root)
        direction, _ = self.expectimax(self.root)
        # print(f'direction: {MOVES[direction]}')
        return direction

"""
    # TODO: Test the function
    # Calculate expectimax
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        if node.is_terminal():
            return None, node.state[1]
        if node.player_type == MAX_PLAYER:
            value = float('-inf')
            direction = None
            for n in node.children:
                if node_big_tile_corner_score < n'':
                    corner_score = expectimax(n)
                if value < self.expectimax(n[1])[1]:
                    value = self.expectimax(n[1])[1]
                    direction = int(n[0])
            return direction, value
        if node.player_type == CHANCE_PLAYER:
            value = 0
            for n in node.children:
                value = value + self.expectimax(n[1])[1] * 1/len(node.children)
            return None, value
        print(f'ERROR: Unexpected line reached: {frameinfo.filename}: {frameinfo.lineno}')
        return None, -1
"""