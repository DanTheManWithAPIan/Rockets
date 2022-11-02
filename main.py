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
pygame.display.set_caption("ROCKETS")
width = 1280
height = 720
background_color = (255, 255, 255)
clock = pygame.time.Clock()
screen = pygame.display.set_mode([width, height])
screen_rect = screen.get_rect()
center = ((screen.get_width() / 2), 50)
point_font = pygame.font.SysFont('Showcard Gothic', 40)
txt_font = pygame.font.SysFont('Showcard Gothic', 20)
intro_font = pygame.font.SysFont('Showcard Gothic', 100)
start_font = pygame.font.SysFont('Showcard Gothic', 60)

rocket = pygame.image.load("images/rocket.png").convert_alpha()
rocket_rescaled = pygame.transform.scale(rocket, (70, 100))

background = pygame.image.load("images/background.png").convert_alpha()
background_rescaled = pygame.transform.scale(background, (width, height))

laser = pygame.image.load("images/laser.png").convert_alpha()
laser = pygame.transform.rotate(laser, 90)
laser_rescaled = pygame.transform.scale(laser, (80, 100))

rock = pygame.image.load("images/rock.png").convert_alpha()
rock_rescaled_sm = pygame.transform.scale(rock, (70, 80))
rock_rescaled_md = pygame.transform.scale(rock, (100, 110))

point_bar = pygame.image.load("images/pointbar.png").convert_alpha()
pb_rescaled = pygame.transform.scale(point_bar, (170, 60))

