# coding=utf-8

# //////////////////
# ФАЙЛ СОБЫТИЙ ИГРЫ
# //////////////////

import sqlite3
import time

from sprites import *
from os import *
import sys
from image import load_image


lvl = 1  # Указываем начальный уровень


def show_energy_bar(energy):   # Функция отрисовки шкалы энергии
    color = 2.55 * energy

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -1 * energy))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110), 2)


def show_shooting_bar(shooting):  # Функция отрисовки шкалы количества пуль
    color = 5.1 * shooting

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -1 * shooting * 2))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110), 2)


def lost_game():  # Функция отрисовки фона при проигрыше
    intro_sound.play()  # Включаем музыку
    img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)  # Получаем фон
    show_image(img)  # Отображаем фон


def won_game(score_top, kill_enemy):  # Функция отрисовки фона при победе
    intro_sound.play()  # Включаем музыку
    global lvl
    if lvl < 8:  # Проверка на уровень дает понять, конец ли игры или нужно задать новый уровень
        lvl += 1
        new_data(lvl, score_top, kill_enemy)  # Сохраняем новые данные в базу данных
        img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)  # Получаем фон
        show_image(img)  # Отображаем фон
    else:  # Обнуляем уровни, игра закончилась, но можно продолжить играть поновой
        lvl = 1
        new_data(lvl, score_top, kill_enemy)  # Сохраняем новые данные в базу данных
        img = load_image(path.join('static', 'img', 'background', 'end.jpg'), True, DISPLAYMODE)  # Получаем фон
        show_image(img)  # Отображаем фон


def exit_game():  # Функция выхода из игры
    pygame.quit()
    sys.exit()


def pause_game():  # Функция выхода из игры
    # Получаем фон
    img = load_image(path.join('static', 'img', f'level_{lvl}', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img, (0, 0))   # Отображаем фон

    pause = True
    # Пока пользователь не нажмет на кнопку P, он не выйдет из паузы
    # Но пользователь может выйти из игры
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                if event.key == pygame.K_p:
                    pause = False
        pygame.display.update()


def wait_for_keystroke_menu():  # Функция клавиш меню
    # Пока пользователь не начнет игру, пока не нажмет на BACK
    # Но пользователь может выйти из игры
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return


def show_info():  # Функция отображения информации события
    img = load_image(path.join('static', 'img',  f'level_{lvl}', 'background', 'background_help.jpg'),
                     True, DISPLAYMODE)  # Получаем фон
    show_image(img)  # Отображаем фон


def show_help():  # Функция отображения подсказки
    img = load_image(path.join('static', 'img', 'background', 'background_help.jpg'), True, DISPLAYMODE)  # Получаем фон
    show_image(img)  # Отображаем фон


def show_image(img):  # Функция отображения фона
    window.blit(img, (0, 0))  # Устонавливаем фон
    pygame.display.update()  # Обновляем дисплей
    wait_for_keystroke_menu()  # Предоставляем пользователю воспользоваться меню


def update_sprites():  # Функция обновления спрайтов
    player = Player()  # Создаем игрока
    player_team = pygame.sprite.RenderUpdates(player)
    group_shooting_player = pygame.sprite.RenderUpdates()   # Создаем пули игрока

    enemy = Enemy(lvl)  # Создаем врага
    enemy_team = pygame.sprite.RenderUpdates()

    return enemy, enemy_team, player, player_team, group_shooting_player


def menu_new_game():  # Функция отображения новой игры
    pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)
    music_channel.play(intro_sound, loops=-1, maxtime=0, fade_ms=0)  # Включаем музыку
    img = load_image(path.join('static', 'img', 'background', 'background.jpg'), True, DISPLAYMODE)  # Получаем фон
    show_image(img)  # Отображаем фон
    music_channel.stop()  # Выключаем музыку


