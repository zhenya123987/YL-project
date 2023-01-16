import os
import sys
import pygame

pygame.init()
size = WIDTH, HEIGHT = 300, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50
HP = 100
MONEY = 0
# основной персонаж
player = None
# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
barers_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, barers_group)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)
        else:
            super().__init__(tiles_group, all_sprites)
            self.image = tile_images[tile_type]
            self.rect = self.image.get_rect().move(
                tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, new_x, new_y):
        if pygame.sprite.spritecollideany(self, barers_group):
            return
        self.rect.x = new_x
        self.rect.y = new_y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Правила игры",
                  "Ваша задача - отыскать в",
                  "подземельях скрытые ",
                  "клады.",
                  "Нажмите влево вправо,",
                  "чтобы перемещаться.",
                  "Нажмите пробел, чтобы",
                  "копать вперед и вниз,",
                  "чтобы копать вниз"]

    fon = pygame.transform.scale(load_image('fon.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 10
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('orange'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('wall2.jpg'),
    'box': load_image('chest.png'),
    'empty': load_image('block.png'),
    'heart': load_image('heart.png')
}
player_image = load_image('hero1.png', color_key=-1)

tile_width = tile_height = 50


def generate_level(level):
    new_player, x, y = None, None, None
    #bckgr = pygame.transform.scale(load_image('backgr.png'), (100, 100))
    #screen.blit(bckgr, (100, 100))
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('box', x, y)
            elif level[y][x] == '&':
                Tile('heart', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


start_screen()
player, level_x, level_y = generate_level(load_level('level1.txt'))
camera = Camera()
running = True
dist = 50
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            player.move(player.rect.x, player.rect.y + dist)
        if key[pygame.K_UP]:
            player.move(player.rect.x, player.rect.y - dist)
        if key[pygame.K_LEFT]:
            player.move(player.rect.x - dist, player.rect.y)
        if key[pygame.K_RIGHT]:
            player.move(player.rect.x + dist, player.rect.y)
    screen.fill(pygame.Color("black"))
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    tiles_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update()
    pygame.display.flip()

pygame.quit()
