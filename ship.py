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
        self.direction = pygame.math.Vector2()
        self.__angle = 0
        self.__bullet_speed = -400
        self.bullets_metadata = []
        self.bullets = []

    def rotate(self, rotation_speed):
        self.__angle += math.radians(rotation_speed)
        for i, corner in enumerate(self.__base_corners.copy()):
            rotated_x = corner.x * \
                math.cos(self.__angle) - corner.y * math.sin(self.__angle)
            rotated_y = corner.x * \
                math.sin(self.__angle) + corner.y * math.cos(self.__angle)
            self.__corners[i].x = rotated_x + self.pos.x
            self.__corners[i].y = rotated_y + self.pos.y

    def __get_direction(self):
        direction = self.pos - self.__corners[0]
        return direction.normalize()

    def move(self, speed):
        self.direction = self.__get_direction()
        speed = -speed
        for i, p in enumerate(self.__corners.copy()):
            self.__corners[i].x += speed * self.direction.x
            self.__corners[i].y += speed * self.direction.y

    def shoot(self):
        b_width = b_height = 2
        bullet = {
            "rect": pygame.Rect(
                self.__corners[0].x, self.__corners[0].y,
                b_width, b_height
            ),
            "direction": self.__get_direction(),
            "is_dead": False
        }
        self.bullets_metadata.append(bullet)

    def update(self, dt):
        for bullet in self.bullets_metadata:
            bullet_dir = bullet["direction"]
            bullet["rect"].x += (self.__bullet_speed *
                                 dt) * bullet_dir.x
            bullet["rect"].y += (self.__bullet_speed *
                                 dt) * bullet_dir.y

        self.bullets_metadata[:] = [
            b for b in self.bullets_metadata if not b["is_dead"]]

        self.bullets = [b['rect'] for b in self.bullets_metadata]

    def render(self, screen):
        self.rect = pygame.draw.polygon(
            screen, self.color, self.__corners, self.width)
        for bullet in self.bullets_metadata:
            bullet_rect = bullet["rect"]
            pygame.draw.rect(screen, 'white', bullet_rect)
            if (bullet_rect.x >= screen.get_width()
                    or bullet_rect.x + bullet_rect.width < 0) \
                    or (bullet_rect.y >= screen.get_height()
                        or bullet_rect.y + bullet_rect.width < 0):
                bullet["is_dead"] = True
