from tkinter import *
import math, random

class Enemy(object):
    def __init__(self, cx, cy, radius, health=150, speed=8, damage=12, worth=7):
        self.cx = cx
        self.cy = cy
        self.radius = radius
        self.speed = speed
        self.origSpeed = speed
        self.health = health
        self.initHP = health
        self.damage = damage
        self.worth = worth
        self.direction = (0, 1)
        self.antLegs = False
        self.color = "brown"
        self.spawnSpeen=100
        self.glued = False
       

    def isCollision(self, data):
        for bullet in data.bullets:
            if ( (self.cx - bullet.cx)**2 + (self.cy - bullet.cy)**2)**.5 < \
                self.radius + bullet.r:
                return bullet
        return None

    def reactToBulletHit(self, data, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            data.game.earnMoney(self)
            data.enemies.remove(self)
        if bullet.color != "gray10":
            data.bullets.remove(bullet)
        if bullet.color == "lavender":
            self.glued = True
            self.speed = 3
        if self.glued:
            if self.speed < self.origSpeed:
                self.speed+=.25
            else:
                self.glued = False

    def followPath(self, data):
        currentCol = int((self.cx + data.cellWidth/4)/data.cellWidth)
        currentRow = int((self.cy+data.cellHeight/4)/data.cellHeight)
        if data.field.board[currentRow][currentCol] == 1: return False
        if (currentRow, currentCol) == data.path[len(data.path) - 1]:
            data.enemies.remove(self)
            data.game.health -= self.damage
            return
        nextCordIndex = data.path.index((currentRow, currentCol))+1
        nextRow, nextCol = data.path[nextCordIndex]
        self.direction = (nextRow - currentRow, nextCol-currentCol)
        if nextCol == 0:
            nextX = nextCol * data.cellWidth  + data.cellWidth/2
        else:
            nextX = nextCol * data.cellWidth  + data.cellWidth/2
        if nextRow == 0:
            nextY = nextRow * data.cellHeight + data.cellHeight/2
        else:
            nextY = nextRow * data.cellHeight + data.cellHeight/2
        
        self.antLegs = not self.antLegs
        if abs(self.cx - nextX) > data.cellWidth//8:
            if self.cx < nextX:
                self.cx += self.speed
            else:
                self.cx -=self.speed
        if abs(self.cy - nextY) > data.cellHeight//8:
            if self.cy < nextY:
                self.cy += self.speed
            else:
                self.cy -= self.speed
            

    def setHP(self, data):
        if data.game.difficulty == "easy":
            self.health*=3*data.game.currWave
            self.initHP*=3*data.game.currWave
            self.spawnSpeen-=3
        else:
            self.health*=5*data.game.currWave
            self.initHP*=5*data.game.currWave
            self.spawnSpeen-=6
        if data.game.currWave >=data.game.waves//2:
            self.health*=2
            self.initHP*=2
        elif data.game.currWave == data.game.waves:
            self.health*=2
            self.initHP*=2
        self.spawnSpeen-=8

    def draw(self, canvas):
        r = self.radius/3 * 2
        x0 = self.cx-r
        y0 = self.cy-r
        x1 = self.cx+r
        y1 = self.cy+r
        self.drawAnt(canvas, x0, y0, x1, y1, r)
        self.drawHealthBar(canvas, x0, y0, x1, y1, r)

    def drawAnt(self, canvas, x0, y0, x1, y1, r):
        rad = self.radius
        drow, dcol = self.direction
        if drow != 0:
            self.drawAntVert(canvas, x0, y0, x1, y1, r, rad, drow)
        else:
            self.drawAntHoriz(canvas, x0, y0, x1, y1, r, rad, dcol)

    def drawAntVert(self, canvas, x0, y0, x1, y1, r, rad, drow):
        cx = self.cx 
        cy = self.cy
        y0L = y0
        adjust = -r
        if drow == -1:
            adjust = 0
        if self.antLegs: 
            adjust += r
            if adjust > r + 1: adjust = -r
        canvas.create_line(cx, y0L + 2*r, cx + rad*4/3, y0L+2*r+adjust, fill = self.color, width = 3 )
        canvas.create_line(cx, y0L +2*r, cx-rad*4/3, y0L+2*r+adjust, fill = self.color, width = 3 )
        canvas.create_line(cx, y0L, cx + rad*4/3, y0L+adjust, fill = self.color, width = 3 )
        canvas.create_line(cx, y0L, cx-rad*4/3, y0L+adjust, fill = self.color, width = 3 )
        canvas.create_oval(x0+(1/3 *r), y0+(1/3 *r), x1-(1/3 *r) + 1, y1-(1/3 *r),\
            fill = self.color)
        canvas.create_oval(x0,y0-(4/3 *r), x1, y1-(4/3 *r), fill = self.color)
        canvas.create_oval(x0, y0+(4/3 *r), x1, y1+(4/3 *r), fill = self.color)

    def drawAntHoriz(self, canvas, x0, y0, x1, y1, r, rad, dcol):
        x0L = x0
        adjust = -r
        if dcol == -1:
            x0L += rad
            adjust = 0
        if self.antLegs: 
            adjust += r
            if adjust > r + 1: adjust = -r
        canvas.create_line(x0L +r, y0+r, x0L +r+adjust, y0+rad*2, fill = self.color, width = 3 )
        canvas.create_line(x0L +r, y0+r, x0L +r+adjust, y0-r, fill = self.color, width = 3 )
        canvas.create_line(x0L-(1/2 *r), y0+rad, x0L-(1/2 *r)+adjust, y0-r, fill = self.color, width = 3 )
        canvas.create_line(x0L-(1/2 *r), y0+rad, x0L-(1/2 *r)+adjust, y0+rad*2, fill = self.color, width = 3 )

        canvas.create_oval(x0+(1/3 *r), y0+(1/3 *r), x1-(1/3 *r), y1-(1/3 *r), fill = self.color)
        canvas.create_oval(x0-(4/3 *r), y0, x1-(4/3 *r), y1, fill = self.color)
        canvas.create_oval(x0+(4/3 *r), y0, x1+(4/3 *r), y1, fill = self.color)
        
        
        

    def drawHealthBar(self, canvas, x0, y0, x1, y1, r):
        canvas.create_rectangle(x0, y0-r/2 - 3, x1, y0 - 3)
        lenBar = (x1 - x0) * (self.health/self.initHP)
        color = "green2"
        if self.health/self.initHP < 1/3 :
            color = "red"
        canvas.create_rectangle(x0, y0-r/2 - 3, x0 + lenBar, y0 - 3, \
            fill =color, width = 0)



class RedAnt(Enemy):
    def __init__(self, cx, cy, radius, health=60, speed=10, damage=10, worth=9):
        super().__init__(cx, cy, radius, health, speed, damage, worth)
        self.color = "red"



class BossAnt(Enemy):
    def __init__(self, cx, cy, radius, health=400, speed=5, damage=18, worth=12):
        super().__init__(cx, cy, radius, health, speed, damage, worth)
        self.color = "gray10"



    def reactToBulletHit(self, data, bullet):
        self.health -= bullet.damage
        if self.health <= 0:
            data.game.earnMoney(self)
            data.enemies.remove(self)
            enemy1 = Enemy(self.cx-5, self.cy-5, 10, self.initHP/10)
            enemy2 = Enemy(self.cx+5, self.cy+5, 10, self.initHP/10)
            data.enemies.insert(0, enemy1)
            data.enemies.insert(0, enemy2)
        if bullet.color != "gray10":
            data.bullets.remove(bullet)
        if bullet.color == "lavender":
            self.glued = True
            self.speed = 2
        if self.glued:
            if self.speed < self.origSpeed:
                self.speed+=.5
            else:
                self.glued = False



class Turret(object):
    def __init__(self, row, col, size, shotRange=200, damage=30, cost=12, fireRate=15,\
            barrel=30):
        self.row = row
        self.col = col
        self.size = size
        self.shotRange = shotRange
        self.damage = damage
        self.fireRate = fireRate
        self.cost = cost
        self.angle = math.pi/2
        self.barrel = barrel
        self.level = 1
        self.upgradeCost = 10

    def fireBullet(self, cx, cy, angle, damage, speed=17):
        return Bullet(cx, cy, angle, damage, speed, "sienna4", 4, True)


    def onTimerFired(self, data, enemy):
        if self.aim(enemy, data):
            cx = self.col * data.cellWidth + int(data.cellWidth)//2
            cy = self.row * data.cellHeight + int(data.cellHeight)//2
            if data.timer%self.fireRate == 0:
                data.bullets.append(self.fireBullet(cx, cy, self.angle, self.damage))
            return True
        else: return False

    def aim(self, enemy, data):
        cx = self.col * data.cellWidth + int(data.cellWidth)//2
        cy = self.row * data.cellHeight + int(data.cellHeight)//2
        cxE, cyE = enemy.cx, enemy.cy
        dist = ((cx-cxE)**2 +(cy-cyE)**2)**.5
        if dist < self.shotRange + enemy.radius:
            diffX = cx-cxE
            if cy > cyE:
                self.angle = math.pi - math.acos(diffX/dist)
            elif cyE > cy:
                self.angle = math.pi + math.acos(diffX/dist)
            return True
        return False

    def upgrade(self, data):
        #1 is fireRate, 2 is bulletsize, 3 is damage
        self.damage += 10
        self.fireRate -=2 
        self.size += 2
        self.barrel += 2
        self.shotRange += 15
        self.level +=1
        self.upgradeCost*=2

    def draw(self, canvas, data):
        cx = self.col * data.cellWidth + data.cellWidth/2
        cy = self.row * data.cellHeight + data.cellHeight/2
        size = self.size
        canvas.create_line(cx, cy, cx - size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy + size, width = 8)
        canvas.create_line(cx, cy, cx - size, cy + size, width = 8)
        canvas.create_oval(cx - size, cy - size, cx + size, cy + size, \
            fill = "dark green")
        canvas.create_line(cx, cy, cx + self.barrel*math.cos(self.angle), \
            cy - self.barrel*math.sin(self.angle), width = "9", fill = "grey34")
        canvas.create_line(cx + self.barrel*math.cos(self.angle), cy - self.barrel*math.sin(self.angle), \
            cx + 3*self.barrel/4 *math.cos(self.angle), cy - 3*self.barrel/4*math.sin(self.angle), \
            width = "13", fill = "grey24")
        radius = size/2
        canvas.create_oval(cx-radius, cy - radius, cx+radius, cy+radius, fill="chartreuse4")

class MachineTurret(Turret):
    def __init__(self, row, col, size, shotRange=100, damage=20, cost=20, fireRate=5,\
            barrel=12):
        super().__init__(row, col, size, shotRange, damage, cost, \
            fireRate, barrel)
        self.trigger = False
        self.upgradeCost = 12

    def fireBullet(self, cx, cy, angle, damage, speed=17):
        self.trigger = not self.trigger
        return Bullet(cx, cy, angle, damage, speed, "dark slate grey", 3, True)


    def upgrade(self, data):
        
        self.damage += 7
        self.fireRate -=1 
        self.size += 2
        self.barrel += 2
        self.shotRange += 20
        self.level +=1
        self.upgradeCost*=2
        

    def draw(self, canvas, data):
        cx = self.col * data.cellWidth + data.cellWidth/2
        cy = self.row * data.cellHeight + data.cellHeight/2
        size = self.size
        canvas.create_line(cx, cy, cx - size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy + size, width = 8)
        canvas.create_line(cx, cy, cx - size, cy + size, width = 8)
        canvas.create_oval(cx - size, cy - size, cx + size, cy + size, \
            fill = "grey75")
        if self.trigger:
            if math.pi/4 < self.angle < 3*math.pi/4 or 5*math.pi/4 < self.angle < 7*math.pi/4:
                y, x = cy + 3, cx 
            else :
                y, x = cy, cx+3
            canvas.create_line(x, y, (x) + 3/4 *self.barrel*math.cos(self.angle - math.pi/2), \
            (y) - 4/5 *self.barrel*math.sin(self.angle - math.pi/2), width = 4 )
        else:
            canvas.create_line(cx, cy, cx + 3/4 *self.barrel*math.cos(self.angle - math.pi/2), \
            cy - 4/5 *self.barrel*math.sin(self.angle - math.pi/2), width = 4 )
        canvas.create_line(cx - self.barrel*math.cos(self.angle), \
            cy + self.barrel*math.sin(self.angle), \
            cx + self.barrel*math.cos(self.angle), \
            cy - self.barrel*math.sin(self.angle), width = 11, fill = "grey20")
        canvas.create_line(cx + (self.barrel-1)*math.cos(self.angle), cy - (self.barrel-1)*math.sin(self.angle), \
            cx + 7*self.barrel/4 *math.cos(self.angle), cy -7*self.barrel/4*math.sin(self.angle), \
            width = "6", fill = "black")
        
class Canon(Turret):
    def __init__(self, row, col, size, shotRange=200, damage=100, cost=50, fireRate=55,\
            barrel=25):
        super().__init__(row, col, size, shotRange, damage, cost, \
            fireRate, barrel)
        self.upgradeCost = 30

    def fireBullet(self, cx, cy, angle, damage, speed=10):
        return Bullet(cx, cy, angle, damage, speed, "gray10", 8, False)

    def draw(self, canvas, data):
        cx = self.col * data.cellWidth + data.cellWidth/2
        cy = self.row * data.cellHeight + data.cellHeight/2
        size = self.size
        canvas.create_rectangle(cx - size, cy-size, cx + size, cy+size, \
            fill="slate gray")
        size = self.size*1.2
        canvas.create_oval(cx - 2*size/3+1, cy-2*size/3+1, cx+2*size/3-1, cy+2*size/3-1, \
            fill = "black", outline = "white")
        canvas.create_line(cx, cy,cx + self.barrel*math.cos(self.angle), \
            cy - self.barrel*math.sin(self.angle), width = str(size*5/9) )
        cirCx = cx + (7/8)*self.barrel*math.cos(self.angle)
        cirCy = cy - (7/8)*self.barrel*math.sin(self.angle)
        canvas.create_oval(cirCx-5*size/14, cirCy-5*size/14, cirCx+5*size/14, \
            cirCy+5*size/14, fill = "black")
    
    def upgrade(self, data):
        self.damage += 50
        self.fireRate -=3 
        self.size += 2
        self.barrel += 3
        self.shotRange += 20
        self.level +=1
        self.upgradeCost*=2

class GlueGun(Turret):
    def __init__(self, row, col, size, shotRange=150, damage=10, cost=25, fireRate=50,\
            barrel=14):
        super().__init__(row, col, size, shotRange, damage, cost, \
            fireRate, barrel)
        self.upgradeCost = 20

    def fireBullet(self, cx, cy, angle, damage, speed=14):
        return Bullet(cx, cy, angle, damage, speed, "lavender", 7, False)

    def draw(self, canvas, data):
        cx = self.col * data.cellWidth + data.cellWidth/2
        cy = self.row * data.cellHeight + data.cellHeight/2
        size = self.size
        canvas.create_line(cx, cy, cx - size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy - size, width = 8)
        canvas.create_line(cx, cy, cx + size, cy + size, width = 8)
        canvas.create_line(cx, cy, cx - size, cy + size, width = 8)
        width = size+3
        x0 = cx - self.barrel*math.cos(self.angle)
        y0 = cy + self.barrel*math.sin(self.angle)
        x1 = cx + self.barrel*math.cos(self.angle)
        y1 = cy - self.barrel*math.sin(self.angle)
        canvas.create_line(cx + (self.barrel)*math.cos(self.angle), cy - (self.barrel)*math.sin(self.angle), \
            cx + 8*self.barrel/4 *math.cos(self.angle), cy -8*self.barrel/4*math.sin(self.angle), \
            width = "6", fill = "orange red")
        canvas.create_line(x0, y0, x1, y1, width = width, fill = "ghost white")
        canvas.create_oval(x1 - width/2, y1-width/2, x1+width/2, y1+width/2, \
            fill = "ghost white", width = 0)

        canvas.create_line(cx - self.barrel/2*math.cos(self.angle), \
            cy + self.barrel/2*math.sin(self.angle), \
            cx + self.barrel*math.cos(self.angle), \
            cy - self.barrel*math.sin(self.angle), width = width, fill = "deep sky blue")
        
        

    def upgrade(self, data):
        self.damage += 5
        self.fireRate -=5 
        self.size += 2
        self.barrel += 2
        self.shotRange += 20
        self.level +=1
        self.upgradeCost*=2

class Bullet(object):
    #From hw15:
    def __init__(self, cx, cy, angle, damage, speed, color, radius=5, \
            fullBull = False):
        self.cx = cx
        self.cy = cy
        self.r = radius
        self.angle = angle
        self.damage = damage
        self.speed = speed
        self.color = color
        self.fullBull = fullBull

    def moveBullet(self):
        speed = random.randint(self.speed-10, self.speed+10)
        dx = math.cos(self.angle)*speed
        dy = math.sin(self.angle)*speed
        self.cx, self.cy = self.cx + dx, self.cy - dy

    def draw(self, canvas):
        cx, cy, r = self.cx, self.cy, self.r
        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, 
            fill=self.color, width=0)
        dx = math.cos(self.angle)*r
        dy = math.sin(self.angle)*r
        if self.fullBull:
            canvas.create_line(cx, cy, cx -dx, cy+dy , \
                fill = self.color, width = 2*self.r)

