# Игра "Змейка" с Сансом из Undertale

Этот код на Python использует Pygame для создания игры "Змейка" с тематикой Undertale, в которой Санс бросает кости в змейку.

## Разбор кода:

### 1. Подключение библиотек и инициализация:

Этот раздел импортирует необходимые библиотеки (Pygame для разработки игр, random для генерации случайных чисел, sys для системных функций, imageio для работы с GIF-файлами, numpy для работы с массивами), инициализирует Pygame и микшер (для звука), устанавливает размеры экрана и создает игровое окно с заголовком.

### 2. Цвета и настройки игры:

Определяет цвета с помощью RGB-значений, устанавливает параметры для змейки (размер, скорость, начальное положение, переменные движения, список для хранения сегментов змейки), а также инициализирует случайное положение еды в игровой области.

### 3. Загрузка GIF Санса и обработка ошибок:

Загружает GIF Санса с помощью imageio. Обрабатывает исключения FileNotFoundError и другие исключения при загрузке GIF, корректно завершая программу, если GIF не найден. Обрабатывает каждый кадр, масштабирует его при необходимости, чтобы он соответствовал экрану, поворачивает его и сохраняет кадры в списке.

### 4. Загрузка музыки и обработка ошибок:

Загружает и воспроизводит фоновую музыку. Включает обработку ошибок на случай, если музыкальный файл не найден или есть проблема с воспроизведением звука.

### 5. Функция отображения счета:

Функция для отображения счета игрока на экране.

### 6. Загрузка изображения головы змейки и обработка ошибок:

Загружает изображение для головы змейки и масштабирует его соответствующим образом. Обрабатывает ошибки при загрузке изображения, создавая запасной зеленый квадрат, если изображение не найдено.

### 7. Параметры костей и загрузка изображения:

Устанавливает параметры для костей (размер, скорость, список для отслеживания активных костей) и загружает изображение кости с обработкой ошибок.

### 8. Функция броска кости:

Эта функция вычисляет случайную траекторию для кости, брошенной Сансом, нацеливаясь на змейку.

### 9. Функция отрисовки змейки:

Рисует змейку на экране. Голова рисуется с помощью загруженного изображения, повернутого в зависимости от направления движения змейки.

### 10. Функция поворота головы змейки:

Вычисляет угол для поворота головы змейки в зависимости от ее направления движения.


### 11. Основной игровой цикл:

Основной игровой цикл обрабатывает события (ввод с клавиатуры, закрытие окна), обновляет положение змейки, рисует игровые элементы (Санс, змейка, еда, кости), проверяет столкновения (со стенами, самой собой или костями), обновляет счет и управляет механизмом броска костей.

### 12. Завершение Pygame:
pygame.quit()
sys.exit()
