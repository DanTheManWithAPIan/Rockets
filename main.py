import pygame
import random as rd

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_0,
)

pygame.init()
width = 1280
height = 720
background_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
center = ((screen.get_width() / 2), 50)
rocket = pygame.image.load("rocket.png")
rocket_rescaled = pygame.transform.scale(rocket, (70, 100))

background = pygame.image.load("background.png")
background_rescaled = pygame.transform.scale(background, (1280, 720))

laser = pygame.image.load("laser.png")
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (30, 40))

rock = pygame.image.load("rock.png")
rock_rescaled = pygame.transform.scale(rock, (100, 105))

class Rocket:
    def __init__(self, rocket_x=200, rocket_y=550, rocket_vel=10, rocket_image=rocket_rescaled):
        self.image = rocket_rescaled.get_rect().copy()
        self.rocket_x = rocket_x
        self.rocket_y = rocket_y
        self.rocket_vel = rocket_vel
        self.rocket_image = rocket_image

    def rocket_x(self):
        return self.rocket_x

    def rocket_y(self):
        return self.rocket_y

    def rocket_vel(self):
        return self.rocket_vel

    def rocket_image(self):
        return self.image


player = Rocket()


class Laser:
    def __init__(self, laser_x=player.rocket_x, laser_y=player.rocket_y, laser_vel=100):
        self.laser_x = laser_x
        self.laser_y = laser_y
        self.laser_vel = laser_vel

    def laser_x(self):
        return self.laser_x

    def laser_y(self):
        return self.laser_y

    def laser_vel(self):
        return self.laser_vel


laser = Laser()


class Rock:
    def __init__(self, rock_x=600, rock_y=0, rock_vel=5, image=rock_rescaled):
        self.image = image
        self.rock_x = rock_x
        self.rock_y = rock_y
        self.rock_vel = rock_vel

    def rock_x(self):
        return self.rock_x

    def rock_y(self):
        return self.rock_y

    def rock_vel(self):
        return self.rock_vel

    def rock_image(self):
        return self.image


def rock_generator(num_of_rocks=5):
    rock_list = []
    for rocks in range(num_of_rocks):
        rand_x = rd.randint(0, width)
        rock_list.append(rock_rescaled.get_rect(topleft=(rand_x, 0)).copy())
    return rock_list


rock1 = Rock(rock_vel=1)
rock2 = Rock(rock_vel=1)
rock3 = Rock(rock_vel=1)
rock4 = Rock(rock_vel=1)
rock5 = Rock(rock_vel=1)
rock_array = rock_generator()
rock_rect1 = rock_array[1]
rock_rect2 = rock_array[1]
rock_rect3 = rock_array[2]
rock_rect4 = rock_array[3]
rock_rect5 = rock_array[4]


def main(rocket_y=player.rocket_y, rocket_x=player.rocket_x, rock1_vel=rock1.rock_vel, rock2_vel=rock2.rock_vel,
         rock3_vel=rock3.rock_vel, rock4_vel=rock4.rock_vel, rock5_vel=rock5.rock_vel):
    running = True
    rock_count = 0
    while running:
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pressed_key[K_ESCAPE]:
                running = False
        if pressed_key[K_LEFT]:
            rocket_x -= player.rocket_vel
        if pressed_key[K_RIGHT]:
            rocket_x += player.rocket_vel

        screen.blit(background_rescaled, (0, 0))

        if rock_count < 5:
            screen.blit(rock1.rock_image(), rock_rect1)
            screen.blit(rock2.rock_image(), rock_rect2)
            screen.blit(rock3.rock_image(), rock_rect3)
            screen.blit(rock4.rock_image(), rock_rect4)
            screen.blit(rock5.rock_image(), rock_rect5)
            rock_rect1.move_ip(0, rock1_vel)
            rock_rect2.move_ip(0, rock2_vel)
            rock_rect3.move_ip(0, rock3_vel)
            rock_rect4.move_ip(0, rock4_vel)
            rock_rect5.move_ip(0, rock5_vel)

        screen.blit(player.rocket_image, (rocket_x, rocket_y))

        pygame.display.update()


main()
