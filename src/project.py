import os
import pygame

class Player():

    def __init__(self, resolution, size = (40, 40), speed = 5):
        self.screen_res = resolution
        self.player_x = resolution[0] // 2
        self.player_y = resolution[1] // 2
        self.dx = 0
        self.dy = 0
        self.width = size[0]
        self.height = size[1]
        self.gravity = 0
        self.size = size
        self.speed = speed
        self.character = self.create_character()
        self.rect = self.character.get_rect()
        self.jumped = False
        self.dead = False

    def create_character(self):
        character = pygame.Surface(self.size)
        character.fill((219, 129, 96))
        return character

    def update(self, screen, world, resolution):
        # draw character & bounding box
        screen.blit(self.character, (self.player_x, self.player_y))
        self.rect.topleft = (self.player_pos())
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        self.get_player_movement()
        self.detect_collision(world)
            
        self.player_x += self.dx
        self.player_y += self.dy

        if self.player_y > resolution[1] + 50:
            self.player_y = resolution[1] + 50
            if self.jumped == True:
                    self.jumped = False

        self.player_is_offscreen()
        if self.dead == True:
            print("You died.")


    def player_pos(self) -> tuple[int, int]:
        return (self.player_x, self.player_y)


    def get_player_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.dx = -self.speed
        elif keys[pygame.K_d]:
            self.dx = self.speed
        else:
            self.dx = 0
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
            self.activate_gravity()
        self.dy = self.gravity


    def activate_gravity(self):
        self.gravity += 1
        if self.gravity > 10:
            self.gravity = 10

    def detect_collision(self, world):
        #check for collision
        for platform in world.platforms_list:
            # check for y collision
            if platform[1].colliderect(self.rect.x, self.rect.y + self.dy, 
                                       self.width, self.height):
                # check for jumping collision
                if self.gravity < 0:
                    self.jumped = True
                    self.dy = platform[1].bottom - self.rect.top
                    self.gravity = 0
                    self.activate_gravity()
                # check for falling collision
                elif self.gravity > 0:
                    self.dy = platform[1].top - self.rect.bottom
                    self.jumped = False
            # check for x collision
            if platform[1].colliderect(self.rect.x + self.dx, self.rect.y, 
                                       self.width, self.height):
                self.dx = 0

    def player_is_offscreen(self):
        if self.player_y > self.screen_res[1] + 10:
            self.dead = True
        else:
            pass


class Platform():

    def __init__(self, size = (), pos = ()):
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
        return platform

class World():
    def __init__(self):
        self.platforms_list = []
        self.platform_params = [{"size": (100, 50), "pos": (618, 432)},
                                {"size": (50, 25), "pos": (750, 300)}]

    def generate_level_1(self, screen, resolution):
        #create background
        green = pygame.Color(82, 179, 143)
        screen.fill(green)
        #create platforms
        for param_pair in self.platform_params:
            platform = Platform(size = param_pair["size"], pos = param_pair["pos"])
            self.platforms_list.append([platform, platform.rect])
             
        for platform in self.platforms_list:
            platform[0].update(screen)

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()
    game_active = True

    os.environ['SDL_VIDEOCENTERED'] = '1'
    info = pygame.display.Info()
    monitor_width, monitor_height = info.current_w, info.current_h
    resolution = (monitor_width, monitor_height)
    screen = pygame.display.set_mode(resolution)
    text_font_large = pygame.font.SysFont("Arial", 75)
    text_font_small = pygame.font.SysFont("Arial", 30)

    player = Player(resolution)
    world = World()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                
            if game_active == False and (event.type == pygame.KEYDOWN 
                                         and event.key == pygame.K_r):
                player = Player(resolution)
                world = World()
                game_active = True

        if game_active == True:
            world.generate_level_1(screen, resolution)
            player.update(screen, world, resolution)
            if player.dead == True:
                game_active = False

        else:
            transparent_surf = pygame.Surface(resolution)
            transparent_surf.fill((0, 0, 0))
            transparent_surf.set_alpha((10))
            screen.blit(transparent_surf, (0, 0))
            draw_text(screen, "You Died" , text_font_large, (170, 20, 10), 675, 350)
            draw_text(screen, "Press 'R' to restart," , text_font_small, (170, 20, 10), 700, 440)
            draw_text(screen, "or 'Esc' to quit" , text_font_small, (170, 20, 10), 725, 475)

        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    main()