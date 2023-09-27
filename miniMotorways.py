from cmu_graphics import *
import math
import copy
import random

class Store:
    def __init__(self, app, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.color = rgb(red,green,blue)
        self.shade = rgb(red/1.2, green/1.2, blue/1.2)
        self.structure = 'store'
        self.stores = []
        self.row = 0
        self.col = 0
        self.dir = 0
        self.makeStore(app)
        self.groceries = 1
        self.parking = []
        
    def structure(self):
        return 'store'
        
    def makeStore(self, app):
        
        row, col = random.randrange(1, app.rows),random.randrange(1,app.cols)
        dir = random.randrange(0,2)
        x = 0
        while not self.placeStore(app, row-1, col-1, dir):
            x+=1
            row, col = random.randrange(1, app.rows),random.randrange(1,app.cols)
            dir = random.randrange(0,2) #0 is down, 1 is right
            if x > 50:
                break
            
            
    def placeStore(self, app, row, col, dir):
        self.dir = dir
        for i in range(5):
            
            if dir == 0:
                if app.city[row+i][col+1] != None or app.city[row+i][col] != None or row > 10:
                    return False
            elif app.city[row][col+i] != None or app.city[row+1][col+i] != None or col > 21:
                return False 
                
        self.stores.append([row,col])
            
        for i in range(3):
            
            if dir == 0:
                app.city[row+i][col] = self
                app.city[row+i][col+1] = self
                
                
            else:
                app.city[row][col+i] = self
                app.city[row+1][col+i] = self
        self.row = row
        self.col = col
        return True
        
    def drawStore(self,app):
        cellLeft, cellTop = app.board.getCellLeftTop(app, self.row, self.col)
        cellWidth, cellHeight = app.board.getCellSize(app)
        
        if self.dir == 0:
            drawRect(cellLeft, cellTop, cellWidth*2, cellHeight*3, border = 'black', borderWidth = 2, fill=rgb(71,76,89))
            
        else: 
            drawRect(cellLeft, cellTop, cellWidth*3, cellHeight*2, border = 'black', borderWidth = 2, fill=rgb(71,76,89))
        
        drawRect(cellLeft+10, cellTop+10, cellWidth*2-20, cellHeight*2-20, border = self.shade, borderWidth = 4, fill=self.color)
        imageWidth, imageHeight = getImageSize(app.grocery)
        for i in range(self.groceries):
            if i < 2:
                drawImage(app.grocery, cellLeft+17+20*i, cellTop+15, height = imageHeight / 8, width= imageWidth / 8)
            else:
                drawImage(app.grocery, cellLeft+17+20*(i-2), cellTop+34, height = imageHeight / 8, width= imageWidth / 8)

class House:
    def __init__(self, app,red, green, blue):
        self.hasPath = False
        self.red = red
        self.green = green
        self.blue = blue
        self.color = rgb(red,green,blue)
        self.shade = rgb(red/1.2, green/1.2, blue/1.2)
        self.structure = 'house'
        self.row = 0
        self.col = 0
        self.makeHouse(app)
        
    
    def makeHouse(self, app):
        row,col = random.randrange(0, app.rows),random.randrange(0,app.cols)
        while adjacent(app, row, col):
            row,col = random.randrange(0, app.rows),random.randrange(0,app.cols)

        app.city[row][col] = self
        self.row = row
        self.col = col
        
    def drawHouse(self,app):
        cellLeft, cellTop = app.board.getCellLeftTop(app, self.row, self.col)
        
        drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight/2, border = self.color, borderWidth = 2, fill=self.color)
        drawRect(cellLeft, cellTop+app.cellHeight/2, app.cellWidth, app.cellHeight/2, border = self.shade, borderWidth = 2, fill=self.shade)
        
        
    def checkPaths(self,app):
        app.completed = False
        if not self.hasPath:
            app.paths = [[self.row,self.col]]
            searchSurrounding(app, self.row, self.col)
                    
            if app.completed == True:
                app.completedPaths.append(Path(app, app.paths))
                self.hasPath = True
            app.paths = []
            
            
            
            
        
