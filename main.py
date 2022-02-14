from cmu_112_graphics import *
import time
import random
import math
#############################     MODEL    ################################
def appStarted(app):
    froggerSetting(app)
    app.mazeBoard = False
    app.inHelpScreen = True
    app.mazeRows = 13
    app.mazeCols=13
    mazeSetting(app, app.mazeRows, app.mazeCols, app.inHelpScreen)
    app.mazeGameOver = False 
    app.mazeTime0 = None
    app.mazeFinalTime = None

# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
def mazeSetting(app, rows=13, cols=13, inHelpScreen=True):
    if (rows < 1):
        rows = 1
    if (cols < 1):
        cols = 1
    app.inHelpScreen = True
    app.rows = rows
    app.cols = cols
    app.islandColor = "dark green"
    app.bridgeColor = "white"
    app.pathColor = "green"
    app.solutionColor = "red"
    app.path = set()
    app.solution = None
    app.playerSpot = (0,0) 
    app.path.add(app.playerSpot)
    app.margin = 5
    app.cW = (app.width-app.margin)/cols
    app.cH = (app.height - app.margin) / rows
    app.maze = makeBlankMaze(rows, cols)
    connectIslands(app.maze)
    resetGame(app)
    app.frogWentUp = False
    app.frogWentDown = True
    app.frogWentRight = False
    app.frogWentLeft = False
    
def resetGame(app):
    row, cols = len(app.maze), len(app.maze[0])
    app.solution = None
    app.path = set()
    app.playerSpot = (0,0) 
    app.path.add(app.playerSpot)
    app.maze = makeBlankMaze(row, cols)
    connectIslands(app.maze)
    
def makeBlankMaze(rows, cols):
    islands = [[0]*cols for row in range(rows)]
    counter = 0
    for row in range(rows):
        for col in range(cols):
            islands[row][col] = makeIsland(counter)
            counter += 1
    return islands

class Struct(object): pass 

def makeIsland(number):
    island = Struct()
    island.east = island.south = False
    island.number = number
    return island

def connectIslands(islands):
    rows,cols = len(islands),len(islands[0])
    for i in range(rows*cols-1):
        makeBridge(islands)
        
def makeBridge(islands):
    rows, cols = len(islands), len(islands[0])
    while True:
        row,col = random.randint(0,rows-1),random.randint(0,cols-1)
        start = islands[row][col]
        if flipCoin(): #try to go east
            if col==cols-1: continue
            target = islands[row][col+1]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.east = True
            renameIslands(start,target,islands)
        else: #try to go south
            if row==rows-1: continue
            target = islands[row+1][col]
            if start.number==target.number: continue
            #the bridge is valid, so 1. connect them and 2. rename them
            start.south = True
            renameIslands(start,target,islands)
        #only got here if a bridge was made
        return

def renameIslands(i1,i2,islands):
    n1,n2 = i1.number,i2.number
    lo,hi = min(n1,n2),max(n1,n2)
    for row in islands:
        for island in row:
            if island.number==hi: 
                island.number=lo

def flipCoin():
    return random.choice([True, False])

def froggerSetting(app):
    app.start0 = time.time()
    app.timeTook = None
    app.gameOverFrogger = False
    app.board = make2dList(13, 13)
    grid(app)
    bottomHalfObstacles(app)
    upperHalfObstacles(app)
    bottomHalfTimers(app)
    upperHalfTimers(app)
    app.frogs=[(12,6)]
    onObject(app)

def onObject(app): # checks if frog is on an upper half object 
    app.onSecondTurtles = False # on row 5
    app.onThirdLogs = False  # on row 4
    app.onSecondLogs = False  # on row 3
    app.onFirstTurtles = False  # on row 2
    app.onFirstLogs = False    # on row 1
 
def grid(app): # overall grid elements 
    app.margin = 50 # only for top and below 
    app.cols = 13  # each column is 53.85 px
    app.rows = 13  # each row is approx 61.5 px
    
def bottomHalfObstacles(app):
    app.trucks = [(7, 2), (7, 6), (7,10)]
    app.buggy = [(8,3), (8, 6), (8,9), (8, 12)]
    app.cars = [(9,2), (9, 5), (9,8), (9, 11)]
    app.tractors = [(10,2), (10,6), (10, 10)]
    app.carts = [(11,1), (11,4), (11,8), (11,11)]
    
def upperHalfObstacles(app):
    app.firstLogs = [(1,1), (1,2), (1,3), (1,4), (1,9), (1,10), (1,11)]
    app.firstTurtles = [(2,1), (2,2), (2,5), (2,6), (2,9), (2,10)]
    app.secondLogs = [(3,0), (3,1), (3,4), (3,5), (3,6), (3,10), (3,11)]
    app.thirdLogs = [(4,2), (4,3), (4,6), (4,7), (4,8), (4,10), (4,11), (4,12)]
    app.secondTurtles = [(5,0), (5,1), (5,2), (5,6), (5,7), (5,10), (5,11)]

def bottomHalfTimers(app):
    app.buggyTractorsStartTime = time.time() # setting time for buggy & tractors
    app.carsCartsStartTime = time.time() # setting time for car & carts
    app.trucksStartTime = time.time() # setting time for trucks 
    
def upperHalfTimers(app):
    app.firstThirdLogStartTime = time.time()
    app.secondLogStartTime = time.time()
    app.turtleStartTime = time.time()

# from https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#creating2dLists
def make2dList(rows, cols):
    return [ ([0] * cols) for row in range(rows) ]

