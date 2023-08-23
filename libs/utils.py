"""File for storing additional classes and methods for Space Invaders."""

import pygame
from PIL import Image

from configs.configs import Colors, Window


class ImageData:
    """Class that stores Image Data like width, height and image itself."""

    def __init__(self, path: str) -> None:
        """
        Standard ImageData constructor.

        :param str path: path to image
        """

        self.image_width, self.image_height = Utils.get_image_dimensions(path=path)
        self.image = pygame.image.load(path)


class Object:
    """Class that stores Object information like x and y positions and its changes."""

    def __init__(self, x: float, y: float, x_change: float, y_change: float) -> None:
        """
        Standard Object constructor.

        :param float x: x coordinates of object
        :param float y: y coordinates of object
        :param float x_change: x change of object
        :param float y_change: y change of object
        """

        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change


class Score:
    """Class that stores Score information and graphical data."""

    def __init__(self, screen: pygame.Surface, window_conf: Window, colors_conf: Colors) -> None:
        """
        Standard Score constructor.

        :param pygame.Surface screen: screen object
        :param Window window_conf: Window configuration object
        :param Colors colors_conf: Colors configuration object
        """

        self.value = 0
        self._x = 5
        self._y = 5
        self._text = lambda score: f"Points: {score}"
        self._screen = screen
        self._window_conf = window_conf
        self._colors_conf = colors_conf

    def show_score(self) -> None:
        """Shows score in Window on screen."""

        score_font = pygame.font.Font(None, self._window_conf.score_font_size)
        self._screen.blit(
            score_font.render(self._text(self.value), True, self._colors_conf.white, self._colors_conf.black),
            (self._x, self._y)
        )


class Utils:
    """Class that stores standard Utils methods."""

    @staticmethod
    def get_image_dimensions(path: str) -> tuple:
        """
        Gets image dimensions.

        :param str path: path to image
        :return: tuple of image width height
        """

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
        """
        Check object collision.

        :param float x1: object 1 x coordinate
        :param float x2: object 2 x coordinate
        :param float y1: object 1 y coordinate
        :param float y2: object 2 y coordinate
        :param ImageData image_data1: ImageData of 1 object
        :param ImageData image_data2: ImageData of 2 object
        :return: True if collision occurs, otherwise False
        """

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