class Road:
    def __init__(self, app, number):
        self.color = rgb(71,76,89)
        self.number = number
        self.structure = 'road'
        
    def makeRoad(self, app, row, col):
        self.number -= 1
        app.city[row][col] = self
        app.city[row][col] = self
        
    def delRoad(self, app):
        if len(self.building) != 0:
            rowcol = self.building.pop()
            row = rowcol[0]
            col = rowcol[1]
            app.city[row][col] = None
            self.number += 1
        
        
class Board:
    def __init__(self, app, rows, cols, height, width, left, top):
        self.rows = rows
        self.cols = cols
        self.boardLeft = left
        self.boardTop = top
        self.boardWidth = width
        self.boardHeight = height
    
    def draw(self, app):
        for row in range(self.rows):
            for col in range(app.cols):
                self.drawCell(app, row, col)
        
    def drawCell(self, app, row, col):
        cellLeft, cellTop = app.board.getCellLeftTop(app, row, col)
        if isinstance(app.city[row][col], Path) or isinstance(app.city[row][col], Road):
            drawRect(cellLeft, cellTop, app.cellWidth, app.cellHeight, borderWidth = 2, border = app.city[row][col].color, fill = app.city[row][col].color)
            if app.traffic[row][col] == 1:
                imageWidth, imageHeight = getImageSize(app.light[app.lightNum])
                drawImage(app.light[app.lightNum], cellLeft,cellTop+3, height = imageHeight / 17, width = imageWidth /17)
                
    def getCellLeftTop(self, app, row, col):
        cellLeft = self.boardLeft + col * app.cellWidth
        cellTop = self.boardTop + row * app.cellHeight
        return (cellLeft, cellTop)
    
    def getCellSize(self, app):
        cellWidth = self.boardWidth / self.cols
        cellHeight = self.boardHeight / self.rows
        return (cellWidth, cellHeight)
        
    def getCell(self, app, x, y):
        dx = x - self.boardLeft
        dy = y - self.boardTop
        cellWidth, cellHeight = self.getCellSize(app)
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
          return (row, col)
        else:
          return None
          
class Path:
    
    def __init__(self, app, directions):
        self.directions = directions
        self.goingHome = False
        self.start = self.directions[0]
        self.end = self.directions[len(self.directions)-1]
        self.structure = 'path'
        self.color = rgb(72,80,95)
        self.broken = False
        self.index = 0
        self.row = self.start[0]
        self.col = self.start[1]
        self.carColor = app.city[self.row][self.col].color
        self.angle = 0
        self.UDLR = 0 #0 is up, 1 is down, 2 is left, 3 is right
        self.pickingUp = False
        self.traffic = False
        self.crash = False
        self.building = app.city[self.end[0]][self.end[1]]
        
        self.store = app.city[self.end[0]][self.end[1]]
        
        for i in self.directions:
            row = i[0]
            col = i[1]
            
            if app.city[row][col] != None and app.city[row][col].structure == 'road':
                app.city[row][col] = self
                
    def stillPath(self, app):
        for i in self.directions:
            row = i[0]
            col = i[1]
            if app.city[row][col] == None or app.city[row][col].structure != 'path':
                self.removePaths(app)
                self.broken = True
                
    def __eq__(self, other):
        return (isinstance(other, Path) and (self.start[0] == other.start[0]) and (self.start[1] == other.start[1]))
                
    def removePaths(self,app):
        for i in app.houses:
            if i.row == self.start[0] and i.col == self.start[1]:
                i.hasPath = False
        for i in self.directions:
            row = i[0]
            col = i[1]
            if app.city[row][col] != None and app.city[row][col].structure == 'path':
                app.city[row][col] = app.road
        for i in app.houses:
            i.checkPaths(app)
        if self in app.completedPaths:
            app.completedPaths.remove(self)

            
    def drive(self,app):
        if self.goingHome:
            self.index -=1
        else:
            self.index +=1
            
        if self.index == 0 or self.index == len(self.directions)-1:
            self.goingHome = not self.goingHome
            
        if self.goingHome:
            change = -1
        else:
            change = 1
                
        row = self.directions[self.index][0]
        col = self.directions[self.index][1]
            
        curr = self.UDLR
        if row > self.directions[self.index+change][0]:
            self.UDLR = 0
        elif row < self.directions[self.index+change][0]:
            self.UDLR = 1
        elif col < self.directions[self.index+change][1]:
            self.UDLR = 2
        else:
            self.UDLR = 3
        
        if self.UDLR == 2 or self.UDLR == 3:
            self.angle = 1
        elif self.UDLR == 0 or self.UDLR == 1:
            self.angle = 0
        
        if self.index == len(self.directions)-1:
            #building = app.city[row][col]
            if self.pickingUp == False:
                self.pickingUp = True
                self.building.parking.append(1)
                
            if self.building.dir == 0:
                row = self.building.row+2
                col = self.building.col+(len(self.building.parking)-1)*.5
                self.angle = 0
            else:
                xchange = random.randrange(0,101) / 100
                row = self.building.row+(len(self.building.parking)-1)*.5
                col = self.building.col+2
                self.angle = 1
        self.row = row
        self.col = col
        
    def drawCar(self,app):
        if not self.crash:
            if self.UDLR == 0:
                yChange = 7
                xChange = 0
            elif self.UDLR == 1:
                yChange = -7
                xChange = 0
            elif self.UDLR == 2:
                yChange = 0
                xChange = 7
            else:
                yChange = 0
                xChange = -7
            
            if self.index == 0 or self.index == len(self.directions)-1:
                xChange, yChange = 0,0
            cellLeft, cellTop = app.board.getCellLeftTop(app, self.row, self.col)
            drawRect(cellLeft+app.cellWidth/2+yChange, cellTop+app.cellHeight/2+xChange, app.cellWidth/4, app.cellHeight/2, fill = self.carColor, rotateAngle = 90*self.angle, align = 'center')
        
        else:
            cellLeft, cellTop = app.board.getCellLeftTop(app, self.row, self.col)
            drawCircle(cellLeft+app.cellWidth/2, cellTop+app.cellHeight/2, 10, fill = 'red', rotateAngle = 90*self.angle, align = 'center')
        
            
        

