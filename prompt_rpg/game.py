import json
from prompt_toolkit import prompt
from pyfiglet import Figlet


class PromptRPG:
    def __init__(self):
        self.start()
        self.game()
        self.end()

    def start(self):
        self.print_banner()
        self.load_world('world.json')

    def end(self):
        pass

    def print_banner(self):
        print(Figlet(font='larry3d').renderText('PromptRPG'))

    def load_world(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)

    def game(self):
        while True:
            text = prompt('>')
            print(text)
            if text == 'exit':
                break


if __name__ == '__main__':
    PromptRPG()
