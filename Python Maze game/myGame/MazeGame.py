# Intended resolution 1920x1080 or 1280x720
from tkinter import Button, Canvas, Entry, PhotoImage, StringVar, Tk, Toplevel, messagebox, Label

# Player movement is controlled using arrow keys.
# Game can be paused using the P key.
# The boss key feature is enabled when pressing the K key.
# In some levels, the user has to unlock doors by obtaining the keys.
# The leaderboard shows the top 3 highscores. If multiple scores are the same, it will choose the latest user with the same score.
# If a user has already started a game, entering that username after reloading the game will load their progress.
# To start a new game, create a new user.

# This are global variables that deal with movements speeds, current level and pause
level = 0
lives = 3
key = False
pause = False
maxLevel = 5
userArray = []
playerMovespeed = 10
enemyMovespeed = 0

# This function deals with saving the user and its progress.
def saveFile():
    global level
    saveArray=[]
    f = open("Users.txt",'r')
    for line in f:
        line = line.strip("\n")
        line = line.split(",")
        if userArray[0] == line[0] and userArray:
            userArray[1] = level
            saveArray.append(userArray)
        elif line == '':
            continue
        else:
            saveArray.append(line)
    f.close()
    sortedArray = sorted(saveArray, key=lambda x:str(x[1]))
    # print(sortedArray)
    w = open("Users.txt",'w')
    for i in range(len(saveArray)):
        if i == len(saveArray)-1:
            w.write(saveArray[i][0]+","+str(saveArray[i][1]))
        else:
            w.write(saveArray[i][0]+","+str(saveArray[i][1])+"\n")
    w.close()
    w = open("Leaderboard.txt",'w')
    for i in range(len(sortedArray)):
        if i == len(sortedArray)-1:
            w.write(sortedArray[i][0]+","+str(sortedArray[i][1]))
        else:
            w.write(sortedArray[i][0]+","+str(sortedArray[i][1])+"\n")
    w.close()

# This function loads the leaderboard file so it is displayed on the menu screen.
#It will load the top 3 users, and if there is less than 3 it will display the users with a score.
def leaderboardFile():
    f = open("Leaderboard.txt",'r')
    leaderList = []
    labelList = []
    for line in f:
        line = line.strip("\n")
        line = line.split(",")
        leaderList.append(line)
    if len(leaderList) > 2:
        for i in range(1,4):
            hiScorer = len(leaderList)-i
            labelList.append(Label(login, text=leaderList[hiScorer][0]+" reached level "+str(int(leaderList[hiScorer][1])+1),font="arial").pack(pady=5,padx=20))
    elif len(leaderList) > 1:
        for i in range(1,3):
            hiScorer = len(leaderList)-i
            labelList.append(Label(login, text=leaderList[hiScorer][0]+" reached level "+str(int(leaderList[hiScorer][1])+1),font="arial").pack(pady=5,padx=20))
    elif len(leaderList) > 0:
        for i in range(1,2):
            hiScorer = len(leaderList)-i
            labelList.append(Label(login, text=leaderList[hiScorer][0]+" reached level "+str(int(leaderList[hiScorer][1])+1),font="arial").pack(pady=5,padx=20))



# This function is called whe the user presses the enter button on the login page.
# It loads the level based on user saves.
def exitLogin():
    global tileArray
    global enemyMovespeed
    window.deiconify()
    tileArray = []
    levelSelector()
    canvas.coords(player, 100,100)
    canvas.coords(enemy, 1000,120)
    canvas.tag_raise(player)
    canvas.tag_raise(enemy)
    login.destroy()
    if level <= maxLevel:
        enemyMovespeed = 1

