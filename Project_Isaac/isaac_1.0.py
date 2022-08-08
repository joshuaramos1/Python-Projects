# Project Developer: Joshua Ramos
# College of Engineering, Class of 2025
# AndrewId: joshuara
# Email: joshuara@andrew.cmu.edu
# Start Date: 11/7/2021
# Time Log:
# TP0 (11/13): 5pm-8pm, 10pm-12pm, 2am-5am
# TP0-TP1 (11/18): 5:30pm-9pm, 10:30pm-2am, 12pm-1:10pm, 10pm-1am
# TP1-TP2 (11/23): 4pm-7pm, 12pm-2:30pm, 11am-3pm, 7pm-10pm, 2:30pm-6pm, 9:00pm-11pm, 11am-12:30pm
# TP2-TP3 (12/1): 8pm-9pm, 3pm-6pm, 10pm-3am, 5pm-7pm, 7pm-9:30pm, 3pm-7pm
# End Date: 12/1/2021
from cmu_112_graphics import *
import random

#################################Image Gallery##################################
#Image Citation: https://bindingofisaacrebirth.fandom.com/wiki/Category:Images
image_key = 'key.png'
image_Isaac = 'Isaac.png'
image_Tear ='tears.png'
image_magicmush = 'magicmush.png'
image_fullheart = 'fullheart.png'
image_bomb = 'bomb.png'
image_halfheart = 'halfheart.png'
image_Trapdoor = 'trapdoor.png'

#Image Citation: https://www.deviantart.com/natsunenuko/art/RPG-Maker-VX-ACE-Isaac-Sprite-624262604
image_Isaac_spritesheet = 'isaac_spritesheet.png'

#Image Citation: https://www.reddit.com/r/bindingofisaac/comments/1ekk2x/basement_and_cellar_wallpapers/
image_basement_room = 'basement_room.png'

# Image Citation: Self
image_freddytears = 'freddytears.png'

#Image Citation: https://blog.guildredemund.net/2015/01/16/the-binding-of-isaac-review/
image_directions = 'directions.png'
image_Door = 'door2.png'

#Image Citation: https://bindingofisaac.fandom.com/es/wiki/Boom_Fly
image_boomfly = 'boomfly.png'

#Image Citation: http://pixelartmaker.com/art/e6d3f057437dca1
image_fly = 'fly.png'

#Image Citation: https://www.reddit.com/r/bindingofisaac/comments/ips0qh/repentance_start_screen_from_tyrones_twitter/
image_startScreen = 'startScreen.png'

###############################Class Creation###################################
class Mob(object):
    def __init__(self, species, start, xpos, ypos, speed, size, health, damage):
        self.species = species
        self.start = start
        self.xpos = xpos
        self.ypos = ypos
        self.speed = speed
        self.size = size
        self.health = health
        self.damage = damage

    def takeDamage(self, damageDealt):
        if isinstance(damageDealt, int):
            #In case health ever goes below zero (it shouldn't).
            if (self.health - damageDealt<0):
                self.health = 0
            else:
                self.health -= damageDealt

    def move(self, targetx, targety):
        if (targetx - self.xpos) < 0:
            self.xpos -= self.speed
        if (targetx - self.xpos) > 0:
            self.xpos += self.speed
        if (targety - self.ypos) < 0:
            self.ypos -= self.speed
        if (targety - self.ypos) > 0:
            self.ypos += self.speed

class Item(object):
    #Items are ....well items... that effect Isaac's tears/appearence.
    def __init__(self, itemName, itemDescription, effects, image, x, y):
        self.name = itemName
        self.itemDescription = itemDescription
        self.effects = effects
        self.size = 10
        self.xpos = x
        self.ypos = y
        self.image = image
    
    def executeEffects(self, other):
        for effect in self.effects:
            trait = effect[0]
            magnitude = effect[1]
            if (trait == 'Speed'):
                other.speed += magnitude

            elif (trait == 'Health'):
                other.health = magnitude

            elif (trait == 'Damage'):
                other.damage += magnitude

            elif (trait == 'TearCoolDown'):
                other.tearCoolDown += magnitude
                
            elif (trait == 'image'):
                other.tearImage = magnitude

class PickUp(Item):
    #PickUps are idle items such as: Hearts, Bombs, Keys, etc.
    def __init__(self, pickUpName, image, x, y):
        self.name = pickUpName
        self.image = image
        self.xpos = x
        self.ypos = y
        self.size = 10

class Door(object):
    def __init__(self, location, orientation, size, image):
        self.location = location
        self.orientation = orientation
        self.xsize = size[0]
        self.ysize = size[1]
        self.image = image
        self.isOpen = 'no'

class Character(object):
    def __init__(self, pos, size, health, image):
        self.xpos = pos[0]
        self.ypos = pos[1]
        self.xsize = size[0]
        self.ysize = size[1]
        self.health = health
        self.image = image
        self.tearImage = image_Tear
        self.bombs = 0
        self.speed = 20
        self.damage = 1
        self.tearCoolDown = 10
        self.shotSpeed = 20
        self.keys = 0
        self.itemEffects = []

    def itemIsPickedUp(self, item):
        #If Isaac picks up an item, it will be added to his collection of items.
        if (isinstance(item, Item)):
            if (isinstance(item, PickUp)):
                #Pickup is a Half Heart
                if (item.name =='Half-Heart'):
                    #Check if Isaac is at full health
                    if (self.health < 6):
                        self.health += 1

                #Pickup is a Full Heart
                elif (item.name =='Full-Heart'):
                    #In case Isaac is at 5/6 Hearts
                    if ((self.health + 2) <= 6):
                        self.health += 2
    
                    elif (self.health < 6):
                        self.health += 1

                elif (item.name =='Bomb'):
                    self.bombs += 1

                elif (item.name =='Key'):
                    self.keys += 1
            
            else:
                #If item is an ability item, executed its effects.
                item.executeEffects(self)

    def takeDamage(self, damageDealt):
        if isinstance(damageDealt, int):
            #In case health ever goes below zero (it shouldn't).
            if ((self.health - damageDealt) < 0):
                self.health = 0
            else:
                self.health -= damageDealt

    def moveIsaac(self, direction):
        if (direction == 'Up'):
            self.ypos -= self.speed

        elif (direction == "Down"):
            self.ypos += self.speed

        elif (direction == 'Left'):
            self.xpos -= self.speed

        elif (direction == 'Right'):
            self.xpos += self.speed

