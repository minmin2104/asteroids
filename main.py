from ship import Ship
import pygame


class Main:
    def __init__(self, win_title, win_width, win_height, fps):
        pygame.init()
        self.__win_width = win_width
        self.__win_height = win_height
        self.__win_title = win_title
        self.screen = pygame.display.set_mode(
            (self.__win_width, self.__win_height))
        pygame.display.set_caption(self.__win_title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = fps
        self.game_loop()

    def game_loop(self):

        ship = Ship(
            pygame.math.Vector2(self.screen.get_width() / 2,
                                self.screen.get_height() / 2),
            15,
            pygame.Color(255, 255, 255))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill('purple')

            ship.render(self.screen)

            pygame.display.flip()

            self.clock.tick(self.fps)


if __name__ == '__main__':
    Main('Asteroid', 800, 600, 60)
