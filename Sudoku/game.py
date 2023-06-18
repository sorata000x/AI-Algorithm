# NOTE: do not modify
# useful functions and variables for Sudoku

SD_DIM = 3
SD_SIZE = SD_DIM ** 2

# domain of positions
sd_domain = list(range(0, SD_SIZE))

# domain of square assignments
sd_domain_num = list(range(1, SD_SIZE + 1))

# coordinates on sudoku board
sd_spots = [(i, j) for i in sd_domain for j in sd_domain]

sd_peers = {} 
for spot in sd_spots:
    i, j = spot
    
    # get row and column peers
    sd_peers[spot] = [(i,c) for c in sd_domain if c!=j] + \
                  [(r,j) for r in sd_domain if r!=i]

    # upper-left coordinate of the square unit
    ul_i = (i//SD_DIM)*SD_DIM
    ul_j = (j//SD_DIM)*SD_DIM

    # get square peers
    for rr in range(SD_DIM):
        for cr in range(SD_DIM):
            peer_spot = (ul_i+rr, ul_j+cr)
            if peer_spot != spot:
                sd_peers[spot].append(peer_spot)

# initializes domains to full possible range
def init_domains():
    domains = {}
    for i, j in sd_spots:
        domains[(i, j)] = [k for k in sd_domain_num]
    return domains

# initializes domains by applying unary constraints specified by "problem"
def restrict_domain(domains, problem):
    for i, j in sd_spots:
        c = problem[i*SD_SIZE+j] 
        if c != '.':
            domains[(i, j)] = [int(c)]
