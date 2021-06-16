import json
from prompt_toolkit import prompt
from pyfiglet import Figlet


class PromptRPG:
    def __init__(self):
        self.should_exit = False
        self.start()
        self.game()
        self.end()

    def start(self):
        self.print_banner()
        self.path_list = []
        self.load_world('world.json')

    def end(self):
        pass

    def print_banner(self):
        print(Figlet(font='larry3d').renderText('PromptRPG'))

    def load_world(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            self.path_list.append(data['name'])

    def game(self):
        while not self.should_exit:
            command = prompt('/'.join(self.path_list) + '>')
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

        # cd ls exit help buy fight file cat

    def execute_exit(self, command):
        self.should_exit = True

    def execute_help(self, command):
        print('This is help message.')

    def execute_ls(self, command):
        pass

    def execute_file(self, command):
        pass

    def execute_cat(self, command):
        pass

    def execute_cd(self, command):
        pass

    def execute_buy(self, command):
        pass

    def execute_fight(self, command):
        pass


if __name__ == '__main__':
    PromptRPG()
