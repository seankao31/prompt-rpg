import pytest
from prompt_rpg.game import Game


@pytest.fixture
def game():
    g = Game()
    g.set_world_file('world.json')
    g.start()
    return g


def test_execute_exit(game):
    game.execute_exit(['exit'])
    assert game.should_exit


def test_execute_ls(game, capsys):
    game.execute_ls(['ls'])
    captured = capsys.readouterr()
    assert captured.out == 'store\nfield\n'


def test_execute_file(game, capsys):
    game.execute_file(['file', 'store'])
    captured = capsys.readouterr()
    assert captured.out == 'store: area\n'


def test_execute_cat(game, capsys):
    game.execute_cat(['cat', 'field'])
    captured = capsys.readouterr()
    assert captured.out == 'field is an area. You can travel to this area.\n'


def test_execute_cd_file(game, capsys):
    game.execute_cd(['cd', 'field'])
    assert game.position['name'] == 'field'
    assert game.position['parent'] == game.world
    assert game.path_list == ['city_a', 'field']


def test_execute_cd_parent(game, capsys):
    game.execute('cd field')

    game.execute_cd(['cd', '..'])
    assert game.position['name'] == 'city_a'
    assert game.path_list == ['city_a']


def test_execute_fight(game):
    game.execute('cd field')

    monster = game.position['children'][0]
    assert monster['name'] == 'monster'
    game.execute_fight(['fight', 'monster'])
    assert monster not in game.position['children']
    assert game.hp == 13
    assert game.coin == 30


def test_execute_buy(game):
    game.execute('cd field')
    game.execute('fight monster')
    game.execute('cd ..')
    game.execute('cd store')

    weapon_a = game.position['children'][0]
    game.execute_buy(['buy', 'weapon_a'])
    assert weapon_a not in game.position['children']
    assert game.coin == 10
    assert game.atk == 25