def new_data(lvl, score_top, kill_enemy):  # Функция сохранения новых значений в базу данный
    con = sqlite3.connect(path.join('db', 'player data.db'))
    cur = con.cursor()
    cur.execute("""INSERT INTO game (lvl, score_top, kill_enemy)  
                VALUES(?, ?, ?)""", (lvl, score_top, kill_enemy))  # Сохраняем все в базу данных
    con.commit()
    con.close()


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        menu_new_game()  # Отображаем меню
        self.time = pygame.time.Clock()  # Создаем объект времени

    def run(self):
        global lvl
        delay_shooting, fps_shooting, kill_enemy, score_top = 0, 0, 0, 0   # Начальные данные игры
        time_elapsed = time.clock()
        con = sqlite3.connect(path.join('db', 'player data.db'))
        cur = con.cursor()
        result = cur.execute('''SELECT lvl, score_top, kill_enemy FROM game
                                    WHERE ID = (SELECT MAX(ID) FROM game)''')  # Забираем последние данные из базы
        for elem in result:
            lvl = elem[0]  # Текущий уровень
            score_top = elem[1]  # Лучший счет
            kill_enemy = elem[2]  # Количество уничтоженых дроидов
        con.commit()
        con.close()

        while True:  # Цикл уровня
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            energy = INIT_ENERGY  # Получаем количество энергии (энергия конаетсс, но не возобновляется)
            enemy, enemy_team, player, player_team, group_shooting_player = update_sprites()   # Обновляю спрайты
            background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background', 'background_1.jpg'),
                                         True, DISPLAYMODE)  # Устонавливаю фон уровня

            group_explosion = pygame.sprite.RenderUpdates()  # Создаю группу взрывов

            check_on_press_keys = True  # Пока равен true, то пользователь может нажимать клавиши
            count_shooting = COUNT_SHOOTING  # Получаю количество пуль (возобновляемые)

            # Меню игрока
            score_box = TextBox("Счёт: {}".format(kill_enemy), font_1, (10, 10))  # Счета
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, (10, 50))  # Ввремя
            lvl_box = TextBox("Уровень: {}".format(lvl), font_1, (10, 80))  # Уровень

            # Информация
            text_info = TextBox("   Нажмите:", font_2, (10, WINDOW_HEIGHT - 160))
            text_esc = TextBox("+ ESC - Выход из игры", font_2, (10, WINDOW_HEIGHT - 120))
            text_f1 = TextBox("+ F2 - Справка", font_2, (10, WINDOW_HEIGHT - 80))
            text_p = TextBox("+ P - Пауза, с инфомацией сражения", font_2, (10, WINDOW_HEIGHT - 40))
            # Группа текста
            group_box = pygame.sprite.RenderUpdates(score_box, lvl_box, time_box, text_esc, text_info, text_f1, text_p)

            while True:  # Цикл действий игры
                window.blit(background_game, (0, 0))  # Отображаю фон
                if check_on_press_keys:  # Клавиши
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:  # Выход
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:  # Информация
                                show_info()
                                # Отнимаю время, которое пользователь находился в информации
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_p:  # Пауза
                                pause_game()
                                # Отнимаю время, которое пользователь находился в паузе
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_F2:  # Помощь
                                show_help()
                                # Отнимаю время, которое пользователь находился в помощи
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_SPACE:  # При каждом нажатии убираем задержку выстрела
                                delay_shooting = 9
                            if event.key == pygame.K_n:  # Новая игра
                                # Обнуляем и сохраняем данные, удоляем врагов
                                start_time = time.clock()
                                lvl, score_top, kill_enemy, energy = 1, 0, 0, INIT_ENERGY
                                new_data(lvl, score_top, kill_enemy)
                                enemy.kill()
                                for enemy in enemy_team:
                                    enemy.kill()
                                background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background',
                                                                       'background_1.jpg'),
                                                             True, DISPLAYMODE)  # Меняем фон
                                menu_new_game()  # Подключаем меню новой игры
                        elif event.type == pygame.KEYUP:
                            # Постоянно обнуляем, иначе будет ездить туда сюда =)
                            player.y_speed = 0

                    key_pressed = pygame.key.get_pressed()
                    # Меняем положение игрок в соответствии с нажатыми клавишами
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:  # Вверх
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:  # Вниз
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:  # Стреляем
                        delay_shooting += 1  # Умеличиваем задержку
                        fps_shooting = 0  # Обнуляем fps (количество кадров в секунду для выстрела)
                        if delay_shooting == 10 and count_shooting - 1 > 0:
                            shooting_player.play()  # Создаем выстрел
                            group_shooting_player.add(PlayerShooting(player.rect.midtop))  # Добавляем его в группу
                            delay_shooting = 0  # Обнуляем задержку
                            count_shooting -= 1  # Уменьшаем количество выстрелов
                    else:
                        fps_shooting += 1  # Увеличиваем fps (количество кадров в секунду для выстрела)
                        if fps_shooting == 25 and count_shooting < COUNT_SHOOTING:  # Это сделано для плавного выстрелов
                            count_shooting += 1  # Увеличиваем количество выстрелов
                            fps_shooting = 0  # Обнуляем fps (количество кадров в секунду для выстрела)

                if len(enemy_team) < MAX_NUMBER_ENEMY:  # Проверяем на не привышение количества врагов на экране
                    if random.randint(0, 50) == 0:  # Появляется случайно
                        enemy_team.add(Enemy(lvl))  # Создается враг

                if energy <= 0 and check_on_press_keys:  # Если энергия кончилась, то нужно убить игрока
                    check_on_press_keys = False  # Теперь нельзя пользоваться игровыми клавишами
                    group_explosion.add(Explosion(player.rect))  # Взрыв на месте игрока
                    player.kill()  # Удаляем игрока

                # Считаем время
                if not time.clock():
                    time_current = time.perf_counter()
                else:
                    time_current = time.clock()
                # Устонавливаем конечное время
                time_elapsed = time_current - start_time

                check = False
                # Провиряем на проигрыш (если враг дошел до края границы, то наш лагерь пал)
                for enemy in enemy_team:
                    if enemy.rect.right <= 0 and lvl != 3:  # У всех уровней край это 0
                        check = True
                    elif lvl == 3 and enemy.rect.right <= 250:  # Но на 3 край рабен 250,
                        # потому что корабли не умеют ходить по суше =)
                        check = True
                if check:  # Если что-то из выше написанного произошло, то удоляем игрока и вызываем фон проигрыша
                    kill_enemy = 0  # Также обнуляется количество убитых врагов
                    explosion_player.play()
                    player.kill()
                    lost_game()
                    break  # Выходим во внешний цикл

                # =========================
                # ОБРАБОТКА СТОЛКНОВЕНИЙ
                # =========================

                # Пуля попала в игрока
                for player in pygame.sprite.groupcollide(player_team, group_shooting_enemy, False, True):
                    hit_player.play()  # Включаем звук попадения
                    energy -= 5  # Отнимаем из энергии 5

                # Пуля попала во врага
                for enemy in pygame.sprite.groupcollide(enemy_team, group_shooting_player, True, True):
                    explosion_enemy.play()  # Взрыв на месте врага
                    group_explosion.add(Explosion(enemy.rect))
                    kill_enemy += 1  # Увеличиваем количество убитых

                    # Если количество убитых равно COUNT_ENEMY_LVL * lvl, то мы выйграли
                    if kill_enemy >= COUNT_ENEMY_LVL * lvl:
                        enemy.kill()  # Убиваем врагов
                        for enemy in enemy_team:
                            enemy.kill()

                        won_game(score_top, kill_enemy)
                        background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background',
                                                               'background_1.jpg'),
                                                     True, DISPLAYMODE)  # Получаем фон

                # =============================
                # ОБНОВЛЯЕМ ВСЕ ГРУППЫ
                # =============================

                enemy_team.update()
                player_team.update()
                group_shooting_player.update()
                group_explosion.update()
                group_shooting_enemy.update()
                group_box.update()

                # =======================
                # ОЧИЩАЕМ СПРАЙТЫ
                # =======================

                enemy_team.clear(window, background_game)
                player_team.clear(window, background_game)
                group_shooting_player.clear(window, background_game)
                group_explosion.clear(window, background_game)
                group_shooting_enemy.clear(window, background_game)
                group_box.clear(window, background_game)

                enemy_team.draw(window)
                player_team.draw(window)
                group_shooting_player.draw(window)
                group_explosion.draw(window)
                group_shooting_enemy.draw(window)
                group_box.draw(window)

                # Вносим новые значения в меню игрока
                score_box.text = "Счёт: {}".format(kill_enemy)
                time_box.text = "Время: %.2f" % time_elapsed
                lvl_box.text = "Уровень: {}".format(lvl)

                if energy < 0:
                    energy = 0
                show_energy_bar(energy)
                show_shooting_bar(count_shooting)
                pygame.display.update()
                self.time.tick(FPS)
            if kill_enemy > score_top:  # Мы проверяем, превышает ли он лучший результат
                score_top = kill_enemy
            menu_new_game()
