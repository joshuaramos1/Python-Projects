import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from math import sqrt
import pygame, random

############################ Moodifiable Variables #############################
"""                 Choose Level 1 or 2 for present level settings              """
###                 Otherwise, input your own personalized Env.              ###
LEVEL = 0 # 0, 1, or 2
NUMOBS = 15
NUMZ = 3
MAPSz = 30
NUMSs = 1
NUMLs = 5

############################# Map Generation ###################################
def createMap(fName, mode):
    f = open(fName, 'w')

    # different obstacle sizes and orientations
    obSzs = [2, 5, 7]
    choices = ['hor', 'vert']
    dirs = [(1, 0), (0, 1), (1, 1)]

    # sets up parameters based on mode
    if mode == 0:
        numObs = NUMOBS
        numZs = NUMZ
        mapSz = MAPSz
        numSs = NUMSs
        numLs = NUMLs

    elif mode == 1:
        numObs = 50
        numZs = 10
        mapSz = 50
        numSs = 2
        numLs = 10
    else:
        numObs = 100
        numZs = 20
        mapSz = 100
        numSs = 5
        numLs = 30

    # create base map
    map = []
    for i in range(mapSz):
        row = []
        for j in range(mapSz):
            row.append('0')
        map.append(row)

    # generates the number of obsstacles needed
    for i in range(numObs):
        # choose random size and orientation
        obSz = obSzs[random.randint(0,len(obSzs)-1)]
        orientation = random.choice(choices)

        # find top, left corner
        if (orientation == 'hor'):
            dir = 0
            left = random.randint(0, mapSz - obSz-1)
            top = random.randint(0, mapSz-1)
        elif (orientation == 'vert'):
            dir = 1
            top = random.randint(0, mapSz - obSz-1)
            left = random.randint(0, mapSz-1)

        # create obstacle
        for j in range(obSz):
            (dx, dy) = dirs[dir]
            x = left + (j*dx)
            y = top + (j*dy)
            map[y][x] = '1'

    # Generates goal
    while True:
        x = random.randint(0, mapSz -1)
        y = random.randint(0, mapSz -1)
        if (map[y][x] == '0'):
            map[y][x] = '5'
            # print(x,y)
            break

    # place searcher
    for i in range(numSs):
      while True:
          x = random.randint(0, mapSz -1)
          y = random.randint(0, mapSz -1)
          if (map[y][x] == '0'):
              map[y][x] = '2'
              break

    # place lost person
    for i in range(numLs):
      while True:
          x = random.randint(0, mapSz -1)
          y = random.randint(0, mapSz -1)
          if (map[y][x] == '0'):
              map[y][x] = '3'
              break

    # place zombies
    for i in range(numZs):
        while True:
            x = random.randint(0, mapSz -1)
            y = random.randint(0, mapSz -1)
            if (map[y][x] == '0'):
                map[y][x] = '4'
                # print(x,y)
                break
    


    # create the file
    for line in map:
        for char in line:
            f.write(char)
        f.write('\n')

#########################Initialize Simulation Variables########################

# Map (WINDOW/BLOCK_SIZE x WINDOW/BLOCK_SIZE) = (30x30 GRID)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

X_SIZE = WINDOW_WIDTH//BLOCK_SIZE
Y_SIZE = WINDOW_HEIGHT//BLOCK_SIZE

# Possible movement variations for Zombies
ZOMBIE_MOVEMENT_ADVANCED = [(-1,-1), (-1, 0), (-1, 1), (0, -1), 
                    (0, 1), (1, -1), (1, 0), (1, 1)]

ZOMBIE_MOVEMENT_NORMAL = [(+1, 0), (0, +1), (-1, 0), (0, -1)]

ZOMBIE_MOVEMENT = ZOMBIE_MOVEMENT_NORMAL

############################Initiate Map and Window#############################



createMap("test.txt", LEVEL) # MODIFY THIS



f = open("test.txt", 'r')
map = f.readlines()
f.close()
mapSz = len(map)
BLOCK_SIZE = 600//mapSz
WINDOW_WIDTH = BLOCK_SIZE * mapSz
WINDOW_HEIGHT = BLOCK_SIZE * mapSz
X_SIZE = mapSz
Y_SIZE = mapSz
################################################################################

