# Подключение необходимых библиотек.  Это как импорт инструментов для работы.
import pygame
import random
import sys
import imageio
import numpy as np

# Инициализация Pygame.  Это как включение Pygame - библиотеки для создания игр.
pygame.init()
pygame.mixer.init()  # Инициализация микшера для музыки.

# Размеры игрового окна.
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height)) # Создаём окно игры.
pygame.display.set_caption("Snake with Sans!") # Задаём заголовок окна.

# Определение цветов.  RGB-значения.
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Настройки змейки.
snake_block_size = 20 # Размер одного блока змейки.
snake_speed = 10 # Скорость игры (кадров в секунду).
snake_x = screen_width // 2 # Начальное положение змейки по горизонтали (в центре).
snake_y = screen_height - snake_block_size * 2 # Начальное положение змейки по вертикали (внизу).
snake_x_change = 0 # Изменение координаты x при движении.
snake_y_change = 0 # Изменение координаты y при движении.
snake_list = [] # Список координат всех блоков змейки.
snake_length = 1 # Начальная длина змейки (один блок).

# Начальное положение еды.
food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size # Случайное положение еды по x, кратное размеру блока.
food_y = round(random.randrange(screen_height // 2, screen_height - snake_block_size) / snake_block_size) * snake_block_size # Случайное положение еды по y, кратное размеру блока, ниже середины экрана.

# Загрузка GIF-а Санса.  Обработка ошибок в случае, если файл не найден.
try:
    gif_reader = imageio.get_reader("sans.gif") # Читаем GIF-файл.
    sans_frames = [] # Список кадров анимации.
    for frame in gif_reader: # Проходим по всем кадрам GIF-а.
        frame = np.array(frame) # Преобразуем кадр в массив NumPy.
        frame = pygame.surfarray.make_surface(frame) # Преобразуем массив в поверхность Pygame.
        if frame.get_width() > screen_width or frame.get_height() > screen_height: # Проверяем, не слишком ли большой кадр.
            frame = pygame.transform.scale(frame, (screen_width // 2, screen_height // 2)) # Масштабируем, если нужно.
        frame = pygame.transform.rotate(frame, -90) # Поворачиваем кадр.
        sans_frames.append(frame) # Добавляем кадр в список.
    gif_index = 0 # Индекс текущего кадра.
    sans_width = sans_frames[0].get_width() # Ширина кадра.
    sans_height = sans_frames[0].get_height() # Высота кадра.
    sans_x = 180 # Положение Санса по x.
    sans_y = -95 # Положение Санса по y (сначала вне экрана).
except (FileNotFoundError, Exception) as e: # Обработка ошибок загрузки GIF-а.
    print(f"Ошибка загрузки GIF: {e}")
    sys.exit(1) # Завершаем программу, если GIF не загрузился.

# Загрузка музыки.  Обработка ошибок.
try:
    pygame.mixer.music.load("sansmp.mp3") # Загружаем музыкальный файл.
    pygame.mixer.music.play(-1) # Запускаем музыку в цикле.
except pygame.error as e: # Обработка ошибок загрузки музыки.
    print(f"Ошибка загрузки музыки: {e}")

# Объект для контроля времени.
clock = pygame.time.Clock()

# Функция для отображения счета.
def display_score(score):
    font_style = pygame.font.SysFont(None, 30) # Создаём шрифт.
    value = font_style.render("Очки решимости: " + str(score), True, white) # Рендерим текст счета.
    screen.blit(value, [0, 0]) # Отображаем текст на экране.

# Загрузка изображения для головы змейки. Обработка ошибок.
try:
    heart_image = pygame.image.load("soul.jpg") # Загрузка изображения сердца
    heart_image = pygame.transform.scale(heart_image, (snake_block_size, snake_block_size)) # Масштабирование под размер блока
except pygame.error as e:
    print(f"{e}")
    heart_image = pygame.Surface((snake_block_size, snake_block_size)) # Создание поверхности, если загрузка не удалась
    heart_image.fill(green) # Заливка зелёным цветом

# Параметры костей.
bone_size = 30 # Размер кости.
bone_speed = 5 # Скорость кости.
bones = [] # Список костей.

# Загрузка изображения кости. Обработка ошибок.
try:
    bone_image = pygame.image.load("bones.png").convert_alpha() # Загрузка изображения кости с альфа-каналом
    bone_image = pygame.transform.scale(bone_image, (bone_size, bone_size)) # Масштабирование
except pygame.error as e:
    print(f"{e}")
    bone_image = pygame.Surface((bone_size, bone_size)) # Создание поверхности, если загрузка не удалась
    bone_image.fill((255, 255, 0)) # Заливка жёлтым цветом

# Функция для "броска" кости.
def throw_bone():
    angle = random.uniform(0, 2 * np.pi) # Случайный угол для траектории кости.
    distance = random.randint(50, 150) # Случайное расстояние для траектории кости.
    x = sans_x + int(distance * np.cos(angle)) + sans_width // 2 - bone_size // 2 # Вычисляем координату x кости.
    y = sans_y + int(distance * np.sin(angle)) + sans_height // 2 - bone_size // 2 # Вычисляем координату y кости.
    target_angle = np.arctan2(snake_y - y, snake_x - x) # Вычисляем угол для попадания в змейку.
    bones.append({'x': x, 'y': y, 'angle': target_angle, 'rect': pygame.Rect(x, y, bone_size, bone_size), 'original_image': bone_image.copy()}) # Добавляем кость в список.

# Функция для отрисовки змейки.
def our_snake(snake_block_size, snake_list):
    for i, (x, y) in enumerate(snake_list): # Проходим по каждому блоку змейки.
        if i == 0: # Голова змейки.
            rotated_heart = pygame.transform.rotate(heart_image, get_snake_head_rotation(snake_list)) # Поворачиваем изображение головы в зависимости от направления движения.
            rotated_rect = rotated_heart.get_rect(center=(x + snake_block_size // 2, y + snake_block_size // 2)) # Центрируем изображение головы
            screen.blit(rotated_heart, rotated_rect.topleft) # Рисуем голову
        else: # Тело змейки.
            pygame.draw.rect(screen, green, [x, y, snake_block_size, snake_block_size]) # Рисуем прямоугольник.

# Функция для вычисления угла поворота головы змейки.
def get_snake_head_rotation(snake_list):
    if not snake_list:
        return 0
    head_x, head_y = snake_list[0]
    if len(snake_list) > 1:
        prev_x, prev_y = snake_list[1]
        dx = head_x - prev_x
        dy = head_y - prev_y
        angle = np.degrees(np.arctan2(dy, dx))
        return angle
    else:
        return 0

# Основной цикл игры.
game_over = False # Флаг окончания игры.
snake_direction = "RIGHT" # Начальное направление движения.
score = 0 # Счёт.
bone_throw_timer = 0 # Таймер для броска костей.


while not game_over: # Цикл продолжается, пока игра не закончилась.
    # Обработка событий (нажатия клавиш, закрытие окна).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            # Управление змейкой.
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                snake_x_change = -snake_block_size
                snake_y_change = 0
                snake_direction = "LEFT"
            elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                snake_x_change = snake_block_size
                snake_y_change = 0
                snake_direction = "RIGHT"
            elif event.key == pygame.K_UP and snake_direction != "DOWN":
                snake_y_change = -snake_block_size
                snake_x_change = 0
                snake_direction = "UP"
            elif event.key == pygame.K_DOWN and snake_direction != "UP":
                snake_y_change = snake_block_size
                snake_x_change = 0
                snake_direction = "DOWN"

    # Проверка на столкновение со стенами.
    if snake_x >= screen_width or snake_x < 0 or snake_y >= screen_height or snake_y < screen_height // 2:
        game_over = True
    # Обновление координат змейки.
    snake_x += snake_x_change
    snake_y += snake_y_change

    # Отрисовка всего на экране.
    screen.fill(black) # Заливка фона чёрным цветом.

    screen.blit(sans_frames[gif_index], (sans_x, sans_y)) # Отрисовка Санса.
    gif_index = (gif_index + 1) % len(sans_frames) # Переключение между кадрами анимации.

    pygame.draw.rect(screen, black, (0, screen_height // 2, screen_width, screen_height // 2), 0) # Рисуем чёрную область для игрового поля.
    pygame.draw.rect(screen, white, (0, screen_height // 2, screen_width, screen_height // 2), 5) # Рисуем белую рамку.

    pygame.draw.rect(screen, red, [food_x, food_y, snake_block_size, snake_block_size]) # Отрисовка еды.

    # Добавление головы змейки в список.
    snake_head = []
    snake_head.append(snake_x)
    snake_head.append(snake_y)
    snake_list.append(snake_head)

    # Удаление хвоста, если змейка увеличилась в длине.
    if len(snake_list) > snake_length:
        del snake_list[0]

    # Проверка на столкновение с самим собой.
    for x in snake_list[:-1]:
        if x == snake_head:
            game_over = True

    our_snake(snake_block_size, snake_list) # Отрисовка змейки.
    score = snake_length - 1 # Обновление счёта.
    display_score(score) # Отображение счёта.

    # Механика броска костей.
    bone_throw_timer += 1
    if bone_throw_timer > 60: # Бросаем кость каждые 60 кадров (примерно 1 секунду).
        throw_bone()
        bone_throw_timer = 0

    # Обновление положения костей, проверка на столкновение и удаление костей за пределами экрана.
    for bone in bones[:]: # Создаём копию списка, чтобы безопасно удалять элементы во время итерации.
        dx = bone_speed * np.cos(bone['angle']) # Изменение координаты x кости.
        dy = bone_speed * np.sin(bone['angle']) # Изменение координаты y кости.
        bone['x'] += dx
        bone['y'] += dy
        bone['rect'].x = bone['x']
        bone['rect'].y = bone['y']

        rotated_bone = pygame.transform.rotate(bone['original_image'], np.degrees(bone['angle'])) # Поворачиваем изображение кости.
        rotated_rect = rotated_bone.get_rect(center=bone['rect'].center) # Центрируем изображение кости

        if rotated_rect.colliderect(pygame.Rect(snake_x, snake_y, snake_block_size, snake_block_size)): # Проверка на столкновение с змейкой.
            game_over = True
            bones.remove(bone)

        if bone['x'] < -bone_size or bone['x'] > screen_width + bone_size or bone['y'] < -bone_size or bone['y'] > screen_height + bone_size: # Проверка на выход кости за пределы экрана.
            bones.remove(bone)

        screen.blit(rotated_bone, rotated_rect) # Отрисовка кости.

    pygame.display.update() # Обновление экрана.

    # Проверка на поедание еды.
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size # Генерация новой еды.
        food_y = round(random.randrange(screen_height // 2, screen_height - snake_block_size) / snake_block_size) * snake_block_size
        snake_length += 1 # Увеличение длины змейки.

    clock.tick(snake_speed) # Контроль скорости игры.

pygame.quit()
sys.exit()
