import json
from prompt_toolkit import prompt


class Game:
    def __init__(self):
        self.should_exit = False

    def set_world_file(self, file_name):
        self.world_file = file_name

    def start(self):
        self.path_list = []
        self.world = {}
        self.position = {}
        self.hp = 15
        self.atk = 5
        self.coin = 0
        self.load_world(self.world_file)

    def end(self):
        pass

    def load_world(self, file_name):
        with open(file_name, 'r') as file:
            self.world = json.load(file)
            self.position = self.world
            self.path_list = [self.position['name']]

    def game_loop(self):
        while not self.should_exit:
            command = prompt('\n' + '/'.join(self.path_list) + '>')
            self.execute(command)

    def execute(self, command):
        # simple parse command
        command = command.split()
        if not command:
            return
        if command[0] == 'exit':
            self.execute_exit(command)
            return
        if command[0] == 'help':
            self.execute_help(command)
            return
        if command[0] == 'ls':
            self.execute_ls(command)
            return
        if command[0] == 'file':
            self.execute_file(command)
            return
        if command[0] == 'cat':
            self.execute_cat(command)
            return
        if command[0] == 'cd':
            self.execute_cd(command)
            return
        if command[0] == 'buy':
            self.execute_buy(command)
            return
        if command[0] == 'fight':
            self.execute_fight(command)
            return
        if command[0] == 'status':
            self.execute_status(command)
            return
        self.command_error(f"No command called {command[0]}.")

    def command_error(self, msg=None):
        if msg is None:
            msg = ""
        print("Command error. " + msg)

    def execute_exit(self, command):
        if len(command) > 1:
            self.command_error("Too many arguments.")
            return
        self.should_exit = True

    def execute_help(self, command):
        print("""
- exit: exit game
- help: help message
- ls: list files in current directory
- file <file_name>: see file type of <file_name>
- cat <file_name>: print content of <file_name>
- cd <directory_name>: change working directory to <directory_name>
- cd ..: change working directory to parent directory
- buy <file_name>: buy the item <file_name> and equip it
- fight <file_name>: fight an enemy <file_name>. Player hits enemy once and vice versa.
- status: print player status
""")

    def execute_ls(self, command):
        if len(command) > 1:
            self.command_error("Too many arguments.")
            return
        for child in self.position['children']:
            print(child['name'])

    def execute_file(self, command):
        if len(command) != 2:
            self.command_error("Need 1 argument.")
            return
        file_name = command[1]
        child = self.get_child(file_name)
        if child is not None:
            print(f"{file_name}: {child['type']}")
            return
        self.command_error("File doesn't exist.")

    def execute_cat(self, command):
        if len(command) != 2:
            self.command_error("Need 1 argument.")
            return
        file_name = command[1]
        child = self.get_child(file_name)
        if child is not None:
            if child['type'] == 'area':
                print(f"{file_name} is an area. You can travel to this area.")
            elif child['type'] == 'enemy':
                print(f"{file_name}: {child['content']}. It has {child['hp']}"
                      f" hp and {child['atk']} atk.")
            else:
                print(f"{file_name}: {child['content']}")
            return
        self.command_error("File doesn't exist.")

    def execute_cd(self, command):
        if len(command) != 2:
            self.command_error("Need 1 argument.")
            return
        file_name = command[1]
        if file_name == '..':
            try:
                self.position = self.position['parent']
                del self.path_list[-1]
            except KeyError:
                print("Already at root.")
            return
        child = self.get_child(file_name)
        if child is not None:
            if child['type'] == 'area':
                child['parent'] = self.position
                self.position = child
                self.path_list.append(self.position['name'])
            else:
                print(f"{file_name} is not an area.")
            return
        self.command_error("File doesn't exist.")

    def execute_buy(self, command):
        if len(command) != 2:
            self.command_error("Need 1 argument.")
            return
        file_name = command[1]
        child = self.get_child(file_name)
        if child is not None:
            if child['type'] == 'weapon':
                if self.coin < child['price']:
                    print("Not enough coins.")
                    return
                self.coin -= child['price']
                self.atk += child['atk']
                self.position['children'].remove(child)
                print(f"You bought {file_name}")
            else:
                self.command_error(f"You can't buy {file_name}")
            return
        self.command_error("File doesn't exist.")

    def execute_fight(self, command):
        if len(command) != 2:
            self.command_error("Need 1 argument.")
            return
        file_name = command[1]
        child = self.get_child(file_name)
        if child is not None:
            if child['type'] == 'enemy':
                child['hp'] -= self.atk
                self.hp -= child['atk']
                if self.hp <= 0:
                    self.game_over()
                    return
                if child['hp'] <= 0:
                    self.coin += child['drop']
                    self.position['children'].remove(child)
                    print(f"You defeated {child['name']}. "
                          f"You got {child['drop']} coins.")
            else:
                self.command_error(f"You can't fight {file_name}")
            return
        self.command_error("File doesn't exist.")

    def execute_status(self, command):
        if len(command) > 1:
            self.command_error("Too many arguments.")
        print(f"HP: {self.hp}")
        print(f"ATK: {self.atk}")
        print(f"Coin: {self.coin}")

    def game_over(self):
        print("YOU DIED")
        self.should_exit = True

    def get_child(self, file_name):
        for child in self.position['children']:
            if child['name'] == file_name:
                return child
        return None