###########################     CONTROL    ###############################
def timerFired(app):
    if app.mazeBoard == False:
        # bottom Half
        # timer for buggy & tractor
        if app.gameOverFrogger == True:
            return
        if time.time()-app.buggyTractorsStartTime >= 0.5: 
            # buggy modification 
            buggyResult = []
            for row, col in app.buggy:
                if col > 13:
                    col = 0
                buggyResult.insert(0, (row, col+1))
            app.buggy = buggyResult
            # tractor modification
            tractorResult = []
            for row, col in app.tractors:
                if col > 13:
                    col = 0
                tractorResult.insert(0, (row, col+1))
            app.tractors = tractorResult
            app.buggyTractorsStartTime = time.time()
            
        if time.time() - app.carsCartsStartTime >= 1: # timer for cars and carts
            # car modification
            carResult = []
            for row, col in app.cars:
                if col < 0:
                    col = 13
                carResult.append((row, col-1))
            app.cars = carResult 
            # cart modification
            cartResult = []
            for row, col in app.carts:
                if col < 0:
                    col = 13
                cartResult.append((row, col-1))
            app.carts = cartResult
            app.carsCartsStartTime = time.time()
            
        if time.time() - app.trucksStartTime >= 0.7:  # timer for trucks
            # truck modification
            truckResult = []
            for row, col in app.trucks:
                if col < 0:
                    col = 13
                truckResult.append((row, col - 1))
            app.trucks = truckResult    
            app.trucksStartTime = time.time()
        
        if checkCollision(app, app.frogs) == True:
            app.frogs = [(12, 6)]
            
        # upper half
        if time.time() - app.firstThirdLogStartTime >= 0.5:
            firstLogResult = []
            for row, col in app.firstLogs:
                firstLogResult.append((row, col-1))
                if col == 0:
                    firstLogResult.pop()
                    firstLogResult.append((row, 13))
            app.firstLogs = firstLogResult
            thirdLogResult = []
            for row, col in app.thirdLogs:
                thirdLogResult.append((row, col-1))
                if col == 0:
                    thirdLogResult.pop()
                    thirdLogResult.append((row, 13))
            app.thirdLogs = thirdLogResult
            # check if frog is on object
            if app.onThirdLogs == True:
                frogMoving = []
                for row, col in app.frogs:
                    frogMoving.append((row, col-1))
                app.frogs = frogMoving 
            if app.onFirstLogs == True:
                frogMoving = []
                for row, col in app.frogs:
                    frogMoving.append((row, col-1))
                app.frogs = frogMoving 
            app.firstThirdLogStartTime = time.time()
            
        if time.time() - app.secondLogStartTime >= 0.25:
            secondLogResult = []
            for row, col in app.secondLogs:
                secondLogResult.append((row, col-1))
                if col == 0:
                    secondLogResult.pop()
                    secondLogResult.append((row, 13))
            app.secondLogs = secondLogResult 
            # check if frog is on object 
            if app.onSecondLogs == True:
                frogMoving = []
                for row, col in app.frogs:
                    frogMoving.append((row, col-1))
                app.frogs = frogMoving 
            app.secondLogStartTime = time.time()
        
        if time.time() - app.turtleStartTime >= 0.7:
            firstTurtleResult = []
            for row, col in app.firstTurtles:
                firstTurtleResult.append((row, col+1))
                if col == 13:
                    firstTurtleResult.pop()
                    firstTurtleResult.insert(0, (row, 0))
            app.firstTurtles = firstTurtleResult
            secondTurtleResult = []
            for row, col in app.secondTurtles:
                secondTurtleResult.append((row, col+1))
                if col == 13:
                    secondTurtleResult.pop()
                    secondTurtleResult.insert(0, (row, 0))
            app.secondTurtles = secondTurtleResult
            # checks if frog is on object and makes the frog move with object  
            if app.onSecondTurtles == True:
                frogMoving = [] 
                for row, col in app.frogs: 
                    frogMoving.append((row, col+1))
                app.frogs = frogMoving 
            if app.onFirstTurtles == True:
                frogMoving = [] 
                for row, col in app.frogs: 
                    frogMoving.append((row, col+1))
                app.frogs = frogMoving 
            app.turtleStartTime = time.time()
        
        for row, col in app.frogs:
            if (checkOnObject(app, app.frogs) == False) and (1<=row<=5):
                app.onSecondTurtles = False 
                app.onThirdLogs = False
                app.onSecondLogs = False 
                app.onFirstTurtles = False
                app.onFirstLogs = False 
                app.frogs = [(12,6)]
                

# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
NORTH = (-1,0)
SOUTH = (1,0)
EAST  = (0,1)
WEST  = (0,-1)

