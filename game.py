# coding=utf-8
from sprites import *
from os import *
import sys
from image import load_image


def lost_game():
    img = load_image(path.join('static', 'img', 'background', 'game_lost.jpg'), True, DISPLAYMODE)
    window.blit(img, (0, 0))
    pygame.display.update()
    wait_for_keystroke()
    new_game()


def won_game():
    img = load_image(path.join('static', 'img', 'background', 'game_won.jpg'), True, DISPLAYMODE)
    window.blit(img, (0, 0))
    pygame.display.update()
    wait_for_keystroke()
    new_game()


def exit_game():
    pygame.quit()
    sys.exit()


def pause_game():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Нажав клавишу esc, мы выходим из игры
                    exit_game()
                if event.key == pygame.K_p:
                    pause = False

        pygame.display.update()


def wait_for_keystroke():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_BACKSPACE:
                    return


def wait_for_keystroke_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Клавиша esc вызывает выход из игры
                    exit_game()
                if event.key == pygame.K_SPACE:
                    return


def show_help():
    img_help = load_image(path.join('static', 'img', 'level_1', 'background', 'background_help.jpg'), True, DISPLAYMODE)
    window.blit(img_help, (0, 0))
    pygame.display.update()
    wait_for_keystroke()


def update_sprites():
    player = Player()  # Настраиваем игрока
    player_team = pygame.sprite.RenderUpdates(player)
    group_shooting_player = pygame.sprite.RenderUpdates()
    enemy = Enemy()  # Настраиваем игрока
    enemy_team = pygame.sprite.RenderUpdates()
    return enemy, enemy_team, player, player_team, group_shooting_player


def new_game():
    background = load_image(path.join('static', 'img', 'level_1', 'background', 'background_1.jpg'), True, DISPLAYMODE)
    window.blit(background, (0, 0))
    pygame.display.update()
    wait_for_keystroke_menu()


class Game(object):
    def __init__(self):
        super(Game, self).__init__()
        pygame.init()
        new_game()
        self.time = pygame.time.Clock()

    def run(self):
        while True:
            energy = INIT_ENERGY
            enemy, enemy_team, player, player_team, group_shooting_player = update_sprites()
            background_game = load_image(path.join('static', 'img', 'level_1', 'background', 'background_1.jpg'),
                                         True, DISPLAYMODE)

            group_explosion = pygame.sprite.RenderUpdates()
            kill_enemy = 0
            check_on_press_keys = True
            while True:
                window.blit(background_game, (0, 0))
                if check_on_press_keys:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit_game()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_F1:
                                show_help()
                            if event.key == pygame.K_p:
                                pause_game()
                        elif event.type == pygame.KEYUP:
                            player.y_speed = 0

                    key_pressed = pygame.key.get_pressed()
                    if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
                        player.y_speed = -RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
                        player.y_speed = RATE_PLAYER_SPEED
                    if key_pressed[pygame.K_SPACE]:
                        group_shooting_player.add(PlayerShooting(player.rect.midtop))

                if len(enemy_team) <= MAX_NUMBER_ENEMY:
                    enemy_team.add(Enemy())
                if energy <= 0 and check_on_press_keys:
                    check_on_press_keys = False  # Чтобы отключить ввод нажатий клавиш
                    group_explosion.add(Explosion(player.rect))
                    player.kill()
                    lost_game()

                # =========================
                # СПРАЙТ СТОЛКНОВЕНИЯ
                # =========================

                for player in pygame.sprite.groupcollide(player_team, group_shooting_enemy, False, True):
                    energy -= 15


                for enemy in pygame.sprite.groupcollide(enemy_team, group_shooting_player, True, True):
                    group_explosion.add(Explosion(enemy.rect, "explosion"))  # Исчезает во взрыве
                    kill_enemy += 1
                    if kill_enemy >= COUNT_ENEMY:
                        won_game()
                # =============================
                # ОБНОВЛЯЕМ ВСЕ ГРУППЫ
                # =============================

                enemy_team.update()
                player_team.update()
                group_shooting_player.update()
                group_explosion.update()
                group_shooting_enemy.update()

                # =======================
                # ОЧИЩАЕМ СПРАЙТЫ
                # =======================

                enemy_team.clear(window, background_game)
                enemy_team.draw(window)
                player_team.clear(window, background_game)
                player_team.draw(window)
                group_shooting_player.clear(window, background_game)
                group_shooting_player.draw(window)
                group_explosion.clear(window, background_game)
                group_explosion.draw(window)
                group_shooting_enemy.clear(window, background_game)
                group_shooting_enemy.draw(window)

                pygame.display.update()
                self.time.tick(FPS)
            pygame.time.delay(time_lapse)
            wait_for_keystroke()
