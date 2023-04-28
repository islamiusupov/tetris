import random
import pygame

game_w = 10
game_h = 15

box_size = 60 #px

screen_width = game_w * box_size
screen_height = (game_h - 1) * box_size

patterns = [
    [
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 0]
    ],
    [
        [1, 1, 0],
        [0, 1, 1]
    ],
    [
        [1, 1],
        [1, 0],
        [1, 0]
    ]
]

class Figure:
    def __init__(self, _x, _y, _pattern, _color):
        self.x = _x
        self.y = _y
        self.pattern = _pattern
        self.color = _color

    def collision_with_board(self, _board):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                if self.pattern[i][j] == 1:
                    if _board[int(self.y / box_size) + i + 1][int(self.x / box_size) + j] == 1:
                        return True
        return False

    def collision(self, _x, _y):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                if self.pattern[i][j] == 1:
                    if _x + j * box_size < 0 or _x + j * box_size > screen_width - box_size:
                        return True
                    if _y + i * box_size < 0 or _y + i * box_size > screen_height - box_size:
                        return True
        return False

    def rotate(self, _direction):
        if _direction == 1:
            self.pattern = [[self.pattern[y][x] for y in range(len(self.pattern))] for x in range(len(self.pattern[0]) - 1, -1, -1)]
        elif _direction == -1:
            self.pattern = [[self.pattern[y][x] for y in range(len(self.pattern) - 1, -1, -1)] for x in range(len(self.pattern[0]))]

    def draw(self, screen):
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[i])):
                if self.pattern[i][j] == 1:
                    pygame.draw.rect(screen, self.color, (self.x + j * box_size, self.y + i * box_size, box_size, box_size))

class Board:
    def __init__(self):
        self.board = []
        for i in range(game_h):
            self.board.append([])
            for j in range(game_w):
                self.board[i].append(0)

    def check_for_lines_to_destroy(self):
        for i in range(len(self.board)):
            if 0 not in self.board[i]:
                self.board.pop(i)
                self.board.insert(0, [0 for _ in range(game_w)])

    def intake_figure(self, _figure):
        for i in range(len(_figure.pattern)):
            for j in range(len(_figure.pattern[i])):
                if _figure.pattern[i][j] == 1:
                    if int(_figure.y / box_size) + i >= game_h:
                        continue
                    if int(_figure.x / box_size) + j >= game_w:
                        continue

                    print(int(_figure.y / box_size) + i, int(_figure.x / box_size) + j)
                    print(len(self.board), len(self.board[0]))
                    self.board[int(_figure.y / box_size) + i][int(_figure.x / box_size) + j] = 1
        self.check_for_lines_to_destroy()

    def draw(self, screen):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (j * box_size, i * box_size, box_size, box_size))

pygame.init()


screen = pygame.display.set_mode((screen_width, screen_height))
board = Board()

circle_radius = 50
circle_color = (0, 255, 0)
circle_x = screen_width // 2
circle_y = screen_height // 2

running = True
active_figure = Figure(0, 0, patterns[1], (255, 0, 0))
space_pressed = False
while running:
    # Handle events
    for event in pygame.event.get():
        if space_pressed:
            speed = 0.4
        else:
            speed = 0.1
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT:
                if not active_figure.collision(active_figure.x - box_size, active_figure.y):
                    active_figure.x -= box_size
                    if active_figure.collision_with_board(board.board):
                        active_figure.x += box_size

            if event.key == pygame.K_RIGHT:
                if not active_figure.collision(active_figure.x + box_size, active_figure.y):
                    active_figure.x += box_size
                    if active_figure.collision_with_board(board.board):
                        active_figure.x -= box_size

            if event.key == pygame.K_UP:
                active_figure.rotate(1)
            if event.key == pygame.K_DOWN:
                active_figure.rotate(-1)
            if event.key == pygame.K_SPACE:
                space_pressed = True

    screen.fill((255, 255, 255))
    active_figure.y += speed
    if active_figure.collision(active_figure.x, active_figure.y):
        print(int(active_figure.y // box_size), int(active_figure.x // box_size))
        print("boom")
        active_figure.y -= speed
        board.intake_figure(active_figure)
        active_figure.y = 0
        active_figure.pattern = patterns[int(random.random() * len(patterns))]
    if active_figure.collision_with_board(board.board):
        board.intake_figure(active_figure)
        active_figure.y = 0
        active_figure.pattern = patterns[int(random.random() * len(patterns))]

    #     active_figure = Figure(0, 0, patterns[random.randint(0, len(patterns) - 1)], (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    board.draw(screen)
    active_figure.draw(screen)

    pygame.display.flip()

# Quit Pygame
pygame.quit()