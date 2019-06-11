from PIL import Image
from pygame.locals import *
from drawable import *


class PongGame:
    """
    Main class of entire game. Connects everything together.
    """

    def __init__(self, screen_width, screen_height):
        # This function initializes all objects needed in the game, paddles and ball are scaling with the screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        self.board = Board(screen_width, screen_height)
        self.player1_paddle = Paddle(screen_width / 100,
                                     screen_height / 6,
                                     screen_width - screen_width / 70 - 10,
                                     screen_height * 0.5 + 50)
        self.player2_paddle = Paddle(screen_width / 100,
                                     screen_height / 6,
                                     0 + screen_width / 70 + 3,
                                     screen_height * 0.5 + 50)
        self.ai_paddle = Paddle(screen_width / 100,
                                screen_height / 6,
                                screen_width - screen_width / 70 - 3 + 100,  # Let's hide ai paddle at start
                                screen_height * 0.5 + 50,
                                (255, 0, 0))
        self.fps_clock = pygame.time.Clock()  # Variable used to control displaying frames
        self.ball = Ball(screen_width / 90, screen_width / 90, screen_width * 0.5, screen_height * 0.5)
        self.score = [0, 0]
        self.is_paused = False
        self.ai = Ai(self.ai_paddle, self.ball)
        self.is_first_run = True

        self.central_line = pygame.Rect(self.screen_width / 2, 0, 1, self.screen_height)  # Aesthetic line in the middle
        pygame.font.init()  # Initialize fonts
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 64)

    def game_loop(self):
        """
        Main function responsible for continuity of game
        """
        while not self.handle_events():
            # Loop used to refresh objects in main loop
            self.ball.move(self.board, self.player1_paddle, self.player2_paddle, self.ai_paddle)
            self.board.draw(  # Draw all drawable objects
                self.ball,
                self.player1_paddle,
                self.player2_paddle,
                self.ai_paddle,
                self,
            )
            self.fps_clock.tick_busy_loop(60)  # Enhance fps to improve UX
            self.player2_paddle.move(self.screen_height, 1)  # move paddle when direction != 0
            self.ai.move(1)
            self.draw_on(self.board.surface)

    def update_score(self, board_width):
        """
        Counting points and after scoring setting ball and paddles to starting position
        """
        if self.ball.rect.left < 0:
            self.score[0] += 1
            self.ball.reset_position()
            time.sleep(1)
            self.player1_paddle.rect.y = self.screen_height / 2
            self.player2_paddle.rect.y = self.screen_height / 2
            self.ai_paddle.rect.y = self.screen_height / 2
        elif self.ball.rect.right > board_width:
            self.score[1] += 1
            self.ball.reset_position()
            time.sleep(1)
            self.player1_paddle.rect.y = self.screen_height / 2
            self.player2_paddle.rect.y = self.screen_height / 2
            self.ai_paddle.rect.y = self.screen_height / 2

    def draw_score(self, surface, text, position_x, position_y):
        """
        Drawing score in a given place
        """
        text = self.font.render(text, True, (150, 150, 150))
        rect = text.get_rect()
        rect.center = position_x, position_y
        surface.blit(text, rect)  # Draw one image onto another

    def draw_on(self, surface):
        """
        Updating and drawing score
        """
        height = self.board.surface.get_height()

        width = self.board.surface.get_width()
        pygame.draw.rect(self.board.surface, (255, 255, 255), self.central_line)
        if self.ai_paddle.rect.x < self.screen_width:
            # Display the appropriate picture depending on who is playing.
            self.draw_score(surface, "Computer: {}".format(self.score[0]), width / 2, height * 0.3)
        else:
            self.draw_score(surface, "Player 2: {}".format(self.score[0]), width / 2, height * 0.3)
        self.draw_score(surface, "Player 1: {}".format(self.score[1]), width / 2, height * 0.7)
        self.update_score(width)

        # Check who won the game.
        if self.score[0] == 5:
            # If player2 wins display image, but when computer wins display another image.
            if self.ai_paddle.rect.x < self.screen_width:
                image = Image.open("pong/images/Computerwins!.jpg")
                new_image = image.resize((self.screen_width, self.screen_height))  # fit image to the screen
                new_image.save("pong/images/temp.jpg")  # to avoid resizing original image all time
            else:
                image = Image.open("pong/images/Player2wins!.jpg")
                new_image = image.resize((self.screen_width, self.screen_height))
                new_image.save("pong/images/temp.jpg")

            background_image = pygame.image.load("pong/images/temp.jpg").convert()
            self.board.surface.blit(background_image, [0, 0])
            self.fps_clock.tick(5)  # reduce fps

        elif self.score[1] == 5:
            image = Image.open("pong/images/Player1wins!.jpg")
            new_image = image.resize((self.screen_width, self.screen_height))
            new_image.save("pong/images/temp.jpg")
            background_image = pygame.image.load("pong/images/temp.jpg").convert()
            self.board.surface.blit(background_image, [0, 0])
            self.fps_clock.tick(5)

    def handle_events(self):
        """
        Function responsible for handling all events gathered from user
        """
        for event in pygame.event.get():
            # Look for events occurred in main loop
            while self.is_first_run:
                # Display start screen for the first time
                background_position = [0, 0]
                image = Image.open("pong/images/start_screen.jpg")
                new_image = image.resize((self.screen_width, self.screen_height))  # To fit image to screen
                new_image.save("pong/images/temp.jpg")  # To avoid resizing original image all time

                background_image = pygame.image.load("pong/images/temp.jpg").convert()
                self.board.surface.blit(background_image, background_position)

                pygame.display.update()

                self.fps_clock.tick(5)
                for events in pygame.event.get():
                    # Handle quit and start when start screen displayed.
                    if events.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if events.type == KEYDOWN and events.key == K_s:
                        self.is_first_run = False

            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.MOUSEMOTION:  # Look for mousemotion to move paddle
                x, y = event.pos
                self.player1_paddle.move(self.screen_height, 0, y)
            if event.type == pygame.KEYDOWN:  # Look for pressing keys to move paddle
                if event.key == pygame.K_DOWN:
                    self.player2_paddle.direction = 1  # Move paddle down while pressing
                if event.key == pygame.K_UP:
                    self.player2_paddle.direction = -1  # Move paddle up while pressing
                if event.key == pygame.K_1:  # Look for ball speed changes
                    self.ball.change_ball_speed(1.5)
                    self.score = [0, 0]
                if event.key == pygame.K_2:
                    self.ball.change_ball_speed(2)
                    self.score = [0, 0]
                if event.key == pygame.K_3:
                    self.ball.change_ball_speed(3)
                    self.score = [0, 0]
                if event.key == pygame.K_4:
                    self.ball.change_ball_speed(4)
                    self.score = [0, 0]
                if event.key == pygame.K_5:
                    self.ball.change_ball_speed(5)
                    self.score = [0, 0]
                if event.key == pygame.K_6:
                    self.ball.change_ball_speed(7)
                    self.score = [0, 0]
                if event.key == pygame.K_7:
                    self.ball.change_ball_speed(9)
                    self.score = [0, 0]
                if event.key == pygame.K_8:
                    self.ball.change_ball_speed(10)
                    self.score = [0, 0]
                if event.key == pygame.K_9:
                    self.ball.change_ball_speed(15)
                    self.score = [0, 0]
                if event.key == pygame.K_g:  # Play with computer
                    self.ai_paddle.rect.x = self.screen_width - self.screen_width / 50 - 3
                    self.player1_paddle.rect.x += 100  # Let's hide player
                    self.score = [0, 0]
                    time.sleep(2)
                if event.key == pygame.K_h:  # Play with AI
                    self.ai_paddle.rect.x += 100  # Let's hide AI
                    self.player1_paddle.rect.x = self.screen_width - self.screen_width / 50 - 3
                    self.score = [0, 0]
                    time.sleep(2)
                if event.key == pygame.K_F1:  # Change AI difficulty
                    self.ai_paddle.max_speed = 4
                    self.ball.x_velocity = 5
                    self.score = [0, 0]
                    time.sleep(2)
                if event.key == pygame.K_F2:
                    self.ai_paddle.max_speed = 8
                    self.ball.x_velocity = 9
                    self.score = [0, 0]
                    time.sleep(2)
                if event.key == pygame.K_F3:
                    self.ball.x_velocity = 13
                    self.ai_paddle.max_speed = 15
                    self.score = [0, 0]
                    time.sleep(2)
                if event.key == pygame.K_s:
                    self.score = [0, 0]
                    self.ball.rect.x = self.screen_width / 2
                    self.ball.rect.y = self.screen_height / 2
                    time.sleep(2)

                if event.key == pygame.K_SPACE:  # Pause the game and display pause screen
                    self.is_paused = True
                    background_position = [0, 0]

                    image = Image.open("pong/images//game_paused.jpg")
                    new_image = image.resize((self.screen_width, self.screen_height))  # to fit image to screen
                    new_image.save("pong/images/temp.jpg")  # to avoid resizing original image all time

                    background_image = pygame.image.load("pong/images/temp.jpg").convert()
                    self.board.surface.blit(background_image, background_position)

                    pygame.display.update()

                    self.fps_clock.tick(5)
                    while self.is_paused:
                        # Handle only exit and unpause events when game is paused
                        for events in pygame.event.get():

                            if events.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if events.type == KEYDOWN and events.key == K_SPACE:
                                self.is_paused = False

            if event.type == KEYUP:  # Behavior while key is going up
                if event.key == K_UP and self.player2_paddle.direction == -1:
                    self.player2_paddle.direction = 0  # Stop paddle when key is going up
                elif event.key == K_DOWN and self.player2_paddle.direction == 1:
                    self.player2_paddle.direction = 0


class Ai:
    """
    Simple AI, based on observing ball, level of AI depends on its speed
    """

    def __init__(self, paddle, ball):
        self.ball = ball
        self.paddle = paddle

    def move(self, direction=0):
        if direction != 0:
            self.paddle.position_y += self.paddle.direction * self.paddle.max_speed
            self.rect = pygame.Rect(self.paddle.position_x,
                                    self.paddle.position_y - int(self.paddle.height * 0.5),
                                    self.paddle.width,
                                    self.paddle.height)
        if self.ball.rect.top < self.paddle.rect.top:  # When ball is under paddle, AI goes down
            self.paddle.rect.centery -= self.paddle.max_speed
        elif self.ball.rect.bottom > self.paddle.rect.bottom:  # When ball is above paddle, AI goes up
            self.paddle.rect.centery += self.paddle.max_speed
