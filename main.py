import pygame, sys, random, math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
width = 1280
height = 720
background_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
center = ((screen.get_width() / 2), 50)
rocket = pygame.image.load("rocket.png")
background = pygame.image.load("background.png")
rocket_rescaled = pygame.transform.scale(rocket, (70, 100))
background_rescaled = pygame.transform.scale(background, (1280, 720))
laser = pygame.image.load("laser.png")
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (30, 40))


class Rocket:
    def __init__(self, rocket_x=200, rocket_y=550, rocket_vel=100):
        self.rocket_x = rocket_x
        self.rocket_y = rocket_y
        self.rocket_vel = rocket_vel

    def rocket_x(self):
        return self.rocket_x

    def rocket_y(self):
        return self.rocket_y

    def rocket_vel(self):
        return self.rocket_vel


Player = Rocket()


class Laser:
    def __init__(self, laser_x=Player.rocket_x, laser_y=Player.rocket_y, laser_vel=100):
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


def main(rocket_y=Player.rocket_y, rocket_x=Player.rocket_x, laser_x=laser.laser_x, laser_y=laser.laser_y):
    global player
    running = True
    while running:
        print(laser_y)
        pressed_key = pygame.key.get_pressed()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pressed_key[K_ESCAPE]:
                running = False
            if pressed_key[K_LEFT]:
                if player.x != 0:
                    rocket_x -= Player.rocket_vel
            if pressed_key[K_RIGHT]:
                if player.x != width - 80:
                    rocket_x += Player.rocket_vel
        screen.blit(background_rescaled, (0, 0))
        screen.blit(rocket_rescaled, (rocket_x, rocket_y))
        if pressed_key[K_SPACE]:
            screen.blit(laser_rescaled, (laser_x, laser_y))
            pygame.display.update()
            if laser_y != 1000:
                for i in range(2):
                    laser_y -= 10
            screen.blit(laser_rescaled, (laser_x, laser_y))
            pygame.display.update()
        pygame.display.update()


main()