def onAppStart(app):
    app.rows =15
    app.cols = int(15*16/9)
    app.selection = 0
    app.reds =[67, 248, 155, 80, 255]
    app.greens = [208, 211, 152, 183, 118]
    app.blues = [226, 130, 195, 128, 170]
    app.roadIcon="cmu://448715/22739366/roadicon.png"
    app.icon = "cmu://448715/22739576/screen-0[12].png"
    app.inst = "cmu://448715/22752421/Mini+Motorways.png"
    app.grocery = "cmu://448715/22759477/a83da6eb79d9c8c16c9dfdfb848518f022234664[1]+(1).png"
    app.light = ['cmu://448715/22819872/yellow.png','cmu://448715/22819879/red.png', 'cmu://448715/22819888/green.png']
    app.lightNum = 1
    start(app)
    
def start(app):
    app.animation = 100
    app.clock = rgb(71,76,89)
    app.instructions = True
    app.points = 0
    app.paused = True
    app.over = False
    app.speed = 400
    app.step = 0
    app.board = Board(app, app.rows, app.cols, 500, 900, 0, 0)
    
    app.cellWidth, app.cellHeight = app.board.getCellSize(app)
    app.road = Road(app, 25)
    app.build = False
    app.stores = []
    app.houses = []
    app.paths = []
    app.completedPaths = []
    app.completed = False
    app.theta = 90

    starter = random.randrange(0,5)
    
    app.city = [[None for i in range(app.cols)] for i in range(app.rows)]
    app.traffic = copy.deepcopy(app.city)
    app.houses.append(House(app, app.reds[starter], app.greens[starter], app.blues[starter]))
    app.stores.append(Store(app,app.reds[starter], app.greens[starter], app.blues[starter]))
    
        
