import random

import pygame

from configs.configs import Colors, Resources, Window
from libs.utils import ImageData, Object, Score, Utils


class SpaceInvaders:

    def __init__(self, invaders_number: int) -> None:

        # Configuration files
        self.colors_conf = Colors()
        self.resources_conf = Resources()
        self.window_conf = Window()

        # Initialize and setup Window
        self.screen = self._screen_settings()
        self.background_image_data = ImageData(path=self.resources_conf.background_image)
        self._play_music(filename=self.resources_conf.main_theme_sound, loops=-1)

        # Score object
        self.score = Score(screen=self.screen, window_conf=self.window_conf, colors_conf=self.colors_conf)

        # Player objects
        self.player_image_data = ImageData(path=self.resources_conf.spaceship_image)
        self.player = Object(
            x=(self.window_conf.screen_width / 2.0) - (self.player_image_data.image_width / 2.0),
            y=self.window_conf.screen_height - self.player_image_data.image_height,
            x_change=0.0,
            y_change=0.0  # y_change not used for Player
        )

        # Invader objects
        self.invader_image_data = ImageData(path=self.resources_conf.alien_image)
        self.invaders = []
        for _ in range(invaders_number):
            self.invaders.append(
                Object(
                    x=random.randint(0, self.window_conf.screen_width - self.invader_image_data.image_width),
                    y=0,
                    x_change=0.5,  # x_change - invader x speed
                    y_change=self.invader_image_data.image_height  # y_change - Invader y movement jump
                )
            )

        # Bullet objects
        self.bullet_image_data = ImageData(path=self.resources_conf.bullet_image)
        self.bullet = Object(
            x=(self.window_conf.screen_width / 2.0) - (self.bullet_image_data.image_width / 2.0),
            y=self.window_conf.screen_height,
            x_change=0.0,
            y_change=3.0
        )
        self.is_bullet_moving = False

        self.running = True
        self.run()

    def run(self) -> None:

        # Main loop
        while self.running:

            # Fill background with image
            self.screen.blit(self.background_image_data.image, (0, 0))

            # Enable/disable laser
            if self.window_conf.laser:
                pygame.draw.line(
                    self.screen,
                    'red',
                    (self.player.x + (self.player_image_data.image_width / 2.0), 0),
                    (self.player.x + (self.player_image_data.image_width / 2.0), self.window_conf.screen_height)
                )

            # Clicking event
            for event in pygame.event.get():

                # Check quit
                if event.type == pygame.QUIT:
                    self.running = False

                # Key pressed and released
                if event.type == pygame.KEYDOWN:
                    # Left arrow
                    if event.key == pygame.K_LEFT:
                        self.player.x_change = -1.7  # Sensitive of Left Arrow
                    # Right arrow
                    if event.key == pygame.K_RIGHT:
                        self.player.x_change = 1.7  # Sensitive of Right Arrow
                    # Space
                    if event.key == pygame.K_SPACE:
                        # Check if bullet is not moving
                        if not self.is_bullet_moving:
                            player_image_half_width = self.player_image_data.image_width / 2.0
                            bullet_image_half_width = self.bullet_image_data.image_width / 2.0
                            self.bullet.x = self.player.x + player_image_half_width - bullet_image_half_width
                            self._blit_object(image=self.bullet_image_data.image, x=self.bullet.x, y=self.bullet.y)
                            self.is_bullet_moving = True
                            self._play_sound(filename=self.resources_conf.shoot_sound)
                # Key released
                if event.type == pygame.KEYUP:
                    self.player.x_change = 0.0

            # Update Score
            self.score.show_score()

            # Adding the change in the player position
            self.player.x += self.player.x_change
            # Adding the change in the invaders position
            for index, _ in enumerate(range(len(self.invaders))):
                self.invaders[index].x += self.invaders[index].x_change

            # Reset bullet if reach top border
            if self.bullet.y <= 0.0:
                self.bullet.y = self.window_conf.screen_height
                self.is_bullet_moving = False
            # Move and draw bullet
            if self.is_bullet_moving:
                self._blit_object(image=self.bullet_image_data.image, x=self.bullet.x, y=self.bullet.y)
                self.is_bullet_moving = True
                self.bullet.y -= self.bullet.y_change

            for index, _ in enumerate(range(len(self.invaders))):

                # Check if Invader touch Player
                collision_point = (
                    self.window_conf.screen_height
                    - self.player_image_data.image_height
                    - self.invader_image_data.image_height
                )
                if self.invaders[index].y >= collision_point:

                    left_corners_distance = abs(self.player.x - self.invaders[index].x)
                    left_sides_collision = (left_corners_distance <= self.invader_image_data.image_width)
                    right_sides_collision = (left_corners_distance <= self.player_image_data.image_width)
                    invader_from_left = (self.invaders[index].x_change > 0.0)
                    invader_from_right = (self.invaders[index].x_change < 0.0)

                    if (left_sides_collision and invader_from_left) or (right_sides_collision and invader_from_right):
                        for internal_index, _ in enumerate(range(len(self.invaders))):
                            self.invaders[internal_index].y = 2000.0
                            self._play_sound(filename=self.resources_conf.ufo_low_pitch_sound)
                        game_over_image_data = ImageData(path=self.resources_conf.game_over_image)
                        self._blit_object(
                            image=game_over_image_data.image,
                            x=(self.window_conf.screen_width / 2.0) - (game_over_image_data.image_width / 2.0),
                            y=(self.window_conf.screen_height / 2.0) - (game_over_image_data.image_height / 2.0)
                        )
                        break

                # Invader wall collision
                touch_right = (
                    self.invaders[index].x >= (self.window_conf.screen_width - self.invader_image_data.image_width)
                )
                touch_left = self.invaders[index].x <= 0.0
                if touch_right or touch_left:
                    self.invaders[index].x_change *= -1.0
                    self.invaders[index].y += self.invader_image_data.image_height

                # Check bullet invader collision
                if Utils.objects_collision(
                    x1=self.bullet.x,
                    x2=self.invaders[index].x,
                    y1=self.bullet.y,
                    y2=self.invaders[index].y,
                    image_data1=self.bullet_image_data,
                    image_data2=self.invader_image_data
                ):
                    self.score.value += 1
                    self.bullet.y = self.window_conf.screen_height
                    self.is_bullet_moving = False
                    self.invaders[index].x = random.randint(
                        0,
                        self.window_conf.screen_width - self.invader_image_data.image_width
                    )
                    self.invaders[index].y = random.randint(0, 0)
                    self.invaders[index].x_change *= -1.0

                # Draw Invader
                self._blit_object(
                    image=self.invader_image_data.image,
                    x=self.invaders[index].x,
                    y=self.invaders[index].y
                )

            # Player wall collision
            if self.player.x <= 0.0:
                self.player.x = 0.0
            elif self.player.x >= self.window_conf.screen_width - self.player_image_data.image_width:
                self.player.x = self.window_conf.screen_width - self.player_image_data.image_width

            # Draw Player
            self._blit_object(image=self.player_image_data.image, x=self.player.x, y=self.player.y)
            pygame.display.update()

    def _screen_settings(self) -> pygame.Surface:
        pygame.init()
        screen = pygame.display.set_mode((self.window_conf.screen_width, self.window_conf.screen_height))
        pygame.display.set_caption(self.window_conf.caption, self.window_conf.caption)
        return screen

    def _play_music(self, filename: str, loops: int) -> None:
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play(loops)

    def _play_sound(self, filename: str) -> None:
        sound = pygame.mixer.Sound(filename)
        sound.play()

    def _blit_object(self, image: pygame.Surface, x: float, y: float) -> None:
        self.screen.blit(image, (x, y))
