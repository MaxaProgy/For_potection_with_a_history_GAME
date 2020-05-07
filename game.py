# coding=utf-8
import sqlite3
import time

from sprites import *
from os import *
import sys
from image import load_image


lvl = 1


def show_energy_bar(energy):
    color = 2.55 * energy

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -1 * energy))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 30, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 25, 30, -110), 2)


def show_shooting_bar(shooting):  # Шкала лазеров
    color = 5.1 * shooting

    color_rgb = (255 - color, color, 0)
    pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110))
    pygame.draw.rect(window, color_rgb, (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -1 * shooting * 2))

    for i in range(10):
        pygame.draw.rect(window, (0, 0, 0), (WINDOW_WIDTH - 30, WINDOW_HEIGHT - 140, 20, -10 * (i + 1)), 2)

    pygame.draw.rect(window, (255, 255, 255), (WINDOW_WIDTH - 35, WINDOW_HEIGHT - 135, 30, -110), 2)


def lost_game():
    intro_sound.play()
    img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)
    show_image(img)


def won_game(score_top, kill_enemy):
    intro_sound.play()
    global lvl
    if lvl < 8:
        lvl += 1
        new_data(lvl, score_top, kill_enemy)
        img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)
        show_image(img)
    else:
        lvl = 1
        new_data(lvl, score_top, kill_enemy)
        img = load_image(path.join('static', 'img', 'background', 'end.jpg'), True, DISPLAYMODE)
        show_image(img)


def exit_game():
    pygame.quit()
    sys.exit()


