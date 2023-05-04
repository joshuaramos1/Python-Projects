# import the pygame module, so you can use it
from planner import *
import threading, time
import sys

############################ Moodifiable Variables #############################
FRAME_RATE_ON = True
FRAME_RATE = 10
ZOMBIE_MOVE_TIME = 0.1 # (Seconds)
N_STEPS = 3
################################################################################

def drawGrid(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            val = m[i][j]
            if val == '0':
                c = BLACK
                s = 1

                x = j * BLOCK_SIZE
                y = i * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, c, rect, s)

            elif val == '1':
                c = BLACK
                s = 0

                x = j * BLOCK_SIZE
                y = i * BLOCK_SIZE
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(screen, c, rect, s)

            elif val == '2':
                c = BLUE
                s = 1
                global SSTARTX
                SSTARTX.append(j)
                global SSTARTY
                SSTARTY.append(i)

            elif val == '3':
                c = GREEN
                s = 1
                global LSTARTX
                LSTARTX.append(j)
                global LSTARTY
                LSTARTY.append(i)

            elif val == '4':
                c = RED
                s = 1
                global ZSTARTX
                ZSTARTX.append(j)
                global ZSTARTY
                ZSTARTY.append(i)
            
            elif val == '5':
                c = WHITE
                s = 0
                global ARENA_EXIT
                ARENA_EXIT = (j, i)
                # print(ARENA_EXIT)



# Initialize Main Screen
logo = pygame.image.load("freddy.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("Apocalypse Simulator")
background = pygame.transform.scale(pygame.image.load("grass.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
screen.blit(background, (0, 0))
drawGrid(map)


# Initialize entity structures
searcher_dict = dict()
lost_dict = dict()
zombie_dict = dict()

# Gives each entity a unique ID
id = 0

# Fill in the entity structures
for i in range(len(ZSTARTX)):
    x = ZSTARTX[i]
    y = ZSTARTY[i]
    zombie_dict[id] = (x, y)
    id += 1

for i in range(len(LSTARTX)):
    x = LSTARTX[i]
    y = LSTARTY[i]
    lost_dict[id] = (x, y)
    id += 1

for i in range(len(SSTARTX)):
    x = SSTARTX[i]
    y = SSTARTY[i]
    searcher_dict[id] = (x, y)
    id += 1

clockobject = pygame.time.Clock()

                    ###### Initialize Variables ######

# Init images
zombie_image = pygame.transform.scale(pygame.image.load("zombie.png"), (BLOCK_SIZE,BLOCK_SIZE))
searcher_image = pygame.transform.scale(pygame.image.load("steve.png"), (BLOCK_SIZE,BLOCK_SIZE))
lost_image = pygame.transform.scale(pygame.image.load("villager.png"), (BLOCK_SIZE,BLOCK_SIZE))
goal_image = pygame.transform.scale(pygame.image.load("gold.png"), (BLOCK_SIZE,BLOCK_SIZE))

# draw entities
for id in zombie_dict:
    loc = zombie_dict[id]
    drawEntity(zombie_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), RED)

for id in searcher_dict:
    loc = searcher_dict[id]
    drawEntity(searcher_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), BLUE)

for id in lost_dict:
    loc = lost_dict[id]
    drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), GREEN)


pygame.display.update()


# Defining algorithm vars.
zombies_next_action = dict()
searchers_map = dict()
searchers_target = dict()
being_searched = []

# Initialize Seearcher Structures and Variables
for searcher_ID in searcher_dict:
    nearest_lost_person_ID = getNearestEntityIDFromDict(searcher_dict[searcher_ID], lost_dict, [])
    nearest_lost_person = lost_dict[nearest_lost_person_ID]
    searchers_target[searcher_ID] = nearest_lost_person_ID # Map searcher ID to their target Lost person ID
    searchers_map[searcher_ID] = generateMap(nearest_lost_person, X_SIZE, Y_SIZE)
    being_searched.append(nearest_lost_person_ID) # Keep track of which lost are being searched to avoid aliasing

for zombie_ID in zombie_dict:
    zombies_next_action[zombie_ID] = (0, 0)


def drawEnv():
    # Refresh Screen Background
    screen.blit(background, (0,0))
    drawGrid(map)
    drawEntity(goal_image, getImageLoc(ARENA_EXIT), getOffsetLoc(getImageLoc(ARENA_EXIT), (0,0)), WHITE)

    # Draws all entities onto screen
    for searcher_ID in searcher_dict:
        searcher_loc = searcher_dict[searcher_ID]
        drawEntity(searcher_image, getImageLoc(searcher_loc), getOffsetLoc(getImageLoc(searcher_loc), (0,0)), BLUE)

    for loc_ID in lost_dict:
        # Apply action
        loc = lost_dict[loc_ID]
        # Plot new position
        drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), GREEN)

    for zombie_ID in zombie_dict:
        # Apply action
        zombie_loc = zombie_dict[zombie_ID]
        (dx, dy) = zombies_next_action[zombie_ID]
        zombie_dict[zombie_ID] = (zombie_loc[0] + dx, zombie_loc[1] + dy)
        # Plot new position
        drawEntity(zombie_image, getImageLoc(zombie_dict[zombie_ID]), getOffsetLoc(getImageLoc(zombie_dict[zombie_ID]), (0,0)), RED)

    pygame.display.update()


