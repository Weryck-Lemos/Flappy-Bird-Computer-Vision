import pygame, random
from pygame.locals import *

W = 400
H = 800
SPEED = 10
GRAVITY = 0.8
GROUND_W = W*2
GROUND_H = 100
PIPE_W = 80
PIPE_H = 500
PIPE_GAP = 300
BACKGROUND = pygame.image.load('Flappy Bird/assets/background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (W, H))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('Flappy Bird/assets/yellowbird-upflap.png').convert_alpha(),
                       pygame.image.load('Flappy Bird/assets/yellowbird-midflap.png').convert_alpha(),
                       pygame.image.load('Flappy Bird/assets/yellowbird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('Flappy Bird/assets/yellowbird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = W/2-100
        self.rect[1] = H/2

    def update(self):
        self.current_image = (self.current_image + 1)%3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed
    
    def jump(self):
        self.speed = -SPEED



class Pipe(pygame.sprite.Sprite):
    def __init__(self,inverted, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Flappy Bird/assets/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_W,PIPE_H))
        self.rect = self.image.get_rect()
        self.rect[0] = x


        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - y)
        else:
            self.rect[1] = H - y 

        self.mask = pygame.mask.from_surface(self.image)
        self.passed = False


    def update(self):
        self.rect[0] -= SPEED




class Ground(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Flappy Bird/assets/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_W, GROUND_H))
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = x
        self.rect[1] = H - GROUND_H 

    def update(self):
        self.rect[0] -= SPEED

 


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(x):
    size = random.randint(100, 300)
    pipe = Pipe(False, x, size)
    pipe_inverted = Pipe(True, x, H -size - PIPE_GAP)
    return (pipe, pipe_inverted)



def reset_game():
    global bird, bird_group, ground_group, pipe_group, score, game_over

    bird = Bird()
    bird_group = pygame.sprite.Group(bird)

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground_group.add(Ground(GROUND_W * i))

    pipe_group = pygame.sprite.Group()
    pipes = get_random_pipes(W + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

    score = 0
    game_over = False


pygame.init()
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont("Arial", 40)
small_font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

reset_game()

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)


ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_W *i)
    ground_group.add(ground)


pipe_group = pygame.sprite.Group()
for i in range(1):
    pipes = get_random_pipes(W * 1 + 600)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])



while True:
    clock.tick(14)
    for event in pygame.event.get():
        if event.type ==  QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.jump()
            if game_over and event.key == K_SPACE:
                reset_game()


    screen.blit(BACKGROUND, (0,0))
    if not game_over:
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])

            new_ground = Ground(GROUND_W - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])

            pipes = get_random_pipes(W*2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        for pipe in pipe_group:
            if not pipe.passed and pipe.rect.right < bird.rect.left:
                pipe.passed = True
                score +=0.5

        bird_group.update()
        pipe_group.update()
        ground_group.update()



        if (pygame.sprite.groupcollide(bird_group , ground_group, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(bird_group , pipe_group, False, False, pygame.sprite.collide_mask)):
            game_over = True

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    score_surface = font.render(f"{int(score)}", True, (255, 255, 255))
    screen.blit(score_surface, (W // 2 - score_surface.get_width() // 2, 40))

    if game_over:
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        restart_text = small_font.render("Pressione ESPAÇO para reiniciar", True, (255, 255, 255))

        screen.blit(game_over_text, (W // 2 - game_over_text.get_width() // 2, H // 2 - 60))
        screen.blit(restart_text, (W // 2 - restart_text.get_width() // 2, H // 2 + 60))


    pygame.display.update()