def pause_game():
    img = load_image(path.join('static', 'img', f'level_{lvl}', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img, (0, 0))

    pause = True
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


def wait_for_keystroke_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return


def show_info():
    img = load_image(path.join('static', 'img',  f'level_{lvl}', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    show_image(img)


def show_help():
    img = load_image(path.join('static', 'img', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    show_image(img)


def show_image(img):
    window.blit(img, (0, 0))
    pygame.display.update()
    wait_for_keystroke_menu()


def update_sprites():
    player = Player(lvl)
    player_team = pygame.sprite.RenderUpdates(player)
    group_shooting_player = pygame.sprite.RenderUpdates()

    enemy = Enemy(lvl)
    enemy_team = pygame.sprite.RenderUpdates()

    return enemy, enemy_team, player, player_team, group_shooting_player


def menu_new_game():
    pygame.mixer.init(frequency=22050, size=-16, channels=8, buffer=4096)
    music_channel.play(intro_sound, loops=-1, maxtime=0, fade_ms=0)
    img = load_image(path.join('static', 'img', 'background', 'background.jpg'), True, DISPLAYMODE)
    show_image(img)
    music_channel.stop()


def new_data(lvl, score_top, kill_enemy):
    con = sqlite3.connect(path.join('db', 'player data.db'))
    cur = con.cursor()
    cur.execute("""INSERT INTO game (lvl, score_top, kill_enemy)
                VALUES(?, ?, ?)""", (lvl, score_top, kill_enemy))
    con.commit()
    con.close()


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        menu_new_game()
        self.time = pygame.time.Clock()

    def run(self):
        global lvl
        delay_shooting, fps_shooting, kill_enemy, score_top = 0, 0, 0, 0
        time_elapsed = time.clock()
        con = sqlite3.connect(path.join('db', 'player data.db'))
        cur = con.cursor()
        result = cur.execute('''SELECT lvl, score_top, kill_enemy FROM game
                                    WHERE ID = (SELECT MAX(ID) FROM game)''')
        for elem in result:
            lvl = elem[0]  # Текущий уровень
            score_top = elem[1]  # Лучший счет
            kill_enemy = elem[2]  # Количество уничтоженых дроидов
        con.commit()
        con.close()

        while True:
            if not time.clock():
                start_time = time.perf_counter()
            else:
                start_time = time.clock()

            energy = INIT_ENERGY
            enemy, enemy_team, player, player_team, group_shooting_player = update_sprites()
            background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background', 'background_1.jpg'),
                                         True, DISPLAYMODE)

            group_explosion = pygame.sprite.RenderUpdates()

            check_on_press_keys = True
            count_shooting = COUNT_SHOOTING

            # Меню игрока
            score_box = TextBox("Счёт: {}".format(kill_enemy), font_1, 10, 10)
            time_box = TextBox("Время: {0:.2f}".format(start_time), font_1, 10, 50)
            lvl_box = TextBox("Уровень: {}".format(lvl), font_1, 10, 80)
            text_info = TextBox("   Нажмите:", font_2, 10, WINDOW_HEIGHT - 160)
            text_esc = TextBox("+ ESC - Выход из игры", font_2, 10, WINDOW_HEIGHT - 120)
            text_f1 = TextBox("+ F2 - Справка", font_2, 10, WINDOW_HEIGHT - 80)
            text_p = TextBox("+ P - Пауза, с инфомацией сражения", font_2, 10, WINDOW_HEIGHT - 40)

            group_box = pygame.sprite.RenderUpdates(score_box, lvl_box, time_box, text_esc, text_info, text_f1, text_p)

            while True:
                window.blit(background_game, (0, 0))
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:
                                show_info()
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_p:
                                pause_game()
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_F2:
                                show_help()
                                start_time = time.clock() - time_elapsed
                            if event.key == pygame.K_SPACE:
                                delay_shooting = 9
                            if event.key == pygame.K_n:
                                start_time = time.clock()
                                lvl, score_top, kill_enemy, energy = 1, 0, 0, INIT_ENERGY
                                new_data(lvl, score_top, kill_enemy)
                                enemy.kill()
                                for enemy in enemy_team:
                                    enemy.kill()
                                background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background',
                                                                       'background_1.jpg'),
                                                             True, DISPLAYMODE)
                                menu_new_game()
                        elif event.type == pygame.KEYUP:
                            player.y_speed = 0

                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:
                        delay_shooting += 1
                        fps_shooting = 0
                        if delay_shooting == 10 and count_shooting - 1 > 0:
                            shooting_player.play()
                            group_shooting_player.add(PlayerShooting(player.rect.midtop, lvl))
                            delay_shooting = 0
                            count_shooting -= 1
                    else:
                        fps_shooting += 1
                        if fps_shooting == 25 and count_shooting < COUNT_SHOOTING:
                            count_shooting += 1
                            fps_shooting = 0

                if len(enemy_team) < MAX_NUMBER_ENEMY:
                    if random.randint(0, 50) == 0:
                        enemy_team.add(Enemy(lvl))

                if energy <= 0 and check_on_press_keys:
                    check_on_press_keys = False
                    group_explosion.add(Explosion(player.rect))
                    player.kill()

                # Считаем время
                if not time.clock():
                    time_current = time.perf_counter()
                else:
                    time_current = time.clock()
                # Устонавливаем конечное время
                time_elapsed = time_current - start_time

                check = False
                for enemy in enemy_team:
                    if enemy.rect.right <= 0 and lvl != 3:
                        check = True
                    elif lvl == 3 and enemy.rect.right <= 250:
                        check = True
                if check:
                    kill_enemy = 0
                    explosion_player.play()
                    player.kill()
                    lost_game()
                    break

                # =========================
                # СПРАЙТ СТОЛКНОВЕНИЯ
                # =========================

                for player in pygame.sprite.groupcollide(player_team, group_shooting_enemy, False, True):
                    hit_player.play()
                    energy -= 5

                for enemy in pygame.sprite.groupcollide(enemy_team, group_shooting_player, True, True):
                    explosion_enemy.play()
                    group_explosion.add(Explosion(enemy.rect))
                    kill_enemy += 1
                    if kill_enemy >= COUNT_ENEMY * lvl:
                        enemy.kill()
                        for enemy in enemy_team:
                            enemy.kill()

                        won_game(score_top, kill_enemy)
                        background_game = load_image(path.join('static', 'img',  f'level_{lvl}', 'background',
                                                               'background_1.jpg'),
                                                     True, DISPLAYMODE)

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
