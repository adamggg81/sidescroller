import pygame


class WorldObjects:
    def __init__(self):
        self.Player = None
        self.camera = None
        self.platforms = None
        self.Enemy = None
        self.fps = 0

    def new_level(self):
        for j in range(len(self.platforms)-1, -1, -1):
            del self.platforms[j]

        for j in range(len(self.Enemy)-1, -1, -1):
            del self.Enemy[j]

    def load_level(self, filename):
        from Player import Player
        from Platform import Platform
        from Frog import Frog
        from Mouse import Mouse
        from Cardinal import Cardinal
        from Hairball import Hairball
        self.new_level()

        self.platforms = []
        self.Enemy = []

        with open(filename) as file:
            line_list = [line.rstrip() for line in file]

        for line in line_list:
            args = line.split(',')
            input_type = args[0]
            if input_type[0] == '#':
                continue
            del args[0]
            arg_container = dict()
            for element in args:
                arg_split = element.split('=')
                arg_container[arg_split[0]] = arg_split[1]

            x = int(arg_container["x"])
            y = int(arg_container["y"])

            if input_type == 'Player':
                target = self.Player
                target.x = x
                target.y = y
            elif input_type == 'Platform':
                width = int(arg_container["width"])
                height = int(arg_container["height"])
                target = Platform(x, y, width, height)
                self.platforms.append(target)
            elif input_type == 'Mouse':
                target = Mouse(x, y)
                self.Enemy.append(target)
            elif input_type == 'Frog':
                target = Frog(x, y)
                self.Enemy.append(target)
            elif input_type == 'Cardinal':
                target = Cardinal(x, y)
                self.Enemy.append(target)

