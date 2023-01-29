import main


def intro_scene(screen, start_font, intro_font, width, height):
    intro_txt = intro_font.render("Welcome to ROCKETS", True, (255, 255, 255))
    start_txt = start_font.render("Press -S- to start!", True, (255, 255, 255))
    screen.blit(intro_txt, (width - 1190, height - 600))
    screen.blit(start_txt, (width - 925, height - 450))
