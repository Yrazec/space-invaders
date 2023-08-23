import pygame
from PIL import Image

from configs.configs import Colors, Window


class ImageData:

    def __init__(self, path: str) -> None:
        self.image_width, self.image_height = Utils.get_image_dimensions(path=path)
        self.image = pygame.image.load(path)


class Object:

    def __init__(self, x: float, y: float, x_change: float, y_change: float) -> None:
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change


class Score:

    def __init__(self, screen: pygame.Surface, window_conf: Window, colors_conf: Colors) -> None:
        self.value = 0
        self._x = 5
        self._y = 5
        self._text = lambda score: f"Points: {score}"
        self._screen = screen
        self._window_conf = window_conf
        self._colors_conf = colors_conf

    def show_score(self) -> None:
        score_font = pygame.font.Font(None, self._window_conf.score_font_size)
        self._screen.blit(
            score_font.render(self._text(self.value), True, self._colors_conf.white, self._colors_conf.black),
            (self._x, self._y)
        )


class Utils:

    @staticmethod
    def get_image_dimensions(path: str) -> tuple:
        width, height = Image.open(path).size
        return width, height

    @staticmethod
    def objects_collision(
        x1: float,
        x2: float,
        y1: float,
        y2: float,
        image_data1: ImageData,
        image_data2: ImageData
    ) -> bool:

        # For bullet-invader collision - x1, y1 and image_data1 are bullet data
        # and x2, y2 and image_data2 are invader data.

        # Left front corner
        x1_in_x2 = (x2 <= x1 <= (x2 + image_data2.image_width))
        y1_in_y2 = (y2 <= y1 <= (y2 + image_data2.image_height))
        if x1_in_x2 and y1_in_y2:
            return True

        # Right front corner
        x1_in_x2 = (x2 <= (x1 + image_data1.image_width) <= (x2 + image_data2.image_width))
        y1_in_y2 = (y2 <= y1 <= (y2 + image_data2.image_height))
        if x1_in_x2 and y1_in_y2:
            return True

        return False