# This function opens the user saves file and checks if the user already exists. If it doesnt exist, it creates a new one.
def user():
    global userString
    global level
    global userArray
    userString = text.get()
    check = open("Users.txt","r")
    emptyCheck = check.read(1)
    check.close
    inputs = open("Users.txt","r")
    if len(userString) < 1 or len(userString) > 12:
        return messagebox.showinfo ('Error', 'Please enter a username between 1 and 12 characters long')
    elif ',' in userString:
        return messagebox.showinfo ('Error', 'Please use valid characters')
    else:
        for line in inputs:
            line = line.strip("\n")
            line = line.split(",")
            if line[0] == userString:
                level = int(line[1])
                currentLevel.set(" level:" + str(level+1) + " ")
                userArray = line
                inputs.close()
                return exitLogin()
        userArray = [userString,'0']
        saves = open("Users.txt",'a')
        if not emptyCheck:
            saves.write(userString+',0')
        else:
            saves.write('\n'+userString+',0')
        saves.close()
        saveFile()
        exitLogin()



# This code creates the main game window and its initial UI.
window = Tk()
window.title("Maze Game")
canvas = Canvas(window, bg="black", width=1280, height=720)
canvas.pack()
window.withdraw()
pauseText = Label(window,text="PAUSED", font=("Arial",50),background="yellow")
currentLevel = StringVar()
currentLevel.set(" level:" + str(level+1) + " ")
currentlives = StringVar()
currentlives.set(" lives:" + str(lives) + " ")
levelCounter = Label(window,textvariable=currentLevel, font=("Arial",25),background="#696969",borderwidth=2, relief="solid")
levelCounter.place(x=20,y=20)
livesCounter = Label(window,textvariable=currentlives, font=("Arial",25),background="#696969",borderwidth=2, relief="solid")
livesCounter.place(x=200,y=20)
playerDisplay = PhotoImage(master = window,file="eye.png")
altPlayerDisplay = PhotoImage(master = window,file="razor.png")
enemyDisplay = PhotoImage(master = window,file="enemy.png")
bossDisplay = PhotoImage(master = window,file="boss.png")
boss = Label(window,image=bossDisplay)
player = canvas.create_image(100,100,image=playerDisplay, tag="player")
enemy = canvas.create_image(1000,100,image=enemyDisplay)

# This function allows the user to choose an alternate sprite for the player.
def enableAlt(x):
    global altCharacter
    global player
    player = canvas.create_image(100,100,image=altPlayerDisplay, tag="player")
    x.pack_forget()

# This code creates the login window
login = Toplevel()
login.wm_title("Main Menu: Enter your username:")
login.geometry("600x600")
text = StringVar(login)
description = Label(login, text="Please enter an existing username to load your progress",font="arial").pack(pady=5,padx=20)
description2 = Label(login, text="Enter a new one to start a new save",font="arial").pack(pady=5,padx=20)
username = Entry(login,textvariable=text).pack(pady=10,padx=20)
enter = Button(login, text="Enter", command=user).pack(pady=10,padx=20)
altCharacter = Button(login, text="Choose Alternate Sprite")
altCharacter.pack(pady=10,padx=20)
altCharacter.config(command=lambda:enableAlt(altCharacter))
description3 = Label(login, text="Use arrow keys to move.\nPress K for a speed cheat.\nPress K to enable the boss key.\nPress P to pause the game.",font="arial").pack(pady=10,padx=20)
leaderboardTitle = Label(login, text="Leaderboard\n Top 3",font=("arial",25),borderwidth=2, relief="solid").pack(pady=10,padx=20)
leaderboardFile()

# This code initializes the variables string images
wallDisplay = PhotoImage(master = window,file="wall.png")
goalDisplay = PhotoImage(master = window,file="goal.png")
pathDisplay = PhotoImage(master = window,file="path.png")
doorDisplay = PhotoImage(master = window,file="door.png")
keyDisplay = PhotoImage(master = window,file="key.png")

# This code initialized the arrays that load and store the different maps.
tileArray = []
mapArray = []
mapArray2 = []
mapArray3 = []
mapArray4 = []
mapArray5 = []

# This function loads each of the maps
def initialiseMaps(map,counter):
    f = open("map"+str(counter)+".txt","r")
    for line in f:
        line = line.strip("\n")
        line = line.split(",")
        map.append(line)
    f.close()

for i in range (1,6):
    if i ==1:
        initialiseMaps(mapArray,i)
    elif i ==2:
        initialiseMaps(mapArray2,i)
    elif i ==3:
        initialiseMaps(mapArray3,i)
    elif i ==4:
        initialiseMaps(mapArray4,i)
    elif i ==5:
        initialiseMaps(mapArray5,i)

