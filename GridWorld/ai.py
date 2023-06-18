from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = [[0, self.grid.start]]
            self.explored = []
        elif self.type == "astar":
            heu = abs(self.grid.start[0]-self.grid.goal[0]) + abs(self.grid.start[1]-self.grid.goal[1])
            self.frontier = [(0+heu, self.grid.start)]
            heapify(self.frontier)
            self.explored = []

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    def dfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        # Also search the goal in frontier to speed up the search
        for n in self.frontier:
            if n == self.grid.goal:
                self.finished = True
                return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and \
                        not self.grid.nodes[n].color_checked and \
                        not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop(0)      # Pop from frontier as a queue

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            self.finished = True
            return

        # Also search the goal in frontier to speed up the search
        for n in self.frontier:
            if n == self.grid.goal:
                self.finished = True
                return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and \
                        not self.grid.nodes[n].color_checked and \
                        not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current
                    self.frontier.append(n)
                    self.grid.nodes[n].color_frontier = True

    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        self.frontier.sort(reverse=True)
        current = self.frontier.pop()

        # Finishes search if we've found the goal.
        if current[1] == self.grid.goal:
            self.finished = True
            return

        # Also search the goal in frontier to speed up the search
        for n in self.frontier:
            if n[1] == self.grid.goal:
                self.finished = True
                return

        children = [(current[1][0] + a[0], current[1][1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current[1]].color_checked = True
        self.grid.nodes[current[1]].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                if not self.grid.nodes[n].puddle and \
                        not self.grid.nodes[n].color_checked and \
                        not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current[1]
                    self.frontier.append([current[0]+self.grid.nodes[n].cost(), n])
                    self.grid.nodes[n].color_frontier = True
            else:
                for f in self.frontier:
                    if f[1] == n and f[0] > current[0]+self.grid.nodes[n].cost():
                        self.previous[n] = current[1]
                        self.frontier.remove(f)
                        heappush(self.frontier, (current[0]+self.grid.nodes[n].cost(), n))
                        self.grid.nodes[n].color_frontier = True

    def astar_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return

        current = heappop(self.frontier)

        # Finishes search if we've found the goal.
        if current[1] == self.grid.goal:
            self.finished = True
            return

        # Also search the goal in frontier to speed up the search
        for n in self.frontier:
            if n[1] == self.grid.goal:
                self.finished = True
                return

        children = [(current[1][0] + a[0], current[1][1] + a[1]) for a in ACTIONS]
        self.grid.nodes[current[1]].color_checked = True
        self.grid.nodes[current[1]].color_frontier = False

        for n in children:
            if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                curHeu = abs(current[1][0] - self.grid.goal[0]) + abs(current[1][1] - self.grid.goal[1])
                real = current[0] - curHeu + self.grid.nodes[n].cost()
                heu = abs(n[0] - self.grid.goal[0]) + abs(n[1] - self.grid.goal[1])
                cost = real+heu
                if not self.grid.nodes[n].puddle and \
                        not self.grid.nodes[n].color_checked and \
                        not self.grid.nodes[n].color_frontier:
                    self.previous[n] = current[1]
                    heappush(self.frontier, (cost, n))
                    self.grid.nodes[n].color_frontier = True
                else:
                    for f in self.frontier:
                        if f[1] == n and f[0] > cost:
                            self.previous[n] = current[1]
                            self.frontier.remove(f)
                            heappush(self.frontier, (cost, n))
                            self.grid.nodes[n].color_frontier = True
