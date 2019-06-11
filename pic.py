from PIL import ImageFont, Image, ImageDraw

'''
These classes are used to generate pictures

'''


class Welcome:
    def __init__(self, width, height, color=(100, 100, 100), f='pong/sub.ttf'):
        font = ImageFont.truetype(f, size=200)

        welcome_pong = 'PONG'
        size_pong = font.getsize(text=welcome_pong)

        img = Image.new('RGB', (width, height), color)

        draw = ImageDraw.Draw(img)
        draw.text(((width - size_pong[0]) / 2, (height - size_pong[1]) / 2.5), welcome_pong, (255, 255, 255), font=font)

        font = ImageFont.truetype(f, size=30)
        welcome_options = '"s" to start\n"1-9" to change a ball speed\n"F1-F3" to change AI diffculty\n"g" to play with AI\n"space" to pause'
        size_options = draw.multiline_textsize(welcome_options, font)

        draw.multiline_text(((width - size_options[0]) / 2, (height - size_options[1]) / 1.25), welcome_options,
                            (255, 255, 255),
                            font=font)
        img.save('pong/images/start_screen.jpg')


class SimpleText:
    def __init__(self, width, height, text, font_size=200, color=(100, 100, 100), f='pong/sub.ttf'):
        font = ImageFont.truetype(f, size=font_size)

        size_pong = font.getsize(text=text)

        img = Image.new('RGB', (width, height), color)

        draw = ImageDraw.Draw(img)
        draw.text(((width - size_pong[0]) / 2, (height - size_pong[1]) / 2.5), text, (255, 255, 255), font=font)
        img.save('pong/images/{}.jpg'.format(text.replace(" ", "")))


def draw_pics(width, height):
    welcome = Welcome(width, height)
    pause = SimpleText(width, height, 'pause')
    player1wins = SimpleText(width, height, 'Player 1 wins!', 80)
    player2wins = SimpleText(width, height, 'Player 2 wins!', 80)
    computerwins = SimpleText(width, height, 'Computer wins!', 80)


if __name__ == '__main__':

    '''
    for testing purpose
    '''

    width = 800
    height = 800

    # welcome = Welcome(width, height)
    # pause = SimpleText(width, height, 'pause')
    # player1wins = SimpleText(width, height, 'Player 1 wins!', 80)
    # player2wins = SimpleText(width, height, 'Player 2 wins!', 80)

    draw_pics(width, height)