# This function takes a map array as a parameter and loads the appropriate tiles on the screen based on the data in the array.
def levelMap(map):
    amountRows = 9
    amountColumns = 16
    global tileArray
    x1 = 0
    y1 = 0
    for a in range(0,amountRows):
        x1 = 0
        for b in range(0,amountColumns):
            if map[a][b] == 'x':
                tileArray.append(canvas.create_image(x1+40,y1+40,image=wallDisplay, tag='wall'))
            elif map[a][b] == 'o':
                tileArray.append(canvas.create_image(x1+40,y1+40,image=pathDisplay, tag='path'))
            elif map[a][b] == 'w':
                tileArray.append(canvas.create_image(x1+40,y1+40,image=goalDisplay, tag='goal'))
            elif map[a][b] == 'd':
                if(key==True):
                    tileArray.append(canvas.create_image(x1+40,y1+40,image=pathDisplay, tag='path'))
                else:
                    tileArray.append(canvas.create_image(x1+40,y1+40,image=doorDisplay, tag='door'))
            elif map[a][b] == 'k':
                if(key==True):
                    tileArray.append(canvas.create_image(x1+40,y1+40,image=pathDisplay, tag='path'))
                else:
                    tileArray.append(canvas.create_image(x1+40,y1+40,image=keyDisplay, tag='key'))
            x1 = x1 + 80
        y1 = y1 + 80

# This function deals with the pause feature. It gets triggered when the user presses the 'P' key on the keyboard.
def stop(event):
    global pause
    global playerMovespeed
    global enemyMovespeed
    if level != maxLevel:
        pause = not pause
        if pause == True:
            playerMovespeed = 0
            enemyMovespeed = 0
            pauseText.place(x=520,y=300)
        else:
            playerMovespeed = 10
            enemyMovespeed = 1
            pauseText.place_forget()

# This function deals with the collision detection of the player and the different tiles (eg. player vs wall).
# It checks the positions of the tiles and the players and checks what action to do.
def collisions(xChange,yChange):
    global level
    global tileArray
    global key
    canvas.move(player,xChange,yChange)
    playerPos = canvas.coords(player)
    enemyPos = canvas.coords(enemy)
    for i in range(len(tileArray)):
        if tileArray:
            currTile = tileArray[i]
            tilePos = canvas.coords(currTile)
            if canvas.itemcget(currTile,'tag') == 'wall':
                if (playerPos[0]-20) < tilePos [0]+40 and (playerPos[0]+20) > tilePos [0]-40 and (playerPos[1]-20) < tilePos [1]+40 and (playerPos[1]+20) > tilePos [1]-40:
                    canvas.move(player,-xChange,-yChange)
                    return
            elif canvas.itemcget(currTile,'tag') == 'door':
                if (playerPos[0]-20) < tilePos [0]+40 and (playerPos[0]+20) > tilePos [0]-40 and (playerPos[1]-20) < tilePos [1]+40 and (playerPos[1]+20) > tilePos [1]-40:
                    canvas.move(player,-xChange,-yChange)
                    return
            elif canvas.itemcget(currTile,'tag') == 'key':
                if (playerPos[0]-20) < tilePos [0]+40 and (playerPos[0]+20) > tilePos [0]-40 and (playerPos[1]-20) < tilePos [1]+40 and (playerPos[1]+20) > tilePos [1]-40:
                    key = True
                    tileArray = []
                    levelSelector()
                    canvas.coords(player, playerPos[0],playerPos[1])
                    canvas.tag_raise(player)
                    canvas.coords(enemy, enemyPos[0],enemyPos[1])
                    canvas.tag_raise(enemy)
                    return
            elif canvas.itemcget(currTile,'tag') == 'goal':
                if (playerPos[0]-20) < tilePos [0]+40 and (playerPos[0]+20) > tilePos [0]-40 and (playerPos[1]-20) < tilePos [1]+40 and (playerPos[1]+20) > tilePos [1]-40:
                    level +=1
                    key = False
                    tileArray = []
                    updateLevelCounter()
                    levelSelector()
                    canvas.coords(player, 100,100)
                    canvas.tag_raise(player)
                    canvas.coords(enemy, 1000,120)
                    canvas.tag_raise(enemy)
                    if level >maxLevel-1:
                        level = 4
                    saveFile()