def searchSurrounding(app, row, col):
    indexArray = [-1, 0, 1]
    #used to iterate through all 8 neighboring cells
    for i in indexArray:
        for x in indexArray:
            #try function is used to prevent out of range errors
                #checks if any neighboring cells are roads (purposefully does not include wraparounds)
            if i == 0 or x == 0:
                if  col+x<26 and row+i <15 and app.city[row+i][col+x] != None and not app.completed:
                    if  (app.city[row+i][col+x].structure == 'road' or app.city[row+i][col+x].structure == 'path') and [row+i,col+x] not in app.paths:
                        app.paths.append([row+i,col+x])
                        searchSurrounding(app, row+i, col+x)
                    if app.city[row][col] != None and (app.city[row][col].structure == 'road' or app.city[row][col].structure == 'path') and app.city[row+i][col+x].structure == 'store' and app.city[row+i][col+x].color == app.city[app.paths[0][0]][app.paths[0][1]].color:
                        app.completed = True
                        app.paths.append([row+i,col+x])
                    
                    

def redrawAll(app):
    drawRect(0, 0, 900, 500, fill = gradient(rgb(232,230,219),rgb(117,115,110)), opacity = 20)
    if not app.instructions:
        for i in app.stores:
            i.drawStore(app)
        app.board.draw(app)
        for i in app.completedPaths:
            i.drawCar(app)
        
        for i in app.houses:
            i.drawHouse(app)
        
        color = 'white' if app.road.number > 0 else 'pink'
        drawImage(app.roadIcon, -10, 435, width = 75, height = 75, opacity = 75)
        drawCircle(45, 480, 13, fill = color, border = 'grey', opacity = 75)
        drawLabel(app.road.number, 45, 480, size = 17, opacity = 75, bold = True, fill = 'grey')
    
        drawImage(app.icon, 70, 450, width = 45, height = 45, opacity = 70)
        drawCircle(115, 480, 13, fill = 'white', border = 'grey', opacity = 75)
        drawLabel(app.points, 115, 480, size = 17, opacity = 75, bold = True, fill = 'grey')
        
        if not app.paused:
            drawRect(865, 20, 5, 20, fill = 'grey', opacity = 50)
            drawRect(875, 20, 5, 20, fill = 'grey', opacity = 50)
        else:
            drawPolygon(865, 20, 865, 40, 880, 30, fill = 'gray', opacity = 50 )
        
        if app.clock == rgb(71,76,89):
            line = 'white'
        else:
            line = rgb(71,76,89)
        drawCircle(825, 30, 25, fill = app.clock, opacity = 50)
    
        x,y = getRadiusEndpoint(825, 30, 20, app.theta)
        drawLine(825, 30, x, y, fill = line)
        
    if app.animation != 0:
        drawRect(0, 0, 900, 500, fill = gradient(rgb(232,230,219),rgb(172,176,172)), opacity = app.animation)
        drawImage(app.inst, -20, 0, width = 900, height = 500, opacity = app.animation)
        
        
def getRadiusEndpoint(cx, cy, r, theta):
    return (cx + r*math.cos(math.radians(theta)),
            cy - r*math.sin(math.radians(theta)))
            
def onMouseMove(app, mouseX, mouseY):
    app.selection = app.board.getCell(app,mouseX, mouseY)
    
    row = app.selection[0]
    col = app.selection[1]
    
    if app.city[row][col] == None and app.build and app.road.number >= 1:
        app.road.makeRoad(app, row, col)
        
def onMousePress(app,mouseX, mouseY):
    app.selection = app.board.getCell(app,mouseX, mouseY)
    row = app.selection[0]
    col = app.selection[1]
        
def onKeyHold(app, keys):
    if 'space' in keys and not app.instructions:
        row = app.selection[0]
        col = app.selection[1]
        app.build = True if app.road.number >= 1 else False
        
            
def onKeyRelease(app,key):
    if 'space' == key and not app.instructions:
        app.build = False
        row = app.selection[0]
        col = app.selection[1]
        
        for i in app.houses:
            i.checkPaths(app)
    
