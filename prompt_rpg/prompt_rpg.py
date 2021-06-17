from .game import Game
from plumbum import cli
from pyfiglet import Figlet


class PromptRPG(cli.Application):
    VERSION = "0.1.0"
    world_file = 'world.json'

    @cli.switch(['-w', '--world'], str, help="Provide a custom world file.")
    def set_world_fild(self, file_name):
        self.world_file = file_name

    def main(self):
        self.game = Game()
        self.start()
        self.game.game_loop()
        self.end()

    def start(self):
        self.print_banner()
        self.game.set_world_file(self.world_file)
        self.game.start()

    def end(self):
        pass

    def print_banner(self):
        print(Figlet(font='larry3d').renderText('PromptRPG'))
