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

background = pygame.image.load("bg.png")
background_rescaled = pygame.transform.scale(background, (width, height))

laser = pygame.image.load("laser.png")
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (30, 40))

rock = pygame.image.load("rock.png")
rock_rescaled = pygame.transform.scale(rock, (100, 105))


class Rocket:
    def __init__(self, rocket_x=200, rocket_y=550, rocket_vel=10):
        super().__init__()
        self.x = rocket_x
        self.y = rocket_y
        self.width = rocket_rescaled.get_width()
        self.height = rocket_rescaled.get_height()
        self.vel = rocket_vel
        self.image = rocket_rescaled

    def display(self):
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        return screen.blit(self.image, (rect.x, rect.y))


player = Rocket()


class Laser:
    def __init__(self, laser_x=player.x, laser_y=player.y, laser_vel=100):
        self.laser_x = laser_x
        self.laser_y = laser_y
        self.laser_vel = laser_vel


laser = Laser()


class Rock:
    def __init__(self, rock_y=-100, rock_vel=5, image=rock_rescaled):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = rd.randint(0, width)
        self.y = rock_y
        self.width = rock_rescaled.get_width()
        self.height = rock_rescaled.get_height()
        self.vel = rock_vel

    def update(self):
        self.y += self.vel
        if self.y >= height + 10:
            self.y = -100
            self.x = rd.randint(0, width-70)

    def display(self):
        rect = self.image.get_rect()
        rect.center = (self.x, self.y)
        return screen.blit(self.image, (rect.x, rect.y))

    def hit_box(self):
        return self.x, self.y, self.width, self.height


objects = []


def rock_generator():
    for i in range(20):
        objects.append(Rock())


rock_generator()


def main():
    running = True
    point_count = 0
    while running:
        clock.tick(60)
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pressed_key[K_ESCAPE]:
                running = False
        if pressed_key[K_LEFT]:
            if player.x >= 50:
                player.x -= player.vel
        if pressed_key[K_RIGHT]:
            if player.x <= width - 50:
                player.x += player.vel

        screen.blit(background_rescaled, (0, 0))
        player.display()

        for obj in range(len(objects)):
            objects[obj].display()
            objects[obj].update()

        if objects[0].y == height + 5:
            point_count += 1

        pygame.display.set_caption(str(point_count))

        pygame.display.update()


main()
