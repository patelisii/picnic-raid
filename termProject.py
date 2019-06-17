#name: Patrick Elisii
#AndrewID: pelisii
#Section: B
#CITATION: run from course website
#CITATION: images from google- shuttleimages
import random
from tkinter import *
from termProjClasses import *


def placeTurret(data, turret):
    row, col = data.game.placingCords
    place = Turret(row, col, data.cellWidth/4)
    if turret == "Machine Turret":
        place = MachineTurret(row, col, data.cellWidth/4)
    elif turret == "Canon":
        place = Canon(row, col, data.cellWidth/4)
    elif turret == "Glue Gun":
        place = GlueGun(row, col, data.cellWidth/4)
    if data.game.buyThis(place.cost): 
        data.field.board[row][col] = 1
        data.turrets.append(place)
        data.game.showTurretMenu = False

def createEnemy(data):
    if data.waveTimer % 80 == 0:
        selectNum = random.randint(1, 10)
        #if %3- red ant, if %5- bigAnt
        enemy = Enemy(data.cellWidth/2, data.height/2, 10)
        if selectNum%4 == 0:
            enemy = RedAnt(data.cellWidth/2, data.height/2, 7)
        if selectNum%6 == 0:
            enemy = BossAnt(data.cellWidth/2, data.height/2, 13)
        enemy.setHP(data)
        data.enemies.append(enemy)


def runGame(data):
    for turret in data.turrets:
        for enemy in data.enemies:
            if turret.onTimerFired(data, enemy): break
    for bullet in data.bullets:
        bullet.moveBullet()
        if bullet.cx > data.width or bullet.cx < 0 or bullet.cy > data.height or \
        bullet.cy < 0:
            data.bullets.remove(bullet)
    for enemy in data.enemies:
        if data.timer % 5 == 0:
            enemy.followPath(data)
        bullet = enemy.isCollision(data)
        if bullet!= None:
            enemy.reactToBulletHit(data, bullet)
    createEnemy(data)
    if data.waveTimer < 100 * data.game.waveLen + 1:
        data.waveTimer += 1
    elif data.enemies == []:
        data.game.isWaveOver = True
        data.game.isPlaying = False
    data.timer += 1

def drawGame(canvas, data):
    data.field.draw(canvas, data)
    for enemy in data.enemies:
        enemy.draw(canvas)
    for bullet in data.bullets:
        bullet.draw(canvas)
    for turret in data.turrets:
        turret.draw(canvas, data)
    data.game.drawMenu(canvas, data)

#CITATION: from course website
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    board =[[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2], 
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], 
            [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] ]


    data.fieldWidth = data.width - data.width/4
    data.field = Field(board, len(board), len(board[0]))
    data.cellWidth = data.fieldWidth/data.field.cols
    data.cellHeight = data.height/data.field.rows
    data.path = []
    data.enemies = []
    data.turrets = []
    data.bullets = []
    data.waveTimer = 0
    data.timer = 0
    data.game = Game()

    #images from google:
    #https://www.deviantart.com/arekkusu-art/art/BACKGROUND-GRASS-567826687
    data.image0 = PhotoImage(file ="grass2.gif")
    #http://www.thepinsta.com/cartoon-summer-food_A413rxnkVuK1oj4lBSr*%
    #7CTuPuL%7C5AtmaxdNOhwhYJhs/
    data.image1 = PhotoImage(file="PicnicScene.gif")
    data.image1 = data.image1.subsample(4,4)
    #http://80skiparty.com/ant-hill-clipart/
    data.image2 = PhotoImage(file="Ant_Hill.gif")
    data.image2 = data.image2.subsample(4,4)
    #https://pilotonline.com/content/tncms/live/#1
    data.image3 = PhotoImage(file="startpicback.gif")
    data.image4 = data.image0.zoom(2, 2)
    

    


def mousePressed(event, data):
    # use event.x and event.y
    if data.game.showStartScreen:
        data.game.startGame(data, event.x, event.y)
    elif data.game.showEntryScreen:
        data.game.takeToGame(data, event.x, event.y)
    elif data.game.isInGame and not data.game.isPlaying and not \
        data.game.isPaused and not data.game.isGameOver and not data.game.isWaveOver:
        #select box and if 1: upgrade, if 0: open turret menu
        if data.game.showTurretMenu:
            turretType = data.game.confirmedBuyTurret(data, event.x, event.y)
            if turretType != None:
                placeTurret(data, turretType)
                data.game.clickTurret = {}
        elif data.game.showUpgradeMenu:
            data.game.upgradeTurret(data, event.x, event.y)
        else:
            data.game.openUpgradeMenu(data, event.x, event.y)
            data.game.openTurretMenu(data, event.x, event.y)
    if data.game.isWaveOver:
        data.game.nextWave(data)
        data.game.startWave(data) 


def keyPressed(event, data):
    # use event.char and event.keysym
    if data.game.isInGame and not data.game.showTurretMenu:
        if event.keysym == "space":
            data.game.isPlaying = True
            #find shortest path
            data.path = data.field.findPath( data.field.rows//2, 0, data.field.rows//2,\
                   data.field.cols-1, [(data.field.rows//2,0 )] )
        elif event.keysym == "p" and data.game.isPlaying:
            data.game.isPaused = not data.game.isPaused
    if event.keysym == "r":
            init(data)
    if (data.game.showTurretMenu or data.game.showUpgradeMenu) and event.keysym == "b":
        data.game.showTurretMenu = False
        data.game.showUpgradeMenu = False
        data.game.resetValues(data)
        

def timerFired(data):
    if data.game.isPlaying and not data.game.isPaused:
        runGame(data)
    data.game.gameOver()
        

def redrawAll(canvas, data):
    # draw in canvas
    # drawBoard(data, canvas)
    if data.game.showStartScreen:
        data.game.drawStartScreen(data, canvas)
    elif data.game.showEntryScreen:
        data.game.drawEntryScreen(canvas, data)
    elif data.game.isInGame:
        drawGame(canvas, data)
    if data.game.isWaveOver:
        data.game.drawNewWave(canvas, data)
    elif data.game.isGameOver:
        data.game.drawGameOver(canvas, data)
        

####################################
# use the run function as-is
####################################

def run(width=1000, height=575):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    
    print("bye!")

run( )



