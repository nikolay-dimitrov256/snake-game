from typing import List
import pygame
import random
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, KEYDOWN, K_ESCAPE, K_SPACE
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(10, 9), Vector2(10, 10), Vector2(10, 11)]
        self.direction = Vector2(0, -1)
        self.apple_eaten = False

        self.head_up = pygame.image.load('Graphics\\head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics\\head_down.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics\\head_left.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics\\head_right.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics\\tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics\\tail_down.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics\\tail_left.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics\\tail_right.png').convert_alpha()

        self.body_horizontal = pygame.image.load('Graphics\\body_horizontal.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics\\body_vertical.png').convert_alpha()
        self.body_top_left = pygame.image.load('Graphics\\body_bottomright.png').convert_alpha()
        self.body_bottom_left = pygame.image.load('Graphics\\body_topright.png').convert_alpha()
        self.body_top_right = pygame.image.load('Graphics\\body_bottomleft.png').convert_alpha()
        self.body_bottom_right = pygame.image.load('Graphics\\body_topleft.png').convert_alpha()

        self.head = self.head_up
        self.tail = self.tail_down

    def draw_snake(self):
        self.head_direction()
        self.tail_direction()

        for index, segment in enumerate(self.body):
            x = segment.x * cell_size
            y = segment.y * cell_size
            rectangle = pygame.Rect(x, y, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, rectangle)

            elif index == len(self.body) - 1:
                screen.blit(self.tail, rectangle)

            else:
                previous_segment = self.body[index + 1] - segment
                next_segment = self.body[index - 1] - segment

                if previous_segment.x == next_segment.x:
                    screen.blit(self.body_vertical, rectangle)
                elif previous_segment.y == next_segment.y:
                    screen.blit(self.body_horizontal, rectangle)

                else:
                    if previous_segment.x == -1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == -1:
                        screen.blit(self.body_bottom_right, rectangle)
                    elif previous_segment.x == -1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == -1:
                        screen.blit(self.body_top_right, rectangle)
                    elif previous_segment.x == 1 and next_segment.y == -1 or previous_segment.y == -1 and next_segment.x == 1:
                        screen.blit(self.body_bottom_left, rectangle)
                    elif previous_segment.x == 1 and next_segment.y == 1 or previous_segment.y == 1 and next_segment.x == 1:
                        screen.blit(self.body_top_left, rectangle)

    def head_direction(self):
        head_relation = self.body[0] - self.body[1]
        if head_relation == Vector2(0, -1):
            self.head = self.head_up
        elif head_relation == Vector2(0, 1):
            self.head = self.head_down
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(1, 0):
            self.head = self.head_right

    def tail_direction(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up

    def move_snake(self):
        body_copy = self.body[:-1]

        if self.apple_eaten:
            body_copy.append(body_copy[-1])
            self.apple_eaten = False

        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy


class Apple:
    def __init__(self):
        self.x = random.randint(0, cells_count - 1)
        self.y = random.randint(0, cells_count - 1)
        self.position = Vector2(self.x, self.y)
        self.image = pygame.image.load('Graphics\\apple.png').convert_alpha()

    def draw_apple(self):
        apple_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        screen.blit(self.image, apple_rect)

    def reposition(self, snake_body: List[Vector2]):
        self.x = random.randint(0, cells_count - 1)
        self.y = random.randint(0, cells_count - 1)
        new_position = Vector2(self.x, self.y)
        if new_position not in snake_body:
            self.position = new_position
        else:
            self.reposition(snake_body)


def draw_checkerboard():
    grass_color = (167, 209, 61)

    for col in range(cells_count):
        for row in range(cells_count):
            if row % 2 == 0:
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)

            elif row % 2 == 1:
                if col % 2 ==1:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)


def draw_score():
    score_text = str(len(snake.body) - 3)
    score_surf = game_font.render(score_text, True, 'white')
    score_x = cell_size * cells_count - 40
    score_y = cell_size * cells_count - 40
    score_rect = score_surf.get_rect(center=(score_x, score_y))
    screen.blit(score_surf, score_rect)


def check_collision(snake_: Snake, apple_: Apple):
    if snake_.body[0] == apple_.position:
        apple_.reposition(snake_.body)
        snake_.apple_eaten = True


def check_hit(snake_: Snake):
    if snake_.body[0].x not in range(cells_count) or snake_.body[0].y not in range(cells_count):
        game_over()

    if snake_.body[0] in snake_.body[1:]:
        game_over()


def game_over():
    global snake

    snake = Snake()


pygame.init()

cell_size = 40
cells_count = 20

screen = pygame.display.set_mode((cell_size * cells_count, cell_size * cells_count))
pygame.display.set_caption('Snake')
icon = pygame.image.load('Graphics\\head_right.png').convert_alpha()
pygame.display.set_icon(icon)
timer = pygame.time.Clock()

snake = Snake()
apple = Apple()
game_font = pygame.font.Font('Fonts\\comicbd.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT + 1
speed = 200
pygame.time.set_timer(SCREEN_UPDATE, speed)

directions_mapper = {K_UP: Vector2(0, -1), K_DOWN: Vector2(0, 1), K_LEFT: Vector2(-1, 0), K_RIGHT: Vector2(1, 0)}

running = True
pause = False

while running:
    screen.fill((175, 215, 70))
    draw_checkerboard()
    draw_score()
    apple.draw_apple()
    snake.draw_snake()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == SCREEN_UPDATE:
            if pause:
                continue

            snake.move_snake()
            check_collision(snake, apple)
            check_hit(snake)

        elif event.type == KEYDOWN:
            if event.key in directions_mapper:
                new_direction = directions_mapper[event.key]

                if list(new_direction + snake.direction) != [0.0, 0.0]:
                    snake.direction = new_direction

            elif event.key == K_ESCAPE:
                running = False

            elif event.key == K_SPACE:
                pause = not pause

    pygame.display.flip()
    timer.tick(60)

pygame.quit()