def keyPressed(app, event):
    # for maze
    if event.key == "m" or event.key=="M":
        app.mazeBoard = True 
        app.mazeTime0 = time.time()
        
    if app.mazeBoard==True: 
        row, col = app.playerSpot      
        if app.inHelpScreen == True:
            app.inHelpScreen = False
        elif event.key == "h" or event.key == "H":
            app.inHelpScreen = True
        elif event.key == "r":
            resetGame(app)
            app.mazeGameOver = False 
            app.mazeTime0 = time.time()
        elif event.key=="s":
        #toggle solution
            if app.solution==None:
                app.solution = solveMaze(app)
            else:
                app.solution=None
        elif event.key == "Up" and isValid(app, row, col, NORTH):
            doMove(app, row, col, NORTH)
            if app.path == solveMaze(app):
                app.mazeGameOver = True
                app.mazeFinalTime = time.time() - app.mazeTime0 
            app.frogWentUp = True
            app.frogWentDown = False
            app.frogWentRight = False
            app.frogWentLeft = False
        elif event.key == "Down" and isValid(app, row, col, SOUTH):
            doMove(app, row, col, SOUTH)
            if app.path == solveMaze(app):
                app.mazeGameOver = True
                app.mazeFinalTime = time.time() - app.mazeTime0 
            app.frogWentUp = False
            app.frogWentDown = True
            app.frogWentRight = False
            app.frogWentLeft = False
        elif event.key == "Left" and isValid(app, row, col, WEST):
            doMove(app, row, col, WEST)
            if app.path == solveMaze(app):
                app.mazeGameOver = True
                app.mazeFinalTime = time.time() - app.mazeTime0 
            app.frogWentUp = False
            app.frogWentDown = False
            app.frogWentRight = False
            app.frogWentLeft = True
        elif event.key == "Right" and isValid(app, row, col, EAST):
            doMove(app, row, col, EAST)
            if app.path == solveMaze(app):
                app.mazeGameOver = True
                app.mazeFinalTime = time.time() - app.mazeTime0 
            app.frogWentUp = False
            app.frogWentDown = False
            app.frogWentRight = True
            app.frogWentLeft = False
            
    # for supper frogger 
    if app.mazeBoard == False or event.key == 'f' or event.key == 'F':
        app.mazeBoard = False
        frogResult = []
        for (row, col) in app.frogs:
            if event.key == 'r' and app.gameOverFrogger == True or event.key=='f':
                frogResult = [(12, 6)]
                app.gameOverFrogger = False
                froggerSetting(app)
            if row == 1:
                app.gameOverFrogger = True
                app.timeTook = time.time()-app.start0
            if event.key == 'Up': 
                if row <= 0: # checks so the frog doesn't go off board 
                    frogResult.append((row, col))
                else:
                    frogResult.append((row-1, col))
                    if checkCollision(app, frogResult):
                        frogResult = [(12, 6)]
                    if checkOnObject(app, frogResult) == True:
                        for (row, col) in frogResult:
                            if row == 5:
                                app.onSecondTurtles = True 
                            if row == 4:
                                app.onThirdLogs = True 
                                app.onSecondTurtles = False 
                            if row == 3:
                                app.onSecondLogs = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                            if row == 2:
                                app.onFirstTurtles = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                                app.onSecondLogs = False 
                            if row == 1:
                                app.onFirstLogs = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                                app.onSecondLogs = False 
                                app.onFirstTurtles = False
                    if checkOnObject(app, frogResult) == False:
                        app.onSecondTurtles = False 
                        app.onThirdLogs = False
                        app.onSecondLogs = False 
                        app.onFirstTurtles = False
                        app.onFirstLogs = False 
            if event.key == "Down":
                if row >= 12:
                    frogResult.append((row, col))
                else:
                    frogResult.append((row+1, col))
                    if checkCollision(app, frogResult):
                        frogResult = [(12, 6)]
                    if checkOnObject(app, frogResult) == True:
                        for (row, col) in frogResult:
                            if row == 5:
                                app.onSecondTurtles = True 
                            if row == 4:
                                app.onThirdLogs = True 
                                app.onSecondTurtles = False 
                            if row == 3:
                                app.onSecondLogs = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                            if row == 2:
                                app.onFirstTurtles = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                                app.onSecondLogs = False 
                            if row == 1:
                                app.onFirstLogs = True
                                app.onSecondTurtles = False 
                                app.onThirdLogs = False
                                app.onSecondLogs = False 
                                app.onFirstTurtles = False
                    if checkOnObject(app, frogResult) == False:
                        app.onSecondTurtles = False 
                        app.onThirdLogs = False
                        app.onSecondLogs = False 
                        app.onFirstTurtles = False
                        app.onFirstLogs = False            
            if event.key == "Left": 
                if col <= 0:
                    frogResult.append((row, col))
                else:
                    frogResult.append((row, col-1))
                    if checkCollision(app, frogResult):
                        frogResult = [(12, 6)]
                    if checkOnObject(app, frogResult) == True:
                        for (row, col) in frogResult:
                            if row == 5:
                                app.onSecondTurtles = True 
                            if row == 4:
                                app.onThirdLogs = True 
                            if row == 3:
                                app.onSecondLogs = True
                            if row == 2:
                                app.onFirstTurtles = True
                            if row == 1:
                                app.onFirstLogs = True
                    if checkOnObject(app, frogResult) == False:
                        app.onSecondTurtles = False 
                        app.onThirdLogs = False
                        app.onSecondLogs = False 
                        app.onFirstTurtles = False
                        app.onFirstLogs = False 
            if event.key == "Right":
                if col >= 12:
                    frogResult.append((row, col))
                else:
                    frogResult.append((row, col+1))
                    if checkCollision(app, frogResult):
                        frogResult = [(12, 6)]
                    if checkOnObject(app, frogResult) == True:
                        for (row, col) in frogResult:
                            if row == 5:
                                app.onSecondTurtles = True 
                            if row == 4:
                                app.onThirdLogs = True 
                            if row == 3:
                                app.onSecondLogs = True
                            if row == 2:
                                app.onFirstTurtles = True
                            if row == 1:
                                app.onFirstLogs = True
                    if checkOnObject(app, frogResult) == False:
                        app.onSecondTurtles = False 
                        app.onThirdLogs = False
                        app.onSecondLogs = False 
                        app.onFirstTurtles = False
                        app.onFirstLogs = False 
        app.frogs = frogResult

def solveMaze(app):
    maze = app.maze
    width = len(maze)
    height = len(maze[0])
    visited = set()
    def solve(row,col):
        if row == width - 1 and col == height-1:
            return True
        if (row, col) in visited:
            return False
        visited.add((row,col))
        if (isValid(app, row, col, (1,0))):
            if (solve(row+1, col)):
                return True
        if (isValid(app, row, col, (0,1))):
            if (solve(row, col+1)):
                return True
        if (isValid(app, row, col, (-1,0))):
            if (solve(row-1, col)):
                return True
        if (isValid(app, row, col, (0, -1))):
            if (solve(row, col-1)):
                return True
        visited.remove((row, col))
        return False
    return visited if solve(0,0) else None 

