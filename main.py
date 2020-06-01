# coding=utf-8

# //////////////////
# ФАЙЛ ЗАПУСКА ИГРЫ
# //////////////////

from game import Game


def main():  # Функция вызова игры (главный файл)
    game = ForProtectionWithAHistory()
    game.run()


class ForProtectionWithAHistory(Game):
    def __init__(self):
        super(ForProtectionWithAHistory, self).__init__()


if __name__ == '__main__':
    main()
