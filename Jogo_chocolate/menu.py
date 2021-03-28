import pygame as pg


class Button:

    def __init__(self, x, y, width, height, callback, text='', text_color=(0, 0, 0)):

        self.img_normal = pg.Surface((100, 32))
        self.img_normal.fill(pg.Color("dodgerblue1"))
        self.image_normal = pg.transform.scale(self.img_normal, (width, height))

        self.img_hover = pg.Surface((100, 32))
        self.img_hover.fill(pg.Color("lightskyblue"))
        self.image_hover = pg.transform.scale(self.img_hover, (width, height))

        self.img_down = pg.Surface((100, 32))
        self.img_down.fill(pg.Color("aquamarine1"))
        self.image_down = pg.transform.scale(self.img_down, (width, height))

        self.image = self.image_normal
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))

        self.font = pg.font.SysFont('Comic Sans MS', 100)

        image_center = self.image.get_rect().center
        text_surf = self.font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)

        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
                self.callback()
        elif event.type == pg.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal
                self.button_down = False


class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.start_button = Button(screen_width/2-300, screen_height/2-150, 600, 300, self.start, "Start")
        self.over = False

    def start(self):
        self.over = True

    def draw_menu(self, screen):
        screen.fill((200, 150, 200))
        screen.blit(self.start_button.image, (self.start_button.x, self.start_button.y))
        pg.display.flip()

    def run_menu(self, screen):
        while not self.over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        self.start()
                self.start_button.handle_event(event)
            self.draw_menu(screen)
        return True


if __name__ == '__main__':
    pg.init()
    screen_h = 500
    screen_w = 800
    screen = pg.display.set_mode([screen_w, screen_h])
    menu = MainMenu(screen_w, screen_h)
    while not menu.over:
        for event in pg.event.get():
            menu.start_button.handle_event(event)
        menu.draw_menu(screen)
    pg.quit()
