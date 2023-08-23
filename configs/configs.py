import pydantic


class Window(pydantic.BaseModel):

    caption: str = pydantic.Field('Space Invaders', description='Window title.')

    screen_width: int = pydantic.Field(800, description='Window width (in pixels).')
    screen_height: int = pydantic.Field(600, description='Window height (in pixels).')

    score_font_size: int = pydantic.Field(20, description='Font size of score text.')

    laser: bool = pydantic.Field(False, description='Vertical red laser.')


class Colors(pydantic.BaseModel):

    white: tuple = pydantic.Field((255, 255, 255), description='White color in RGB mode.')
    black: tuple = pydantic.Field((0, 0, 0), description='Black color in RGB mode.')

    red: tuple = pydantic.Field((255, 0, 0), description='Red color in RGB mode.')
    green: tuple = pydantic.Field((0, 255, 0), description='Green color in RGB mode.')
    blue: tuple = pydantic.Field((0, 0, 255), description='Blue color in RGB mode.')

    cyan: tuple = pydantic.Field((0, 255, 255), description='Cyan color in RGB mode.')
    magenta: tuple = pydantic.Field((255, 0, 255), description='Magenta color in RGB mode.')
    yellow: tuple = pydantic.Field((255, 255, 0), description='Yellow color in RGB mode.')


class Resources(pydantic.BaseModel):

    main_theme_sound = pydantic.Field('resources/sounds/main-theme.mpeg', description='Main theme sound.')
    shoot_sound = pydantic.Field('resources/sounds/shoot.wav', description='Shoot sound.')
    ufo_low_pitch_sound = pydantic.Field('resources/sounds/ufo-low-pitch.wav', description='UFO low pitch sound.')

    alien_image = pydantic.Field('resources/images/alien.png', description='Alien image.')
    bullet_image = pydantic.Field('resources/images/bullet.png', description='Bullet image.')
    spaceship_image = pydantic.Field('resources/images/spaceship.png', description='Spaceship image.')

    background_image = pydantic.Field('resources/images/space-background-800x600.jpg', description='Background image.')
    game_over_image = pydantic.Field('resources/images/game-over.png', description='Game Over image.')