def isValid(app, row, col, direction):
    maze = app.maze
    rows, cols = len(maze), len(maze[0])
    if not (0<=row<=rows and 0<=col<cols):
        return False
    if direction == EAST:
        return maze[row][col].east
    if direction==SOUTH: 
        return maze[row][col].south
    if direction==WEST: 
        return maze[row][col-1].east
    if direction==NORTH: 
        return maze[row-1][col].south
    assert False

def doMove(app, row, col, direction):
    (drow, dcol) = direction
    maze, path = app.maze, app.path
    rows,cols = len(maze),len(maze[0])
    if not (0<=row<rows and 0<=col<cols): 
        return False
    if ((row+drow,col+dcol)) in path: 
        path.remove((row,col))
    else: 
        path.add((row+drow,col+dcol))
    app.playerSpot = (row+drow,col+dcol)

def checkCollision(app, L):
    for (frogRow, frogCol) in L:
        for (truckRow, truckCol) in app.trucks:
            if frogCol == truckCol and frogRow == truckRow:
                return True
        for (buggyRow, buggyCol) in app.buggy:
            if frogCol == buggyCol and frogRow == buggyRow:
                return True
        for (carRow, carCol) in app.cars:
            if frogCol == carCol and frogRow == carRow:
                return True
        for (tractorRow, tractorCol) in app.tractors:
            if frogCol == tractorCol and frogRow == tractorRow:
                return True
        for (cartRow, cartCol) in app.carts:
            if frogCol == cartCol and frogRow == cartRow:
                return True
    return False 

def checkOnObject(app, L):
    for (frogRow, frogCol) in L:
        for (secondTurtleRow, secondTurtleCol) in app.secondTurtles:
            if frogRow == secondTurtleRow and frogCol == secondTurtleCol:
                return True 
        for (thirdLogRow, thirdLogCol) in app.thirdLogs:
            if frogRow ==  thirdLogRow and frogCol == thirdLogCol:
                return True
        for (secondLogRow, secondLogCol) in app.secondLogs:
            if frogRow == secondLogRow and frogCol == secondLogCol:
                return True
        for (firstTurtleRow, firstTurtleCol) in app.firstTurtles:
            if frogRow == firstTurtleRow and frogCol == firstTurtleCol:
                return True
        for (firstLogRow, firstLogCol) in app.firstLogs:
            if frogRow == firstLogRow and frogCol == firstLogCol:
                return True
    return False 

#############################     VIEW    #################################
def redrawAll(app, canvas):
    if app.mazeBoard == False:
        drawBoard(app, canvas)
        drawTrucks(app, canvas)
        drawBuggies(app, canvas)
        drawCars(app, canvas)
        drawTractors(app, canvas)
        drawCarts(app, canvas)
        drawLogs(app, canvas)
        drawTurtles(app, canvas)
        drawLand(app, canvas)
        drawFrogs(app, canvas)
        if app.gameOverFrogger == True:
            drawInstructions(app, canvas)
    # from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
    if app.mazeBoard == True:
        if app.inHelpScreen == True:
            return drawHelpScreen(app, canvas)
        canvas.create_rectangle(0,0, app.width, app.height, fill="darkBlue")
        drawBridges(app, canvas)
        drawIslands(app, canvas)
        if app.solution != None:
            drawSolutionPath(app, canvas)
        drawPlayerPath(app, canvas)
        if app.mazeGameOver == True:
            drawVictory(app, canvas)

def drawVictory(app, canvas):
    canvas.create_text(app.width//2, app.height//2, text=(f"You Made It! It took {app.mazeFinalTime:.2f}seconds!"+ 
                                                          "\n" 
                                                          +"Press r to restart and f to play the frogger game"),
                        fill = "red", font="Helvetica 20 bold")

def drawInstructions(app, canvas):
    canvas.create_text(app.width//2, 20, 
                       text=f"You Won! It took {app.timeTook:.2f} seconds! Press r to restart and m to play a Maze Game!",
                       fill="black", font="Helvetica 20 bold")