def zombie_thread(zombie_ID, cmap):
  while True:

    zombie_start_time = time.time()

    time.sleep(ZOMBIE_MOVE_TIME) # Delay

    if (FRAME_RATE_ON):
        clockobject.tick(FRAME_RATE) # Set Frame rate to 10 fps

    # Get current zombie loc
    zombie_loc = zombie_dict[zombie_ID]
    # Get next action
    current_searcher_dict = dictCopy(searcher_dict)
    (dx, dy) = zombie_planner(zombie_loc, current_searcher_dict, cmap)
    # Apply action
    zombie_dict[zombie_ID] = (zombie_loc[0] + dx, zombie_loc[1] + dy)

    # Timer
    zombie_end_time = time.time()
    # print(zombie_end_time - zombie_start_time)
    


def main():

    num_of_lost_not_found = len(lost_dict)
    num_of_searchers_eaten = 0
    success = False

    clockobject = pygame.time.Clock()

                        ###### Initialize Variables ######

    # Init images
    zombie_image = pygame.transform.scale(pygame.image.load("zombie.png"), (BLOCK_SIZE,BLOCK_SIZE))
    searcher_image = pygame.transform.scale(pygame.image.load("steve.png"), (BLOCK_SIZE,BLOCK_SIZE))
    lost_image = pygame.transform.scale(pygame.image.load("villager.png"), (BLOCK_SIZE,BLOCK_SIZE))
    goal_image = pygame.transform.scale(pygame.image.load("gold.png"), (BLOCK_SIZE,BLOCK_SIZE))

    # draw entities
    for id in zombie_dict:
        loc = zombie_dict[id]
        drawEntity(zombie_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), RED)

    for id in searcher_dict:
        loc = searcher_dict[id]
        drawEntity(searcher_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), BLUE)

    for id in lost_dict:
        loc = lost_dict[id]
        drawEntity(lost_image, getImageLoc(loc), getOffsetLoc(getImageLoc(loc), (0,0)), GREEN)

    
    pygame.display.update()


    # Defining algorithm vars.
    zombies_next_action = dict()
    searchers_map = dict()
    searchers_target = dict()
    being_searched = []

    # Initialize Seearcher Structures and Variables

    for searcher_ID in searcher_dict:
        nearest_lost_person_ID = getNearestEntityIDFromDict(searcher_dict[searcher_ID], lost_dict, [])
        nearest_lost_person = lost_dict[nearest_lost_person_ID]
        searchers_target[searcher_ID] = nearest_lost_person_ID # Map searcher ID to their target Lost person ID
        searchers_map[searcher_ID] = generateMap(nearest_lost_person, X_SIZE, Y_SIZE)
        being_searched.append(nearest_lost_person_ID) # Keep track of which lost are being searched to avoid aliasing

    for zombie_ID in zombie_dict:
        zombies_next_action[zombie_ID] = (0, 0)
        t = threading.Thread(target=zombie_thread, args=(zombie_ID, map,))
        t.daemon = True
        t.start()
    drawEnv()



    # define a variable to control the main loop
    running = True

    # Number of times search planner is run
    num_planned = 0
    total_plan_time = 0
    simulation_start_time = time.time()
    # main loop
    while running:

        if (FRAME_RATE_ON):
            clockobject.tick(FRAME_RATE) # Set Frame rate to FRAME_RATE fps

        # Refresh Screen
        screen.blit(background, (0,0))
        drawGrid(map)
        drawEntity(goal_image, getImageLoc(ARENA_EXIT), getOffsetLoc(getImageLoc(ARENA_EXIT), (0,0)), WHITE)



        ########################### Planner Begins #############################

        # # Conduct the respective tasks per searcher
        searcher_ID_list = list(searcher_dict.keys())
        n = 0

        search_start_time = time.time() 

        while n < len(searcher_ID_list):

            searcher_ID = searcher_ID_list[n]
            searcher = searcher_dict[searcher_ID]

            if (searcher == (-1, -1)):
                # This is a dead searcher
                n += 1
                continue
            
            curr_Hmap = searchers_map[searcher_ID]
            
            for lost_ID in lost_dict:

                lost = lost_dict[lost_ID]

                if in_view(searcher, lost, 2):

                    # Move lost from lost dict to searcher dict
                    num_of_lost_not_found -= 1
                    del lost_dict[lost_ID] # remove from lost dict
                    searcher_dict[lost_ID] = lost # add to searcher dict
                    searcher_ID_list.append(lost_ID)
                    # Generate new searchers new goal
                    nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_dict, being_searched)
                    being_searched.append(nearest_lost_person_ID) # This lost person is now being tracked, record it in being_searched
                    
                    if (nearest_lost_person_ID == -1): # If no lost left
                        goal = ARENA_EXIT
                    else:
                        goal = lost_dict[nearest_lost_person_ID]
                        
                    searchers_target[lost_ID] = nearest_lost_person_ID
                    searchers_map[lost_ID] = generateMap(goal, X_SIZE, Y_SIZE)

                    # Iterate through all searchers, to redirect any searcher
                    # who had been looking for this lost person
                    for searcher_ID in searcher_dict:
                        if searchers_target[searcher_ID] == lost_ID:
                            # Generate old searchers new goal
                            nearest_lost_person_ID = getNearestEntityIDFromDict(lost, lost_dict, being_searched)
                            being_searched.append(nearest_lost_person_ID)# This lost person is now being tracked, record it in being_searched
                            
                            if (nearest_lost_person_ID == -1): # If no lost left
                                goal = ARENA_EXIT
                            else:
                                goal = lost_dict[nearest_lost_person_ID]
                            
                            searchers_target[searcher_ID] = nearest_lost_person_ID
                            searchers_map[searcher_ID] = generateMap(goal, X_SIZE, Y_SIZE)
                            
                    curr_Hmap = searchers_map[searcher_ID] # Update current searchers map

                    break # break here because we have already found our lost person
            
            # Find the nearest zombie
            nearest_zombie_ID = getNearestEntityIDFromDict(searcher, zombie_dict, [])
            nearest_zombie = zombie_dict[nearest_zombie_ID]

            (searcher_next_action, new_map) = LRTA(searcher, nearest_zombie, searcher_dict, N_STEPS, curr_Hmap, map, X_SIZE, Y_SIZE)
            # Update the searchers map if it changes (due to LRTA)
            
            searchers_map[searcher_ID] = new_map

            # Apply next actions

            searcher = (searcher[0] + searcher_next_action[0], searcher[1] + searcher_next_action[1])
            searcher_dict[searcher_ID] = searcher
            drawEntity(searcher_image, getImageLoc(searcher), getOffsetLoc(getImageLoc(searcher), (0,0)), BLUE)


            # Check if searcher has reached goal
            remove_from_searchers_list = []
            for searcher_ID in searcher_dict:
                searcher_loc = searcher_dict[searcher_ID]
                if (euclid_dist(searcher_loc, ARENA_EXIT) <= 1):
                    remove_from_searchers_list.append(searcher_ID)

            # Check if zombie has caught any searcher:
            for searcher_ID in searcher_dict:
                searcher_loc = searcher_dict[searcher_ID]
                for zombie_ID in zombie_dict:
                    zombie_loc = zombie_dict[zombie_ID]
                    if (zombie_loc == searcher_loc):
                        # Remove searcher if they're eaten
                        remove_from_searchers_list.append(searcher_ID)
                        searcher_ID_list.remove(searcher_ID)
                        n -= 1
                        num_of_searchers_eaten += 1
                        break

            # Delete searchers if they have reached the goal
            for elem in remove_from_searchers_list:
                searcher_dict[elem] = (-1, -1)

            # Once all searchers are gone (escaped or dead)
            searcher_exists = getNearestEntityIDFromDict((0,0), searcher_dict, [])
            if searcher_exists == -1:
                
                ################### Simulation Complete  #######################

                running = False

                if (num_of_lost_not_found == 0) and (num_of_searchers_eaten == 0):
                    success = True

                average_plan_time = total_plan_time/num_planned
                avg_plan_time_in_ns = round(average_plan_time*(10**9))
                simulation_end_time = time.time()
                total_simulation_time = round(simulation_end_time - simulation_start_time)


                #############################STDOUT######################### 
                print(f'{int(success)} {avg_plan_time_in_ns} {total_simulation_time}')
                ############### Modify This for Diff. run.py output ############

                return

            # End of Loop
            n += 1

        ########################### Planner Ends #############################

        search_end_time = time.time()
        # Total execution time of one time-step of the searcher planner
        total_plan_time += search_end_time - search_start_time
        num_planned += 1


        drawEnv() # Update Animation
        
        # Event to check for closing tab
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
                """ Simulation has been force closed """
                #############################STDOUT######################### 
                print(f'{0} {0} {0} {0} {0}')
                ############### Modify This for Diff. run.py output ############
                return 

        





if __name__== "__main__":
    # call the main function
    main()




    