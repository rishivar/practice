import scipy.signal as signal
import numpy as np
import json

CONFIG_PATH = "config.json"

class GameOfLife:
    def __init__(self):
        with open(CONFIG_PATH) as f:
            json_str = f.read()
        
        self.config = json.loads(json_str)
        
        self.cur_board = None
        
        #Initialise Stats
        self.num_iters = 0
        self.num_alive = 0
        self.pattern_name = None

    def get_options(self):
        return self.config

    def select(self, pattern_name):
        if pattern_name.lower() not in self.config:
            return False #err: invalid selection
        else:
            self.pattern_name = pattern_name
            self.cur_board = np.array(self.config[pattern_name.lower()], dtype=np.uint8)
            self.num_alive = 0
            self.num_iters = 0
            return True

    def update(self):
        kernel = np.ones((3,3), dtype=np.uint8)
        if self.cur_board is None:
            return False 

        new_board = signal.convolve2d(self.cur_board, kernel, mode="same")

        (m, n) = self.cur_board.shape
        for i in range(m):
            for j in range(n):
                if new_board[i,j] == 3:
                    new_board[i, j] = 1
                elif new_board[i, j] == 4:
                    new_board[i, j] = self.cur_board[i, j]
                else:
                    new_board[i, j] = 0

        self.cur_board = new_board
        self.num_iters += 1
        self.num_alive = sum(sum(self.cur_board))
        return True

    def get_board(self):
        return self.cur_board

    def get_stats(self):
        d = {
            "pattern": self.pattern_name,
            "alive": self.num_alive,
            "iters": self.num_iters
        }
        return d


print("Welcome to the Game Of Life!")
g = GameOfLife()
configs = g.get_options()

menu = """
Type the following for execution:
list - show all board pattern models
view pattern_name - view the board model for pattern
select pattern_name - selects the pattern
update n - Shows each step and updates the board
state - Shows the current state of the board.
quit - Quit 
"""


def command(fn):
    def secure_fn(cmd_list):
        try:
            fn(cmd_list)
        except IndexError:
            print("Invalid format/command")
    return secure_fn


@command
def ls(cmd):
    for k in configs.keys():
        print(k)


@command
def view(cmd):
    if cmd[1] not in configs:
        print("Invalid pattern name")
    else:
        print(np.array(configs[cmd[1]], dtype=np.uint8))


@command
def update(cmd):
    if g.get_stats()["pattern"] is None:
        print("Please select a pattern first.")
        return

    for i in range(int(cmd[1])):
        print("\n#{}:".format(i+1))
        g.update()
        print(g.get_board())


@command
def select(cmd):
    if not g.select(cmd[1]):
        print("No pattern called {} exists!".format(cmd[1]))


cmd_map = {
    "list": ls,
    "view": view,
    "select": select,
    "update": update,
    "state": lambda cmd: print(g.get_stats()),
    "quit": lambda cmd: exit()
}


def execute(cmd_list):
    try:
        fn = cmd_map[cmd_list[0]]
    except KeyError:
        print("{} is not a valid command!".format(cmd_list[0]))
        return
    fn(cmd_list)




while True:
    pattern = g.get_stats()["pattern"]

    if pattern == None:
        print(">", end=' ')
    else:
        print("{}>".format(pattern), end=' ')

    execute(input().split())
