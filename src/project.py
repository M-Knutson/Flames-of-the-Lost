import os
import pygame

class Player():

    def __init__(self, character, resolution, size = (50, 50), speed = 5):
        self.character = character
        self.player_x = resolution[0] // 2
        self.player_y = resolution[1] // 2
        self.size = size
        self.speed = speed
        
    def update(self):
        pass

    def player_pos(self) -> tuple:
        return (self.player_x, self.player_y)

    def player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_x -= self.speed

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()

    os.environ['SDL_VIDEOCENTERED'] = '1'
    info = pygame.display.Info()
    monitor_width, monitor_height = info.current_w, info.current_h
    resolution = (monitor_width - 50, monitor_height - 50)
    screen = pygame.display.set_mode(resolution)

    #player_x = monitor_width // 2
    #player_y = monitor_height // 2
    player_size = 50
    character = pygame.Surface((player_size, player_size))
    character.fill((219, 129, 96))
    player = Player(character, resolution, size=player_size)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        green = pygame.Color(82, 179, 143)
        screen.fill(green)

        player.player_movement()
        screen.blit(player.character, (player.player_x, player.player_y))

        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    main()