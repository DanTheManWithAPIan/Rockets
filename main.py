import itertools
import pygame
import random as rd

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_s,
    K_UP,
    K_DOWN,
    K_SPACE,
    K_r,
)

pygame.init()
width = 1280
height = 720
background_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
screen_rect = screen.get_rect()
center = ((screen.get_width() / 2), 50)
point_font = pygame.font.SysFont('arial', 40)
txt_font = pygame.font.SysFont('arial', 20)
intro_font = pygame.font.SysFont('arial', 100)
start_font = pygame.font.SysFont('arial', 60)

rocket = pygame.image.load("rocket.png")
rocket_rescaled = pygame.transform.scale(rocket, (70, 100))

background = pygame.image.load("background.png")
background_rescaled = pygame.transform.scale(background, (width, height))

laser = pygame.image.load("laser.png")
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (80, 100))

rock = pygame.image.load("rock.png")
rock_rescaled = pygame.transform.scale(rock, (70, 80))

point_bar = pygame.image.load("pointbar.png")
pb_rescaled = pygame.transform.scale(point_bar, (150, 50))

explosion1 = pygame.image.load("explosion1.png")
explosion2 = pygame.image.load("explosion2.png")
explosion3 = pygame.image.load("explosion3.png")
explosion1 = pygame.transform.scale(explosion1, (100, 105))
explosion2 = pygame.transform.scale(explosion2, (120, 127))
explosion3 = pygame.transform.scale(explosion3, (140, 150))



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
        self.x = rd.randint(0, width)
        self.y = rock_y
        self.width = rock_rescaled.get_width()
        self.height = rock_rescaled.get_height()
        self.vel = rd.randint(1, 5)
        self.chance = rd.uniform(0, 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

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
        self.x = player.x - 5
        self.y = player.y - 70
        self.width = laser_rescaled.get_width()
        self.height = laser_rescaled.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.vel = 40

    def display(self):
        self.rect.center = (self.x, self.y)
        return screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.y -= self.vel


player = Rocket()
laser = Laser()


def main():
    loser = False
    intro = True
    running = True
    point_count = 1
    level = 0
    objects = []
    laser_list = []
    start_ticks = pygame.time.get_ticks()
    time_elapsed_since_last_action = 0
    ending_timer = 0
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
        if pressed_key[K_LEFT] and not loser:
            if player.rect.x > screen_rect.left:
                player.x -= player.vel
        if pressed_key[K_RIGHT] and not loser:
            if player.rect.x < screen_rect.right - 70:
                player.x += player.vel
        if pressed_key[K_UP] and not loser:
            if player.y >= screen_rect.top + 500:
                player.y -= player.vel
        if pressed_key[K_DOWN] and not loser:
            if player.y <= screen_rect.bottom - 60:
                player.y += player.vel
        if pressed_key[K_s] and level == 0:
            rock_generator(30)
            intro = False
            level += 1

        # SCREEN AND PLAYER DISPLAY
        screen.blit(background_rescaled, (0, 0))
        if not loser:
            player.display()

        # LASER DISPLAY
        if not intro and not loser:
            if pressed_key[K_SPACE] and time_elapsed_since_last_action > 400:
                laser_shooter()
                time_elapsed_since_last_action = 0
            for obj in range(len(laser_list)):
                laser_list[obj].display()
                laser_list[obj].update()
                if laser_list[obj].y < -100:
                    laser_list.pop(obj)

        # HIT DETECTION FOR LASERS AND ROCKS and point counter
        if not intro and not loser:
            for rock in objects[:]:
                for laser in laser_list[:]:
                    if pygame.sprite.collide_rect(laser, rock):
                        objects.remove(rock)
                        laser_list.remove(laser)
                        point_count += 1

        # LEVELER MORE ROCKS EVERY 10 SECONDS
        if not intro and not loser:
            if seconds > 20 and level == 1:
                rock_generator(50)
                level += 1
            elif seconds > 40 and level == 2:
                rock_generator(70)
                level += 1
            elif seconds > 60 and level == 3:
                rock_generator(80)
                level += 1

        # ROCK DISPLAY
        if not intro and not loser:
            for obj in range(len(objects)):
                objects[obj].display()
                objects[obj].update()

        # HIT DETECTION FOR PLAYER AND ROCKS
        if not intro and not loser:
            for obj in range(len(objects)):
                rock_rect = pygame.Rect(objects[obj].x, objects[obj].y, objects[obj].width, objects[obj].height)
                player_rect = pygame.Rect(player.x + 10, player.y + 10, player.width - 10, player.height - 10)
                if pygame.Rect.colliderect(rock_rect, player_rect):
                    loser = True

        # Below is rendering my point box with points
        if not intro and not loser:
            screen.blit(pb_rescaled, (width - 162, 660))
            points = point_font.render(str(point_count), True, (255, 255, 255))
            total_points_txt = txt_font.render("POINTS:", True, (255, 255, 255))
            screen.blit(total_points_txt, (width - 150, 672))
            screen.blit(points, (width - 70, 662))

        # Below is rendering intro screen
        if intro:
            intro_txt = intro_font.render("Welcome to -ROCKETS-", True, (255, 255, 255))
            start_txt = start_font.render("Press -S- to start!", True, (255, 255, 255))
            screen.blit(intro_txt, (width - 1100, height - 600))
            screen.blit(start_txt, (width - 850, height - 450))

        if loser:
            ending_timer += ck
            if 2000 > ending_timer > 0:
                screen.blit(explosion1, (player.x - 30, player.y - 30))
            if ending_timer > 1000:
                loser_txt = intro_font.render("Well Played", True, (255, 255, 255))
                screen.blit(loser_txt, (width - 850, height - 600))
            if 3000 > ending_timer > 2000:
                screen.blit(explosion2, (player.x - 40, player.y - 40))
            if ending_timer > 3000:
                score_txt1 = intro_font.render("Score:", True, (255, 255, 255))
                score_txt2 = intro_font.render(str(point_count), True, (255, 255, 255))
                screen.blit(score_txt1, (width - 820, height - 500))
                screen.blit(score_txt2, (width - 510, height - 495))
                screen.blit(explosion3, (player.x - 50, player.y - 50))
            if ending_timer > 5000:
                exit_txt = txt_font.render("Press ESC to exit", True, (255, 255, 255))
                screen.blit(exit_txt, (width - 720, height - 200))
            if ending_timer > 10000 and loser:
                player.x = 10000
                player.y = 10000
            if pressed_key[K_r]:
                loser = False
        pygame.display.set_caption("ROCKETS")
        pygame.display.update()


main()
