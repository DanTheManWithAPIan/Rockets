import pygame
import main


def outro_scene(width, height, intro_font, txt_font, screen, point_count):
    ending_timer = 0
    ck = pygame.clock.tick()
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