# Searcher Vars
SSTARTX = []
SSTARTY = []

# Lost Vars
LSTARTX = []
LSTARTY = []

# Zombie Vars
ZSTARTX = []
ZSTARTY = []

# Final goal
ARENA_EXIT = (0,0)

# Colors
BLUE = (0,0,255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# initialize the pygame module
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


################################################################################


dXY = [(-1,-1), (-1, 0), (-1, 1), (0, -1), 
       (0, 1), (1, -1), (1, 0), (1, 1)]

def drawEntity(image, entity_loc, image_loc, color):
    screen.blit(image, image_loc)
    pygame.draw.circle(screen, color, entity_loc, 5, 0)
    rect = pygame.Rect(entity_loc[0], entity_loc[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect, 1)

def in_bounds(x: int, y: int, x_size: int, y_size: int) -> bool: 
    # might need to modify these bounds
    return ((x >= 0) and (y >= 0) and (x <= x_size - 1) and (y <= y_size - 1))


def euclid_dist(loc1: tuple, loc2: tuple) -> float:
    # gets the euclidean distance between two locations on the map
    
    if loc1 == (-1, -1):
        # (-1, -1) implies that entity doesn't exit, thus is not in sight
        return 10000

    if loc2 == (-1, -1):
        # (-1, -1) implies that entity doesn't exit, thus is not in sight
        return 10000

    dx = loc1[0] - loc2[0]
    dy = loc1[1] - loc2[1]
    return sqrt(pow(dx, 2) + pow(dy, 2))


def in_view(person: tuple, entity: tuple, dist: int) -> bool:
    return (euclid_dist(person, entity) < dist)

def heuristic(loc1: tuple, loc2: tuple) -> float:
    # computes heuristic from lecture for LRTA
    x1 = loc1[0]
    y1 = loc1[1]
    x2 = loc2[0]
    y2 = loc2[1]
    return max(abs(x1 - x2), abs(y1 - y2)) + 0.4*min(abs(x1 - x2), abs(y1 - y2))

def zombie_planner(zombie_loc: tuple, searcher_pos: dict, map: list) -> tuple:
    # Returns the action that will minimize the distance between the zombie and
    # its closest searcher
    nearest_searcher_ID = getNearestEntityIDFromDict(zombie_loc, searcher_pos, [])
    if nearest_searcher_ID == -1:
        return (0,0)
    nearest_searcher = searcher_pos[nearest_searcher_ID]


    #### COMMENT THIS IN/OUT TO ACTIVATE DIRECT SEARCH OR LIMITED VIEW ####
    if euclid_dist(nearest_searcher, zombie_loc) > 5:
        while True:
            
            action = (random.randint(-1, 1), random.randint(-1, 1))
            next_state = (zombie_loc[0] + action[0], zombie_loc[1] + action[1])
            # print(next_state)
            if not in_bounds(next_state[1], next_state[0], X_SIZE, Y_SIZE):
                # Can't go out of bounds
                continue
            
            if (map[next_state[1]][next_state[0]] == '1'):
                # Can't go through obstacles
                continue

            # print("found move")
            return action



    smallest_dist = 1000
    best_action = (0, 0)

    for (dx, dy) in ZOMBIE_MOVEMENT:
        next_state = (zombie_loc[0] + dx, zombie_loc[1] + dy)

        if not in_bounds(next_state[1], next_state[0], X_SIZE, Y_SIZE):
            # Can't go out of bounds
            continue

        if (map[next_state[1]][next_state[0]] == '1'):
            # Can't go through obstacles
            continue

        curr_dist = euclid_dist(nearest_searcher, next_state)

        if (curr_dist < smallest_dist):
            smallest_dist = curr_dist
            best_action = (dx, dy)
    
    return best_action

def getOffsetLoc(loc, offset):
    # Gets images offset needed to center it on point
    return (loc[0] + offset[0], loc[1] + offset[1])

def getImageLoc(loc): 
    # Gets the images location on window with respect to the entries location
    # in the map list
    return (loc[0]*BLOCK_SIZE, loc[1]*BLOCK_SIZE)

def applyAction(loc, action):
    # Enacts and action on a location and returns new state
    return (loc[0] + action[0], loc[1] + action[1])

def generateMap(lost, x_size, y_size) -> list:
    # Generates a 2D list that emulates a map where each entry is the heuristic
    # value of that node with respect to the goal state
    map = []
    
    for row in range(0, y_size):

        temp_col = []
        for col in range(0, x_size):
            curr_pos = (row, col)
            temp_col.append(heuristic(curr_pos, lost))
            # temp_col = temp_col + []
        map.append(temp_col)
    
    return map

def dictCopy(oldDict):

    # zEvent.clear() # pause zombie thread

    newDict = dict()
    keyList = oldDict.keys()
    for key in keyList:
        newDict[key] = oldDict[key]

    # zEvent.set() # resume zombie thread

    return newDict

def getNearestEntityIDFromDict(curr_state: tuple, entity_pos: dict, lost_being_searched: list) -> int:
    # closest_entity = (0, 0)
    smallest_dist = -1
    closest_entity_ID = -1

    # There are no enitities in the dict
    if entity_pos == {}:
        return -1
        # return default_goal

    for id in entity_pos:
        entity = entity_pos[id]

        if entity == (-1,-1):
            continue

        
        curr_dist = euclid_dist(curr_state, entity)

        if lost_being_searched != []: # We are looking at a dict of lost
            if id in lost_being_searched: 
                # Here we avoid returning a lost person that is already being tracked
                continue

        if (smallest_dist == -1):
            smallest_dist = curr_dist
            # closest_entity = entity
            closest_entity_ID = id
        else:
            if (smallest_dist > curr_dist):
                smallest_dist = curr_dist
                # closest_entity = entity
                closest_entity_ID = id

    return closest_entity_ID


def LRTA(curr_state: tuple, zombie: tuple, searcher_dict: list, N_steps: int, Hmap: list, map: list, x_size: int, y_size: int) -> tuple:
    # With an extended horizon of N_STEPS, this function updates map heuristic 
    # values accordingly and returns the first step in the path

    
    n = 0 # Counter to keep track of steps

    first_next_action = (0, 0)

    # Determine next 4 states and update map accordingly
    while n < N_steps:
        next_action = (0, 0)
        best_neighbor = curr_state
        best_f = -1

        for (dx, dy) in dXY: 
            neighbor = (curr_state[0] + dx, curr_state[1] + dy)
            
            if not in_bounds(neighbor[1], neighbor[0], x_size, y_size):
                continue
            
            if (euclid_dist(neighbor, zombie) < 2):
                continue

            if (int(map[neighbor[1]][neighbor[0]]) != 0):
                # Can't go through obstacles
                continue

            # Check neighboring searchers to make sure no collisions occur
            skip = False
            for searcher_ID in searcher_dict:
                searcher_pos = searcher_dict[searcher_ID]
                if (neighbor == searcher_pos):
                    skip = True
                    break
            
            if skip == True:
                skip = False
                continue
                

            heuristic_val = Hmap[neighbor[0]][neighbor[1]]

            if ((dx == 0) or (dy == 0)):
                graph_cost = 1
            else:
                graph_cost = 1.4

            f = heuristic_val + graph_cost

            if (best_f == -1):
                best_f = f
                best_neighbor = neighbor
            else:
                if (best_f > f):
                    best_f = f
                    best_neighbor = neighbor

        next_action = (best_neighbor[0] - curr_state[0], best_neighbor[1] - curr_state[1])
        
        if n == 0:
            # This is the first step in the path, store it
            first_next_action = next_action

        # Do not update the goal state
        curr_f = Hmap[curr_state[0]][curr_state[1]]
        if (curr_f == 0):
            n += 1
            continue

        if (best_f > Hmap[curr_state[0]][curr_state[1]]):
            Hmap[curr_state[0]][curr_state[1]] = best_f

        curr_state = (curr_state[0] + next_action[0], curr_state[1] + next_action[1])

        n += 1
        
        
    
    return (first_next_action, Hmap)







