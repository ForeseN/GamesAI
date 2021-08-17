import pygame
import os
import random
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()

# Global Constants
HEIGHT = 600
WIDTH = 1100
FPS = 60
WHITE = (255, 255, 255)
BIRD_HEIGHTS = [210, 245]
FONT = pygame.font.SysFont('comicsans', 50)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

RUNNING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoRun1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoRun2.png'))]

JUMPING = pygame.image.load(os.path.join('Assets/Dino', 'DinoJump.png'))
DUCKING = [pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck1.png')),
           pygame.image.load(os.path.join('Assets/Dino', 'DinoDuck2.png'))]

SMALL_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus1.png')), pygame.image.load(
    os.path.join('Assets/Cactus', 'SmallCactus2.png')), pygame.image.load(os.path.join('Assets/Cactus', 'SmallCactus3.png'))]

LARGE_CACTUS = [pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus1.png')), pygame.image.load(
    os.path.join('Assets/Cactus', 'LargeCactus2.png')), pygame.image.load(os.path.join('Assets/Cactus', 'LargeCactus3.png'))]

BIRD_OG = [pygame.image.load(os.path.join('Assets/Bird', 'Bird1.png')),
           pygame.image.load(os.path.join('Assets/Bird', 'Bird2.png'))]

CLOUD = pygame.image.load(os.path.join('Assets/Other', 'Cloud.png'))

BG = pygame.image.load(os.path.join('Assets/Other', 'Track.png'))
DEAD_DINO = pygame.image.load(os.path.join('Assets/Dino', 'DinoDead.png'))

BIRD_IMG_1 = pygame.image.load(os.path.join('Assets/Bird', 'Bird1.png'))
BIRD_IMG_2 = pygame.image.load(os.path.join('Assets/Bird', 'Bird2.png'))

BIRD_IMG_1_SCALED = pygame.transform.scale(BIRD_IMG_1, (110, 130))
BIRD_IMG_2_SCALED = pygame.transform.scale(BIRD_IMG_2, (110, 130))

BIRD = [BIRD_IMG_1_SCALED, BIRD_IMG_2_SCALED]


def collide(obj1, obj2):
    offset_x = int(obj2.x) - int(obj1.x)
    offset_y = int(obj2.y) - int(obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_HEIGHT = 165
    JUMP_VEL_MULTIPLIER = 3
    JUMP_DISTANCE = 1.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.ACCELARATION = 0
        self.y_vel = self.JUMP_VEL_MULTIPLIER
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.mask = pygame.mask.from_surface(self.run_img[0])
        self.x = 80
        self.y = self.dino_rect.y

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.ACCELARATION = ((
                (game_speed**2) * (self.JUMP_DISTANCE**2))/2/self.JUMP_HEIGHT)**(1/3)
            self.y_vel = game_speed * self.JUMP_DISTANCE/self.ACCELARATION
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not(self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.y = self.Y_POS
        self.step_index += 1

    def jump(self):

        self.image = self.jump_img
        self.dino_rect.y -= self.y_vel
        self.y -= self.y_vel
        self.y_vel -= self.ACCELARATION
        if self.dino_rect.y >= self.Y_POS:
            self.dino_jump = False
            self.dino_rect.y = self.Y_POS
            self.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

    def collision(self, obj):
        return collide(self, obj)


class Cloud:

    def __init__(self):
        self.x = WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < - self.width:
            self.x = WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = WIDTH
        self.x = WIDTH

    def update(self):
        self.rect.x -= game_speed
        self.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def collision(self, obj):
        return collide(self, obj)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.y = 325
        self.mask = pygame.mask.from_surface(self.image[0])


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
        self.y = 300
        self.mask = pygame.mask.from_surface(self.image[0])


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice(BIRD_HEIGHTS)
        self.index = 0
        self.y = self.rect.y
        self.mask = pygame.mask.from_surface(self.image[0])

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        SCREEN.blit(self.image[self.index//10], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, score, obstacles
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 10
    x_pos_bg = 0
    y_pos_bg = 380
    score = 0
    obstacles = []
    death_count = 0

    def Score():
        global score, game_speed
        score += 0.5
        if score % 100 == 0:
            game_speed += 1

        score_text = FONT.render('' + str(round(score)), 1, (255, 255, 255))
        WIN.blit(score_text, (WIDTH-score_text.get_width()-10, 10))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        WIN.blit(BG, (x_pos_bg, y_pos_bg))
        WIN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            WIN.blit(BG, (image_width+x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.QUIT()

        WIN.fill((0, 0, 0))
        background()
        Score()

        cloud.draw(WIN)
        cloud.update()
        userInput = pygame.key.get_pressed()

        player.draw(WIN)
        player.update(userInput)
        # pygame.draw.rect(WIN, (255, 0, 0), player.dino_rect, 2)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        for obstacle in obstacles:
            obstacle.draw(WIN)
            obstacle.update()

        clock.tick(FPS)
        pygame.display.update()
        for obstacle in obstacles:
            if player.collision(obstacle):
                pygame.time.delay(1000)
                death_count += 1
                menu(death_count)

    pygame.quit()


def menu(death_count):
    global score
    run = True
    while run:
        WIN.fill((0, 0, 0))

        if death_count == 0:
            text = FONT.render('Press any Key to Start', True, (255, 255, 255))
        else:
            text = FONT.render('Press any Key to Restart',
                               True, (255, 255, 255))
            score_text = FONT.render(
                'Your Score:' + str(score), True, (255, 255, 255))
            WIN.blit(score_text, (WIDTH//2 - score_text.get_width() //
                                  2, HEIGHT//2 - score_text.get_height()//2+50))
        WIN.blit(text, (WIDTH//2 - text.get_width() //
                        2, HEIGHT//2 - text.get_height()//2))
        WIN.blit(RUNNING[0], (WIDTH//2 - 20, HEIGHT//2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.QUIT()
                else:
                    main()


menu(death_count=0)