explosion1 = pygame.image.load("images/explosion1.png").convert_alpha()
explosion2 = pygame.image.load("images/explosion2.png").convert_alpha()
explosion3 = pygame.image.load("images/explosion3.png").convert_alpha()
explosion4 = pygame.image.load("images/explosion4.png").convert_alpha()
explosion5 = pygame.image.load("images/explosion5.png").convert_alpha()
explosion6 = pygame.image.load("images/explosion6.png").convert_alpha()
explosion1 = pygame.transform.scale(explosion1, (100, 105))
explosion2 = pygame.transform.scale(explosion2, (120, 127))
explosion3 = pygame.transform.scale(explosion3, (140, 150))
explosion4 = pygame.transform.scale(explosion4, (130, 140))
explosion5 = pygame.transform.scale(explosion5, (120, 127))
explosion6 = pygame.transform.scale(explosion6, (100, 105))


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
        self.image = rd.choice([rock_rescaled_sm, rock_rescaled_md])
        self.x = rd.randint(0, width)
        self.y = rock_y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel = rd.randint(1, 5)
        self.chance = rd.uniform(0, 1)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.y += self.vel
        if self.chance < .4:
            self.x -= self.vel
        if self.chance > .7:
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
    winner = False
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
    level2 = True
    level3 = True
    level4 = True
    level5 = True

    def rock_generator(x):
        for i in range(x):
            objects.append(Rock())

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
        # Movement inputs below
        if not loser:
            if pressed_key[K_LEFT] and player.rect.x > screen_rect.left:
                player.x -= player.vel
            if pressed_key[K_RIGHT] and player.rect.x <= screen_rect.right - 70:
                player.x += player.vel
            if pressed_key[K_UP] and player.y >= screen_rect.top + 500:
                player.y -= player.vel
            if pressed_key[K_DOWN] and player.y <= screen_rect.bottom - 60:
                player.y += player.vel
            if pressed_key[K_s] and level == 0:
                rock_generator(20)
                intro = False
                level += 1

        # SCREEN AND PLAYER DISPLAY
        screen.blit(background_rescaled, (0, 0))
        if not loser:
            player.display()

        # LASER DISPLAY
        if not intro and not loser and not winner:
            if pressed_key[K_SPACE] and time_elapsed_since_last_action > 400:
                laser_list.append(Laser())
                time_elapsed_since_last_action = 0
            for obj in range(len(laser_list)):
                laser_list[obj].display()
                laser_list[obj].update()
                if laser_list[obj].y < -100:
                    laser_list.pop(obj)

        # HIT DETECTION FOR LASERS AND ROCKS and point counter
        if not intro and not loser and not winner:
            for rock in objects[:]:
                for laser in laser_list[:]:
                    if pygame.sprite.collide_rect(laser, rock):
                        objects.remove(rock)
                        laser_list.remove(laser)
                        point_count += 1

        # If rocks get to 10 then spawn next level if rocks get to 1 you win
        if len(objects) == 10:
            level += 1
        if len(objects) == 1:
            winner = True

        # Game leveler 5 levels
        if not intro and not loser and not winner:
            if level == 2 and level2:
                rock_generator(20)
                level2 = False
            elif level == 3 and level3:
                rock_generator(40)
                level3 = False
            elif level == 4 and level4:
                rock_generator(50)
                level4 = False
            elif level == 5 and level5:
                rock_generator(60)
                level5 = False

        # HIT DETECTION FOR PLAYER AND ROCKS
        if not intro and not loser and not winner:
            for obj in range(len(objects)):
                objects[obj].display()
                objects[obj].update()
                rock_rect = pygame.Rect(objects[obj].x, objects[obj].y, objects[obj].width, objects[obj].height)
                player_rect = pygame.Rect(player.x + 10, player.y + 10, player.width - 10, player.height - 10)
                if pygame.Rect.colliderect(rock_rect, player_rect):
                    loser = True

        # Below is rendering my point box with points
        if not intro and not loser and not winner:
            screen.blit(pb_rescaled, (width - 180, 650))
            points = point_font.render(str(point_count), True, (255, 255, 255))
            total_points_txt = txt_font.render("POINTS:", True, (255, 255, 255))
            screen.blit(total_points_txt, (width - 165, 673))
            screen.blit(points, (width - 80, 665))

        # Below is rendering intro screen
        if intro:
            intro_txt = intro_font.render("Welcome to ROCKETS", True, (255, 255, 255))
            start_txt = start_font.render("Press -S- to start!", True, (255, 255, 255))
            screen.blit(intro_txt, (width - 1190, height - 600))
            screen.blit(start_txt, (width - 925, height - 450))

        # Below is loser end screen
        if loser and not intro and not winner:
            ending_timer += ck
            if 2000 > ending_timer > 0:
                screen.blit(explosion1, (player.x - 30, player.y - 30))
            if ending_timer > 1000:
                loser_txt = intro_font.render("Well Played", True, (255, 255, 255))
                screen.blit(loser_txt, (width - 980, height - 600))
            if 3500 > ending_timer > 2000:
                screen.blit(explosion2, (player.x - 40, player.y - 40))
            if ending_timer > 3000:
                score_txt1 = intro_font.render("Score:", True, (255, 255, 255))
                score_txt2 = intro_font.render(str(point_count), True, (255, 255, 255))
                screen.blit(score_txt1, (width - 860, height - 500))
                screen.blit(score_txt2, (width - 500, height - 495))
            if 5000 > ending_timer > 3500:
                screen.blit(explosion3, (player.x - 50, player.y - 50))
            if ending_timer > 5000:
                exit_txt = txt_font.render("Press ESC to exit or R to restart", True, (255, 255, 255))
                screen.blit(exit_txt, (width - 835, height - 200))
            if 6500 > ending_timer > 5000:
                screen.blit(explosion4, (player.x - 50, player.y - 50))
            if 8000 > ending_timer > 6500:
                screen.blit(explosion5, (player.x - 50, player.y - 50))
            if 9500 > ending_timer > 8000:
                screen.blit(explosion6, (player.x - 50, player.y - 50))
            if ending_timer > 9500:
                player.x = 10000
                player.y = 10000
            if pressed_key[K_r]:
                objects.clear()
                level = 1
                point_count = 0
                ending_timer = 0
                player.x = 400
                player.y = 600
                rock_generator(20)
                loser = False
        # Below is winner end screen
        if winner and not intro:
            objects.clear()
            ending_timer += ck
            if ending_timer > 1000:
                winner_txt = intro_font.render("YOU WIN!", True, (255, 255, 255))
                screen.blit(winner_txt, (width - 850, height - 600))
            if ending_timer > 3000:
                score_txt1 = intro_font.render("Score:", True, (255, 255, 255))
                score_txt2 = intro_font.render(str(point_count), True, (255, 255, 255))
                screen.blit(score_txt1, (width - 860, height - 500))
                screen.blit(score_txt2, (width - 510, height - 495))
            if ending_timer > 5000:
                exit_txt = txt_font.render("Press ESC to exit", True, (255, 255, 255))
                screen.blit(exit_txt, (width - 750, height - 200))

        pygame.display.update()


main()