def onKeyPress(app,key):
    if key == 'h':
        starter = random.randrange(5)
        app.houses.append(House(app, app.reds[starter], app.greens[starter], app.blues[starter]))
    
    if key == 'p':
        if not app.over:
            app.paused = not app.paused
        
    if key == 's':
        starter = random.randrange(5)
        app.stores.append(Store(app,app.reds[starter], app.greens[starter], app.blues[starter]))
        
    if key == 'x':
        row = app.selection[0]
        col = app.selection[1]
        if app.traffic[row][col] == 1:
            app.traffic[row][col] = None
        if app.city[row][col] != None and app.city[row][col].structure == 'road':
            app.city[row][col] = None
            app.road.number += 1
        elif app.city[row][col] != None and app.city[row][col].structure == 'path':
            app.road.number += 1
            app.city[row][col] = None
            x = len(app.completedPaths)
            while x!=0:
                x-=1
                app.completedPaths[x].stillPath(app)
        
    if key == 't':
        row = app.selection[0]
        col = app.selection[1]
        if app.city[row][col] != None and app.city[row][col].structure == 'road' or app.city[row][col].structure == 'path':
            app.traffic[row][col] = 1
        
    if key == 'space':
        if app.instructions:
            app.instructions = False
            app.paused = False
        

def adjacent(app, row, col):
    index = [-1, 0, 1]
    for i in index:
            
            for x in index:
                
                if row+i < len(app.city)-1 and col+x < len(app.city[0])-1 and app.city[row+i][col+x] != None and row+i>-1 and col+x>-1:
                        return True
    return False
    
def onStep(app):
    if app.step % 240 == 0:
            if app.clock == rgb(71,76,89):
                app.clock = 'white'
            else:
                app.clock = rgb(71,76,89)
                
    if not app.over:
        app.step += 1
    else:
        app.step = -1
    if not app.instructions and app.animation != 0:
        app.animation -= 4
        
    if not app.paused:
        app.theta -= 1.5
        if app.step % 15 == 0:
            if app.lightNum == 1:
                app.lightNum = 2
            elif app.lightNum == 2:
                app.lightNum = 0
            elif app.lightNum == 0:
                app.lightNum += 1
            
            
        if app.step % 56 == 0 and app.step%10 != 0:
            for i in app.completedPaths:
                if not i.broken and i.pickingUp:
                    i.building.parking.pop()
                    i.pickingUp = False
                    if i.store.groceries != 0:
                        i.store.groceries -=1
                        app.points += 1
            
        if app.step % 10 == 0:
            locations = {0:[], 1:[], 2:[], 3:[]}
            for i in app.completedPaths:
                if not i.broken and not i.pickingUp:
                    if i.store.groceries == 0 and i.start != [i.row,i.col]:
                        i.goingHome = True
                    if not (i.start == [i.row,i.col] and i.store.groceries == 0) and not i.traffic:
                        if app.traffic[int(i.row)][int(i.col)] == 1:
                            if app.lightNum == 2:
                                i.drive(app)
                        else:
                            i.drive(app)
                    
                if not i.broken:
                    if [i.row, i.col] in locations[i.UDLR] and app.city[i.row][i.col].structure != 'store':
                        if app.traffic[i.row][i.col] == 1 and not i.traffic:
                            print('traffic light!')
                            i.traffic = True
                        elif app.traffic[i.row][i.col] == 1 and i.traffic:
                            i.traffic = False
                            i.drive(app)
                        else:
                            #i.crash = True
                            #app.over = True
                            pass
                    locations[i.UDLR].append([i.row, i.col])
                        
            
                    
        if app.step % app.speed == 0:
            for i in app.stores:
                if i.groceries == 4:
                    print('game over')
                    app.over = True
                    app.paused = True
                else:
                    i.groceries += 1
                
                
        if app.step % 300 == 0 and app.step % 480 != 0 and app.step != 300:
            store = random.choice(app.stores)
            red,green,blue = store.red, store.green, store.blue
            app.houses.append(House(app,red, green, blue))
        
        
        if app.step% 480 == 0:
            color = random.randrange(5)
            red,green,blue = app.reds[color], app.greens[color], app.blues[color]
            app.stores.append(Store(app, red, green, blue))
            app.road.number += 10
        
        if app.step % 500 == 0:
            app.speed -= 3
            app.houses.append(House(app, app.stores[len(app.stores)-1].red, app.stores[len(app.stores)-1].green, app.stores[len(app.stores)-1].blue))
        
def main():
    runApp(width = 900, height = 500)

main()

