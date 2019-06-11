import json
import os
from pic import *

from classes import *

if __name__ == "__main__":

        # Apply configuration file

        with open('pong/config.json', 'r') as f:
            config = json.load(f)

        ball_velocity = int(config['DEFAULT']['BALL_SPEED'])
        ai_speed = int(config['DEFAULT']['AI_SPEED'])

        screen_width = int(config['DEFAULT']['SCREEN_WIDTH'])
        screen_height = int(config['DEFAULT']['SCREEN_HEIGHT'])

        # draw pictures
        draw_pics(screen_width, screen_height)
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # Center the screen
        game = PongGame(screen_width, screen_height)  # Create game object
        game.ball.x_velocity = ball_velocity
        game.ball.y_velocity = ball_velocity
        game.ai.paddle.max_speed = ai_speed

        flag = game.game_loop()  # Start game loop