# from https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#mazeSolving
def drawPlayerPath(app, canvas):
    path = app.path
    (pRow, pCol) = app.playerSpot
    color = app.pathColor
    r = min(app.cW, app.cH)/10
    width = min(app.cW, app.cH)/30
    for row, col in path:
        cx, cy = islandCenter(app, row, col)
        canvas.create_oval(cx-2*r,cy-2*r,cx+2*r,cy+2*r,fill=color,width=0)
        
        if (row+1, col) in path and isValid(app, row, col, SOUTH):
            canvas.create_line(islandCenter(app, row, col), 
                                islandCenter(app, row+1, col),
                                fill=color, width=width)
        if (row, col+1) in path and isValid(app, row, col, EAST):
            canvas.create_line(islandCenter(app, row,col),
                                   islandCenter(app, row,col+1),
                                   fill=color, width=width)
    cx, cy = islandCenter(app, pRow, pCol)
    if app.frogWentDown == True:
        canvas.create_oval(cx-3*r, cy-3*r, cx+3*r, cy+3*r, fill="lightGreen",
                           width=0)
        canvas.create_oval(cx+r-20,cy+r+10, cx+r-10, cy+r+20, fill="lightGreen",
                           width=0)
        canvas.create_oval(cx+r-3, cy+r+10, cx+r+7, cy+r+20, fill="lightGreen", 
                           width=0)
        canvas.create_rectangle(cx-2*r, cy-2*r, cx-2*r-10, cy-2*r+3, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx+2*r, cy-2*r, cx+2*r+10, cy-2*r+3, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-2*r, cy-2*r+20, cx-2*r-10, cy-2*r+23, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx+2*r, cy-2*r+20, cx+2*r+10, cy-2*r+23, 
                                fill="lightGreen", width=0)
        canvas.create_oval(cx+r-18, cy+r+12, cx+r-12, cy+r+18, fill="black", 
                           width=0)
        canvas.create_oval(cx+r-1, cy+r+12, cx+r+5, cy+r+18, fill="black", 
                           width=0)
    if app.frogWentRight == True:
        canvas.create_oval(cx-3*r, cy-3*r, cx+3*r, cy+3*r, fill="lightGreen", 
                           width=0)
        canvas.create_oval(cx+3*r-2, cy-3*r+10, cx+3*r+8, cy-3*r+20, 
                           fill="lightGreen", width=0)
        canvas.create_oval(cx+3*r-5, cy-3*r+25, cx+3*r+5, cy-3*r+35, 
                           fill='lightGreen', width=0)
        canvas.create_oval(cx+3*r, cy-3*r+12, cx+3*r+6, cy-3*r+18, 
                           fill="black", width=0)
        canvas.create_oval(cx+3*r-3, cy-3*r+27, cx+3*r+3, cy-3*r+33, 
                           fill="black", width = 0)
        canvas.create_rectangle(cx-3*r+20, cy-3*r-8, cx-3*r+23, cy-3*r+2, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+10, cy-3*r-8, cx-3*r+13, cy-3*r+2, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+20, cy+3*r-2, cx-3*r+23, cy+3*r+8, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+10, cy+3*r-2, cx-3*r+13, cy+3*r+8 , 
                                fill="lightGreen", width=0)
    if app.frogWentLeft == True:
        canvas.create_oval(cx-3*r, cy-3*r, cx+3*r, cy+3*r, fill="lightGreen", 
                           width=0)
        canvas.create_oval(cx-3*r+2, cy-3*r+10, cx-3*r-8, cy-3*r+20,
                           fill="lightGreen", width=0)
        canvas.create_oval(cx-3*r+5, cy-3*r+25, cx-3*r-5, cy-3*r+35, 
                           fill="lightGreen", width=0)
        canvas.create_oval(cx-3*r, cy-3*r+12, cx-3*r-6, cy-3*r+18, 
                           fill="black", width=0)
        canvas.create_oval(cx-3*r+3, cy-3*r+27, cx-3*r-3, cy-3*r+33, 
                           fill="black", width=0)
        canvas.create_rectangle(cx-3*r+20, cy-3*r-8, cx-3*r+23, cy-3*r+2, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+10, cy-3*r-8, cx-3*r+13, cy-3*r+2, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+20, cy+3*r-2, cx-3*r+23, cy+3*r+8, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-3*r+10, cy+3*r-2, cx-3*r+13, cy+3*r+8 , 
                                fill="lightGreen", width=0)
    if app.frogWentUp == True:
        canvas.create_oval(cx-3*r, cy-3*r, cx+3*r, cy+3*r, fill="lightGreen", 
                           width=0)
        canvas.create_oval(cx+r-20,cy-r-20, cx+r-10, cy-r-10, fill="lightGreen", 
                           width=0)
        canvas.create_oval(cx+r-3, cy-r-20, cx+r+7, cy-r-10, fill="lightGreen", 
                           width=0)
        canvas.create_oval(cx+r-18, cy-r-18, cx+r-12, cy-r-12, fill='black',
                           width=0)
        canvas.create_oval(cx+r-1, cy-r-18, cx+r+5, cy-r-12, fill="black", 
                           width=0)
        canvas.create_rectangle(cx-2*r, cy-2*r, cx-2*r-10, cy-2*r+3, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx+2*r, cy-2*r, cx+2*r+10, cy-2*r+3, 
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx-2*r, cy-2*r+20, cx-2*r-10, cy-2*r+23,
                                fill="lightGreen", width=0)
        canvas.create_rectangle(cx+2*r, cy-2*r+20, cx+2*r+10, cy-2*r+23, 
                                fill="lightGreen", width=0)


def drawSolutionPath(app, canvas):
    color = app.solutionColor
    r = min(app.cW, app.cH)/6
    width = min(app.cW, app.cH)/15
    for (row, col) in app.solution:
        (cx, cy) = islandCenter(app, row, col)
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill=color,width=0)
        if (row+1, col) in app.solution and isValid(app, row, col, SOUTH):
            canvas.create_line(islandCenter(app, row, col), 
                            islandCenter(app, row+1, col),
                            fill = color, width = width)
        if (row, col+1) in app.solution and isValid(app, row, col, EAST):
            x0 = islandCenter(app, row, col)
            x1 = islandCenter(app, row, col+1)
            canvas.create_line(x0, x1, fill = color, width = width)

def drawIslands(app, canvas):
    islands = app.maze
    rows,cols = len(islands),len(islands[0])
    color = app.islandColor
    r = min(app.cW,app.cH)/8
    for row in range(rows):
        for col in range(cols):
            (cx, cy) = islandCenter(app, row, col)
            canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, fill=color, width=0)

def drawBridges(app, canvas):
    islands = app.maze
    rows, cols = len(islands), len(islands[0])
    color = app.bridgeColor
    width = min(app.cW, app.cH)/30
    idk = min(app.cW,app.cH)/8
    for r in range(rows):
        for c in range(cols):
            island = islands[r][c]
            if (island.east):
                canvas.create_line(islandCenter(app, r,c),
                                   islandCenter(app, r,c+1),
                                   fill=color, width=width)
            if (island.south):
                canvas.create_line(islandCenter(app, r,c),
                                   islandCenter(app, r+1,c),
                                   fill=color, width=width)
                
def islandCenter(app, row, col):
    cellWidth,cellHeight = app.cW,app.cH
    return (col+0.5)*cellWidth,(row+0.5)*cellHeight
        
