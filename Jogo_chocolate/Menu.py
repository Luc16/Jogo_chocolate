import pygame as pg


class Button:

    def __init__(self, x, y, width, height, callback, text='', text_color=(255, 255, 255)):

        self.img_normal = pg.Surface((100, 32))
        self.img_normal.fill(pg.Color(171, 0, 0))
        self.image_normal = pg.transform.scale(self.img_normal, (width, height))

        self.img_hover = pg.Surface((100, 32))
        self.img_hover.fill(pg.Color(128, 0, 0))
        self.image_hover = pg.transform.scale(self.img_hover, (width, height))

        self.img_down = pg.Surface((100, 32))
        self.img_down.fill(pg.Color(60, 0, 0))
        self.image_down = pg.transform.scale(self.img_down, (width, height))

        self.image = self.image_normal
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))

        self.font = pg.font.SysFont('Comic Sans MS', 60)

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
        self.start_button = Button(screen_width/2-65, screen_height/2-30, 150, 50, self.start, "Iniciar")
        self.font = pg.font.SysFont('Arial', 30, True)
        story_text = ["Carlinhos descobriu recentemente que é diabético",
                      "e agora o médico o proibiu de comer doces.",
                      "No entanto, ele tem tido sonhos estranhos com",
                      "chocolates e sempre que ele come muito nesses",
                      "sonhos ele acaba comendo na vida real.",
                      "Ajude Carlinhos a evitar o máximo de chocolates!!"]
        self.story = [self.font.render(text, True, (0, 0, 0)) for text in story_text]
        self.font_names = pg.font.SysFont('Arial', 10, True)
        names_text = ["Ana Luisa Holthausen de Carvalho",
                      "Gustavo Vieira Alcântara",
                      "João Pedro Carolino Morais",
                      "Luc Joffily Ribas",
                      "Philipe Medeiros Serra"]
        self.names = [self.font_names.render(name, True, (0, 0, 0)) for name in names_text]
        self.image = pg.image.load("images/menu.png")
        self.story_over = False
        self.proceed = False
        self.over = False

    def start(self):
        if self.story_over:
            self.over = True
        else:
            self.proceed = True

    def draw_menu(self, screen):
        if self.proceed and not self.story_over:
            screen.fill((0, 180, 255))
            for index, text in enumerate(self.story):
                screen.blit(text, (30, 45*index + 60))
            screen.blit(self.font_names.render("Feito por:", True, (0, 0, 0)), (30, 385))
            for index, name in enumerate(self.names):
                screen.blit(name, (30, 15*index + 400))
            screen.blit(self.font.render("Aperte enter para começar", True, (255, 0, 0)), (400, 450))
        else:
            screen.fill((0, 0, 0))
            screen.blit(self.image, (0, 0))
            screen.blit(self.start_button.image, (self.start_button.x, self.start_button.y))
        pg.display.flip()

    def run_menu(self, screen):
        while not self.over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if self.proceed:
                            self.story_over = True
                        self.start()
                self.start_button.handle_event(event)
            self.draw_menu(screen)
        return True


if __name__ == '__main__':
    pg.init()
    screen_h = 500
    screen_w = 800
    tela = pg.display.set_mode([screen_w, screen_h])
    menu = MainMenu(screen_w, screen_h)
    while not menu.over:
        for evento in pg.event.get():
            menu.start_button.handle_event(evento)
        menu.draw_menu(tela)
    pg.quit()
