import sys
import pygame
import time
import random
import copy

pygame.init()

text_color = (149, 255, 251)

lenght_of_screen = 1000
height_of_screen = 700

default_x_coor = lenght_of_screen / 2
default_y_coor = height_of_screen / 2

size_of_food = 10

screen = pygame.display.set_mode((lenght_of_screen, height_of_screen))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

snake_color = (0, 255, 0)
food_color = (148, 49, 38)
screnn_color = (0, 64, 106)

black = (0, 0, 0)

score_size = 30
score_x_coor = 400
score_y_coor = 30

dead_text_size = 70
dead_text_x_coor = 200
dead_text_y_coor = 280

def show_score(score):
    font = pygame.font.SysFont("Times New Roman", score_size)
    text = font.render("SCORE: " + str(score), True, text_color)
    screen.blit(text, (score_x_coor, score_y_coor))

class Snake:
    def __init__(self, x_coordinate, y_coordinate):
        self.length = 1
        self.x = x_coordinate
        self.y = y_coordinate
        self.x_delta = 1
        self.y_delta = 0
        self.body = [[self.x, self.y]]

    def show(self):
        for item in self.body:
            pygame.draw.rect(screen, snake_color, (item[0], item[1], size_of_food, size_of_food))

    def growth(self):
        self.length += 1
        self.body.append(self.body[-1])

    def check_eat(self):
        if abs(self.body[0][0] - food_x_coordinate) < size_of_food and abs(self.body[0][1] - food_y_coordinate) < size_of_food:
            return True

    def died(self):
        size = self.length - 1
        for size in range(size, 0, -1):
            if self.length > 4 and abs(self.body[0][0] - self.body[size][0]) < size_of_food and abs(self.body[0][1] - self.body[size][1]) < size_of_food:
                return True
            size -= 1



class Food:
    def new_location(self):
        global food_x_coordinate, food_y_coordinate
        food_x_coordinate = random.randrange(1, (lenght_of_screen - size_of_food) / size_of_food) * size_of_food
        food_y_coordinate = random.randrange(1, (height_of_screen - size_of_food) / size_of_food) * size_of_food

    def show(self):
        pygame.draw.rect(screen, food_color, (food_x_coordinate, food_y_coordinate, size_of_food, size_of_food))


def game():
    score = 0

    snake = Snake(default_x_coor, default_y_coor)
    food = Food()
    food.new_location()

    while True:

        screen.fill(screnn_color)
        snake.show()
        food.show()
        show_score(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    if snake.y_delta == 0:
                        snake.x_delta = 0
                        if event.key == pygame.K_UP:
                            snake.y_delta = -1
                        elif event.key == pygame.K_DOWN:
                            snake.y_delta = 1
                    elif snake.x_delta == 0:
                        snake.y_delta = 0
                        if event.key == pygame.K_LEFT:
                            snake.x_delta = -1
                        elif event.key == pygame.K_RIGHT:
                            snake.x_delta = 1

        size = snake.length - 1
        for size in range(size, 0, -1):
            snake.body[size] = copy.deepcopy(snake.body[size - 1])
            size -= 1
        snake.body[0][0] += snake.x_delta * size_of_food
        snake.body[0][1] += snake.y_delta * size_of_food

        if snake.check_eat():
            score += 1
            snake.growth()
            food.new_location()

        if snake.died():
            font = pygame.font.SysFont("Times New Roman", dead_text_size)
            text = font.render("THE GAME IS OVER", True, text_color)
            screen.fill(black)
            screen.blit(text, (dead_text_x_coor, dead_text_y_coor))
            pygame.display.update()
            time.sleep(3)

        if snake.body[0][0] > lenght_of_screen:
            snake.body[0][0] = 0
        elif snake.body[0][0] < 0:
            snake.body[0][0] = lenght_of_screen
        if snake.body[0][1] > height_of_screen:
            snake.body[0][1] = 0
        elif snake.body[0][1] < 0:
            snake.body[0][1] = height_of_screen

        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    game()

