import math
import random
import time
import pygame


class Board:
    """
    Class used for creating main screen
    """

    def __init__(self, screen_width, screen_height):
        self.surface = pygame.display.set_mode([screen_width, screen_height])
        pygame.display.set_caption("PONG")

    def draw(self, *args):
        # This function draws main board and others drawable items
        background_color = (100, 100, 100)
        self.surface.fill(background_color)
        for drawable in args:
            drawable.draw_on(self.surface)

        pygame.display.update()  # Update portions of the screen


class Drawable:
    """
    Base class for objects like ball, paddles
    """

    def __init__(self, width, height, position_x, position_y, color=(255, 255, 255)):
        self.width = width
        self.height = height
        self.color = color
        self.position_x = position_x
        self.position_y = position_y
        self.surface = pygame.Surface([width, height],  # Create surface of the game
                                      pygame.SRCALPHA,  # The pixel format will include a per-pixel alpha
                                      32).convert_alpha()
        self.rect = self.surface.get_rect(x=position_x, y=position_y)  # Get the rectangular area of the Surface

    def draw_on(self, surface):
        # Method used to drawing surface on the screen
        surface.blit(self.surface, self.rect)


class Ball(Drawable):
    """
    Simple ball
    """

    def __init__(self, width, height, position_x, position_y, color=(255, 255, 255), x_velocity=5, y_velocity=5):
        super(Ball, self).__init__(width, height, position_x, position_y, color)
        pygame.draw.ellipse(self.surface, self.color, [0, 0, self.width, self.height])  # Draw the ball
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.direction_x = position_x
        self.direction_y = position_y

    def bounce_y(self):
        # Bounce in y direction and get some random acceleration
        self.y_velocity *= -1 + random.uniform(-0.1, 0.1)

    def bounce_x(self):
        # Bounce in x direction and get some random acceleration
        self.x_velocity *= -1 + random.uniform(-0.1, 0.1)

    def reset_position(self):
        # Move ball to initial position and throw in random direction
        self.rect.x = self.direction_x
        self.rect.y = self.direction_y
        self.y_velocity += random.uniform(-0.1, 0.1)
        self.x_velocity += random.uniform(-0.1, 0.1)
        rand = math.floor(random.uniform(0, 2))
        if rand == 1:
            self.bounce_x()
        if rand == 0:
            self.bounce_y()

    def move(self, board, *args):
        # Function used to move ball
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        if self.rect.y < 0 or self.rect.y > board.surface.get_height() - self.height:
            self.bounce_y()  # Bounce the ball when hits top or bottom of screen

        for paddle in args:
            # Loop used to moving hitboxes and checks if ball hits paddle
            if self.rect.colliderect(paddle.rect):  # Returns true if two rectangles overlap
                self.bounce_x()
                self.y_velocity = random.randint(-9, 9)

    def change_ball_speed(self, speed):
        # Function used to change ball speed and center ball on screen
        self.x_velocity = speed
        self.y_velocity = speed
        self.rect.x = self.position_x
        self.rect.y = self.position_y
        time.sleep(2)


class Paddle(Drawable):
    """
    Paddle, moves in y axis with limited speed
    """

    def __init__(self, width, height, position_x, position_y, color=(255, 255, 255)):
        super(Paddle, self).__init__(width, height, position_x, position_y, color)
        self.max_speed = 15
        self.surface.fill(color)
        self.direction = 0

    def move(self, screen_height, direction=0, y=0):
        if direction != 0:
            # Move paddle when user wants, used to move paddle with arrows and AI paddle
            self.rect.y += self.direction * self.max_speed
        else:
            # Behavior when user wants to play with mouse
            delta = y - self.rect.y
            if abs(delta) > self.max_speed:
                delta = self.max_speed if delta > 0 else - self.max_speed
            self.rect.y += delta

        if self.rect.top < 0:
            # Boundary checks to avoid situation when paddle goes to high
            self.rect.top = 0
        if self.rect.bottom > screen_height - 1:
            # Boundary checks to avoid situation when paddle goes to low
            self.rect.bottom = screen_height - 1

