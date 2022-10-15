import pygame
import random as rd

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_0,
    K_UP,
    K_DOWN,
    K_SPACE,
)

pygame.init()
width = 1280
height = 720
background_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
screen_rect = screen.get_rect()
center = ((screen.get_width() / 2), 50)
rocket = pygame.image.load("rocket.png")
rocket_rescaled = pygame.transform.scale(rocket, (70, 100))

background = pygame.image.load("background.png")
background_rescaled = pygame.transform.scale(background, (width, height))

laser = pygame.image.load("laser.png")
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (80, 100))

rock = pygame.image.load("rock.png")
rock_rescaled = pygame.transform.scale(rock, (70, 80))


class Rocket:
    def __init__(self, rocket_x=200, rocket_y=600, rocket_vel=10):
        super().__init__()
        self.x = rocket_x
        self.y = rocket_y
        self.width = rocket_rescaled.get_width()
        self.height = rocket_rescaled.get_height()
        self.vel = rocket_vel
        self.image = rocket_rescaled
        self.rect = self.image.get_rect()

    def display(self):
        self.rect.center = (self.x, self.y)
        return screen.blit(self.image, (self.rect.x, self.rect.y))

    def rocket_rect(self):
        rocket_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return rocket_rect


class Rock:
    def __init__(self, rock_y=-200):
        super().__init__()
        self.image = rock_rescaled
        self.rect = self.image.get_rect()
        self.x = rd.randint(0, width)
        self.y = rock_y
        self.width = rock_rescaled.get_width()
        self.height = rock_rescaled.get_height()
        self.vel = rd.randint(1, 5)
        self.chance = rd.uniform(0, 1)

    def update(self):
        self.y += self.vel
        if self.chance < .5:
            self.x -= self.vel
        if self.chance > .6:
            self.x += self.vel
        if self.y >= height + 10:
            self.y = -100
            self.x = rd.randint(0, width - 70)

    def display(self):
        self.rect.center = (self.x, self.y)
        return screen.blit(self.image, (self.rect.x, self.rect.y))


class Laser:
    def __init__(self):
        super().__init__()
        self.image = laser_rescaled
        self.rect = self.image.get_rect()
        self.x = player.x - 5
        self.y = player.y - 70
        self.width = laser_rescaled.get_width()
        self.height = laser_rescaled.get_height()
        self.vel = 40

    def display(self):
        self.rect.center = (self.x, self.y)
        return screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.y -= self.vel


player = Rocket()
laser = Laser()


def main():
    running = True
    point_count = 1
    level = 0
    objects = []
    start_ticks = pygame.time.get_ticks()
    laser_list = []
    time_elapsed_since_last_action = 0

    def rock_generator(x):
        for i in range(x):
            objects.append(Rock())

    def laser_shooter():
        laser_list.append(Laser())

    while running:
        ck = clock.tick(60)
        time_elapsed_since_last_action += ck
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        pressed_key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pressed_key[K_ESCAPE]:
                running = False
        if pressed_key[K_LEFT]:
            if player.rect.x > screen_rect.left:
                player.x -= player.vel
        if pressed_key[K_RIGHT]:
            if player.rect.x < screen_rect.right - 70:
                player.x += player.vel
        if pressed_key[K_UP]:
            if player.y >= screen_rect.top + 500:
                player.y -= player.vel
        if pressed_key[K_DOWN]:
            if player.y <= screen_rect.bottom - 60:
                player.y += player.vel
        if pressed_key[K_0] and level == 0:
            rock_count = 10
            rock_generator(rock_count)
            level += 1

        # SCREEN AND PLAYER DISPLAY
        screen.blit(background_rescaled, (0, 0))
        player.display()

        # LASER DISPLAY
        if pressed_key[K_SPACE] and time_elapsed_since_last_action > 100:
            laser_shooter()
            time_elapsed_since_last_action = 0
        for obj in range(len(laser_list)):
            laser_list[obj].display()
            laser_list[obj].update()
        for obj in range(len(laser_list)):
            laser_rect = pygame.Rect(laser_list[obj].x, laser_list[obj].y, laser_list[obj].width, laser_list[obj].height)
            rock_rect = pygame.Rect(objects[obj].x, objects[obj].y, objects[obj].width, objects[obj].height)
            if pygame.Rect.colliderect(rock_rect, laser_rect):
                objects[obj].pop


        # LEVELER MORE ROCKS EVERY 10 SECONDS
        if seconds >= 10 and level == 1:
            rock_count = 13
            rock_generator(rock_count)
            level += 1
        elif seconds >= 20 and level == 2:
            rock_count = 16
            rock_generator(rock_count)
            level += 1
        elif seconds >= 30 and level == 3:
            rock_count = 20
            rock_generator(rock_count)
            level += 1

        # ROCK DISPLAY
        if level >= 1:
            for obj in range(len(objects)):
                objects[obj].display()
                objects[obj].update()
        if level >= 1:
            for obj in range(len(objects)):
                if objects[obj].y == height + 5:
                    point_count += 1

        # HIT DETECTION
        for obj in range(len(objects)):
            rock_rect = pygame.Rect(objects[obj].x, objects[obj].y, objects[obj].width, objects[obj].height)
            player_rect = pygame.Rect(player.x + 10, player.y + 10, player.width - 10, player.height - 10)
            if pygame.Rect.colliderect(rock_rect, player_rect):
                running = False

        pygame.display.set_caption("POINT COUNT " + str(point_count))
        pygame.display.update()


main()
