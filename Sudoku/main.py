# NOTE: do not modify
from ai import AI
from game import sd_domain, init_domains, restrict_domain, sd_spots,\
    SD_DIM, SD_SIZE
import time, argparse
import multiprocessing
import os

parser = argparse.ArgumentParser(description='Sudoku')
parser.add_argument('--test', '-t', dest="test", type=int, default=0, \
    help='0: propagation only test case; \
          1: propagation and search test case; \
          2: all "easy" test cases; \
          3: all "hard" test cases'
)

parser.add_argument('--display', '-d', dest="disp", type=bool, default=False, \
    nargs='?', const=True, \
    help='fully display all tests'
)

parser.add_argument('--extra', '-e', dest="ec", type=bool, default=False, \
    nargs='?', const=True, \
    help='test EC'
)

args = parser.parse_args()

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

def verify(domains, orig_domains):
    for spot in sd_spots:
        domain = domains[spot]
        if len(domain) > 1:
            return False
        if domain[0] not in orig_domains[spot]:
            return False
    
    # verify every row unit
    for row in sd_domain:
        seen = []
        for column in sd_domain:
            num = domains[(row, column)][0]
            if num in seen:
                return False
            seen.append(num)

    # verify every column unit
    for column in sd_domain:
        seen = []
        for row in sd_domain:
            num = domains[(row, column)][0]
            if num in seen:
                return False
            seen.append(num)

    #verify every square unit
    for sq_r in range(SD_DIM):
        for sq_c in range(SD_DIM):
            ul_r = sq_r * SD_DIM
            ul_c = sq_c * SD_DIM

            seen = []
            for r in range(SD_DIM):
                for c in range(SD_DIM):
                    num = domains[(r + ul_r, c + ul_c)][0]
                    if num in seen:
                        return False
                    seen.append(num)
    return True

# tester statuses
PASSED, FAILED, TIME_EXCEEDED = 0, 1, 2

def test(problem, time_limit, disp=False, ec=False):
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p = multiprocessing.Process(target = _test, name = "Solve", args=(return_dict,problem,disp,ec,))
    p.start()
    p.join(time_limit)

    ret = None

    # If thread is active
    if p.is_alive():
        print ("Time limit of {} seconds exceeded.".format(time_limit))

        # Terminate foo
        p.terminate()
        p.join()

        ret = TIME_EXCEEDED
    else:
        result = return_dict["result"]
        ret = PASSED if result else FAILED

    return ret

CNF_FILE = "temp.cnf"

def _test(return_dict, problem, disp=False, ec=False):
    ai = AI()
    orig_domains = init_domains(); 
    restrict_domain(orig_domains, problem); 

    if disp:
        print("====Problem====")
        display(orig_domains)
        print()

    start = time.time()

    if not ec:
        result = ai.solve(problem)
    else:
        with open(CNF_FILE, 'w') as file:
            file.write(ai.sat_encode(problem))
        stream = os.popen("./picosat {}".format(CNF_FILE))
        output = stream.read()
        if len(output) == 0:
            print("ERROR: picosat not installed/in PATH.")
            result = None
        else:
            #os.remove(CNF_FILE)
            sat_assignments = parse_picosat(output)
            result = ai.sat_decode(sat_assignments)

    end = time.time()
    t = end - start

    # we assume all test cases are solveable
    passed = False if result == None else verify(result, orig_domains)

    if disp:
        if result != None:
            print("====Solution===")
            display(result)
        # this should never happen with our test cases
        else:
            print("==No solution==")

        print()
        print("Time: {} seconds.".format(t))
        print()
        if passed:
            print("Solution: PASSED.")
        else:
            print("Solution: FAILED.")
        print()

    return_dict["result"] = passed

def test_all(filename, time_limit, max_timeouts, disp=False, ec=False):
    with open(filename, 'r') as file:
        lines = file.readlines()
        problems = [line[:-1] for line in lines]

    num_problems = len(problems)
    timeouts = 0
    for p_i, problem in enumerate(problems):
        print("Test {}/{}:".format(p_i + 1, num_problems))

        result = test(problem, time_limit, disp=disp, ec=ec)
        if result == PASSED:
            print("PASSED")
        elif result == FAILED:
            print("FAILED; Exiting...")
            return
        else:
            timeouts += 1
            print("TIMEOUT; {}/{} allowable timeouts occurred".format(timeouts, max_timeouts))
            if timeouts >= max_timeouts:
                print("FAILED; Exiting...")
                return

        print()

    print("All tests PASSED.")

def parse_picosat(output):
    assignments = {}
    lines = output.split("\n")
    lines = lines[1:]
    for line in lines:
        chars = line.split(" ")
        chars = chars[1:]
        for char in chars:
            num = int(char)
            if num < 0:
                assignments[-num] = False
            elif num > 0:
                assignments[num] = True
    return assignments

prop_tc = "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."
prop_and_search_tc = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"

EASY_TIME = 10
HARD_TIME = 20

if __name__ == '__main__':
    disp = args.disp
    ec = args.ec
    if ec:
        print("*Testing EC...*")
    if args.test == 0:
        test(prop_tc, EASY_TIME, disp=True, ec=ec)
    elif args.test == 1:
        test(prop_and_search_tc, HARD_TIME, disp=True, ec=ec)
    elif args.test == 2:
        test_all("problems/easy.txt", EASY_TIME, 2, disp, ec)
    elif args.test == 3:
        test_all("problems/hard.txt", HARD_TIME, 30, disp, ec)
