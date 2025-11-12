import os
import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()
    dt = 0

    os.environ['SDL_VIDEOCENTERED'] = '1'
    info = pygame.display.Info()
    monitor_width, monitor_height = info.current_w, info.current_h

    resolution = (monitor_width, monitor_height)
    screen = pygame.display.set_mode(resolution)

    running = True



if __name__ == "__main__":
    main()