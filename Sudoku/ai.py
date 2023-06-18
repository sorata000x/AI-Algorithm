from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE, \
    sd_domain
import random, copy
import inspect

# Debug
# Reference: https://stackoverflow.com/questions/45621045/python-print-debugging-show-file-and-line-number
def print_reach_error():
    lineno = inspect.currentframe().f_back.f_lineno
    print(f"ERROR: Unexpected reach line {lineno}")

def check_draw_delim(ind):
    return ((ind + 1) != SD_SIZE) and ((ind + 1) % SD_DIM == 0)

def display(domains):
    for i in sd_domain:
        for j in sd_domain:
            d = domains[(i,j)]
            if len(d) == 1:
                print(d[0], end='')
            else: 
                print('.', end='')
            if check_draw_delim(j):
                print(" | ", end='')
        print()
        if check_draw_delim(i):
            print("-" * (SD_DIM * SD_DIM + 3 * (SD_DIM - 1)))

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem)

        # TODO: implement backtracking search. 
        assignments = {}     # (i, j): a
        decisions = []       # decision stack (see: https://www.geeksforgeeks.org/stack-in-python/)
        while True:
            assignments, domains = self.propagate(copy.deepcopy(assignments), copy.deepcopy(domains))
            if 'conflict' not in assignments:
                if self.allAssigned(assignments, domains):
                    return self.solution(assignments, domains)
                else:
                    assignments, s = self.makeDecision(copy.deepcopy(assignments), copy.deepcopy(domains))
                    decisions.append((copy.deepcopy(assignments), s, copy.deepcopy(domains)))
            else:
                if not decisions:
                    return None
                else:
                    assignments, domains, decisions = self.backtrack(copy.deepcopy(decisions))

        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignments function 
        #   and turn the value into a single element list and return them as a domain map. 
        # <- TODO: delete this block


    def propagate(self, assignments, domains):
        while True:
            for s in domains:
                if len(domains[s]) == 1 and not s in assignments:    # D(s) is singleton
                    assignments[s] = domains[s][0]
            for s in domains:
                if s in assignments and len(domains[s]) > 1:     # update domain
                    domains[s] = [assignments[s]]
            for s in domains:
                if len(domains[s]) == 0:
                    assignments['conflict'] = s      # conflict at s
                    return assignments, domains
            flag = False
            for s in domains:
                for p in sd_peers[s] :      # remove inconsistent value
                    for a in domains[s]:
                        if p in assignments and a == assignments[p]:
                            domains[s].remove(a)
                            flag = True
            if not flag:
                return assignments, domains
                
        
    def removeInconsistent(self, s, assignments, domains):
        flag = False
        for p in sd_peers[s] :      # remove inconsistent value
            for a in domains[s]:
                if p in assignments and a == assignments[p]:
                    domains[s].remove(a)
                    flag = True
        return flag, domains
    
    def allAssigned(self, assignments, domains):
        for s in domains:
            if s not in assignments:
                return False
        return True    
    
    def solution(self, assignments, domains):
        for s in assignments:
            domains[s] = [assignments[s]]
        return domains
    
    def makeDecision(self, assignments, domains):
        for s in domains:
            if s not in assignments:
                assignments[s] = domains[s][0]   # DECISION: always pick the first to assign
                return assignments, s
        print_reach_error()
        
    def backtrack(self, decisions):
        assignments, s, domains = decisions.pop()
        a = assignments[s]
        assignments.pop(s, None)
        domains[s].remove(a)
        return assignments, domains, decisions

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        
        var = {
            1: "-4 -3 -2  1  0\n",
            2: "-4 -3  2 -1  0\n",
            3: "-4 -3  2  1  0\n",
            4: "-4  3 -2 -1  0\n",
            5: "-4  3 -2  1  0\n",
            6: "-4  3  2 -1  0\n",
            7: "-4  3  2  1  0\n",
            8: " 4 -3 -2 -1  0\n",
            9: " 4 -3 -2  1  0\n",
        }
        
        domains = init_domains()
        restrict_domain(domains, problem)
        
        text = ""
        
        count = 0

        # TODO: write CNF specifications to 'text'
        for s in domains:
            for p in sd_peers[s]:
                if len(domains[p]) == 1:
                    count += 1
                    
        text += f"p cnf 4 {count}\n"
                    
        for s in domains:
            for p in sd_peers[s]:
                if len(domains[p]) == 1:
                    i = domains[p][0]
                    text += var[i]

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignmentss solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignmentss):
        # TODO: decode 'assignmentss' into domains
        print(assignmentss)
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