class Tear(object):
    def __init__(self, direction, x, y, image):
        self.direction = direction
        self.xpos = x
        self.ypos = y
        self.size = 10
        self.image = image    

################################Core App Functions##############################
def appStarted(app):
    app.gameStarted = False
    app.gameOver = False
    app.restart = False
    app.paused = False
    app.displayHitboxes = False
    
    # Image Control:
    scalefactor = 5/2
    app.pos = (app.width//2, app.height//2)
    app.size = ((28)*scalefactor, (33)*scalefactor)
    app.Isaac = Character(app.pos, app.size, 6, image_Isaac)
    app.scaled_image_startScreen = app.scaleImage(app.loadImage(image_startScreen), 4/5)
    app.scaled_image_bomb = app.scaleImage(app.loadImage(image_bomb), 1.5)
    app.scaled_image_key = app.scaleImage(app.loadImage(image_key), 1)
    app.scaled_image_halfheart = app.scaleImage(app.loadImage(image_halfheart), 1)
    app.scaled_image_fullheart = app.scaleImage(app.loadImage(image_fullheart), 1)
    app.scaled_image_magicmush = app.scaleImage(app.loadImage(image_magicmush), 1.5)
    app.scaled_image_freddytears = app.scaleImage(app.loadImage(image_freddytears), 0.25)
    app.scaled_image_door = app.scaleImage(app.loadImage(image_Door), 1.5)
    app.scaled_image_trapdoor = app.scaleImage(app.loadImage(image_Trapdoor), scalefactor)
    app.scaled_image_directions = app.scaleImage(app.loadImage(image_directions), 1)
    app.scaled_image_boomfly = app.scaleImage(app.loadImage(image_boomfly), 2)
    app.scaled_image_fly = app.scaleImage(app.loadImage(image_fly), 1/4)
    app.scaled_image_room = app.scaleImage(app.loadImage(image_basement_room), 1/2)
    app.scaled_image_isaac = app.scaleImage(app.loadImage(app.Isaac.image), scalefactor)
    app.scaled_image_tear = app.scaleImage(app.loadImage(app.Isaac.tearImage), 1)
    
    app.spriteKey = None
    spriteControl(app) #Used for Isaac's sprite setup.

    # Creating Rooms/Floors:
    app.level = 1
    app.grid = createGrid(app)
    app.marginx = 35
    app.marginy = 40
    app.roomwidth = app.width - 2*app.marginx
    app.roomheight = app.height - 2*app.marginy
    app.spawnRoom = len(app.grid)*len(app.grid[0]) // 2
    app.currentRoom = app.spawnRoom
    app.color = 'black'
    app.visitedRooms = set()
    app.topdoor = Door((app.width//2, app.marginy), 'Top', (50,25), app.scaled_image_door)
    app.bottomdoor = Door((app.width//2, app.height - app.marginy), 'Bottom', (50,25), app.scaled_image_door)
    app.leftdoor = Door((app.marginx, app.height//2), 'Left', (25,50), app.scaled_image_door)
    app.rightdoor = Door((app.width - app.marginx, app.height//2), 'Right', (25,50), app.scaled_image_door)
    app.trapdoor = Door((app.width//2, 4*app.marginy), 'floor', (25,25), app.scaled_image_trapdoor)
    app.doors = [app.topdoor, app.bottomdoor, app.leftdoor, app.rightdoor, app.trapdoor]
    app.currentLocation = findLocation(app)

    # Making MiniMap:
    app.cellSizex = 140//len(app.grid)
    app.cellSizey = 140//len(app.grid[0])
    app.minimapx = app.width*(8/9)
    app.minimapy = app.height*(2/10)
    app.displayMap = False
    
    # Key Contol:
    app.count = 0
    app.keysBeingPressed = set()
    app.tears = []    
    app.tearCoolDown = 0

    # Graph Control:
    app.graphSize = 5
    app.graphCellSizex = (app.width - 8*app.marginx)/app.graphSize
    app.graphCellSizey = (app.height - 8*app.marginy)/app.graphSize
    app.displayGraph = False
    app.nodeLocations = {}
    app.graphCells = []
    app.graph = []
    app.whoConnectsWithWho = {}
    app.target = closestNode(app, app.Isaac)
    createGraph(app)
    
    # Entity Control:
    app.monstersInRoom = []
    app.monsterPool = [('Boomfly', 30, 3, 6, 2), ('Fly', 10, 3, 3, 1)]
    app.newRoomEntered = True
    app.damageCoolDown = 0
    app.magicmush = ('Magic Mushroom', 'All Stats Up!', 
                    [ ('Damage', +1), ('Speed', +10), ('Health', 6), 
                    ('TearCoolDown', -5) ],
                    app.scaled_image_magicmush, app.width//2, app.height//2)
    app.freddyTears = ('Freddy Tears', 'is it a bear?', 
                      [ ('image', image_freddytears) ], 
                      app.loadImage(image_freddytears), 
                      app.width//2, app.height//2)
    app.itemPool = [app.freddyTears,app.magicmush]
    app.itemRoom = 1
    app.itemInRoom = None
    halfheart = ('Half-Heart', app.scaled_image_halfheart)
    fullheart = ('Full-Heart', app.scaled_image_fullheart)
    key = ('Key', app.scaled_image_key)
    bomb = ('Bomb', app.scaled_image_bomb)
    app.itemPickUpPool = [halfheart, fullheart, key, bomb]
    app.roomCleared = True
    app.spawnNewItem = False
    app.descriptionCoolDown = 0
    app.description = ''

def timerFired(app):
    if (app.gameStarted == True):

        # If User's health has been killed or has completed Level 5.
        if ((app.Isaac.health <= 0) or (app.level > 5)):
            app.gameOver = True
        
        # If game is paused, everything will freeze.
        if (app.paused != True):
            moveIsaac(app)
            moveTears(app)
            moveRooms(app)
            spawnMonsters(app)
            monsterControl(app)
            generateDoor(app)
            damageControl(app)
            itemControl(app)
            spriteControl(app)
            app.spriteCounter = (1 + app.spriteCounter) % len(app.isaacSprites)
            app.damageCoolDown -= 1
            app.tearCoolDown -= 1
            app.count += 1 
            app.descriptionCoolDown -= 1
            restart(app)
     
def keyReleased(app, event):
    # If game is paused, all key releases will be inactive.
    if (app.paused != True):

        if (event.key == 'a'):
            app.keysBeingPressed.remove('a')
            app.spriteKey = None

        elif (event.key == 'w'):
            app.keysBeingPressed.remove('w')
            app.spriteKey = None

        elif (event.key == 's'):
            app.keysBeingPressed.remove('s')
            app.spriteKey = None

        elif (event.key == 'd'):
            app.keysBeingPressed.remove('d')
            app.spriteKey = None

        elif (event.key == 'Right'):
            app.keysBeingPressed.remove('Right')

        elif (event.key == 'Left'):
            app.keysBeingPressed.remove('Left')

        elif (event.key == 'Up'):
            app.keysBeingPressed.remove('Up')

        elif (event.key == 'Down'):
            app.keysBeingPressed.remove('Down')
        
def keyPressed(app, event):
    if (event.key == 'p'): #Pause game
        if (app.paused == False):
            app.paused = True
        else:
            app.paused = False

    if (event.key == 'r'): # Restart game
        app.restart = True
        app.paused = False
        app.gameOver = False

    # If game is paused, all keys except restart and pause will be inactive.
    if (app.paused != True):

        #User shoots tears
        if (event.key == 'Right'):
            app.keysBeingPressed.add('Right')
        
        elif (event.key == 'Left'):
            app.keysBeingPressed.add('Left')
        
        elif (event.key == 'Up'):
            app.keysBeingPressed.add('Up')
        
        elif (event.key == 'Down'):
            app.keysBeingPressed.add('Down')
        
        #User places Bomb or uses Active Item
        elif (event.key == 'e'):
            pass

        elif (event.key == 'Space'): #Start Game Key
            app.gameStarted = True

        elif (event.key == 'Tab'): #Display MiniMap Key
            if (app.displayMap == False):
                app.displayMap = True
            else:
                app.displayMap = False
        
        elif (event.key == 'g'): #Display Graph Key
            if (app.displayGraph == False):
                app.displayGraph = True
            else:
                app.displayGraph = False

        elif (event.key == 'h'): #Display Hitboxes Key
            if (app.displayHitboxes == False):
                app.displayHitboxes = True
            else:
                app.displayHitboxes = False 

        elif (event.key == 'k'): #The kill all Monsters in room Key
            app.monstersInRoom = []

        #User Moves Isaac
        elif (event.key == 'a'):
            app.keysBeingPressed.add('a')
            app.spriteKey = 'left'

        elif (event.key == 'w'):
            app.keysBeingPressed.add('w')
            app.spriteKey = 'up'

        elif (event.key == 's'):
            app.keysBeingPressed.add('s')
            app.spriteKey = 'down'

        elif (event.key == 'd'):
            app.keysBeingPressed.add('d')
            app.spriteKey = 'right'

        elif (event.key == 't'): # Skip level (does not change floor/room: debugger tool)
            app.level += 1

#################################Grid_Creation##################################
# Citation:
# Jamis Buck - The Buckblog
# http://weblog.jamisbuck.org/2011/1/27/maze-generation-growing-tree-algorithm
# Jamis Buck's recursive "Growing Tree" algorithmic approach 
# was considered during the development of this code. To clarify, his code was 
# not used in any way. I read his approach/pseudocode and modified the approach
# to fit my model. Essentially, this is the source I used for research purposes.
def createGrid(app):
    # Determines hole number and size of grid based on current level.
    if (app.level == 1):
        holes = 0
        size = 3

    elif ((app.level == 2) or (app.level == 3)):
        holes = 0
        size = 4

    elif ((app.level == 4) or (app.level == 5)):
        holes = 1
        size = 5

    # Searches through 1000 testcases for a completed grid in case of failure.
    testcases = 1000
    for i in range(testcases):
        solution = wrapperGenerateGrid(size, holes)
        if (solution != False):
            return solution

def wrapperGenerateGrid(n, holes):
    count = 0
    blankGrid = [[0]*n for i in range(n)]
    while True:
        # Randomly create holes in grid.
        grid = generateHoles(blankGrid, holes)
        solution = generateGrid(grid)
        if (count >= 1):
            # In order to prevent an infinite loop due to Recursion and While.
            break
        count += 1

        if (solution == False):
            continue
        else:
            break
    return solution

def generateGrid(grid):
    # Begin with a random location on the map.
    startx = random.randint(0,len(grid) - 1)
    starty = random.randint(0,len(grid[0]) - 1)
    # Here I will be keeping track of visited cells.
    cellSet = set()
    cellSet.add((startx,starty))
    grid[startx][starty] = 1
    return helperGrid(grid, cellSet, startx, starty, 2) 

def helperGrid(grid, cells, sx, sy, step):
    N = (0, +1)
    S = (0, -1)
    E = (+1, 0)
    W = (-1, 0)
    if (checkGrid(grid)):
        return grid
    else:
        dir = [(0,0), N, S, E, W]
        random.shuffle(dir)
        for path in dir:
            dx, dy = path
            nx, ny = sx + dx, sy + dy
            if ((nx >= 0) and (nx < len(grid)) 
            and (ny >= 0) and (ny < len(grid[0]))):
                # Checks if the next cell is within the board.
                if ((grid[nx][ny] != 'H') and (grid[nx][ny] == 0)):
                    # Checks if the next cell has not been visited yet.
                    cells.add((nx,ny))
                    grid[nx][ny] = step
                    
                    solution = helperGrid(grid, cells, nx, ny, step+1)
                    if (solution != False):
                        return solution
                    # If path is not a solution, undo changes.
                    cells.remove((nx, ny))
                    grid[nx][ny] = 0
        return False

def checkGrid(grid):
    # Checks if grid has been filled with numbers.
    gridNums = list()
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (grid[row][col] == 0):
                # Looks for zeroes in grid.
                return False
            gridNums.append(grid[row][col])
    check = []
    # Checks for duplicate numbers in case of failure to comeplete maze.
    for num in gridNums:
        if (num not in check):
            check.append(num)
        else:
            return False
    return True

def generateHoles(grid, holes):
    # Generates holes in grid according to level type.
    for i in range(holes):
        # Randomly creates holes in map.
        holerow = random.randint(0, len(grid) - 1)
        holecol = random.randint(0, len(grid[0]) - 1)
        if (grid[holerow][holecol] == 1):
            continue
        else:
            grid[holerow][holecol] = 'H'
    return grid

def findLocation(app):
    for row in range(len(app.grid)):
        for col in range(len(app.grid[0])):
            if (app.grid[row][col] == app.currentRoom):
                return (row, col)

###############################Entity Generation################################
def spawnMonsters(app):
    # This function controls the generation of monsters in each room.
    # If a new room has been entered then monsters will spawn.
    if ((app.newRoomEntered == True) 
    and (app.currentLocation not in app.visitedRooms)):
        # Mosters will only spawn randomly among the corners of the graph.
        topleft = app.nodeLocations[1]
        topright = app.nodeLocations[6]
        bottomleft = app.nodeLocations[31]
        bottomright = app.nodeLocations[36]
        corners = [topleft,topright,bottomleft,bottomright]

        # Each level will (at max) spawn a corresponding number of mobs.
        if (app.level == 1):
            numOfMobs = 1
        elif (app.level == 2):
            numOfMobs = 2
        elif (app.level == 3):
            numOfMobs = 3
        elif ((app.level == 4) or (app.level == 5)):
            numOfMobs = 4

        for i in range(numOfMobs):
            randomMonster = random.choices(app.monsterPool)[0]
            randomLocation = random.choices(corners)[0]
            xpos = randomLocation[0]
            ypos = randomLocation[1]
            species = randomMonster[0]
            size = randomMonster[1]
            speed = randomMonster[2]
            health = randomMonster[3]
            damage = randomMonster[4]
            if (randomLocation == topleft):
                start = 1
            elif (randomLocation == topright):
                start = 6
            elif (randomLocation == bottomleft):
                start = 31
            elif (randomLocation == bottomright):
                start = 36
            app.monstersInRoom.append(Mob(species, start, xpos, ypos, speed, size, health, damage))
        # Item generation and Monster generation work hand-in hand; thus, Item
        # generation can be executed here.
        spawnItems(app)
        app.newRoomEntered = False

def spawnItems(app):
    # If a new room has been entered, Monsters will be generated.
    # If the Item Pool is ever emtpy (due to all items being picked up) then
    # PickUp items will be generated instead.
    # Ability items will only be generated within the item rooms.
    if ((app.itemPool != []) and (app.currentRoom == app.itemRoom) 
    and (app.newRoomEntered == True)):
        randomItem = random.choices(app.itemPool)[0]
        app.itemPool.remove(randomItem)
        itemName = randomItem[0]
        itemDescription = randomItem[1]
        effects = randomItem[2]
        image = randomItem[3]
        x = randomItem[4]
        y = randomItem[5]
        app.itemInRoom = Item(itemName, itemDescription, effects, image, x, y)
        app.itemImage = app.itemInRoom.image

    # If the user is in a normal room then items from the PickUp item pool
    # will be generated.
    elif ((app.newRoomEntered == True) and (app.currentRoom != app.spawnRoom)):
        randomItem = random.choices(app.itemPickUpPool)[0]
        if (randomItem != None):
            pickUpName = randomItem[0]
            image = randomItem[1]
            x = app.width//2
            y = app.height//2
            app.itemInRoom = PickUp(pickUpName, image, x, y)
            app.itemImage = app.itemInRoom.image
    
def closestNode(app, entity):
    #Find Closest Node to entity.
    xpos = entity.xpos
    ypos = entity.ypos
    bestNode = None
    bestDist = None
    for node in app.nodeLocations:
        (nx, ny) = app.nodeLocations[node]
        dist = ((nx - xpos)**2 + (ny - ypos)**2)**0.5
        # Best case algorithm is used here to find shortest distance.
        if (bestDist == None or dist < bestDist):
            bestDist = dist
            bestNode = node
    return bestNode

def monsterControl(app):
    # This function is used to direction ever monster currently on the floor
    # to the User according to their respoective searching algorithms.
    app.target = closestNode(app, app.Isaac)
    # The monsters' target will be the closes node to the User.
    for monster in app.monstersInRoom:
        # If a monster loses all of their health then they are killed (removed)
        if (monster.health <= 0):
            app.monstersInRoom.remove(monster)
        else:
            if (monster.species == 'Fly'):
                pass
            if (monster.species == 'Boomfly'):
                nearestNode = closestNode(app, monster)
                path = findShortestPath(app, nearestNode, app.target)
                
                if (nearestNode != app.target):
                    # If the nearest node to the monster is not the target,
                    # then it will continue to move along the path that will 
                    # lead it to the target (User).
                    for node in path:
                        (x, y) = app.nodeLocations[node]
                        monster.move(x, y)
            # If the User has exited the graph's bounds and the monster has
            # an edge of the graph then the monster will exit the graph as well
            # and utilize a direct following algorithm to find the target (User)
            monster.move(app.Isaac.xpos, app.Isaac.ypos)

    if ((app.monstersInRoom == []) and (app.currentRoom != app.spawnRoom)):
        app.roomCleared = True
        app.spawnNewItem = True
    else:
        app.roomCleared = False
    
def itemControl(app):
    # An item will only spawn when the current room has been cleared of monsters
    if (isinstance(app.itemInRoom, Item)) and (app.roomCleared == True):
        item = app.itemInRoom
        # If an item has been collided with (picked up) then its effects
        # will be executed.
        if (hasCollided(item.xpos,item.ypos,item.size,item.size,
        app.Isaac.xpos,app.Isaac.ypos,app.Isaac.xsize,app.Isaac.ysize)):
            app.Isaac.itemIsPickedUp(app.itemInRoom)
            if (not isinstance(item, PickUp)):
                app.description = item.itemDescription
                app.descriptionCoolDown = 20
            app.itemInRoom = None

    app.scaled_image_tear = app.scaleImage(app.loadImage(app.Isaac.tearImage), 0.35)

def damageControl(app):
    # This function controls the exertion of damage on entities due to collision
    for monster in app.monstersInRoom:
        # If the user collides with a monster then both the user and the monster
        # take damage with respect to each others' attack damage.
        if (hasCollided(monster.xpos,monster.ypos,monster.size,monster.size,
        app.Isaac.xpos,app.Isaac.ypos,app.Isaac.xsize,app.Isaac.ysize)):
            if (app.damageCoolDown <= 0):
                monster.takeDamage(1)
                app.Isaac.takeDamage(monster.damage)
                app.damageCoolDown = 15
                
        for tear in app.tears:
            # If a tear collides with a monster then the tear will be removed
            # and the monster will take damage with respect to the User's attack
            # damage.
            if (hasCollided(tear.xpos,tear.ypos,tear.size,tear.size,
            monster.xpos,monster.ypos,monster.size,monster.size)):
                monster.takeDamage(app.Isaac.damage)
                app.tears.remove(tear)

def generateDoor(app):
    N = (-1, 0)
    S = (+1, 0)
    E = (0, +1)
    W = (0, -1)
    # Look in all directions from current room location.
    for dir in [N,S,E,W]:
        (crow, ccol) = app.currentLocation
        (drow, dcol) = dir
        nrow, ncol = crow + drow, ccol + dcol
        # Check if genrated door is within bounds of map.
        if ((nrow < 0) or (nrow >= len(app.grid)) 
        or (ncol < 0) or (ncol >= len(app.grid))):
            continue
        # Check if there is a nearby room to enter.
        else:
            if ((app.grid[nrow][ncol] == (app.currentRoom + 1)) 
            or (app.grid[nrow][ncol] == (app.currentRoom - 1))):
                if (app.monstersInRoom != []):
                    break
                else:
                    if (dir == N):
                        app.topdoor.isOpen = 'yes'

                    elif (dir == S):
                        app.bottomdoor.isOpen = 'yes'

                    elif (dir == E):
                        app.rightdoor.isOpen = 'yes'

                    elif (dir == W):
                        app.leftdoor.isOpen = 'yes'
                    
                    # The location of the trapdoor depends on the current
                    # floor number (level).
                    if ((app.level == 4) or (app.level == 5)):
                        if (app.currentRoom == (len(app.grid)*len(app.grid[0]) - 1)):
                            app.trapdoor.isOpen = 'yes'

                    if ((app.level == 1) or (app.level == 2) or (app.level == 3)):
                        if (app.currentRoom == len(app.grid)*len(app.grid[0])):
                            app.trapdoor.isOpen = 'yes'

def restart(app):
    # This function resets the entire game. ie. Stats, Rooms, Level, etc.
    if (app.restart == True):
        app.gameOver = False
        app.itemPool = [app.freddyTears, app.magicmush]
        app.monstersInRoom = []
        app.Isaac = Character(app.pos, app.size, 6, image_Isaac)
        app.level = 1
        app.visitedRooms = set()
        app.grid = createGrid(app)
        app.currentRoom = len(app.grid)*len(app.grid[0])//2
        app.cellSizex = 140//len(app.grid)
        app.cellSizey = 140//len(app.grid[0])
        for r in range(len(app.grid)):
            for c in range(len(app.grid[0])):
                if (app.grid[r][c] == app.currentRoom):
                    app.currentLocation = (r, c)
                    break
        app.restart = False

##################################Movement Control##############################
def createGraph(app):
    node = 1
    for rows in range(app.graphSize + 1):
        templist = []
        for cols in range(app.graphSize + 1):
            templist.append(node)
            x0 = 4*app.marginx + (cols)*app.graphCellSizex
            y0 = 4*app.marginy + (rows)*app.graphCellSizey
            app.nodeLocations[node] = (x0, y0)
            if ((rows < app.graphSize) and (cols < app.graphSize)):
                app.graphCells.append((x0,y0))
            node += 1
        app.graph.append(templist)
    
    #Graph Directory Creation
    N, S, E, W,  = (-1, 0), (+1, 0), (0, +1), (0, -1)
    NE, SE, NW, SW = (-1, +1), (+1, +1), (-1, -1), (+1, -1)
    for row in range(len(app.graph)):
        for col in range(len(app.graph[0])):
            for elem in [N, S, E, W, NE, SE, NW, SW]:
                (drow, dcol) = elem
                nrow, ncol = drow + row, dcol + col
                if ((nrow < 0) or (nrow >= len(app.graph)) 
                or (ncol < 0) or (ncol >= len(app.graph[0]))):
                    continue
                else:
                    key = app.graph[row][col]
                    connectsTo = app.graph[nrow][ncol]
                    if (key not in app.whoConnectsWithWho):
                        app.whoConnectsWithWho[key] = [connectsTo]
                    else:
                        app.whoConnectsWithWho[key].append(connectsTo)

def findShortestPath(app, startNode, target):
    # https://www.geeksforgeeks.org/building-an-undirected-graph-and-finding-shortest-path-using-dictionaries-in-python/
    # This code utilizes BFS to find the shortest path between two nodes.
    graph = app.whoConnectsWithWho
    seen = set()
    allPaths = [[startNode]]
    if (startNode == target):
        return startNode
    else:
        while True:
            currnode = allPaths[0][-1]
            path = allPaths[0]
            for node in graph:
                if ((currnode in graph[node]) and (node not in seen)):
                    npath = path + [node]
                    allPaths.append(npath)
                    seen.add(node)
                    if (node == target):
                        return npath
            allPaths.remove(path)

def hasCollided(cx1, cy1, xsize1, ysize1, cx2, cy2, xsize2, ysize2):
    xsize1 /= 2
    ysize1 /= 2
    xsize2 /= 2
    ysize2 /= 2
    # If entities' outer edges (Hor. and Vert.) come into contact, they have
    # collided. Collision is checked by detecting if one entity's outer edge
    # is within the range of the other's corresponding edges.
    # ie. Hor. is used to check Hor. | Vert used to check Vert.
    if (((cy1+ysize1 <= cy2+ysize2 and cy1+ysize1 >= cy2-ysize2) or 
       (cy1-ysize1 <= cy2+ysize2 and cy1-ysize1 >= cy2-ysize2)) 
    and 
       ((cx1+xsize1 <= cx2+xsize2 and cx1+xsize1 >= cx2-xsize2) or 
       (cx1-xsize1 <= cx2+xsize2 and cx1-xsize1 >= cx2-xsize2))):
            return True
    else:
        return False

def spriteControl(app):
    # Citation: CMU 15-112
    # URL: https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#spritesheetsWithCropping
    # This code was referenced and modified to fit a 
    # spritesheet with more than one row of sprites.
    trow = None
    # The variable 'trow' represents a cropped row of the sheet.
    if (app.spriteKey == 'down'):
        trow = 0

    elif (app.spriteKey == 'left'):
        trow = 1

    elif (app.spriteKey == 'right'):
        trow = 2

    elif (app.spriteKey == 'up'):
        trow = 3

    else:
        # If Isaac is currently not moving then a standstill front-facing image
        # will be displayed.
        app.spriteKey = None
        image = app.scaleImage(app.loadImage(image_Isaac_spritesheet).crop((96, 0, 96*2, 64)), 2.7)
        app.isaacSprites = [image]

    spritestrip = app.loadImage(image_Isaac_spritesheet)
    for row in range(4):
        for col in range(3):
            if (row == trow):
                sprite = app.scaleImage(spritestrip.crop((96*col, row*64, 96*(col + 1), 64*(row + 1))), 2.7)
                app.isaacSprites.append(sprite)
                
    app.spriteCounter = 0

def moveIsaac(app):
    # If a move is not within the bounds of the room, Isaac will be bounced back
    if ('a' in app.keysBeingPressed):
        if ((app.Isaac.xpos - app.Isaac.xsize//2) <= app.marginx):
            app.Isaac.xpos = app.marginx + app.Isaac.xsize//2
        else:
            app.Isaac.moveIsaac('Left')

    if ('w' in app.keysBeingPressed):
        if ((app.Isaac.ypos - app.Isaac.ysize//2) <= app.marginy):
            app.Isaac.ypos = app.marginy + app.Isaac.ysize//2
        else:
            app.Isaac.moveIsaac('Up')

    if ('s' in app.keysBeingPressed):
        if ((app.Isaac.ypos + app.Isaac.ysize//2) >= app.marginy + app.roomheight):
            app.Isaac.ypos = app.height - app.marginy - app.Isaac.ysize//2
        else:
            app.Isaac.moveIsaac('Down')

    if ('d' in app.keysBeingPressed):
        if ((app.Isaac.xpos + app.Isaac.xsize//2) >= app.marginx + app.roomwidth):
            app.Isaac.xpos = app.width - app.marginx - app.Isaac.xsize//2
        else:
            app.Isaac.moveIsaac('Right')

def moveTears(app):
    # Tears will only be generated if the coolDown condition has been satisfied.
    if (app.tearCoolDown <= 0):
        if ('Right' in app.keysBeingPressed):
            app.tears.append(Tear('Right', app.Isaac.xpos, app.Isaac.ypos, image_Tear))
            app.tearCoolDown = app.Isaac.tearCoolDown

        elif ('Left' in app.keysBeingPressed):
            app.tears.append(Tear('Left', app.Isaac.xpos, app.Isaac.ypos, image_Tear))
            app.tearCoolDown = app.Isaac.tearCoolDown

        elif ('Up' in app.keysBeingPressed):
            app.tears.append(Tear('Up', app.Isaac.xpos, app.Isaac.ypos, image_Tear))
            app.tearCoolDown = app.Isaac.tearCoolDown

        elif ('Down' in app.keysBeingPressed):
            app.tears.append(Tear('Down', app.Isaac.xpos, app.Isaac.ypos, image_Tear))
            app.tearCoolDown = app.Isaac.tearCoolDown

    # Tears will be moved according to specified direction and User's shotspeed.
    for tear in app.tears:
        if (tear.direction == 'Right'):
            tear.xpos += app.Isaac.shotSpeed

        elif (tear.direction == 'Left'):
            tear.xpos -= app.Isaac.shotSpeed

        elif (tear.direction == 'Up'):
            tear.ypos -= app.Isaac.shotSpeed

        elif (tear.direction == 'Down'):
            tear.ypos += app.Isaac.shotSpeed

def moveRooms(app):
    # This function controls the movement from room to room 
    # and floor to floor within game.
    app.visitedRooms.add(app.currentLocation)
    for door in app.doors:
        # Isaac can only open doors that are open.
        if (door.isOpen == 'yes'):
            # If the User's hitbox makes contact with a door then the 
            # room will change accordingly.
            if (hasCollided(door.location[0], door.location[1], door.xsize, 
            door.ysize, app.Isaac.xpos, app.Isaac.ypos, app.Isaac.xsize, 
            app.Isaac.ysize)):
                (row, col) = app.currentLocation
                if (door.orientation == 'Top'):
                    row -= 1

                elif (door.orientation == 'Bottom'):
                    row += 1

                elif (door.orientation == 'Left'):
                    col -= 1

                elif (door.orientation == 'Right'):
                    col += 1

                # If a trapdoor is entered, a new floor 
                # is genereated and entered.
                elif (door.orientation == 'floor'):
                    if (app.level == 5):
                        app.gameOver = True
                        break
                    app.level += 1
                    app.visitedRooms = set()
                    app.grid = createGrid(app)
                    app.spawnRoom = len(app.grid)*len(app.grid[0]) // 2
                    app.currentRoom = app.spawnRoom
                    app.cellSizex = 140 // len(app.grid)
                    app.cellSizey = 140 // len(app.grid[0])
                    for r in range(len(app.grid)):
                        for c in range(len(app.grid[0])):
                            if (app.grid[r][c] == app.currentRoom):
                                app.currentLocation = (r, c)
                                break
                    break
                
                app.currentRoom = app.grid[row][col]
                app.currentLocation = (row, col)
                app.Isaac.xpos = app.width // 2
                app.Isaac.ypos = app.height // 2
                app.tears = []
                app.monstersInRoom = []
                app.newRoomEntered = True
                break 

    for door in app.doors:
        door.isOpen = 'no'   

################################Draw Functions##################################
def drawRoom(app, canvas):
    # This function draws the room and User GUI.
    canvas.create_image(app.width//2, app.height//2, 
    image=ImageTk.PhotoImage(app.scaled_image_room))
    canvas.create_rectangle(app.marginx,app.marginy, 
    app.width - app.marginx, app.height - app.marginy)
   
    # The spawn room of each floor contains game interaction directions.
    if (app.currentRoom == app.spawnRoom):
        canvas.create_image(app.width//2, app.height//2, 
        image=ImageTk.PhotoImage(app.scaled_image_directions))

    canvas.create_text(3*app.marginx,2*app.marginy - 20, text=f'Health: {app.Isaac.health}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 0 , text=f'Damage: {app.Isaac.damage}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 20, text=f'Speed: {app.Isaac.speed}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 40, text=f'Range: Infinite lol', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 60, text=f'Current Room: {app.currentRoom}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 80, text=f'Bombs: {app.Isaac.bombs}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 100, text=f'Keys: {app.Isaac.keys}', font='Arial 12')
    canvas.create_text(3*app.marginx,2*app.marginy + 120, text=f'Current Floor: {app.level}', font='Arial 12')
    
    # Whenver an item is picked up, its description is displayed.
    if (app.descriptionCoolDown > 0):
        canvas.create_text(app.width//2,app.height//2, text=f'{app.description}', font='Arial 52 bold', fill='yellow')

def drawGraph(app, canvas):
    for cell in app.graphCells:
        (x0, y0) = cell
        canvas.create_rectangle(x0, y0, x0 + app.graphCellSizex, y0 + app.graphCellSizey, outline= 'black')
    
    for node in app.nodeLocations:
        (x0, y0) = app.nodeLocations[node]
        canvas.create_text(x0,y0, text=str(node), fill='red')

def drawCell(app, canvas, leftedge, topedge, rows, cols, color):
    # Citation: 15-112 Tetris Assignment Week 6
    # Grid construction algorithm used in Tetris Assingment was considered when this
    # function was being developed.
    x0 = leftedge + cols*app.cellSizex
    y0 = topedge + rows*app.cellSizey
    # If Isaac has visited a room, change its color. 
    # MiniMap starts off blank (black) and then become gray as it is discovered
    # Room Isaac is in is colored yellow.
    canvas.create_rectangle(x0, y0, x0 + app.cellSizex, 
    y0 + app.cellSizey, fill=color, outline= 'black')
  
def drawPausedMenu(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
    text='Paused', font='Arial 60 bold')

def drawMiniMap(app, canvas):
    leftedge = app.minimapx-70
    topedge = app.minimapy-70
    rightedge = app.minimapx+70
    bottomedge = app.minimapy+70
    canvas.create_rectangle(leftedge,topedge,rightedge,bottomedge, fill='black')
    for row in range(len(app.grid)):
        for col in range(len(app.grid[0])):
            # Highlights Isaac's current room.
            if (app.grid[row][col] == app.currentRoom):
                color = 'yellow'
            elif ((row,col) in app.visitedRooms):
                color = 'gray'
            else:
                color = 'black'
            drawCell(app, canvas, leftedge, topedge, row, col, color)
       
def drawHitboxes(app, canvas):
    # This function allows the user to view entity hitboxes.
    # User's Hitbox
    canvas.create_rectangle(app.Isaac.xpos - app.size[0]//2, app.Isaac.ypos - app.size[1]//2, app.Isaac.xpos + app.size[0]//2, app.Isaac.ypos + app.size[1]//2, outline='red')
    # Monsters' Hitboxes
    for monster in app.monstersInRoom:
        cx = monster.xpos
        cy = monster.ypos
        canvas.create_rectangle(cx-monster.size, cy-monster.size, cx+monster.size, cy+monster.size, outline='red')
    
    # Tear Hitboxes
    for tear in app.tears:
        canvas.create_oval(tear.xpos-tear.size, tear.ypos-tear.size, tear.xpos+tear.size,tear.ypos+tear.size, outline='blue')
    
    # Door Hitboxes
    for door in app.doors:
        # Determine how manu doors curent room needs.
        if (door.isOpen == 'yes'):
            cx = door.location[0]
            cy = door.location[1]
            canvas.create_rectangle(cx-door.xsize,cy-door.ysize,cx+door.xsize,
            cy+door.ysize, outline='red')

    # Item Hitboxes 
    if ((isinstance(app.itemInRoom, Item)) and (app.roomCleared == True)):
        cx = app.itemInRoom.xpos
        cy = app.itemInRoom.ypos
        size = app.itemInRoom.size
        canvas.create_rectangle(cx - size, cy - size, cx + size, cy + size, outline='yellow')

def drawImages(app, canvas):
    # This function pastes images of all entities in the room.
    for monster in app.monstersInRoom:
        cx = monster.xpos
        cy = monster.ypos
        if (monster.species == 'Boomfly'):
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.scaled_image_boomfly))
        
        elif (monster.species == 'Fly'):
            canvas.create_image(cx, cy, image=ImageTk.PhotoImage(app.scaled_image_fly))
    
    for tear in app.tears:
        canvas.create_image(tear.xpos, tear.ypos, image=ImageTk.PhotoImage(app.scaled_image_tear))
    
    for door in app.doors:
        if (door.isOpen == 'yes'):
            cx = door.location[0]
            cy = door.location[1]
            if (door.orientation == 'floor'):
                canvas.create_image(cx,cy, 
                image=ImageTk.PhotoImage(app.scaled_image_trapdoor))
            
            elif (door.orientation == 'Top'):
                canvas.create_image(cx,cy, 
                image=ImageTk.PhotoImage(app.scaled_image_door))
            
            elif (door.orientation == 'Bottom'):
                bottomdoorimage = app.scaled_image_door.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                canvas.create_image(cx,cy, 
                image=ImageTk.PhotoImage(bottomdoorimage))
            
            elif (door.orientation == 'Left'):
                leftdoorimage = app.scaled_image_door.transpose(Image.Transpose.ROTATE_90)
                canvas.create_image(cx,cy, 
                image=ImageTk.PhotoImage(leftdoorimage))
            
            elif (door.orientation == 'Right'):
                rightdoorimage = app.scaled_image_door.transpose(Image.Transpose.ROTATE_270)
                canvas.create_image(cx,cy, 
                image=ImageTk.PhotoImage(rightdoorimage))

    if ((isinstance(app.itemInRoom, Item)) and (app.roomCleared == True)):
        cx = app.itemInRoom.xpos
        cy = app.itemInRoom.ypos
        canvas.create_image(cx, cy, 
        image=ImageTk.PhotoImage(app.itemInRoom.image))
         
def drawGameOver(app, canvas):
    # This function displays the game-over screen.
    canvas.create_rectangle(0,0,app.width,app.height,fill='gray')
    canvas.create_text(app.width//2,app.height//2,text='Game Over', 
    font='Arial 60 bold')

def drawStartScreen(app, canvas):
    # This function displays the start screen.
    canvas.create_image(app.width//2,app.height//2,
    image=ImageTk.PhotoImage(app.scaled_image_startScreen))

def redrawAll(app, canvas): 
    # Until the game has started, none of the game's images will load.
    if app.gameStarted == True:
        # If the game is over, all images will be removed and replaced with the 
        # game-over screen.
        if app.gameOver == False:
            drawRoom(app, canvas)

            if app.paused != False:
                drawPausedMenu(app, canvas)

            if app.displayMap == True:
                drawMiniMap(app, canvas)

            if app.displayGraph == True:
                drawGraph(app, canvas)

            drawImages(app, canvas)
            sprite = app.isaacSprites[app.spriteCounter]
            canvas.create_image(app.Isaac.xpos,
            app.Isaac.ypos - 15,image=ImageTk.PhotoImage(sprite))

            if app.displayHitboxes == True:
                drawHitboxes(app, canvas)
        else:
            drawGameOver(app, canvas)
    else:
        drawStartScreen(app, canvas)
        canvas.create_text(app.width//2 - 50, (3/4)*app.height + 100, 
        text='(Space)', font='Arial 30 bold', fill='black')

# Game Must Be Run in a 960x540 App.       
runApp(width=960, height=540)