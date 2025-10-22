from asteroid import Asteroid
from ship import Ship
import random
import pygame


class Game:
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

    def spawn_asteroid(self):
        edge = random.choice(['top', 'bottom', 'left', 'right'])

        if edge == 'top':
            pos_x = random.randint(0, self.__win_width)
            pos_y = -10
        elif edge == 'bottom':
            pos_x = random.randint(0, self.__win_width)
            pos_y = 10
        elif edge == 'left':
            pos_y = random.randint(0, self.__win_height)
            pos_x = -10
        else:
            pos_y = random.randint(0, self.__win_height)
            pos_x = 10

        pos = pygame.math.Vector2(pos_x, pos_y)
        mid_screen = pygame.math.Vector2(
            self.__win_width / 2, self.__win_height / 2)
        vec_to_mid = pos - mid_screen
        x_dir_offset = random.randint(-100, 100)
        y_dir_offset = random.randint(-100, 100)
        vec_to_mid.x += x_dir_offset
        vec_to_mid.y += y_dir_offset
        direction = vec_to_mid.normalize()
        vert_count = random.randint(8, 24)
        base_radius = random.randint(15, 60)
        speed = random.randint(90, 300)
        return Asteroid(pos, direction, vert_count, base_radius, speed)

    def main(self):

        ship = Ship(
            pygame.math.Vector2(self.screen.get_width() / 2,
                                self.screen.get_height() / 2),
            15,
            pygame.Color(255, 255, 255))

        asteroids = []
        last_spawn_time = 0
        spawn_cooldown = 2  # Second

        last_shot_time = 0
        game_time = 0
        shooting_cooldown = 0.5  # Second

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.__screen_fill)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                ship.move(200 * self.dt)
            if keys[pygame.K_LEFT]:
                ship.rotate(-200 * self.dt)
            if keys[pygame.K_RIGHT]:
                ship.rotate(200 * self.dt)
            if keys[pygame.K_x]:
                if game_time - \
                        last_shot_time >= shooting_cooldown:
                    ship.shoot()
                    last_shot_time = game_time

            ship.update(self.dt)
            ship.render(self.screen)

            if game_time - \
                    last_spawn_time >= spawn_cooldown:
                asteroid = self.spawn_asteroid()
                age = random.randint(15, 20)
                asteroids.append(
                    {'asteroid': asteroid, 'age': age, 'is_dead': False,
                     'timeout': game_time})
                last_spawn_time = game_time

            # Update asteroids
            for asteroid in asteroids:
                asteroid['asteroid'].move(self.dt)
                asteroid['asteroid'].render(self.screen)
                if game_time - asteroid['timeout'] >= asteroid['age']:
                    asteroid['is_dead'] = True

            asteroids[:] = [ast for ast in asteroids if not ast['is_dead']]
            print(len(asteroids))

            pygame.display.flip()

            self.dt = self.clock.tick(self.fps) / 1000
            game_time += self.dt

        pygame.quit()


if __name__ == '__main__':
    Game('Asteroid', 800, 600, 60, 'black')