class Field(object):
    def __init__(self, board, rows, cols, health=100):
        self.rows = rows
        self.cols = cols
        self.health = health
        self.board = board

    def getDirs(self, row):
        if row > len(self.board)//2:
            return [(0,1), (-1, 0), (1, 0), (0, -1)]
        else:
            return [(0,1), (1, 0), (-1, 0), (0, -1)]
        

    def findPath(self, srow, scol, erow, ecol, path=[]):
        if srow == erow and scol == ecol:
            return path
        if self.board[erow][ecol] == 1:
            return None
        for direction in self.getDirs(srow):
            drow, dcol = direction
            if (srow+drow, scol+dcol) not in path and \
                self.isValid( srow, scol, direction):
                path.append((srow+drow,scol+dcol))
                tmpSolution = self.findPath( srow+drow, scol+dcol, erow, ecol, path)
                if tmpSolution != None:
                    return tmpSolution
                path.remove((srow+drow,scol+dcol))
        return None

    
    def isValid(self, row, col, direction):
        if self.board[row][col] == 1:
            return False
        row += direction[0]
        col += direction[1]
        if row >= len(self.board) or row < 0 or col >= len(self.board[0]) or \
            col < 0:
            return False
        elif self.board[row][col] != 1:
            return True
        else:
            return False


    def draw(self, canvas, data):
        canvas.create_image(data.fieldWidth/2, data.height/2, image = data.image0)
        canvas.create_image(data.cellWidth/4 *3, data.height/2 + 20, image = data.image2)
        canvas.create_image(data.fieldWidth - data.cellWidth, data.height/2, \
            image=data.image1)
        #draw path


