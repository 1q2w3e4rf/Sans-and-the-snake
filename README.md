# Игра "Змейка" с Сансом из Undertale

Этот код на Python использует Pygame для создания игры "Змейка" с тематикой Undertale, в которой Санс бросает кости в змейку.

## Разбор кода:

### 1. Подключение библиотек и инициализация:
import pygame
import random
import sys
import imageio
import numpy as np

pygame.init()
pygame.mixer.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Змейка с Сансом!")

Этот раздел импортирует необходимые библиотеки (Pygame для разработки игр, random для генерации случайных чисел, sys для системных функций, imageio для работы с GIF-файлами, numpy для работы с массивами), инициализирует Pygame и микшер (для звука), устанавливает размеры экрана и создает игровое окно с заголовком.

### 2. Цвета и настройки игры:
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

snake_block_size = 20
snake_speed = 10
snake_x = screen_width // 2
snake_y = screen_height - snake_block_size * 2
snake_x_change = 0
snake_y_change = 0
snake_list = []
snake_length = 1

food_x = round(random.randrange(0, screen_width - snake_block_size) / snake_block_size) * snake_block_size
food_y = round(random.randrange(screen_height // 2, screen_height - snake_block_size) / snake_block_size) * snake_block_size

Определяет цвета с помощью RGB-значений, устанавливает параметры для змейки (размер, скорость, начальное положение, переменные движения, список для хранения сегментов змейки), а также инициализирует случайное положение еды в игровой области.

### 3. Загрузка GIF Санса и обработка ошибок:
try:
    gif_reader = imageio.get_reader("sans.gif")
    sans_frames = []
    for frame in gif_reader:
        # ... (обработка и масштабирование кадра) ...
    gif_index = 0
    sans_width = sans_frames[0].get_width()
    sans_height = sans_frames[0].get_height()
    sans_x = 180
    sans_y = -95
except (FileNotFoundError, Exception) as e:
    print(f"Ошибка загрузки GIF: {e}")
    sys.exit(1)
Загружает GIF Санса с помощью imageio. Обрабатывает исключения FileNotFoundError и другие исключения при загрузке GIF, корректно завершая программу, если GIF не найден. Обрабатывает каждый кадр, масштабирует его при необходимости, чтобы он соответствовал экрану, поворачивает его и сохраняет кадры в списке.

### 4. Загрузка музыки и обработка ошибок:
try:
    pygame.mixer.music.load("sansmp.mp3")
    pygame.mixer.music.play(-1)
except pygame.error as e:
    print(f"Ошибка загрузки музыки: {e}")
Загружает и воспроизводит фоновую музыку. Включает обработку ошибок на случай, если музыкальный файл не найден или есть проблема с воспроизведением звука.

### 5. Функция отображения счета:
def display_score(score):
    font_style = pygame.font.SysFont(None, 30)
    value = font_style.render("Очки решимости: " + str(score), True, white)
    screen.blit(value, [0, 0])
Функция для отображения счета игрока на экране.

### 6. Загрузка изображения головы змейки и обработка ошибок:
try:
    heart_image = pygame.image.load("sans2.jpg")
    heart_image = pygame.transform.scale(heart_image, (snake_block_size, snake_block_size))
except pygame.error as e:
    print(f"{e}")
    heart_image = pygame.Surface((snake_block_size, snake_block_size))
    heart_image.fill(green)
Загружает изображение для головы змейки и масштабирует его соответствующим образом. Обрабатывает ошибки при загрузке изображения, создавая запасной зеленый квадрат, если изображение не найдено.

### 7. Параметры костей и загрузка изображения:
bone_size = 30
bone_speed = 5
bones = []

try:
    bone_image = pygame.image.load("rekikol.png").convert_alpha()
    bone_image = pygame.transform.scale(bone_image, (bone_size, bone_size))
except pygame.error as e:
    print(f"{e}")
    bone_image = pygame.Surface((bone_size, bone_size))
    bone_image.fill((255, 255, 0))
Устанавливает параметры для костей (размер, скорость, список для отслеживания активных костей) и загружает изображение кости с обработкой ошибок.

### 8. Функция броска кости:
def throw_bone():
    # ... (Вычисление позиции и угла кости) ...
    bones.append({'x': x, 'y': y, 'angle': target_angle, 'rect': pygame.Rect(x, y, bone_size, bone_size), 'original_image': bone_image.copy()})
Эта функция вычисляет случайную траекторию для кости, брошенной Сансом, нацеливаясь на змейку.

### 9. Функция отрисовки змейки:
def our_snake(snake_block_size, snake_list):
    for i, (x, y) in enumerate(snake_list):
        if i == 0:
            rotated_heart = pygame.transform.rotate(heart_image, get_snake_head_rotation(snake_list))
            rotated_rect = rotated_heart.get_rect(center=(x + snake_block_size // 2, y + snake_block_size // 2))
            screen.blit(rotated_heart, rotated_rect.topleft)
        else:
            pygame.draw.rect(screen, green, [x, y, snake_block_size, snake_block_size])
Рисует змейку на экране. Голова рисуется с помощью загруженного изображения, повернутого в зависимости от направления движения змейки.

### 10. Функция поворота головы змейки:
def get_snake_head_rotation(snake_list):
    # ... (Вычисление угла поворота головы змейки в зависимости от движения) ...
Вычисляет угол для поворота головы змейки в зависимости от ее направления движения.


### 11. Основной игровой цикл:
game_over = False
snake_direction = "RIGHT"
score = 0
bone_throw_timer = 0

while not game_over:
    # ... (Обработка событий, движение, отрисовка, обнаружение столкновений, обновление счета, механика броска и движения костей, условия окончания игры) ...
Основной игровой цикл обрабатывает события (ввод с клавиатуры, закрытие окна), обновляет положение змейки, рисует игровые элементы (Санс, змейка, еда, кости), проверяет столкновения (со стенами, самой собой или костями), обновляет счет и управляет механизмом броска костей.

### 12. Завершение Pygame:
pygame.quit()
sys.exit()
