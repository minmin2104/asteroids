from ship import Ship
import math
import pygame


class Main:
    def __init__(self, win_title, win_width, win_height, fps, screen_fill):
        pygame.init()
        self.__win_width = win_width
        self.__win_height = win_height
        self.__win_title = win_title
        self.__screen_fill = screen_fill
        self.screen = pygame.display.set_mode(
            (self.__win_width, self.__win_height))
        pygame.display.set_caption(self.__win_title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = fps
        self.dt = 0
        self.main()

    def main(self):

        ship = Ship(
            pygame.math.Vector2(self.screen.get_width() / 2,
                                self.screen.get_height() / 2),
            15,
            pygame.Color(255, 255, 255))

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.__screen_fill)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ship.rotate(-200 * self.dt)
            if keys[pygame.K_RIGHT]:
                ship.rotate(200 * self.dt)

            ship.update(self.dt)
            ship.render(self.screen)

            pygame.display.flip()

            self.dt = self.clock.tick(self.fps) / 1000


if __name__ == '__main__':
    Main('Asteroid', 800, 600, 60, 'black')