# This function deals with the boss key feature. It gets triggered when the user presses the 'K' key on the keyboard.
def bossKey(event):
    global pause
    global playerMovespeed
    global enemyMovespeed
    if level != maxLevel:
        pause = not pause
        if pause == True:
            playerMovespeed = 0
            enemyMovespeed = 0
            boss.place(x=0,y=0)
        else:
            playerMovespeed = 10
            enemyMovespeed = 1
            boss.place_forget()

# This function deals with the level selection. It passes the appropriate array based on the level.
def levelSelector():
    global playerMovespeed
    global enemyMovespeed
    if level == 0:
        levelMap(mapArray)
    elif level == 1:
        levelMap(mapArray2)
    elif level == 2:
        levelMap(mapArray3)
    elif level == 3:
        levelMap(mapArray4)
    elif level == 4:
        levelMap(mapArray5)
    else:
        canvas.create_rectangle(300,300,800,400,fill='red')
        canvas.create_text(550, 350, text="You Win!",font=("Purisa", 50))
        playerMovespeed = 0
        enemyMovespeed = 0

# This function deals with the logic behind the enemy chasing the player.
# This function also deals with updating the lives counter.
def enemyLogic():
    global lives
    global key
    global tileArray
    global level
    playerPos = canvas.coords(player)
    enemyPos = canvas.coords(enemy)
    if(playerPos[0] < enemyPos[0]):
        canvas.move(enemy,-enemyMovespeed,0)
    if(playerPos[1] < enemyPos[1]):
        canvas.move(enemy,0,-enemyMovespeed)
    if(playerPos[0] > enemyPos[0]):
        canvas.move(enemy,enemyMovespeed,0)
    if(playerPos[1] > enemyPos[1]):
        canvas.move(enemy,0,enemyMovespeed)
    if (playerPos[0]-20) < enemyPos [0]+40 and (playerPos[0]+20) > enemyPos [0]-40 and (playerPos[1]-20) < enemyPos [1]+40 and (playerPos[1]+20) > enemyPos [1]-40:
        lives = lives - 1
        currentlives.set(" lives:" + str(lives) + " ")
        if(lives == 0):
            level = 0
            key = False
            tileArray = []
            levelSelector()
            canvas.coords(player, 100,100)
            canvas.tag_raise(player)
            canvas.coords(enemy, 1000,120)
            canvas.tag_raise(enemy)
            saveFile()
            lives = 3
            currentLevel.set(" level:" + str(level+1) + " ")
            currentlives.set(" lives:" + str(lives) + " ")
        else:
            canvas.coords(player, 100,100)
            canvas.tag_raise(player)
            canvas.coords(enemy, 1000,120)
            canvas.tag_raise(enemy)
    window.after(25, enemyLogic)

levelSelector()
enemyLogic()

# This function is used to update the level counter on the top left of the screen.
def updateLevelCounter():
    if level != maxLevel:
        currentLevel.set(" level:" + str(level+1) + " ")

# This function allows the user to enable a cheat and increase their movespeed.
def cheat(event):
    global playerMovespeed
    playerMovespeed = 20

# These functions deal with the player movement based on the arrow keys.
def UP(event):
        collisions(0,-playerMovespeed)
def DOWN(event):
        collisions(0,playerMovespeed)
def LEFT(event):
        collisions(-playerMovespeed,0)
def RIGHT(event):
        collisions(playerMovespeed,0)

# Key bindings to their respecting functions.
window.bind('<Up>', UP)
window.bind('<Down>',DOWN)
window.bind('<Left>', LEFT)
window.bind('<Right>', RIGHT)
window.bind('<P>', stop)
window.bind('<p>', stop)
window.bind('<K>', bossKey)
window.bind('<k>', bossKey)
window.bind('<x>', cheat)
window.bind('<X>', cheat)

window.mainloop()
