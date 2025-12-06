import os
import pygame

class Player():

    def __init__(self, resolution, size = (40, 40), speed = 5):
        self.screen_res = resolution
        self.player_x = 400
        self.player_y = 610
        self.dx = 0
        self.dy = 0
        self.width = size[0]
        self.height = size[1]
        self.gravity = 0
        self.size = size
        self.speed = speed
        self.player_index = 0
        self.character_list = self.create_character()
        self.rect = self.character_list[0].get_rect()
        self.jumped = False
        self.dead = False
        self.win = False

    def create_character(self):
        character_list = []
        for img in range(1, 9):
            character =  pygame.image.load(f"art/character/Calci_Sprite-{img}.png")
            character_list.append(character)
        return character_list

    def update(self, screen, world):
        self.animate_player()
        screen.blit(self.character_list[int(self.player_index)], (self.player_x, self.player_y))
        self.rect.topleft = (self.player_pos())

        self.get_player_movement()
        self.detect_collision(world)
        self.detect_checkpoint_collision(world)
            
        self.player_x += self.dx
        self.player_y += self.dy

        self.is_player_offscreen()

    def animate_player(self):
        self.player_index += 0.1
        if self.player_index >= len(self.character_list):
            self.player_index = 0

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

        
    def detect_checkpoint_collision(self, world):
        for point in world.checkpoint_list:
            if point[1].colliderect(self.rect):
                self.win = True

    def is_player_offscreen(self):
        if self.player_y > self.screen_res[1] + 10:
            self.dead = True
        else:
            pass


class Platform():

    def __init__(self, size = (), pos = ()):
        self.size = size
        self.pos = pos
        self.platform = self.create_platform()
        self.rect = self.create_bounding_box()


    def update(self, screen):
        screen.blit(self.platform, self.pos)


    def create_platform(self):
        if self.size == (152, 75):
            platform = pygame.image.load('art/fotl_platform_large.png').convert_alpha()
        if self.size == (110, 50):
            platform = pygame.image.load('art/fotl_platform_medium.png').convert_alpha()
        if self.size == (50, 25):
            platform = pygame.image.load('art/fotl_platform_small.png').convert_alpha()
        return platform
    

    def create_bounding_box(self):
        height_adjustment = self.size[1] - 2
        if self.size == (152, 75):
            height_adjustment = self.size[1] - 22
        bounding_box = pygame.Rect(self.pos[0], self.pos[1] + 2, self.size[0], height_adjustment)
        return bounding_box

class Checkpoint():
    def __init__(self,size = (), pos = ()):
        self.pos = pos
        self.size = size
        self.checkpoint = self.create_checkpoint()
        self.rect = self.create_bounding_box()

    def create_checkpoint(self):
        image = pygame.image.load('art/fotl_checkpoint.png').convert_alpha()
        return image
    
    def create_bounding_box(self):
        centered_x = self.pos[0] + 25
        bounding_box = pygame.Rect(centered_x, self.pos[1], self.size[0], self.size[1])
        return bounding_box
    
    def update(self, screen):
        screen.blit(self.checkpoint, (self.pos))

class World():
    def __init__(self):
        self.platforms_list = []
        self.checkpoint_list = []

    def generate_level_1(self):
        #create platforms
        platform_params = [{"size": (110, 50), "pos": (175, 500)},
                                {"size": (50, 25), "pos": (300, 600)},
                                {"size": (50, 25), "pos": (200, 400)},
                                {"size": (110, 50), "pos": (350, 650)},
                                {"size": (110, 50), "pos": (460, 650)},
                                {"size": (152, 75), "pos": (650, 550)},
                                {"size": (50, 25), "pos": (935, 705)},
                                {"size": (50, 25), "pos": (1000, 480)},
                                {"size": (50, 25), "pos": (1150, 480)},
                                {"size": (50, 25), "pos": (1245, 400)},
                                {"size": (110, 50), "pos": (1050, 310)},
                                {"size": (50, 25), "pos": (930, 260)},
                                {"size": (152, 75), "pos": (590, 300)},
                                {"size": (152, 75), "pos": (495, 300)}]
        for param_pair in platform_params:
            platform = Platform(size = param_pair["size"], pos = param_pair["pos"])
            self.platforms_list.append([platform, platform.rect])

        #create checkpoint
        checkpoint_params = [{"size": (15, 65), "pos": (515, 237)}]
        for params in checkpoint_params:
            checkpoint = Checkpoint(size = params["size"], pos = params["pos"])
            self.checkpoint_list.append([checkpoint, checkpoint.rect])

    def draw_world(self, screen):
        background = pygame.image.load('art/fotl_background.png').convert_alpha()
        screen.blit(background, (0,0))
        for platform in self.platforms_list:
            platform[0].update(screen)
        for checkpoint in self.checkpoint_list:
            checkpoint[0].update(screen)

def draw_text(screen, text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def main():
    pygame.init()
    pygame.display.set_caption("Flames of the Lost")
    clock = pygame.time.Clock()
    game_active = True

    #os.environ['SDL_VIDEOCENTERED'] = '1'
    #info = pygame.display.Info()
    #monitor_width, monitor_height = info.current_w, info.current_h
    #resolution = (monitor_width, monitor_height)
    resolution = (1536, 864)
    screen = pygame.display.set_mode(resolution)
    text_font_large = pygame.font.SysFont("Arial", 75)
    text_font_italics = pygame.font.SysFont("Arial", 75, italic=True)
    text_font_small = pygame.font.SysFont("Arial", 30)

    player = Player(resolution)
    world = World()
    world.generate_level_1()

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
                world.generate_level_1()
                game_active = True

        if game_active == True:
            world.draw_world(screen)
            player.update(screen, world)
            if player.dead == True:
                game_active = False
            if player.win == True:
                game_active = False

        elif game_active == False and player.win == True:
            transparent_surf = pygame.Surface(resolution)
            transparent_surf.fill((0, 0, 0))
            transparent_surf.set_alpha(10)
            screen.blit(transparent_surf, (0, 0))
            draw_text(screen, "Thanks for playing this demo of:", text_font_small, (82, 179, 143), 630, 325)
            draw_text(screen, "Flames of the Lost", text_font_italics, (222, 178, 91), 550, 375)
            draw_text(screen, "Press 'R' to restart," , text_font_small, (82, 179, 143), 700, 480)
            draw_text(screen, "or 'Esc' to quit" , text_font_small, (82, 179, 143), 725, 515)
            draw_text(screen, "created by: M. Knutson" , text_font_small, (82, 179, 143), 670, 575)

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