import unittest
from lit import World, Player


class TestGame(unittest.TestCase):

    def test_w_key(self):
        world = World("map.yaml")
        player = Player()
        world.place_player(player, 1, 1)
        #print(world.world)
        world.do_command('move south')
        world.do_command('move south')
        world.do_command('move east')
        world.do_command('move east')
        world.do_command('move east')
        self.assertEqual( world.game_over , True)
        
    def test_without_key(self):
        world = World("map.yaml")
        player = Player()
        world.place_player(player, 1, 1)
        #print(world.world)
        world.do_command('move south')
        world.do_command('move east')
        world.do_command('move south')
        world.do_command('move east')
        world.do_command('move east')
        self.assertEqual( world.game_over , False)
        
if __name__ == '__main__':
    unittest.main()
