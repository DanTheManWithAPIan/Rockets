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
    def __init__(self, rocket_x=200, rocket_y=550, rocket_vel=10, hit_points=1):
        self.rocket_x = rocket_x
        self.rocket_y = rocket_y
        self.rocket_vel = rocket_vel
        self.hit_points = hit_points

    def rocket_x(self):
        return self.rocket_x

    def rocket_y(self):
        return self.rocket_y

    def rocket_vel(self):
        return self.rocket_vel

    def hit_points(self):
        return self.hit_points

    def hit(self):
        self.hit_points -= 1


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
    def __init__(self, rock_x=600, rock_y=0, rock_vel=5):
        self.rock_x = rock_x
        self.rock_y = rock_y
        self.rock_vel = rock_vel

    def rock_x(self):
        return self.rock_x

    def rock_y(self):
        return self.rock_y

    def rock_vel(self):
        return self.rock_vel


rock = Rock()


def main(rocket_y=player.rocket_y, rocket_x=player.rocket_x, rock_y=rock.rock_y, rock_x=rock.rock_x,
         rock_vel=rock.rock_vel):
    running = True
    while running:
        pressed_key = pygame.key.get_pressed()
        pygame.display.flip()
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
        screen.blit(rock_rescaled, (rock_x, rock_y))
        screen.blit(rocket_rescaled, (rocket_x, rocket_y))

        if pressed_key[K_0]:
            while rock_y <= 720:
                rock_y += rock.rock_vel
                pygame.display.update()

        pygame.display.update()


main()
