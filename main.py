from asteroid import Asteroid
from ship import Ship
import random
import pygame
import os


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

    def game_over(self):
        while self.game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state = "game_quit"
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.game_state = "playing"
                        self.init()

            game_over_surface = self.game_over_text.render(
                "GAME OVER", True, pygame.Color(255, 255, 255))
            game_over_rect = self.screen.blit(
                game_over_surface,
                (self.screen.get_width() / 2 -
                    game_over_surface.get_width() / 2,
                 self.screen.get_height() / 2 -
                 game_over_surface.get_height() / 2))

            restart_surface = self.restart_text.render(
                "Click anywhere to restart",
                True,
                pygame.Color(255, 255, 155)
            )
            self.screen.blit(restart_surface, (
                game_over_rect.x - restart_surface.get_height() / 2,
                game_over_rect.y + game_over_rect.height + 10))

            pygame.display.flip()

    def update_asteroid(self, asteroids, ship, game_time):
        for asteroid in asteroids:
            asteroid['asteroid'].move(self.dt)
            asteroid['asteroid'].render(self.screen)
            if game_time - asteroid['timeout'] >= asteroid['age']:
                asteroid['is_dead'] = True
            # Handle asteroid collision
            if ship.bullets:
                bullet_index = asteroid['asteroid'].collide_rects(
                    ship.bullets)
                if bullet_index > -1:
                    self.explode_sound.play()
                    ship.bullets_metadata[bullet_index]['is_dead'] = True
                    self.score += 1
                    asteroid['is_dead'] = True
            if ship:
                if asteroid['asteroid'].collide_rect(ship.rect):
                    print("YOU HIT A METEOR! LOST!")
                    pygame.mixer.music.stop()
                    self.ship_explode_sound.play()
                    self.game_state = "game_over"

    def init(self):
        self.music = os.path.join("assets", "bgm.mp3")
        pygame.mixer.init()
        pygame.mixer.music.load(self.music)
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.3)

        shot_sound_path = os.path.join("assets", "shot.mp3")
        self.shot_sound = pygame.mixer.Sound(shot_sound_path)

        explode_sound_path = os.path.join("assets", "explosion1.mp3")
        self.explode_sound = pygame.mixer.Sound(explode_sound_path)

        ship_explode_sound_path = os.path.join("assets", "ship_explode.mp3")
        self.ship_explode_sound = pygame.mixer.Sound(ship_explode_sound_path)

        pygame.font.init()
        retro_font = os.path.join("assets", "retro_gaming.ttf")
        self.score_text = pygame.font.Font(retro_font)
        self.score = 0

        self.game_state = "playing"
        self.game_over_text = pygame.font.Font(retro_font, size=72)
        self.restart_text = pygame.font.Font(retro_font, size=32)

        self.ship = Ship(
            pygame.math.Vector2(self.screen.get_width() / 2,
                                self.screen.get_height() / 2),
            15,
            pygame.Color(255, 255, 255))

        self.asteroids = []
        self.last_spawn_time = 0
        self.spawn_cooldown = 2  # Second

        self.last_shot_time = 0
        self.game_time = 0
        self.shooting_cooldown = 0.5  # Second

    def main(self):

        self.init()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(self.__screen_fill)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.ship.move(200 * self.dt)
            if keys[pygame.K_LEFT]:
                self.ship.rotate(-200 * self.dt)
            if keys[pygame.K_RIGHT]:
                self.ship.rotate(200 * self.dt)
            if keys[pygame.K_x]:
                if self.game_time - \
                        self.last_shot_time >= self.shooting_cooldown:
                    self.shot_sound.play()
                    self.ship.shoot()
                    self.last_shot_time = self.game_time

            self.ship.update(self.dt)
            self.ship.render(self.screen)

            if self.game_time - \
                    self.last_spawn_time >= self.spawn_cooldown:
                asteroid = self.spawn_asteroid()
                age = random.randint(15, 20)
                self.asteroids.append(
                    {'asteroid': asteroid, 'age': age, 'is_dead': False,
                     'timeout': self.game_time})
                self.last_spawn_time = self.game_time

            # Update self.asteroids
            self.update_asteroid(self.asteroids, self.ship, self.game_time)

            self.asteroids[:] = [
                ast for ast in self.asteroids if not ast['is_dead']]

            score_text_surface = self.score_text.render(
                f"Score: {self.score:0>4}", True, pygame.Color(255, 255, 255))

            self.screen.blit(
                score_text_surface, (self.screen.get_width() -
                                     score_text_surface.get_width() - 5, 5))

            self.game_over()

            pygame.display.flip()

            self.dt = self.clock.tick(self.fps) / 1000
            self.game_time += self.dt

        pygame.quit()


if __name__ == '__main__':
    Game('Asteroid', 800, 600, 60, 'black')
