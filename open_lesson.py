import random
import pygame, sys
from pygame.math import Vector2


#   Код класса Змеи
class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(8, 10), Vector2(9, 10)]
        self.direction = Vector2(-1, 0)
        self.new_block = False
        self.color = (249, 242, 29)
        self.SNAKE_COLOR = random.choice(['red', 'green', 'blue', 'yellow'])

        self.head_up = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/head_u.png'),
                                              (cell_size, cell_size))
        self.head_right = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/head_r.png'),
                                                 (cell_size, cell_size))
        self.head_left = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/head_l.png'),
                                                (cell_size, cell_size))
        self.head_down = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/head_d.png'),
                                                (cell_size, cell_size))
        #   Загрузка спрайтов тела
        self.body_vertical = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/body_v.png'),
                                                    (cell_size, cell_size))
        self.body_horizontal = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/body_h.png'),
                                                      (cell_size, cell_size))
        #   Загрузка спрайтов поворота тела
        self.body_pov_ur = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/pov_ur.png'),
                                                  (cell_size, cell_size))
        self.body_pov_rd = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/pov_rd.png'),
                                                  (cell_size, cell_size))
        self.body_pov_dl = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/pov_dl.png'),
                                                  (cell_size, cell_size))
        self.body_pov_lu = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/pov_lu.png'),
                                                  (cell_size, cell_size))
        #   Загрузка спрайтов хвоста
        self.tale_up = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/tale_u.png'),
                                              (cell_size, cell_size))
        self.tale_right = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/tale_r.png'),
                                                 (cell_size, cell_size))
        self.tale_down = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/tale_d.png'),
                                                (cell_size, cell_size))
        self.tale_left = pygame.transform.scale(pygame.image.load('snake32/' + self.SNAKE_COLOR + '/tale_l.png'),
                                                (cell_size, cell_size))



        print("Snake Created!")

    def draw(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, self.color, block_rect)

    def move(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def grow(self):
        self.new_block = True


#   Код класса фрукта
class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = pygame.math.Vector2(self.x, self.y)
        apple_path = 'snake32/apple_' + str(random.randint(1, 5)) + '.png'
        self.apple = pygame.transform.scale(
            pygame.image.load(apple_path),
            (cell_size, cell_size)
        )
        print("Fruit  created!")

    def draw(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size, cell_size)
        # pygame.draw.rect(screen, (243, 55, 80), fruit_rect)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = pygame.math.Vector2(self.x, self.y)
        apple_path = 'snake32/apple_' + str(random.randint(1, 5)) + '.png'
        self.apple = pygame.transform.scale(
            pygame.image.load(apple_path),
            (cell_size, cell_size)
        )


#   Код Главного класса
class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        print("Main created!")

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.snake.draw()
        self.fruit.draw()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.grow()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y <cell_number:
            self.game_over()
        if self.snake.body[1:].__contains__(self.snake.body[0]):
            self.game_over()

    def draw_score(self):
        score_text = str(len(self.snake.body)-3)
        score_surface = game_font.render(score_text, True, (255, 255, 255))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.fruit.apple.get_rect(
            midright=(score_rect.left, score_rect.centery)
        )
        bg_rect = pygame.Rect(
            apple_rect.left-10, apple_rect.top-4,
            apple_rect.width+ score_rect.width+20, apple_rect.height + 8
        )
        pygame.draw.rect(screen, (70, 182, 90), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.fruit.apple, apple_rect)


    def game_over(self):
        pygame.quit()
        sys.exit()


#   Код основной программы

pygame.init()
cell_size = 32
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number, cell_size*cell_number))
clock = pygame.time.Clock()
game_font = pygame.font.SysFont('arial', 24)

main = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main.snake.direction.y != 1:
                    main.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main.snake.direction.x != -1:
                    main.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main.snake.direction.y != -1:
                    main.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main.snake.direction.x != 1:
                    main.snake.direction = Vector2(-1, 0)

    screen.fill((29, 249, 132))
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)

