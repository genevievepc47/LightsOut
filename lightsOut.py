#pygame template
"""Genevieve Cohen
Period 10 Honors computer programming (python)
"""

import pygame
import sys
import random
import math


pygame.init()#initialize game engine

#set up the drawing surface
width = 500 
height = 500

w= width- width/7
h = height- height/7

size = (width,height) #tuple
surface = pygame.display.set_mode(size)

#set the window title bar
pygame.display.set_caption("Lights Out")

# declare color constants
BLACK = (0  ,0  ,0  )
WHITE = (255,255,255)
RED =   (255,0  ,0  )
GREEN = (0  ,255,0  )
BLUE =  (0  ,0  ,255)
DARKGREEN = (25, 109, 0)
SIZE = 7 #size of the game board, be careful if you change this. for instance if you use at 5x5 grid then you can't always solve every combination of lights


'''
put text on the screen
'''
def showMessage(words, fontName, size, xVal, yVal, foreColor, bg = None):
    fontName = pygame.font.SysFont(fontName, size, 0,0)
    text = fontName.render(words,True, foreColor,bg)
    
    #get the rectangle bounding box of the text
    textBounds = text.get_rect()
    
    #center at x,y
    textBounds.center = (xVal, yVal)
    
    surface.blit(text, textBounds)
    return textBounds
    
'''
show a message sideways
'''
def showMessageSideways(words, fontName, size, xVal, yVal, foreColor, bg = None):
    
    fontName = pygame.font.SysFont(fontName, size, 0,0)
    text = fontName.render(words,True, foreColor,bg)
    text = pygame.transform.rotate(text, 90)
    #get the rectangle bounding box of the text
    textBounds = text.get_rect()
    
    #center at x,y
    textBounds.center = (xVal, yVal)
    
    surface.blit(text, textBounds)
    return textBounds

def toggleLights(board, r, c):
    
    if(board[r][c]== 1):#if the one you pressed is on
        board[r][c] = 0#turn it off
    else:#if the cell you pressed is off
        board[r][c] = 1#turn it on
        
    #toggle the lights around it
    #down
    if(r+1 < len(board)):#if going down is in bounds
        if(board[r+1][c] == 1):#if down is on already
            board[r+1][c] =0 #turn it off
        else:#if board is off
            board[r+1][c] = 1#turn it on
        
    #up    
    if(r-1 >=0):#if going up is in bounds
        if(board[r-1][c] ==1):#if up is already on
            board[r-1][c] = 0#turn it off
        else:#if it is off
            board[r-1][c]= 1#turn it on
            
    #left
    if(c-1 >=0):#if going left is in bounds
        if(board[r][c-1] ==1):#if left is on already
            board[r][c-1] = 0#turn it off
        else:#if left is off
            board[r][c-1] = 1#turn it on
    
    #right
    if(c+1 < len(board)):#if going right is in bounds
        if(board[r][c+1] == 1):#if right is on already
            board[r][c+1] = 0#turn it off
        else:#if right is off
            board[r][c+1] = 1#turn it on
            
    return board
    

def drawScreen(board, gameOver, clicks):
    #make the grid
    
    #draw rectangles
    for r in range(len(board)):
        for c in range(len(board)):
            
            if(board[r][c] == 1):#if the light is on
                cellColor = GREEN
            else:#if the light is off
                cellColor = DARKGREEN
            pygame.draw.rect(surface, cellColor, (int(c*w/len(board) ), int(r*h/len(board) ),int((w/len(board))- w/50 ), int((h/len(board)))-h/50 ) , 0)#draw green squares inside the black ones
           
    #instructions
    instructions = ''
    if(gameOver == True):#if the game is over, they won
        showMessage("You Won!", "Consolas", w/20, width/2, height-height/10, WHITE)
        showMessage("Press ENTER to play again!", "Consolas", width/30, width/2, height-height/17, WHITE)
    else:#if the game is not over
        showMessage("Turn off all of the lights to win.", "Consolas", width/30, width/2, height-height/8, WHITE)
        showMessage("Click on a light to toggle it and the lights around it." ,"Consolas", width/30, width/2, height-height/11, WHITE)
        showMessage("Press ENTER to start over.","Consolas", width/30, width/2, height-height/19, WHITE)
    
    #logo
    if(gameOver == False):#if the game is not over
        showMessageSideways("Lights-Out", "Consolas", w/7, width-width/15, height/2.5, DARKGREEN)
    else:#if the game is over, show the logo with the lights out
        showMessageSideways("Lights-Out", "Consolas", w/7, width-width/15, height/2.5, GREEN)
        
    #num clicks
    showMessage(("Clicks: " + str(clicks) ), "Consolas", w/30, w/10, height-height/30, WHITE)
                            