def drawHelpScreen(app, canvas):
    font = "Helvetica 32 bold"
    canvas.create_text(app.width//2, 50, text="Maze Solver", font=font)
    font = "Helvetica 24 bold"
    messages = [
                "arrows to solve manually",
                "r to reset (make new maze)",
                "s to toggle solution on/off",
                "h to view this help screen",
                "press any key to continue"
                "press f to go back to frogger game"
                ]
    for i in range(len(messages)):
        canvas.create_text(app.width//2, 150+50*i, text=messages[i], font=font)

def drawTurtles(app, canvas):
    for (row, col) in app.firstTurtles:
        (x0, y0, x1, y1) = getCellBounds(app, row, col) 
        canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="orange", width=0)
        canvas.create_oval(x1, y0+17, x1-17, y1-17, fill="lightGreen", width=0)
        canvas.create_rectangle(x0+20, y0+13, x0+30, y0+16,fill="white",width=0)
        canvas.create_rectangle(x0+10, y0+17, x0+15, y0+20,fill="white",width=0)
        canvas.create_rectangle(x0+33, y0+17, x0+40, y0+20,fill="white",width=0)
        # turtle eyes
        canvas.create_oval(x1, y0+17, x1-10, y0+25, fill="white", width=0)
        canvas.create_oval(x1, y0+29, x1-10, y0+37, fill="white", width=0)
        canvas.create_oval(x1-3, y0+19, x1-6, y0+22, fill="black")
        canvas.create_oval(x1-3, y0+31, x1-6, y0+34, fill="black")
        # turtle legs
        canvas.create_oval(x0+14, y0+1, x0+23, y0+12,fill="lightGreen", width=0)
        canvas.create_oval(x0+40, y0+1, x0+49, y0+12,fill="lightGreen", width=0)
        canvas.create_oval(x0+14, y1-1, x0+23, y1-12,fill="lightGreen", width=0)
        canvas.create_oval(x0+40, y1-1, x0+49, y1-12,fill="lightGreen", width=0)
        # turtle tail
        canvas.create_oval(x0+1, y0+25, x0+8, y0+30, fill="lightGreen", width=0) 
    for (row, col) in app.secondTurtles:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x0+5, y0+5, x1-5, y1-5, fill="orange", width=0)
        canvas.create_oval(x1, y0+17, x1-17, y1-17, fill="lightGreen", width=0)
        canvas.create_rectangle(x0+20, y0+13, x0+30, y0+16,fill="white",width=0)
        canvas.create_rectangle(x0+10, y0+17, x0+15, y0+20,fill="white",width=0)
        canvas.create_rectangle(x0+33, y0+17, x0+40, y0+20,fill="white",width=0)
        # turtle eyes
        canvas.create_oval(x1, y0+17, x1-10, y0+25, fill="white", width=0)
        canvas.create_oval(x1, y0+29, x1-10, y0+37, fill="white", width=0)
        canvas.create_oval(x1-3, y0+19, x1-6, y0+22, fill="black")
        canvas.create_oval(x1-3, y0+31, x1-6, y0+34, fill="black")
        # turtle legs
        canvas.create_oval(x0+14, y0+1, x0+23, y0+12,fill="lightGreen", width=0)
        canvas.create_oval(x0+40, y0+1, x0+49, y0+12,fill="lightGreen", width=0)
        canvas.create_oval(x0+14, y1-1, x0+23, y1-12,fill="lightGreen", width=0)
        canvas.create_oval(x0+40, y1-1, x0+49, y1-12,fill="lightGreen", width=0)
        # turtle tail
        canvas.create_oval(x0+1, y0+25, x0+8, y0+30, fill="lightGreen", width=0)

def drawLogs(app, canvas):
    for (row, col) in app.firstLogs:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0+12, x0+15, y0+15, fill="orange", width=0)
        canvas.create_rectangle(x0+17, y0+12, x0+22,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+25, y0+12, x0+33,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+35, y0+12, x0+43,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+45, y0+12, x1, y0+15, fill="orange", width=0)
        canvas.create_rectangle(x0, y1-12, x0+15, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+17, y1-12, x0+22, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+25, y1-12, x0+33, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+35, y1-12, x0+43, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+45, y1-12, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0, y0+15, x1, y1-15, fill="orange", width=0)
        canvas.create_rectangle(x0, y0+20, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+4, y0+17, x0+20, y0+19, fill="white",width=0)
        canvas.create_rectangle(x0+30, y0+17, x0+40, y0+19,fill="white",width=0)
        canvas.create_rectangle(x0+19, y0+21, x0+35, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+45, y0+21, x0+55, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+1, y0+25, x0+22, y0+28, fill="white",width=0)
        canvas.create_rectangle(x0+50, y0+25, x0+60, y0+28,fill="white",width=0)
    for (row, col) in app.secondLogs:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0+12, x0+15, y0+15, fill="orange", width=0)
        canvas.create_rectangle(x0+17, y0+12, x0+22,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+25, y0+12, x0+33,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+35, y0+12, x0+43,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+45, y0+12, x1, y0+15, fill="orange",width=0)
        canvas.create_rectangle(x0, y1-12, x0+15, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+17, y1-12, x0+22, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+25, y1-12, x0+33, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+35, y1-12, x0+43, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+45, y1-12, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0, y0+15, x1, y1-15, fill="orange", width=0)
        canvas.create_rectangle(x0, y0+20, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+4, y0+17, x0+20, y0+19,fill="white",width=0)
        canvas.create_rectangle(x0+30, y0+17, x0+40, y0+19,fill="white",width=0)
        canvas.create_rectangle(x0+19, y0+21, x0+35, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+45, y0+21, x0+55, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+1, y0+25, x0+22, y0+28, fill="white",width=0)
        canvas.create_rectangle(x0+50, y0+25, x0+60, y0+28,fill="white",width=0)
    for (row, col) in app.thirdLogs:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0, y0+12, x0+15, y0+15, fill="orange", width=0)
        canvas.create_rectangle(x0+17, y0+12, x0+22,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+25, y0+12, x0+33,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+35, y0+12, x0+43,y0+15,fill="orange",width=0)
        canvas.create_rectangle(x0+45, y0+12, x1, y0+15, fill="orange", width=0)
        canvas.create_rectangle(x0, y1-12, x0+15, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+17, y1-12, x0+22, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+25, y1-12, x0+33, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+35, y1-12, x0+43, y1-15,fill="brown",width=0)
        canvas.create_rectangle(x0+45, y1-12, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0, y0+15, x1, y1-15, fill="orange", width=0)
        canvas.create_rectangle(x0, y0+20, x1, y1-15, fill="brown", width=0)
        canvas.create_rectangle(x0+4, y0+17, x0+20, y0+19,fill="white",width=0)
        canvas.create_rectangle(x0+30, y0+17, x0+40, y0+19,fill="white",width=0)
        canvas.create_rectangle(x0+19, y0+21, x0+35, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+45, y0+21, x0+55, y0+23,fill="white",width=0)
        canvas.create_rectangle(x0+1, y0+25, x0+22, y0+28,fill="white",width=0)
        canvas.create_rectangle(x0+50, y0+25, x0+60, y0+28,fill="white",width=0)

