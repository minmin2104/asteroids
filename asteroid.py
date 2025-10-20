import math
import random
import pygame


class Asteroid:
    def __init__(self, pos, direction, vertex_count, base_radius):
        self.__pos = pos  # Center
        self.__direction = direction
        self.__vertex_count = vertex_count
        self.__relative_vertices = [
            pygame.math.Vector2(0, 0) for i in range(vertex_count)
        ]
        self.__base_radius = base_radius
        self.__create()
        self.__absolute_vertices = [
            v + self.__pos for v in self.__relative_vertices
        ]

    def __create(self):
        angle_inc = 360 // self.__vertex_count
        angles = [a for a in range(
            0, angle_inc * self.__vertex_count, angle_inc)]
        angles = list(
            map(lambda a: a + (random.uniform(-0.10, 0.10) * angle_inc),
                angles))
        angles.sort()
        for i, vert in enumerate(self.__relative_vertices):
            radius_offset = random.uniform(-0.15, 0.15) * self.__base_radius
            radius = self.__base_radius + radius_offset
            x = radius * math.cos(math.radians(angles[i]))
            y = radius * math.sin(math.radians(angles[i]))
            vert.x = x
            vert.y = y

    def render(self, screen):
        pygame.draw.polygon(screen, 'white', self.__absolute_vertices, width=1)
