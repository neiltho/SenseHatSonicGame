from sense_hat import SenseHat
from time import sleep
import random


sense = SenseHat()
sense.low_light = True
red = (255,0,0)
cyan = (0,255,255)
grey = (122, 122, 122)
yellow = (255, 255, 0)
blue = (0, 0, 225)
start_delay = 2
grid_min = 0
grid_max = 7
grid_size = 8
paused = True
m = (0, 0, 0)



g = (0, 255, 0)
light_green = (0,20,0)
y = (255, 255, 0)
yellow = (255, 255, 0)
r = (255, 0, 0)
v = open('gamedata.txt','a')
p = open('gamedata.txt','r')

pause_screen = [
y, y, y, y, y, y, y, y,
y, y, m, y, y, m, y, y,
y, y, m, y, y, m, y, y,
y, y, m, y, y, m, y, y,
y, y, m, y, y, m, y, y,
y, y, m, y, y, m, y, y,
y, y, y, y, y, y, y, y,
y, y, y, y, y, y, y, y,
]

start_screen = [
m, y, y, y, y, y, y, m,
r, m, m, m, m, m, m, g,
r, m, m, m, m, m, m, g,
r, m, m, m, m, m, m, g,
r, m, m, m, m, m, m, g,
r, m, m, m, m, m, m, g,
r, m, m, m, m, m, m, g,
m, m, m, m, m, m, m, m,
]
# choosing difficulty
sense.set_pixels(start_screen)
print("Welcome to Sense hat Sonic game")
print("Choose a difficulty " + "or move joystick down for highscores")
diff = 0


while diff == 0:
    for event in sense.stick.get_events():
        if event.direction == "left":
            diff = 3
        elif event.direction == "right":
            diff = 1  
        elif event.direction == "up":
            diff = 2
        elif event.direction == "down":
            print(p.read())
            


if diff == 3:
    speed = 0.25
elif diff == 2:
    speed = 0.45
elif diff == 1:
    speed = 0.6


#game
sleep(2)
while True:
    gameOverFlag = False
    generateRandomFoodFlag = False
    manMovementDelay = speed
    manMovementDelayDecrease = -0.02
    score = 0
    sense.clear()
    #sets man starting position and direction
    manPosX = [3]
    manPosY = [6]
    movementX = 0
    movementY = -1
    moved = 0
    joystick_right = 0
    joystick_up = 0
    joystick_left = 0
    joystick_down = 0
    times_paused = 0
    
    with open("gamedata.txt") as f:
        for line in f:
            pass
        last_line = line
    highscore = int(last_line)
    


    # Generate random food position
    while True:
        foodPosX = random.randint(0, 7)
        foodPosY = random.randint(0, 7)
        if foodPosX != manPosX[0] or foodPosY != manPosY[0]:
            break
    
    while not gameOverFlag:
        # Check if man eats food
        if foodPosX == manPosX[0] and foodPosY == manPosY[0]:
            generateRandomFoodFlag = True
            manMovementDelay += manMovementDelayDecrease
            score = score + 1
        # Check if game-over
        if gameOverFlag:
            break

        # Check joystick events
        for event in sense.stick.get_events():
            if event.direction == "left" and movementX != 1:
                movementX = -1
                movementY = 0
                joystick_left += 1
            elif event.direction == "right" and movementX != -1:
                movementX = 1
                movementY = 0
                joystick_right += 1
            elif event.direction == "up" and movementY != 1:
                movementY = -1
                movementX = 0
                joystick_up += 1
            elif event.direction == "down" and movementY != -1:
                movementY = 1
                movementX = 0
                joystick_down += 1
            elif event.direction == "middle":
                times_paused += 1
                sense.clear()
                pasued = True
                while pasued:
                    sense.set_pixels(pause_screen)
                    for event in sense.stick.get_events():
                        if event.direction == "middle":
                            pasued = False
                # Update the game 
                sense.clear()
                sense.set_pixel(foodPosX, foodPosY, yellow)
                for x, y in zip(manPosX, manPosY):
                    sense.set_pixel(x, y, grey)
            if gameOverFlag:
                break
            
            
        # Move man
        for i in range((len(manPosX) - 1), 0, -1):
            manPosX[i] = manPosX[i - 1]
            manPosY[i] = manPosY[i - 1]

        manPosX[0] += movementX
        manPosY[0] += movementY

        #Check game borders
        if manPosX[0] > grid_max:
            gameOverFlag = True
        elif manPosX[0] < grid_min:
            gameOverFlag = True
        if manPosY[0] > grid_max:
            gameOverFlag = True
        elif manPosY[0] < grid_min:
            gameOverFlag = True
        if gameOverFlag:
            break

        # generate food cords
        if generateRandomFoodFlag:
            generateRandomFoodFlag = False
            retryFlag = True
            while retryFlag:
                foodPosX = random.randint(0, 7)
                foodPosY = random.randint(0, 7)
                retryFlag = False
                for x, y in zip(manPosX, manPosY):
                    if x == foodPosX and y == foodPosY:
                        retryFlag = True
                        break

        # Update 
        sense.clear(light_green)
        #put down food
        sense.set_pixel(foodPosX, foodPosY, yellow)
        #move man
        for x, y in zip(manPosX, manPosY):  
            sense.set_pixel(x, y, cyan)

        # man speed (game loop delay)
        sleep(manMovementDelay)
        moved += 1

    #clear
    sense.clear(grey)
    sleep(1)
    sense.clear()           
    #show score + reset
    #print("\n")
    print("Stats")
    print("Score: "+ str(score))
    if score > highscore:
        print("Highscore: "+str(score))
    else:
        print("Highscore: "+str(highscore))
    
    print("Times moved: "+str(moved-1))
    print("Times joystick moved up:" + str(joystick_up))
    print("Times joystick moved down:" + str(joystick_down))
    print("Times joystick moved right:" + str(joystick_right))
    print("Times joystick moved left:" + str(joystick_left))
    if times_paused > 0:
        print("Times paused: " + str(times_paused))
    
    #present highscore
    if score > highscore:
        sense.show_message("Game over! New Highscore :D {}".format(score), text_colour=blue,scroll_speed=0.05)
        print("\n")
        name = input("Name for highscore: ")
        v.write(name+"\n")
        v.write(str(score)+"\n")
        v.close()
    else:
        sense.show_message("Game over! Score: {}".format(score), text_colour=yellow,scroll_speed=0.05)
        sense.show_message("Highscore: {}".format(highscore), text_colour=blue,scroll_speed=0.05)
    sense.clear(grey)
    sleep(1)
                                                                                                                                                                                                                                                                                                                                                                                                                  
  
  
  
  
  