def drawCars(app, canvas):
    for (row, col) in app.cars:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0+5, y0+10, x1-5, y1-10, 
                                fill = "yellow",width = 0 ) # body part
        canvas.create_rectangle(x0+8, y0+4 , x0+20, y0+10, 
                                fill = "purple", width = 0) # above left wheel 
        canvas.create_rectangle(x0+35, y0+4 , x1-10, y0+10, 
                                fill = "purple", width = 0) # above right wheel
        canvas.create_rectangle(x0+8, y1-4 , x0+20, y1-10, 
                                fill = "purple", width = 0) # bottom left wheel 
        canvas.create_rectangle(x0+35, y1-4 , x1-10, y1-10, 
                                fill = "purple", width = 0) # bottom right wheel
        canvas.create_rectangle(x0+10, y0+10, x1-15, y0+13,
                                fill="lightBlue", width=0)
        canvas.create_rectangle(x0+10, y1-10, x1-15, y1-13,
                                fill="lightBlue", width=0)
        canvas.create_rectangle(x0+1, y0+12, x0+6, y1-12,
                                fill="lightBlue", width=0)

def drawTractors(app, canvas):
    for (row, col) in app.tractors:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0+10, y0+13, x0+40, y1-13, 
                                fill="grey", width = 0) # body part
        canvas.create_rectangle(x0+15, y0+5, x0+30, y0+13,
                                fill = "green", width = 0) # above wheel
        canvas.create_rectangle(x0+15, y1-13, x0+30, y1-5, 
                                fill = "green", width = 0) # below wheel
        canvas.create_rectangle(x0+40, y0+13, x0+46, y1-13, fill="black", 
                                outline = "grey", width = "3") 
        canvas.create_rectangle(x0+46, y0+3, x0+55, y1-3, 
                                fill = "grey", width = 0)

def drawFrogs(app, canvas):
    for (row, col) in app.frogs:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        # body
        canvas.create_oval(x0+10, y0+8, x1-10, y1-8, fill="green", width=0)
        canvas.create_oval(x0+20, y1-25, x0+23, y1-15, fill="yellow", width=0)
        canvas.create_oval(x0+14, y1-35, x0+17, y1-26,fill="lightGreen",width=0)
        canvas.create_oval(x0+25, y1-14, x0+30, y1-12,fill="lightGreen",width=0)
        canvas.create_oval(x0+32, y1-18, x0+40, y1-14, fill="yellow", width=0)
        canvas.create_oval(x0+25, y1-23, x0+30, y1-17,fill="lightGreen",width=0)
        # front left leg 
        canvas.create_rectangle(x0+9, y0+15, x0+30, y0+17, 
                                fill="green", width=0)
        canvas.create_rectangle(x0+9, y0+5, x0+11, y0+15, 
                                fill="green", width=0)
        # front right leg 
        canvas.create_rectangle(x1-30, y0+15, x1-8, y0+17, 
                                fill="green", width=0)
        canvas.create_rectangle(x1-10, y0+5, x1-8, y0+15, 
                                fill="green", width=0)
        # bottom left leg 
        canvas.create_rectangle(x0+7, y1-17, x0+25, y1-21, 
                                fill="green", width=0)
        canvas.create_rectangle(x0+7, y1-5, x0+11, y1-17, 
                                fill="green", width=0)
        # bottom right leg 
        canvas.create_rectangle(x1-30, y1-17, x1-7, y1-21, 
                                fill="green", width=0)
        canvas.create_rectangle(x1-7, y1-5, x1-11, y1-17, 
                                fill="green", width=0)
        # eyes
        canvas.create_oval(x0+15, y0+3, x0+30, y0+18, fill="green", width=0)
        canvas.create_oval(x0+18, y0+5,x0+27, y0+14, fill="white", width=0)
        canvas.create_oval(x0+21, y0+8, x0+24, y0+11, fill="black")
        canvas.create_oval(x0+33, y0+3, x0+48, y0+18, fill="green", width=0)
        canvas.create_oval(x0+36, y0+5, x0+45, y0+14, fill="white", width=0)
        canvas.create_oval(x0+39, y0+8, x0+42, y0+11, fill="black")

