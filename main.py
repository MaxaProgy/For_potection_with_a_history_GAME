# coding=utf-8
from game import Game


def main():  # Функция вызова игры(главный файл)
    game = ForPprotectionWithAHistory()
    game.run()


class ForPprotectionWithAHistory(Game):
    def __init__(self):
        super(ForPprotectionWithAHistory, self).__init__()


if __name__ == '__main__':
    main()
