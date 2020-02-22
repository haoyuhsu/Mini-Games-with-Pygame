# This is 2048 Game

import pygame, sys, random, time

# Initialize Seed
random.seed()

def SameBesides(List):
    for i in range(3):
        for j in range(3):
            if (List[i][j] == List[i][j+1]):   # check beside block
                return True
            elif (List[i][j] == List[i+1][j]): # check up-down block
                return True
    if (List[3][3] == List[3][2] or List[3][3] == List[2][3]):  # check the button-right corner
        return True
    else:
        return False   # response No same block beside each other
def EndingDetect(List):
    counter = 0
    for i in range(4):
        for j in range(4):
            if (List[i][j]!=0):  
                counter+=1    # count the number of cells (Not 0)
    if (counter==16):  # if the grid is full (16 cell)
        if (SameBesides(List)==True):
            return False    # Not Ending
        else:
            return True     # Ending
    else:
        return False  # Not Ending
def RandomGeneration(List):
    counter = 0
    for i in range(4):
        for j in range(4):
            if (List[i][j]!=0):
                counter+=1
    repeat = 1
    # when the num of cells NOt equal to 16, add a num
    while (repeat==1 and counter!=16):
        repeat = 0
        # Generate Random Coordinate
        addingVert = random.randint(0,3)  # y-coordinate
        addingHorz = random.randint(0,3)  # x-coordinate
        if (List[addingVert][addingHorz]==0):
            List[addingVert][addingHorz] = 2  # when the empty cell found
        else:
            repeat = 1  # repeat again
    return List

def MovingLeft(numberList):
    for i in range(4):  # check each row
        num = [0,0,0,0]   # Create a num List
        count = 0
        j = 0
        while (j <= 3):
            if (numberList[i][j]!=0):
                k = 1   # basic parameter
                check = 0
                while (check==0 and k <= 3-j):
                    check = 1
                    if (j+k <= 3):
                        # if the right hand side is 0, skip to another one
                        if (numberList[i][j+k]==0 and j+k < 3):
                            k+=1       # plus 1 to parameter
                            check = 0  # check again
                        # finally got a num
                        else:
                            # when two nums are equal
                            if (numberList[i][j]==numberList[i][j+k]):
                                num[count] = numberList[i][j]*2  # add the num to the List
                                count += 1    # ready to store num at next cell in List
                                k+=1  # extra movement
                            else:
                                num[count] = numberList[i][j]
                                count += 1
                if (j==3):  # if the far right has a num 
                    num[count] = numberList[i][j]
                j+=k  # jummp to the next 'k' cell
            else:
            	j+=1  # when the cell is 0, go to another one
        numberList[i][0] = num[0]
        numberList[i][1] = num[1]
        numberList[i][2] = num[2]
        numberList[i][3] = num[3]
    return numberList
# the concept same as the fuction above
def MovingRight(numberList):
    for i in range(4):
        num = [0,0,0,0]
        count = 3
        j = 3
        while (j >= 0):
            if (numberList[i][j]!=0):
                k = 1
                check = 0
                while (check==0 and j-k >= 0):
                    check = 1
                    if (j-k >= 0):
                        if (numberList[i][j-k]==0 and j-k > 0):
                            k+=1
                            check = 0
                        else:
                            if (numberList[i][j]==numberList[i][j-k]):
                                num[count] = numberList[i][j]*2
                                count -= 1
                                k+=1
                            else:
                                num[count] = numberList[i][j]
                                count -= 1
                if (j==0):
                    num[count] = numberList[i][j]
                j-=k
            else:
            	j-=1
        numberList[i][0] = num[0]
        numberList[i][1] = num[1]
        numberList[i][2] = num[2]
        numberList[i][3] = num[3]
    return numberList
def MovingUp(numberList):
    for j in range(4):  # check each column
        num = [0,0,0,0]  # create a num List
        count = 0
        i = 0
        while (i <= 3):
            if (numberList[i][j]!=0):
                k = 1    # basic parameter
                check = 0
                while (check==0 and k <= 3-i):
                    check = 1
                    if (i+k <= 3):
                    	# if the lower cell is 0, skip to another one
                        if (numberList[i+k][j]==0 and i+k < 3):
                            k+=1       # plus 1 to parameter
                            check = 0  # check again
                        # finally got a num
                        else:
                            # when the two nums are equal
                            if (numberList[i][j]==numberList[i+k][j]):
                                num[count] = numberList[i][j]*2   # add the num to the List
                                count += 1    # ready to store num at next cell in List
                                k+=1   # extra movement      
                            else:
                                num[count] = numberList[i][j]
                                count += 1
                if (i==3):   # if the buttom cell has num
                    num[count] = numberList[i][j]

                i+=k   # jummp to the next 'k' cell
            else:
            	i+=1   # when the cell is 0, go to another one
        numberList[0][j] = num[0]
        numberList[1][j] = num[1]
        numberList[2][j] = num[2]
        numberList[3][j] = num[3]
    return numberList
