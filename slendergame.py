Priscilla Boateng, Ana Goddard
# the gamebox code used was created by Luther Tychonievich

"""The point of this game is to help Slenderman get power ups, which give him direly needed health, and avoid the
hazards which take away his health points. He needs at least 18 health points by the point the timer hits 60!
If his health meter hits zero because you hit too many hazards, you lose!


Animation: Slenderman is animated and moves across the screen with user input

Collectibles: the capri-suns (red boxes) which give Slenderman health points, and the milk, which subtracts health pts.

Timer:  have a visible timer that counts to 60, game ends if you don't have enough points by the time it hits 60

Health Meter: Your collectibles refill Slenderman's health. If you hit too many hazards and it goes to below zero, you
lose!

"""

import pygame
import gamebox
import random

# images

width = 800
height = 600
camera = gamebox.Camera(width, height)
slenderman = gamebox.from_image(400, 560, "http://www.pngonly.com/wp-content/uploads/2017/05/Slender-Man-Small-PNG.png")
slenderman.scale_by(0.2)
background = gamebox.from_image(300, 300,
                                'https://3c1703fe8d.site.internapcdn.net/newman/gfx/news/2018/europeslostf.jpg')

# variables

game_on = False
score_count = 0
counter = 0  # how many times tick is run
milk = []  # he's lactose intolerant! very bad
capri_sun = []  # that good stuff
points = 0  # corresponds to energy

instructions = """ Hey, it's Slenderman! I'm back at my lair trying to refuel with my favorite power-up, Capri-Sun.
    Somebody infiltrated my food supply and snuck milk into my Capri-Suns, knowing that I'm severely lactose intolerant.
    I can't go on my next mission until I have more power. I need someone to find the uncontaminated Capri-Sun. 
    Will you help me?

    Get 18 points before the timer reaches 60 seconds. Each Capri-Sun (red box) gives you 1 point and each dairy
    contaminated Capri-Sun (the white boxes) subtracts 1 point. Use the arrow keys to maneuver Slenderman to the 
     correct drank. Go any direction you want, just don't touch the milk! """

# title screen and instructions

to_draw = []  # This list will contain all boxes we draw this tick

game_title = gamebox.from_text(400, 30, 'Slenderman!', 40, 'red', True)
to_draw.append(game_title)
camera.clear('black')

ypos = 200
for line in instructions.split('\n'):
    to_draw.append(gamebox.from_text(400, ypos, line, 20, 'red'))
    ypos += 20

# Draw and display

for box in to_draw:
    camera.draw(box)
    camera.display()


def tick(keys):  # makes our game run

    to_draw = []
    global counter
    global points
    counter += 1

    # moves the milk minefield and capri suns
    if counter % 45 == 0:
        num_obs = random.randint(0, 4)  # how many obs to be created
        for i in range(num_obs):
            milk.append(gamebox.from_color(random.randrange(20, 780), 0, 'white', 20, 20))

    if counter % 45 == 0:
        num_obs1 = random.randint(0, 4)
        for i in range(num_obs1):
            capri_sun.append(gamebox.from_color(random.randrange(20, 780), 0, 'red', 20, 20))

    camera.clear("black")

    camera.draw(background)
    camera.draw(slenderman)

    # moving slenderman

    if pygame.K_RIGHT in keys:
        slenderman.x += 5
    if pygame.K_LEFT in keys:
        slenderman.x -= 5
    if pygame.K_UP in keys:
        slenderman.y -= 5
    if pygame.K_DOWN in keys:
        slenderman.y += 5

    if slenderman.x > width:
        slenderman.x = 0
    if slenderman.x < 0:
        slenderman.x = width
    if slenderman.y > height:
        slenderman.y = 0
    if slenderman.y < 0:
        slenderman.y = height

    for m in milk:
        m.y += 1  # move the obstacle down
        camera.draw(m)

    for cs in capri_sun:
        cs.y += 1  # move the good stuff down
        camera.draw(cs)

    camera.draw(slenderman)

    # code to make power ups/obstacles go away when he touches and add/subtracts points

    for good in capri_sun:
        if slenderman.touches(good):
            capri_sun.remove(good)
            points += 1

    for lactose in milk:
        if slenderman.touches(lactose):
            milk.remove(lactose)
            points -= 1

    # this adds names

    names = str(' Priscilla Boateng ')
    to_draw.append(gamebox.from_text(400, 40, names, 25, 'white'))

    start = str('Use the arrow keys to get red Capri-Suns! Avoid the milk!')
    to_draw.append(gamebox.from_text(400, 60, start, 25, 'white'))

    # this creates and displays timer and health level (points)

    time = pygame.time.get_ticks()
    time_secs = int(time / 1000)
    to_draw.append(gamebox.from_text(80, 30, "Timer: " + str(time_secs), 40, 'white'))
    to_draw.append(gamebox.from_text(80, 50, "Health: " + str(points), 40, 'white'))

    # ends the game if the timer hits 60 and player hasn't gotten at least 20 points

    if time_secs >= 60 and points < 18 or points < 0:
        camera.clear('black')
        to_draw.append(gamebox.from_text(400, 300, "GAME OVER", 50, 'white'))
        to_draw.append(gamebox.from_text(80, 30, "Timer: " + str(time_secs), 40, 'black'))
        to_draw.append(gamebox.from_text(80, 50, "Health: " + str(points), 40, 'black'))

    # ends the game if the player gets 20 points (wins)

    elif points >= 18:
        camera.clear('black')
        to_draw.append(gamebox.from_text(400, 300, "You win! Thanks for power-up. Xoxo, Slenderman.", 30, 'white'))
        to_draw.append(gamebox.from_text(80, 30, "Timer: " + str(time_secs), 40, 'black'))
        to_draw.append(gamebox.from_text(80, 50, "Health: " + str(points), 40, 'black'))

    for i in to_draw:
        camera.draw(i)
    camera.display()


ticks_per_second = 30
gamebox.timer_loop(ticks_per_second, tick)