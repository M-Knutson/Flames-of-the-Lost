import os
import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()

    os.environ['SDL_VIDEOCENTERED'] = '1'
    info = pygame.display.Info()
    monitor_width, monitor_height = info.current_w, info.current_h
    resolution = (monitor_width - 50, monitor_height - 50)
    screen = pygame.display.set_mode(resolution)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        green = pygame.Color(82, 179, 143)
        screen.fill(green)
        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    main()