import pygame


class Ship:
    def __init__(self, pos: pygame.math.Vector2, center_distance, color, width=1):
        self.pos = pos
        self.width = width
        self.__center_distance = center_distance
        self.__corners = [
            pygame.math.Vector2(self.pos.x, self.pos.y - self.__center_distance),
            pygame.math.Vector2(self.pos.x - self.__center_distance, self.pos.y + self.__center_distance),
            pygame.math.Vector2(self.pos.x + self.__center_distance, self.pos.y + self.__center_distance),            
        ]
        self.color = color
        self.rect = None

    def render(self, screen):
        self.rect = pygame.draw.polygon(screen, self.color, self.__corners, self.width)
