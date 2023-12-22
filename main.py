import pygame
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, \
    QMainWindow, QLabel, QLineEdit, QComboBox, QPlainTextEdit


a = False
level = 0
start = False


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)

        self.layout = QVBoxLayout()
        self.comboBox = QComboBox()
        a = ['уровень 1', 'уровень 2', 'уровень 3']
        for i in a:
            self.comboBox.addItem(i)
        self.layout.addWidget(self.comboBox)
        self.comboBox.currentIndexChanged.connect(self.Levl)

        self.addButton = QPushButton('начать игру')
        self.layout.addWidget(self.addButton)

        self.setLayout(self.layout)
        self.addButton.clicked.connect(self.Start)

    def Start(self):
        global start
        start = True

    def Levl(self, i):
        global level
        level = i


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.x = x
        self.y = y
        self.image = pygame.Surface([20, 20])
        self.image.fill((0, 0, 255))
        self.rect = pygame.Rect(x, y, 20, 20)

    def update(self):
        global a
        if not pygame.sprite.spritecollideany(self, bord):
            self.rect = self.rect.move(0, 1)
        if pygame.sprite.spritecollideany(self, forester):
            self.rect = self.rect.move(0, -1)
            a = True
        elif not pygame.sprite.spritecollideany(self, forester):
            a = False

    def remo(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def finding(self, m):
        self.rect = self.rect.move(m, 0)

    def finding1(self, m):
        self.rect = self.rect.move(0, m)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(bord)
        self.image = pygame.Surface([50, 10])
        self.image.fill((129, 129, 129))
        self.rect = pygame.Rect(x1, y1, 50, 10)


class Forester(pygame.sprite.Sprite):
    def __init__(self, x1, y1):
        super().__init__(all_sprites)
        self.add(forester)
        self.image = pygame.Surface([10, 50])
        self.image.fill((255, 0, 0))
        self.rect = pygame.Rect(x1, y1, 10, 50)


if __name__ == '__main__':
    pygame.init()
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    pygame.display.set_caption('Платформы')
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    screen.fill((0, 0, 0))
    running = True
    all_sprites = pygame.sprite.Group()
    bord = pygame.sprite.Group()
    forester = pygame.sprite.Group()
    clock = pygame.time.Clock()
    b = False
    f = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    f = True
            if event.type == pygame.MOUSEBUTTONDOWN and f:
                if event.button == 1:
                    x, y = event.pos
                    Forester(x, y)
                    f = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    Border(x, y)
                elif event.button == 3:
                    x, y = event.pos
                    if not b:
                        a0 = Ball(x, y)
                        b = not b
                    else:
                        a0.remo(x, y)
            if event.type == pygame.KEYDOWN:
                if event.key == 1073741906:
                    a0.finding1(-20)
                if a:
                    if event.key == 1073741906:
                        a0.finding1(-10)
                    if event.key == 1073741905:
                        a0.finding1(10)
                if event.key == 1073741903:
                    a0.finding(10)
                if event.key == 1073741904:
                    a0.finding(-10)
        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(50)