'''
send it the size of board you want to make
it makes a board sizexsize, fills it with random lights on and lights off
returns the new board
'''
def initBoard(size, cellRects):
    board = []
    emptyBoard = []# a board where all the lights are off, used to compare to see if game is over
    
    
    for r in range(size):#loop through rows
        board.append([0]*size)
        emptyBoard.append([0]*size)
   
    
    #put random lights on
    numLights = random.randint(1,(size-1)*(size-1))#get a random number of lights to turn on, from one light to all lights
    counter = 0
   
    while (counter< numLights):#while more lights still need to be turned on
        row = random.randint(0,size-1)#get a random row to turn a light on in
        col = random.randint(0,size-1)#get a random col to turn a light on in
        
        
        if(board[row][col] != 1):#if it is not already on
            board[row][col] = 1#turn it on
            
            counter +=1#mark that a light has been turned on
            
    #fill cellRects
    for r in range(len(board)):
        newlist = []
        for c in range(len(board)):
            
            
            
            newlist.append(pygame.Rect((int(c*w/len(board) ), int(r*h/len(board) ),int((w/len(board))- w/50 ), int((h/len(board)))-h/50 ))  )  
        cellRects.append(newlist)
    return board, cellRects, emptyBoard
        
#----------------------------------MAIN PROGRAM LOOP-----------------------------------------
def main():
    gameOver = False
    clicks = 0
    
    cellRects = []
    
    board, cellRects, emptyBoard = initBoard(SIZE, cellRects) #turn some lights on, and fill cellRects
    while(True):
        
        
        for event in pygame.event.get():
            if(event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
           
           
            #other single keypress events
            if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gameOver == False):#if they click the cell
                pos = pygame.mouse.get_pos()
                #test collision for mouse over cells   
                for r in range(SIZE):#loop through the rows of cells  
                    for c in range(SIZE):#loop through the columns of cells
                        cellBounds = cellRects[r][c]
                        
                        #print("i am on cell", r, c)
                        if(cellBounds.collidepoint(pygame.mouse.get_pos())):#if the mouse is over the cell
                            board = toggleLights(board, r, c)
                            clicks +=1
                if(board ==  emptyBoard):#iff all the lights are off
                    gameOver = True
                            
                            
             
            #check for if they hit enter to reset
            if(event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN ):#if they hit enter    
                gameOver = False
                clicks = 0
                board, cellRects, emptyBoard = initBoard(SIZE, cellRects) #turn some lights on, and fill cellRects
        #game logic goes here
        
    
        #set background fill
        surface.fill(BLACK)
        
        #drawing code goes here
        drawScreen(board, gameOver, clicks)
        
        
        pygame.display.update()
        
main()


'''
instructions
1.Plan, what variables will you need. How will you keep track of which lights are on. When will the game end.
2.(initBoard)Make an empty board of the size, fill it with 0s to represent lights off (not all sizes work)
3.Draw the grid, draw black squares with smaller green squares inside of them to make the grid. Or just fill the background with black and draw green squares to make the grid. leave space for instructions/logo
4.(add to  initBoard)Fill it with random number of lights on in random places
 5.modify draw board to light up the lights with 1 in them
 6. (odd to initboard) take the loop that you have in draw screen to draw the green rectangles, and instead of drawing them, add them to a list of cellRects.
 7.detect clicks, loop thorugh cellRects and check if the mous position collides with anny of the cells when they click
 8. If it does collide, send the board, row, and col to toggleLights()
 9. make toggleLights, should accept what it needs to know to toggle the light they clicked on and the ones around it
 10. toggleLights should toggle the light they clicked on, up, down, left and right lights as well
 11. make a gameover condition and diplay a win message, used an array with all the lights off to compare to see if board had all lights off. you can add an loss mechanism, give the user a certain number of clicks to solve it in.
 12. add instructions, telling the user how to play, and that they can hit enter to start over
 13. make the logo. put a lights out logo somewhere on the screen, make it look nice and creative
 14. check if they hit enter to reset. then reset variables back to original values
 15. keep track of their clicks for each game. The point of the game is to solve the puzzle in the least amount of clicks
 16. display the clicks, send the number of clicks to draw screen, and blit it to the screen there with show message
 
 



'''