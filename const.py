# coding=utf-8

# //////////////////
# ФАЙЛ КОНСТАНТ
# //////////////////

import pygame
import os


# Функция подключения файлов со звуком
def load_sound(filename, sound_lvl=1.0):
    path = os.path.join('static', 'sound', filename)  # Получаем путь к файлу
    sound = pygame.mixer.Sound(path)  # Загрузка мелодий
    sound.set_volume(sound_lvl)  # Настройка громкости звука
    return sound


# инициализация Pygame:
pygame.init()

# Размеры изображения врага
LENGTH_ENEMY = 52
WIDTH_ENEMY = 35

# Размеры изображения врага в стельбе
LENGTH_ENEMY_SHOOTING = 51
WIDTH_ENEMY_SHOOTING = 61

# Размеры изображения пули врага
LENGTH_SHOOTING_ENEMY = 15
WIDTH_SHOOTING_ENEMY = 25

# Размеры изображения игрока
LENGTH_PLAYER = 95
WIDTH_PLAYER = 89

# Размеры изображения пули игрока
LENGTH_SHOOTING = 17
WIDTH_SHOOTING = 12

# Размеры изображения взрыва
LENGTH_EXPLOSION = 64
WIDTH_EXPLOSION = 60

# Размеры экрана игры
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
DISPLAYMODE = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(DISPLAYMODE)  # Устанавливаю размер экрана

# Количество энергии игрока
INIT_ENERGY = 100

# Количество fps
FPS = 40

RATE_ENEMY_SPEED = 2  # Устанавливаю скорость врага
RATE_PLAYER_SPEED = 3  # Устанавливаю скорость игрока

DELAY = 5  # Устанавливаю задержку смены изображений

MAX_NUMBER_ENEMY = 5  # Устанавливаю максимальное количество врагов на экране (в один момент времени)

COUNT_SHOOTING = 50  # Максимальное количество пуль у игрока
COUNT_ENEMY_LVL = 10  # Устанавливаю старотовое количество врагов (1 ураовень => 10)

# Устанавливаю количество кадров у спрайтов
COUNT_EXPLOSION = 4
COUNT_ENEMY = 17
COUNT_PLAYER = 2
COUNT_SHOOTING_PLAYER = 4
COUNT_SHOOTING_ENEMY = 2

# =======
# ШРИФТЫ
# =======

TEXT_COLOR = (255, 255, 255)  # Цвет шрифта белый
font_1 = pygame.font.SysFont("Impact", 22)  # Устанавливаю название и размер шрифта №1
font_2 = pygame.font.SysFont("Impact", 15)  # Устанавливаю название и размер шрифта №2

# =======
# ЗВУКИ
# =======
intro_sound = load_sound('intro.ogg', 0.3)  # Звук заставки
explosion_enemy = load_sound('explosion_enemy.ogg', 0.3)  # Звук взрыва врага
shooting_player = load_sound("shooting_player.ogg", 0.3)  # Звук стрельбы игрока
shooting_enemy = load_sound('shooting_enemy.ogg', 0.3)  # Звук стрельбы врага
explosion_player = load_sound("explosion_player.ogg", 0.3)  # Звук взрыва игрока
hit_player = load_sound("hit_player.ogg", 0.3)  # Звук попадения пули врага в игрока

music_channel = pygame.mixer.Channel(4)