# the concept same as the fuction above
def MovingDown(numberList):
    for j in range(4):
        num = [0,0,0,0]
        count = 3
        i = 3
        while (i >= 0):
            if (numberList[i][j]!=0):
                k = 1
                check = 0
                while (check==0 and i-k >= 0):
                    check = 1
                    if (i-k >= 0):
                        if (numberList[i-k][j]==0 and i-k > 0):
                            k+=1
                            check = 0
                        else:
                            if (numberList[i][j]==numberList[i-k][j]):
                                num[count] = numberList[i][j]*2
                                count -= 1
                                k+=1
                            else:
                                num[count] = numberList[i][j]
                                count -= 1
                if (i==0):
                    num[count] = numberList[i][j]
                i-=k
            else:
            	i-=1
        numberList[0][j] = num[0]
        numberList[1][j] = num[1]
        numberList[2][j] = num[2]
        numberList[3][j] = num[3]
    return numberList

# Gameover function
def gameOver():
    myFont = pygame.font.SysFont('monaco', 72)
    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (200, 15)
    playSurface.blit(GOsurf, GOrect)
    pygame.display.flip()
    time.sleep(5)
    pygame.quit()  # pygame exit
    sys.exit()     # console exit

def show(List):
    # Grid's Background
    background = pygame.Rect(trans_x-10, trans_y-10, 4*box_w+3*gap+20, 4*box_h+3*gap+20)
    bg_color = color_dic['gray']  # Background color
    pygame.draw.rect(playSurface, bg_color, background)
    # Grid
    for i in range(4):
        for j in range(4):
            # Box position (top-left)
            x_pos = j*(box_w+gap)+trans_x
            y_pos = i*(box_h+gap)+trans_y
            # number -> Box's color
            color_name = ColorChange(List[i][j])  # Get the color name
            RGB = color_dic[color_name]           # Get RGB value of the color
            # Draw each box
            box_rect = pygame.Rect(x_pos, y_pos, box_w, box_h)
            pygame.draw.rect(playSurface, RGB, box_rect)
            # Setting Font
            Font1 = pygame.font.SysFont('monaco', 50)
            # if the box num is 0, mix it with bg_color (same as not showing)
            if List[i][j] == 0:
                FontColor = bg_color
            else:
                FontColor = color_dic['black']
            # Paste the text onto surf1
            surf1 = Font1.render('{0}'.format(List[i][j]), True, FontColor)
            rect1 = surf1.get_rect()
            rect1.center = box_rect.center    # Align the text with the box
            playSurface.blit(surf1, rect1)

def ColorChange(num):
    # return the string
    return {
        0: 'gray',
        2: 'white',
        4: 'light_yellow',
        8: 'sandy_brown',
        16: 'coral',
        32: 'tomato',
        64: 'red',
        128: 'yellow_1',
        256: 'yellow_2',
        512: 'yellow_3',
        1024: 'yellow_3',
        2048: 'yellow_3',
        4096: 'green',
        8192: 'blue',
    } [num]  # according to the num

check_errors = pygame.init()
if (check_errors[1] > 0):
    print("(!) Had {0} initializing errors,exiting... ".format(check_errors[1]))
    sys.exit(-1)
else:
    print("(+) Pygame successfully initialized!")

pygame.font.init()

# Screen Parameters
width = 600
height = 600

# Translate Coordinate
trans_x = 100
trans_y = 100

# Screen
playSurface = pygame.display.set_mode((width, height))
pygame.display.set_caption('2048 Game!')

# Setting Colors
# Get RGB from 'https://www.rapidtables.com/web/color/RGB_Color.html'
color_dic = {}      # Create a dictionary to store Color
color_dic['black'] = pygame.Color(0, 0, 0)
color_dic['gray'] = pygame.Color(150, 150, 150)          # bg
color_dic['white'] = pygame.Color(245, 245, 245)         # 2
color_dic['light_yellow'] = pygame.Color(255, 248, 220)  # 4
color_dic['sandy_brown'] = pygame.Color(244, 164, 96)    # 8
color_dic['coral'] = pygame.Color(255, 127, 80)          # 16
color_dic['tomato'] = pygame.Color(255, 99, 71)          # 32
color_dic['red'] = pygame.Color(210, 0, 0)               # 64
color_dic['yellow_1'] = pygame.Color(255, 255, 204)      # 128
color_dic['yellow_2'] = pygame.Color(255, 255, 153)      # 256
color_dic['yellow_3'] = pygame.Color(255, 255, 102)      # 512, 1024, 2048
color_dic['green'] = pygame.Color(0, 255, 0)             # 4096
color_dic['blue'] = pygame.Color(0, 0, 255)              # 8192
color_dic['purple'] = pygame.Color(238, 130, 238)        # 16384, 32768

# FPS Controller
fpsController = pygame.time.Clock()

frame_rate = 50

# initializing the numberList
numberList = [[0 for i in range(4)] for j in range(4)]
numberList = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# Grid Size
box_h = 90
box_w = 90
# gap between the Box
gap = 20

numberList = RandomGeneration(numberList)

while True:
    # Background
    playSurface.fill(color_dic['black'])

    # Checking gameover or not
    if (EndingDetect(numberList)==True):
        gameOver()

    # Block Movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                numberList = MovingRight(numberList)
                numberList = RandomGeneration(numberList)
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                numberList = MovingLeft(numberList)
                numberList = RandomGeneration(numberList)
            if event.key == pygame.K_UP or event.key == ord('w'):
                numberList = MovingUp(numberList)
                numberList = RandomGeneration(numberList)
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                numberList = MovingDown(numberList)
                numberList = RandomGeneration(numberList)
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    # show Grid
    show(numberList)

    pygame.display.flip()            # update the full display Surface to the screen
    fpsController.tick(frame_rate)   # run under certain framerate
