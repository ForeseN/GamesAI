from __future__ import print_function
import pygame
import os
import random
import neat
import visualize
import pickle
pygame.init()

# Global Constants
HEIGHT = 600
WIDTH = 1100
FPS = 60
WHITE = (255, 255, 255)
BIRD_HEIGHTS = [210, 245]

# LOADING RESOURCES
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

    def update(self):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

    def update_bot(self, choice):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if choice == 0 and not self.dino_jump:
            self.ACCELARATION = ((
                (game_speed**2) * (self.JUMP_DISTANCE**2))/2/self.JUMP_HEIGHT)**(1/3)
            self.y_vel = game_speed * self.JUMP_DISTANCE/self.ACCELARATION
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif choice == 1 and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not(self.dino_jump or choice != 1):
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


def eval_genomes(genomes, config):

    global game_speed, x_pos_bg, y_pos_bg, score, obstacles

    nets = []
    ge = []
    dinos = []

    # PREPARING THE NETS
    for id, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dinosaur())
        g.fitness = 0
        ge.append(g)

    clock = pygame.time.Clock()
    cloud = Cloud()
    game_speed = 15
    x_pos_bg = 0
    y_pos_bg = 380
    score = 0
    obstacles = []

    def Score():  # SELF EXPLANATORY
        global score, game_speed
        score += 1
        if score % 100 == 0 and game_speed <= 40:
            game_speed += 1
        for x, dino in enumerate(dinos):
            ge[x].fitness += 1

        score_text = FONT.render('' + str(round(score)), 1, (255, 255, 255))
        WIN.blit(score_text, (WIDTH-score_text.get_width()-10, 10))

    def background():  # DRAWING BACKGROUND
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

        # DRAWING CLOUDS
        cloud.draw(WIN)
        cloud.update()

        userInput = pygame.key.get_pressed()

        # DRAWING OBSTACLES
        if len(obstacles) == 0:
            chosen_number = random.randint(0, 2)
            if chosen_number == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif chosen_number == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                obstacles.append(Bird(BIRD))

        # DRAWING OBSTACLES
        for obstacle in obstacles:
            obstacle.draw(WIN)
            obstacle.update()

        # CHECKING FOR COLLISION
        for obstacle in obstacles:
            for x, dino in enumerate(dinos):
                if dino.collision(obstacle):
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        if len(dinos) <= 0:
            run = False

        #  ------------------ INPUTS -----------------------------
        for x, dino in enumerate(dinos):
            dino.draw(WIN)
            try:
                if obstacles[0].y == 210:
                    # HIGH BIRD == DUCK
                    output = nets[x].activate(
                        ((obstacles[0].x - dino.x)/WIDTH, 1))
                    # print((obstacles[0].x - dino.x)/WIDTH, 1)
                else:
                    # EVERYTHING ELSE == JUMP
                    output = nets[x].activate(
                        ((obstacles[0].x - dino.x)/WIDTH, 0))
                    # print((obstacles[0].x - dino.x)/WIDTH, 0)
            except IndexError:
                # NO ENEMY JUST RUN
                output = nets[x].activate(((WIDTH - dino.x)/WIDTH, -999))
                # print(((WIDTH - dino.x)/WIDTH, -999))
            choice = output.index(max(output))
            dino.update_bot(choice)

        clock.tick(FPS)
        pygame.display.update()
        if score > 10500:  # BEST GENOME FOUND
            for x, dino in enumerate(dinos):
                dinos.pop(x)
                nets.pop(x)
                ge.pop(x)
                run = False


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)  # CONFIG

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))  # SHOW STATS
    stats = neat.StatisticsReporter()  # IN THE
    p.add_reporter(stats)  # COMMAND-LINE

    # WINNER OF THE PACK, ONCE IT GETS TO 10000 SCORE, THE PROGRAM STOPS (THE STOP HAPPENS IN THE WHILE LOOP) AND IT SAVED WITH PICKLE AS A FILE.
    winner = p.run(eval_genomes, 10000)
    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()

    print(winner)
    print('\nBest genome:\n{!s}'.format(winner))

    # ONCE YOU FIND A WINNER, IT DRAWS A GRAPH WITH USEFUL INFORMATION ABOUT THE GENERATIONS
    node_names = {-1: 'A', -2: 'B', 0: 'A XOR B'}
    visualize.draw_net(config, winner, True)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_feedforward.txt')
    run(config_path)
