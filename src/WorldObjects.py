import pygame


class WorldObjects:
    def __init__(self):
        self.Player = None
        self.camera = None
        self.platforms = None
        self.Enemy = None
        self.fps = 0
        self.current_level = ''
        self.width = 0
        self.height = 0

    def delete_dead_enemies(self):
        dead_index = []
        for j in range(len(self.Enemy)):
            enemy = self.Enemy[j]
            if not enemy.alive:
                dead_index.append(j)
        for j in range(len(dead_index) - 1, -1, -1):
            del self.Enemy[dead_index[j]]

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

        # track the current level for reload
        # perhaps better to keep the list data to avoid unnecessary file re-read, but fine for now
        self.current_level = filename

        # Append to this dictionary whenever a new enemy is added
        # This allows an effective string-to-function conversion on enemy type
        enemy_types = {
            "Frog": Frog,
            "Mouse": Mouse,
            "Cardinal": Cardinal,
            "Hairball": Hairball
        }

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
            all_keys = list(arg_container.keys())

            if "x" in all_keys:
                x = int(arg_container["x"])
            else:
                x = 0
            if "y" in all_keys:
                y = int(arg_container["y"])
            else:
                y = 0
            if "width" in all_keys:
                width = int(arg_container["width"])
            else:
                width = 0
            if "height" in all_keys:
                height = int(arg_container["height"])
            else:
                height = 0

            if input_type == 'World':
                self.width = width
                self.height = height
            elif input_type == 'Player':
                target = self.Player
                target.x = x
                target.y = y
            elif input_type == 'Platform':
                target = Platform(x, y, width, height)
                self.platforms.append(target)
            elif input_type == 'Enemy':
                this_enemy = arg_container["type"]
                target = enemy_types[this_enemy](x, y)
                self.Enemy.append(target)