class Game(object):
    def __init__(self):
        self.waves = 10
        self.waveLen = 8
        self.currWave = 1
        self.money = 100
        self.difficulty = "easy"
        self.health = 100
        self.initHealth = 100

        self.isPaused = False
        self.isPlaying = False
        self.showStartScreen = True
        self.showEntryScreen = False
        self.isInGame = False
        self.isGameOver = False
        self.isWaveOver = False
        self.didWin = False
        self.cantPlaceTurret = False
        self.showTurretMenu = False
        self.showUpgradeMenu = False
        self.upgradeCords = None
        self.upGradeCost = None
        self.maxLevel = False

        self.highlightCell = None
        self.turretOptions = {"Turret": [12, "Damage = 30","Range = 200", "Fire Rate = 20" ] \
                            , "Machine Turret": [20, "Damage = 20","Range = 100", "Fire Rate = 40" ], \
                            "Canon": [50, "Damage = 100","Range = 200", "Fire Rate = 5" ], \
                            "Glue Gun": [25, "Damage = 10","Range = 150", "Fire Rate = 4" ]}
        self.clickTurret = {}
        self.placingCords = None
        
        self.menuStats = {"Money": "$%d"%self.money, "Wave": self.currWave}
        self.menuOptions = ["Press Space to Start!", \
                            "Press R to restart"]

    def resetValues(self, data):
        self.highlightCell = None
        self.placingCords = None
        self.showUpgradeMenu = False
        self.upgradeCords = None
        self.upGradeCost = None
        self.maxLevel = False

    def setDifficulty(self, difficulty):
        self.difficulty = difficulty
        if difficulty == "easy":
            self.health = 100
            self.initHealth = 100
            self.money = 75
        if difficulty == "hard":
            self.health = 75
            self.initHealth = 75
            self.money = 40


    def startGame(self, data, x, y):
        cxS = data.width/2
        cyS = 3*data.height/5
        if abs(cxS - x) < 110 and abs(cyS - y) < 70:
            self.showStartScreen = False
            self.showEntryScreen = True

    def takeToGame(self, data, x, y):
        xE = data.width/4 - 50
        xH = 3*data.width/4 - 50
        yB = 3*data.height/4
        if xE <= x <= xE +100 and yB < y < yB +75:
            self.setDifficulty("easy")
            self.showEntryScreen = False
            self.isInGame = True
        elif xH <= x <= xH +100 and yB < y < yB +75:
            self.setDifficulty("easy")
            self.showEntryScreen = False
            self.isInGame = True

    def drawStartScreen(self, data, canvas):
        canvas.create_image(data.width/2, data.height/2, image = data.image3)
        canvas.create_rectangle(0, 0, 30, data.height, fill="lime green", \
            outline = "dodger blue", width=4)
        canvas.create_rectangle(data.width-30, 0, data.width, data.height, fill="lime green", \
            outline = "dodger blue", width=4)
        canvas.create_rectangle(0, 0, data.width, 30, fill="lime green", \
            outline = "dodger blue", width=4)
        canvas.create_rectangle(0, data.height-30, data.width, data.height, fill="lime green", \
            outline = "dodger blue", width=4)
        
        
        canvas.create_text(data.width/3, data.height/4, text = "PICNIC RAID", \
            font = "arial 70 bold")
        cxS = data.width/2
        cyS = 3*data.height/5
        canvas.create_rectangle(cxS - 110, cyS - 70, cxS + 110, cyS+70, fill = "lime green", width = 3)
        canvas.create_text(cxS, cyS, text = "START", font = "arial 55")
        
    def nextWave(self, data):
        #increments enemies health and length of wave
        
        self.currWave += 1
        self.waveLen += 3

    def drawNewWave(self, canvas, data):
        if self.currWave == self.waves:
            self.isWaveOver = False
            self.isGameOver = True
            self.didWin = True
            self.endGame()
            return
        canvas.create_rectangle(data.fieldWidth/4, data.height/3, \
            3*data.fieldWidth/4, 2*data.height/3, fill = "RoyalBlue1", width=3)
        canvas.create_text(data.fieldWidth/2, data.height/2-20, \
            text = "WAVE COMPLETED", font = "arial 35 bold")
        canvas.create_rectangle(data.fieldWidth/3, data.height/2 +20, 2*data.fieldWidth/3, \
            data.height/2+60 , fill="white", width = 4)
        canvas.create_text(data.fieldWidth/2, data.height/2 + 40, \
            text = "Click anywhere to move on", font = "arial 20")


    def startWave(self, data):
        data.game.isWaveOver = False
        data.waveTimer = 0
        data.timer = 0
        data.bullets = []
        for turret in data.turrets:
            turret.angle = math.pi/2

    def gameOver(self):
        if self.health<=0:
            self.health = 0
            self.endGame()

    def endGame(self):
        # self.isInGame = False
        self.isPlaying = False
        self.isWaveOver = False
        self.isGameOver = True

    def drawGameOver(self, canvas, data):
        if self.didWin:
            canvas.create_rectangle(data.fieldWidth/4, data.height/3, \
                3*data.fieldWidth/4, 2*data.height/3, fill = "green2", width=5)
            canvas.create_text(data.fieldWidth/2, data.height/2, \
                text = "YOU WON!", font = "arial 50")
        else:
            canvas.create_rectangle(data.fieldWidth/4, data.height/3, \
                3*data.fieldWidth/4, 2*data.height/3, fill = "red", width=5)
            canvas.create_text(data.fieldWidth/2, data.height/2, \
                text = "YOU LOST!", font = "arial 50")

    def earnMoney(self, enemy):
        self.money += enemy.worth

    def buyThis(self, cost):
        if self.money >= cost:
            self.money -= cost
            return True
        return False

    def drawCell(self, data, canvas, row, col):
        pX = col * data.cellWidth
        pY = row * data.cellHeight
        canvas.create_rectangle(pX, pY, pX + data.cellWidth, pY + data.cellHeight,  \
            width =5)


    def drawTurretMenu(self, canvas, data):
        x, y = self.highlightCell
        col = int((x)/data.cellWidth)
        row = int((y)/data.cellHeight)
        self.placingCords = (row, col)
        self.drawCell(data, canvas, row, col)
        canvas.create_rectangle(data.fieldWidth, 0, data.width, data.height, \
            fill = "light grey")
        xT = data.fieldWidth + (data.width - data.fieldWidth)/2
        canvas.create_text(xT, 20, text = "Select Turret:", font = "arial 35")
        canvas.create_text(xT, data.height - 30, text = "Click \"B\" to exit", \
            font = "arial 20")
        self.drawTurretOptions(canvas, data, xT)

    def drawTurretOptions(self, canvas, data, midX, margin=20, start=100, \
        boxHeight=70):
        canvas.create_rectangle(data.fieldWidth + margin, 50, \
            data.width - margin, 50+ 40,fill = "green", width = 5)
        canvas.create_text(midX, 70, text = "Money: $%d"%self.money \
            , font = "arial 20 bold")
        
        numBox = 0
        for option in self.turretOptions: 
            y0 = start + (boxHeight + 10)*numBox
            canvas.create_rectangle(data.fieldWidth + margin, y0, \
                data.width - margin, y0+boxHeight, fill = "white")
            canvas.create_text(midX, y0+1/4*boxHeight, text = option + \
                " : $%d"%self.turretOptions[option][0], font = "arial 18")
            canvas.create_text(midX-10, y0+1/2*boxHeight, text = self.turretOptions[option][1])
            canvas.create_text(midX-10,4+ y0+5/8*boxHeight, text = self.turretOptions[option][2])
            canvas.create_text(midX-10, y0+7/8*boxHeight, text = self.turretOptions[option][3])

            self.clickTurret[option] = (data.fieldWidth + margin, y0)
            numBox+=1
        

    def confirmedBuyTurret(self, data, x, y):
        for turret in self.clickTurret:
            fx, fy = self.clickTurret[turret]
            if 0 <= x - fx <= data.width-data.fieldWidth - 20 and\
                0 <= y - fy <= 70:
                return turret
        return None


    def upgradeTurret(self, data, x, y):
        x0 = data.fieldWidth+30
        y0 = 150
        x1 = data.width-30
        y1 = 250
        if x0 <= x <= x1 and y0 <= y <= y1:
            row, col = self.upgradeCords
            for turret in data.turrets:
                if turret.row == row and turret.col == col:
                    if self.buyThis(turret.upgradeCost) and turret.level <3:
                        turret.upgrade(data)
                        break
            self.showUpgradeMenu = False
            self.upgradeCords = None
            self.maxLevel = False
        


    def openUpgradeMenu(self, data, x, y):
        col = int((x)/data.cellWidth)
        row = int((y)/data.cellHeight)
        if data.field.board[row][col] == 1:
            for turret in data.turrets:
                if turret.row == row and turret.col == col:
                    if turret.level>=3: 
                        self.maxLevel = True
                    self.upGradeCost = turret.upgradeCost
                    break
            self.showUpgradeMenu = True
            self.upgradeCords = (row, col)
            

    def openTurretMenu(self, data, x, y):
        col = int((x)/data.cellWidth)
        row = int((y)/data.cellHeight)
        if self.validPlaceTurret(row, col, data):
            self.showTurretMenu = True
            if x < data.fieldWidth:
                self.highlightCell = (x, y)
        else:
            self.cantPlaceTurret = True

    def validPlaceTurret(self, row, col, data):
        if data.field.board[row][col] != 0 or data.game.isPlaying or data.game.isWaveOver or data.game.isGameOver:
            return False
        data.field.board[row][col] = 1
        if col > data.field.cols//2:
            path = data.field.findPath( data.field.rows//2, data.field.cols-1, data.field.rows//2,\
               0 , [(data.field.rows//2,data.field.cols-1 )] )
            if path!=None: path.reverse()
        else:
            path = data.field.findPath( data.field.rows//2, 0, data.field.rows//2,\
                   data.field.cols-1, [(data.field.rows//2,0 )] )
        data.field.board[row][col] = 0
        if path == None:
            return False
        return True



    def drawHealth(self, canvas, data):
        x0 = data.fieldWidth +25
        y0 = 100
        x1 = data.width - 25
        y1 = 130
        canvas.create_text(data.fieldWidth +40, 80, text="Health:", \
            font = "arial 20")
        canvas.create_rectangle(x0, y0, x1, y1)
        lenBar = (x1 - x0) * (self.health/self.initHealth)
        color = "green2"
        if self.health/self.initHealth < 1/3 :
            color = "red"
        canvas.create_rectangle(x0, y0, x0 + lenBar, y1, \
            fill =color, width = 0)


    def drawMenuOptions(self, canvas, data):
        startY = 300
        diffText = 30
        boxHeight = 100
        margin = 30
        xM = data.fieldWidth + (data.width-data.fieldWidth)/2
        index = 1
        canvas.create_rectangle(data.fieldWidth+margin, startY, \
            data.width-margin, startY+boxHeight, fill = "white", width = 3)
        for option in self.menuOptions:
            canvas.create_text(xM , startY + diffText*index, \
                text = option, font = "arial 18 bold")
            index+=1

    def drawStats(self, canvas, data):
        self.menuStats = {"Money": "$%d"%self.money, "Wave": self.currWave}
        startY = 160
        diffBox = 50
        boxHeight = 40
        margin = 30
        boxWidth = data.width-data.fieldWidth - 2*margin
        xL = data.fieldWidth + margin
        index = 0
        for stat in self.menuStats:
            canvas.create_rectangle(xL, startY + diffBox*index, data.width-margin, \
                startY + diffBox*index + boxHeight, fill = "white", width = 3)
            canvas.create_text(xL +boxWidth/2, startY + diffBox*index + boxHeight/2, \
                text = stat + ": " +str(self.menuStats[stat]), font = "arial 20")
            index+=1

    def drawUpgradeMenu(self, canvas, data):
        row, col = self.upgradeCords
        self.drawCell(data, canvas, row, col)
        canvas.create_rectangle(data.fieldWidth, 0, data.width, data.height, \
            fill = "light grey")
        canvas.create_text(data.fieldWidth + (data.width-data.fieldWidth)/2, \
            30, text = "Upgrade", font = "arial 40 bold")
        canvas.create_rectangle(data.fieldWidth+30, 150, \
            data.width-30, 250, fill = "white", width = 3)
        if not self.maxLevel:
            canvas.create_text(data.fieldWidth + (data.width-data.fieldWidth)/2, \
                200, text = "Buy Upgrade for $%d"%self.upGradeCost, font = "arial 18")
        else:
            canvas.create_text(data.fieldWidth + (data.width-data.fieldWidth)/2, \
                200, text = "Turret at max level!", font = "arial 18")
        xT = data.fieldWidth + (data.width - data.fieldWidth)/2
        canvas.create_text(xT, data.height - 30, text = "Click \"B\" to exit", \
            font = "arial 20")


    def drawSideMenu(self, canvas, data):
        canvas.create_rectangle(data.fieldWidth, 0, data.width, data.height, \
            fill = "light grey")
        xT = data.fieldWidth + 20
        canvas.create_text(data.fieldWidth + (data.width-data.fieldWidth)/2, \
            30, text = "Picnic Raid", font = "arial 40 bold")
        self.drawMenuOptions(canvas, data)
        self.drawHealth(canvas, data)
        self.drawStats(canvas, data)
    
    def drawSelectDifficulty(self, canvas, data):
        canvas.create_text(data.width/2, data.height*2/3, text="Choose Difficulty",\
            font = "arial 30 bold")
        boxWidth = 100
        boxHeight = 75
        b1cx = data.width/4
        b2cx = 3*data.width/4
        canvas.create_rectangle(b1cx - boxWidth/2, 3*data.height/4, b1cx + \
            boxWidth/2, 3*data.height/4 + boxHeight, fill = "yellow", width = 3 )
        canvas.create_text(b1cx, 3*data.height/4 + boxHeight/2 \
            , text="EASY", font="arial 30 bold")
        canvas.create_rectangle(b2cx - boxWidth/2, 3*data.height/4, \
            b2cx + boxWidth/2, 3*data.height/4 + boxHeight, fill="orange", width=3 )
        canvas.create_text(b2cx, 3*data.height/4 + boxHeight/2, \
            text="HARD", font="arial 30 bold")

    def drawEntryScreen(self, canvas, data):
        canvas.create_text(data.width/2, 50, text = "HOW TO PLAY:", font ="arial 50 bold")
        instructions = \
        """
        Welcome to Picnic Raid! The goal of this game is to protect your picnic 
        from the pesky ants. Ants can travel anywhere on the canvas to 
        get to the picnic. Click anywhere on the grass to open the turret 
        menu where you can purchase turrets. You can set your turrets before the 
        start of each wave. Click on any of your turrets to upgrade them, increasing 
        the turret's damage, range, fire rate, and size. Survive all ten waves 
        of ants to win the game. If enough ants reach your picnic, you lose the 
        game and your delicious lunch. Good luck!
        """
        canvas.create_text(data.width/2, 210, text = instructions, font = "arial 24")


        self.drawSelectDifficulty(canvas, data)

    def drawMenu(self, canvas, data):
        self.drawSideMenu(canvas, data)
        if self.showTurretMenu:
            self.drawTurretMenu(canvas, data)
        elif self.showUpgradeMenu:
            self.drawUpgradeMenu(canvas, data)





