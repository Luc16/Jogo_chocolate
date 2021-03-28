import pygame as pg
import random
import Menu
from pygame.locals import *
import math


class Background:
    def __init__(self, surface, b_type, x=0, right=False):
        self.x = x
        self.y = 0
        self.b_type = b_type
        if b_type == "margin":
            files = ["images/umpalumpas.png", "images/ovo.png", "images/Caminho de biscoito.png", "images/arvore.png"]
            self.images = [pg.transform.flip(pg.image.load(file), right, False) for file in files]
            self.height = self.images[0].get_height()
            self.img_idx = [x % len(files) for x in range((pg.display.get_surface().get_height() // self.height) + 2)]
        else:
            files = ["images/fundo.png"]
            self.images = [pg.transform.flip(pg.image.load(file), right, False) for file in files]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.surface = surface
        self.speed = 5

    def move(self):
        self.y += self.speed

    def draw(self):

        if self.b_type == "margin":
            for index, value in enumerate(self.img_idx):
                self.surface.blit(self.images[value], (self.x, self.y + self.height * index, self.width, self.height))

            if self.y + self.height >= self.height:
                self.img_idx.insert(0, self.img_idx[-1])
                del self.img_idx[-1]
                self.y = -self.height
        else:
            self.surface.blit(self.images[0], (self.x, self.y, self.width, self.height))

            if self.y >= self.height:
                self.y = 0

            self.surface.blit(self.images[0], (self.x, self.y, self.width, self.height))

            if self.y > 0:
                self.surface.blit(self.images[0], (self.x, self.y - self.height, self.width, self.height))

            if self.y + self.height < self.height:
                self.surface.blit(self.images[0], (self.x, self.y + self.height, self.width, self.height))


class Player:

    def __init__(self):
        self.x = 400
        self.y = 250
        self.width = 30
        self.height = 60
        self.speed = 5
        self.live = True
        self.count = 0
        self.collision_rect = Rect((self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
        self.images = [pg.image.load("images/remo_frente.png"), pg.image.load("images/remo_tras.png")]

    def move(self, keys):
        if self.live:
            if keys[pg.K_a]:
                self.x -= self.speed
            elif keys[pg.K_d]:
                self.x += self.speed
            if keys[pg.K_w]:
                self.y -= self.speed
            elif keys[pg.K_s]:
                self.y += self.speed

    def collide_map(self, screen_width, screen_height, margin):
        # colisão lado
        edge = margin * screen_width + self.width / 2
        if self.x < edge:
            self.x = edge
        elif self.x > screen_width - edge:
            self.x = screen_width - edge
        # colisão y
        if self.y > 0.9 * screen_height:
            self.y = 0.9 * screen_height
        elif self.y < 0.1 * screen_height:
            self.y = 0.1 * screen_height

    def draw_player(self, screen):
        if self.live:
            self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2
            if self.count > 24:
                self.count = 0
            if self.count < 12:
                screen.blit(self.images[0], (self.x - self.width / 2 - 15, self.y - self.height / 2 - 16))
            else:
                screen.blit(self.images[1], (self.x - self.width / 2 - 15, self.y - self.height / 2 - 16))
            self.count += 1

    def collide_chocolate(self, chocolate):
        if self.collision_rect.colliderect(chocolate.collision_rect):
            if not chocolate.choc_type == "beneath":
                self.live = False
            else:
                if chocolate.awake:
                    self.live = False

    def collide_power_up(self, power_up):
        if self.collision_rect.colliderect(power_up.collision_rect):
            power_up.caught = True


class Chocolate:

    def __init__(self, interval, screen_width, screen_height, choc_type):
        self.screen_height = screen_height
        self.speed = 5
        self.width = int(120 * screen_height / 1600)
        self.height = int(30 * screen_height / 1000)
        self.x = screen_width / 2
        self.y = -screen_height / 2
        self.live = True
        self.choc_type = choc_type
        self.image = pg.image.load("images/nestle.png")
        if self.choc_type == "fast":
            self.image = pg.image.load("images/alpino.png")
            self.speed += 4
        elif self.choc_type == "big":
            self.image = pg.image.load("images/toblerone.png")
            self.speed -= 2
            self.width = 150
            self.height = 50
        elif self.choc_type == "beneath":
            self.image = pg.image.load("images/diamante.png")
            self.image = pg.transform.scale(self.image, (self.width, self.height))
            self.x, self.y = 400, 250
            self.awake = False
            self.wait = 0
            self.created = False
        self.range = [interval[0] + self.width // 2, interval[1] - self.width // 2]
        self.collision_rect = Rect((self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))

    @staticmethod
    def blit_alpha(self, target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pg.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)
        target.blit(temp, location)

    def move(self):
        if self.live:
            if self.choc_type == "slow":
                self.y += self.speed
                if self.y > self.screen_height:
                    self.live = False
            elif self.choc_type == "fast":
                self.y += self.speed
                if self.y > self.screen_height * 1.5:
                    self.live = False
            elif self.choc_type == "big":
                self.y += self.speed
                if self.y > self.screen_height * 3:
                    self.live = False
            elif self.choc_type == "beneath":
                if self.awake:
                    self.y += self.speed
                if self.y > self.screen_height * 2:
                    self.awake = False
                    self.wait = 0
                    self.created = False
                    self.live = False

    def draw_chocolate(self, screen, count):
        if self.live:
            if self.choc_type == "slow":
                self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2
                screen.blit(self.image, (self.collision_rect.x, self.collision_rect.y))

            if self.choc_type == "fast":
                self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2
                screen.blit(self.image, (self.collision_rect.x, self.collision_rect.y))

            if self.choc_type == "big":
                self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2
                screen.blit(self.image, (self.collision_rect.x, self.collision_rect.y))

            if self.choc_type == "beneath":

                if not self.created:
                    self.created = True
                    self.wait = count
                # intervalo de 2sec para emergir
                if (self.choc_type == "beneath") and (count - self.wait >= 120) and self.live:
                    self.awake = True
                    screen.blit(self.image, (self.collision_rect.x, self.collision_rect.y))
                else:
                    self.blit_alpha(self, screen, self.image, (self.collision_rect.x, self.collision_rect.y), (count - self.wait)*2)

                self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2

    def refresh(self, exceptions):
        self.live = True
        collide = True
        while collide:
            self.x = random.randint(self.range[0], self.range[1])
            if self.choc_type == "beneath":
                self.y = random.randint(0, self.screen_height)
            else:
                self.y = random.randint(-self.screen_height, 0)
            self.collision_rect = Rect((self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
            collide = False
            for rec in exceptions:
                if rec.colliderect(self.collision_rect):
                    collide = True
                    break


class PowerUp:

    def __init__(self, interval, screen_height, pwu_type):
        self.range = interval
        self.screen_height = screen_height
        self.speed = 5
        self.width = 20
        self.height = 40
        self.x = random.randint(interval[0], interval[1] - self.width // 2)
        self.y = random.randint(-screen_height*3, -screen_height)
        self.live = True
        self.caught = False
        self.pwu_type = pwu_type
        self.image = pg.image.load("images/cenoura.png")
        self.collision_rect = Rect((self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
        self.time = 0

    def move(self):
        if self.pwu_type == "Cenoura":
            if self.y > self.screen_height:
                self.live = False
            self.y += self.speed

    def draw_power_up(self, screen):
        if self.live:
            if self.pwu_type == "Cenoura":
                self.collision_rect.x, self.collision_rect.y = self.x - self.width / 2, self.y - self.height / 2
                screen.blit(self.image, (self.collision_rect.x, self.collision_rect.y))

    def refresh(self, exceptions):
        self.live = True
        collide = True
        while collide:
            self.x = random.randint(self.range[0], self.range[1] - self.width // 2)
            self.y = random.randint(-self.screen_height * 5, -self.screen_height * 2)
            self.collision_rect = Rect((self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
            collide = False
            for rec in exceptions:
                if rec.colliderect(self.collision_rect):
                    collide = True
                    break


class Game:

    def __init__(self):
        self.playing = True
        self.screen_width = 800
        self.screen_height = 500
        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        self.menu = Menu.MainMenu(self.screen_width, self.screen_height)
        self.player = Player()
        self.margin = 3 / 16
        self.num_chocolates = 3
        self.counter = 0
        self.slowed = False
        self.time_slow = 0
        self.multiplier = 1
        self.font = pg.font.SysFont('Arial', 30, True)
        self.score = 0
        self.score_bar = self.font.render("Pontos:" + str(self.score), True, (0, 0, 0))
        self.file = open("max.txt")
        self.max_score = int(self.file.read())
        self.max_bar = self.font.render("Top:" + str(self.max_score), True, (0, 0, 0))
        self.file.close()
        self.background_river = Background(self.screen, "river", 0)
        self.background_margin_left = Background(self.screen, "margin")
        self.background_margin_right = Background(self.screen, "margin", int(self.screen_width * (1 - self.margin)),
                                                  right=True)
        self.clock = pg.time.Clock()
        self.power_up = PowerUp([self.margin * self.screen_width, self.screen_width - self.margin * self.screen_width],
                                self.screen_height, "Cenoura")
        self.chocolates = [
            Chocolate([self.margin * self.screen_width, self.screen_width - self.margin * self.screen_width],
                      self.screen_width, self.screen_height, "slow") for i in range(self.num_chocolates)]
        random.seed()

    def run(self):
        while self.playing:
            self.playing = self.menu.run_menu(self.screen)
            self.clock.tick(60)
            self.counter += 1
            self.handle_events()
            self.actions()
            self.draw()

    def refresh(self):
        ex = [x.collision_rect for x in self.chocolates]
        if not self.power_up.caught:
            self.power_up.move()
            if not self.power_up.live:
                self.power_up.refresh(ex)
            if self.power_up.y > self.screen_height:
                self.power_up.refresh(ex)
        for chocolate in self.chocolates:
            chocolate.move()
            if not chocolate.live:
                chocolate.refresh(ex)
                self.score += 1
                if self.score-2 > self.max_score:
                    self.max_score = self.score-2
                    self.file = open("max.txt", "w")
                    self.file.write(str(self.max_score))
                    self.file.close()
                    self.max_bar = self.font.render("Top:" + str(self.max_score), True, (0, 0, 0))
        if self.counter > 60 * self.multiplier * self.multiplier:
            chocs = ["slow", "fast", "big", "beneath"]
            if self.multiplier < 3:
                choc = chocs[0]
            elif self.multiplier < 8:
                val = random.randint(0, 3)
                choc = chocs[val]
            elif self.multiplier < 12:
                val = random.randint(1, 3)
                choc = chocs[val]
            else:
                val = random.randint(2, 3)
                choc = chocs[val]
            self.chocolates.append(
                Chocolate([self.margin * self.screen_width,
                           self.screen_width - self.margin * self.screen_width],
                          self.screen_width, self.screen_height, choc))
            self.multiplier += 1

    def actions(self):
        self.restart()
        self.player.collide_map(self.screen_width, self.screen_height, self.margin)
        self.refresh()
        self.background_river.move()
        self.background_margin_left.move()
        self.background_margin_right.move()
        self.score_bar = self.font.render("Pontos:" + str(max(0, self.score - 2)), True, (0, 0, 0))
        for chocolate in self.chocolates:
            self.player.collide_chocolate(chocolate)
        self.player.collide_power_up(self.power_up)
        self.carrot_effect()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
        self.player.move(pg.key.get_pressed())

    def restart(self):
        if not self.player.live:
            self.file.close()
            self.file = open("max.txt")
            self.max_score = int(self.file.read())
            self.max_bar = self.font.render("Top:" + str(self.max_score), True, (0, 0, 0))
            self.file.close()
            self.counter = 0
            self.multiplier = 1
            self.score = 0
            self.power_up.caught = False
            self.slowed = True
            self.time_slow = 0
            self.player.live = True
            self.chocolates = [Chocolate([self.margin * self.screen_width,
                                          self.screen_width - self.margin * self.screen_width],
                                         self.screen_width, self.screen_height,
                                         "slow") for i in range(self.num_chocolates)]
            self.menu.over = False

    def carrot_effect(self):
        if self.power_up.caught:
            if not self.slowed:
                self.slowed = True
                self.time_slow = self.counter
                self.background_river.speed = 3
                self.background_margin_left.speed = 3
                self.background_margin_right.speed = 3
                self.power_up.live = False
            for chocolate in self.chocolates:
                if chocolate.choc_type == "slow" or chocolate.choc_type == "beneath":
                    chocolate.speed = 3
                elif chocolate.choc_type == "big":
                    chocolate.speed = 1
                elif chocolate.choc_type == "fast":
                    chocolate.speed = 6
            if self.counter - self.time_slow == 420:
                self.power_up.caught = False
        else:
            if self.slowed:
                self.slowed = False
                for chocolate in self.chocolates:
                    if chocolate.choc_type == "slow" or chocolate.choc_type == "beneath":
                        chocolate.speed = 5
                    elif chocolate.choc_type == "big":
                        chocolate.speed = 3
                    elif chocolate.choc_type == "fast":
                        chocolate.speed = 9
                self.background_river.speed = 5
                self.background_margin_left.speed = 5
                self.background_margin_right.speed = 5

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.background_river.draw()
        self.background_margin_left.draw()
        self.background_margin_right.draw()
        # Barco
        self.player.draw_player(self.screen)
        # Chocolate
        self.power_up.draw_power_up(self.screen)
        for chocolate in self.chocolates:
            chocolate.draw_chocolate(self.screen, self.counter)

        pg.draw.rect(self.screen, (128, 176, 0), (0, 0, int(self.margin*self.screen_width), 40))
        self.screen.blit(self.score_bar, (0, 5))
        pg.draw.rect(self.screen, (128, 176, 0), (int((1-self.margin) * self.screen_width), 0, self.screen_width, 40))
        self.screen.blit(self.max_bar, ((1-self.margin) * self.screen_width, 5))
        pg.display.flip()


if __name__ == '__main__':
    pg.init()
    Game().run()
    pg.quit()