def drawCarts(app, canvas):
    for (row, col) in app.carts:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0+5, y0+10, x0+30, y1-10,fill="red", width = 0)
        canvas.create_rectangle(x0+35, y0+5, x0+55, y1-5, fill="red", width = 0)
        canvas.create_rectangle(x0+25, y0+15, x0+45, y1-15, fill ="red",width=0)
        canvas.create_rectangle(x0+15, y0+15, x0+25, y1-15, 
                                fill ="lightBlue", width = 0)
        canvas.create_rectangle(x0+25, y0+10, x0+45, y0+15, 
                                fill = "lightBlue", width = 0)
        canvas.create_rectangle(x0+25, y1-15, x0+45, y1-10, 
                                fill = "lightBlue", width = 0)
        canvas.create_rectangle(x0+10, y0+5, x0+20, y0+10, 
                                fill = "yellow", width = 0) # above left wheel
        canvas.create_rectangle(x0+10, y1-10, x0+20, y1-5,
                                fill = "yellow", width = 0) # below left wheel
        canvas.create_rectangle(x0+44, y0+2, x0+51, y0+5,
                                fill = "yellow", width = 0) # above right wheel
        canvas.create_rectangle(x0+44, y1-5, x0+51, y1-2, 
                                fill = "yellow", width = 0) # below right wheel
        canvas.create_rectangle(x0+55, y0+8, x0+58, y0+15, 
                                fill = "lightBlue", width = 0)
        canvas.create_rectangle(x0+55, y1-15, x0+58, y1-8,
                                fill = 'lightBlue', width = 0)
        
def drawTrucks(app, canvas):
    for (row, col) in app.trucks:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_oval(x1-10, y0+15, x1, y0+20, fill="red", width=0)
        canvas.create_oval(x1-10, y0+35, x1, y0+40, fill="red", width=0)
        canvas.create_rectangle(x0+15, y0+10, x1-5, y1-10, 
                                fill="lightBlue", width = 0)
        canvas.create_rectangle(x0, y0+10, x0+14, y1-10, fill="lightBlue",
                                width=0)
        canvas.create_rectangle(x0+12, y0+20, x0+17, y0+35, fill="red", width=0)
        canvas.create_rectangle(x0+10, y0+6, x0+20, y0+10, fill = "orange", 
                                width=0) # above left wheel
        canvas.create_rectangle(x0+45, y0+6, x0+55, y0+10, fill = "orange",
                                width = 0) # above right wheel
        canvas.create_rectangle(x0+10, y1-10, x0+20, y1-6, fill = "orange",
                                width = 0) # below left wheel
        canvas.create_rectangle(x0+45, y1-10, x0+55, y1-6, fill = "orange", 
                                width = 0) # below right wheel
        
def drawBuggies(app, canvas):
    for (row, col) in app.buggy:
        (x0, y0, x1, y1) = getCellBounds(app, row, col)
        canvas.create_rectangle(x0+5, y0+10, x0+40, y1-10, fill="pink", width=0)
        canvas.create_polygon(x0+40, y0+10, x0+50, y0+24, x0+40, y1-10,
                            x0+25, y0+24, fill="pink",width = 0)
        canvas.create_rectangle(x0+8, y0+5, x0+20, y0+10, 
                                fill="green", width=0)
        canvas.create_rectangle(x0+25, y0+5, x0+33, y0+10, 
                                fill="lightGreen",width=0)
        canvas.create_rectangle(x0+8, y1-10, x0+20, y1-5,
                                fill="green", width = 0)
        canvas.create_rectangle(x0+25, y1-10, x0+33, y1-5, 
                                fill="lightGreen",width=0)
        canvas.create_rectangle(x0+8, y0+17, x0+30, y1-17, fill="red", width=0)
        canvas.create_polygon(x0+30, y0+17, x0+40, y0+26, x0+30, y1-17, 
                              fill="red", width=0)
        canvas.create_rectangle(x0, y0+15, x0+15, y0+20, fill="red", width=0)
        canvas.create_rectangle(x0, y1-20, x0+15, y1-15, fill="red", width=0)
        
def drawLand(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if row == 0 or row == 6 or row == 12:
                canvas.create_rectangle(x0, y0, x1, y1, fill='grey', width=0)
                canvas.create_rectangle(x0+2, y0+3, x0+30, y0+20, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0+32, y0+2, x1-7, y0+15, fill="pink", 
                                        width=0)
                canvas.create_rectangle(x1-6, y0+4, x1, y0+23, fill="pink", 
                                        width=0)
                canvas.create_rectangle(x0+1, y0+22, x0+25, y0+35, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0+31, y0+17, x1-7, y0+28, fill="pink", 
                                        width=0)
                canvas.create_rectangle(x0+27,y0+29, x1-1, y1-15, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0, y0+37, x0+25, y1-5, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0+28, y0+41, x0+40, y1-2, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0+42, y0+42, x1-2, y1-1, fill="pink",
                                        width=0)
                canvas.create_rectangle(x0, y1-4, x0+18, y1-1, fill="pink", 
                                        width=0)
                canvas.create_rectangle(x0+20, y1-4, x0+25, y1-1, fill="pink", 
                                        width=0)

# from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            (x0, y0, x1, y1) = getCellBounds(app, row, col)
            if 0<=row<=6:
                canvas.create_rectangle(x0, y0, x1, y1, fill='darkBlue', width=0)
            else:
                canvas.create_rectangle(x0, y0, x1, y1, fill='black', width=0)

# from https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html
def getCellBounds(app, row, col):
    gridWidth  = app.width 
    gridHeight = app.height - app.margin*2
    x0 = gridWidth * col / app.cols
    x1 = gridWidth * (col+1) / app.cols
    y0 = app.margin+gridHeight * row / app.rows
    y1 = app.margin+gridHeight * (row+1) / app.rows
    return (x0, y0, x1, y1)

runApp(width=800, height=800)