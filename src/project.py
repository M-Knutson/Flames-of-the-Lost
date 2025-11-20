import os
import pygame

class Player():

    def __init__(self, resolution, size = (50, 50), speed = 5):
        self.player_x = resolution[0] // 2
        self.player_y = resolution[1] // 2
        self.dx = self.player_x
        self.dy = self.player_y
        self.gravity = 0
        self.size = size
        self.speed = speed
        self.character = self.create_character()
        self.rect = self.character.get_rect()
        self.jumped = False

    def create_character(self):
        character = pygame.Surface(self.size)
        character.fill((219, 129, 96))
        return character

    def update(self, screen, world, resolution):
        # draw character & bounding box
        screen.blit(self.character, (self.player_x, self.player_y))
        self.rect.topleft = (self.player_pos())
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        self.get_player_movement(resolution)

        #check for collision
        #for platform in world.platform_list:
            #if platform[1].colliderect(self.rect):
                #if self.player_y >=

        if self.dy > resolution[1] // 2:
            self.dy = resolution[1] // 2
            if self.jumped == True:
                self.jumped = False
        self.player_x = self.dx
        self.player_y = self.dy


    def player_pos(self) -> tuple[int, int]:
        return (self.player_x, self.player_y)


    def get_player_movement(self, resolution):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.dx -= self.speed
        if keys[pygame.K_d]:
            self.dx += self.speed
        # jumping & gravity
        if (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.jumped == False:
            if self.gravity > 0:
                self.gravity = -5
            self.gravity -= 1
            if self.gravity < -13:
                self.jumped = True
        if not (keys[pygame.K_SPACE] or keys[pygame.K_w]) and self.jumped == False:
            if self.gravity < 0:
                self.jumped = True
        if self.jumped == True:
            self.gravity += 1
        if self.gravity > 10:
            self.gravity = 10
        self.dy += self.gravity


class Platform():

    def __init__(self, size = (), pos = ()):
        #self.tile_list = []
        self.size = size
        self.pos = pos
        self.platform = self.create_platform()
        self.rect = self.platform.get_rect()

    def update(self, screen):
        screen.blit(self.platform, self.pos)
        self.rect.topleft = (self.pos)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

    def create_platform(self):
        platform = pygame.Surface(self.size)
        platform.fill((38, 110, 80))
        #self.tile_list.append(platform)
        return platform

class World():
    def __init__(self):
        self.platforms_list = []

    def generate_level_1(self, screen, resolution):
        #create background
        green = pygame.Color(82, 179, 143)
        screen.fill(green)
        #create platforms
        platform_1 = Platform(size = (100, 50), 
                              pos = ((resolution[0] // 2), (resolution[1] // 2) + 50))
        self.platforms_list.append([platform_1, platform_1.rect])
        for platform in self.platforms_list:
            platform[0].update(screen)

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()

    os.environ['SDL_VIDEOCENTERED'] = '1'
    info = pygame.display.Info()
    monitor_width, monitor_height = info.current_w, info.current_h
    resolution = (monitor_width, monitor_height)
    screen = pygame.display.set_mode(resolution)

    player = Player(resolution)
    world = World()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        world.generate_level_1(screen, resolution)

        player.update(screen, world, resolution)

        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    main()