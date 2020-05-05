# coding=utf-8
from game import Game


def main():  # Функция вызова игры(главный файл)
    game = TankWars()
    game.run()


class TankWars(Game):
    def __init__(self):
        super(TankWars, self).__init__()


if __name__ == '__main__':
    main()
