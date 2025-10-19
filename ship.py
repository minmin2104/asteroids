import pygame
import math


class Ship:
    def __init__(self, pos: pygame.math.Vector2,
                 center_distance, color, width=1):
        self.pos = pos
        self.width = width
        self.__center_distance = center_distance
        self.__corners = [
            # The front
            pygame.math.Vector2(self.pos.x, self.pos.y -
                                self.__center_distance),
            # Left side
            pygame.math.Vector2(self.pos.x - self.__center_distance,
                                self.pos.y + self.__center_distance),
            # Extrude inward
            self.pos,
            # Right side
            pygame.math.Vector2(self.pos.x + self.__center_distance,
                                self.pos.y + self.__center_distance),
        ]
        self.__base_corners = [
            pygame.math.Vector2(0, -self.__center_distance),
            pygame.math.Vector2(-self.__center_distance,
                                self.__center_distance),
            pygame.math.Vector2(0, 0),
            pygame.math.Vector2(self.__center_distance,
                                self.__center_distance),
        ]
        self.color = color
        self.rect = None
        self.angle = 0

    def rotate(self, rotation_speed):
        self.angle += math.radians(rotation_speed)
        for i, corner in enumerate(self.__base_corners.copy()):
            rotated_x = corner.x * \
                math.cos(self.angle) - corner.y * math.sin(self.angle)
            rotated_y = corner.x * \
                math.sin(self.angle) + corner.y * math.cos(self.angle)
            self.__corners[i].x = rotated_x + self.pos.x
            self.__corners[i].y = rotated_y + self.pos.y

    def move(self, speed):
        direction = self.pos - self.__corners[0]
        direction = direction.normalize()
        speed = -speed
        for i, p in enumerate(self.__corners.copy()):
            self.__corners[i].x += speed * direction.x
            self.__corners[i].y += speed * direction.y

    def update(self, dt):
        pass

    def render(self, screen):
        self.rect = pygame.draw.polygon(
            screen, self.color, self.__corners, self.width)
