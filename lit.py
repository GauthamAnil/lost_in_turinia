import sys
import yaml

introduction = '''
   ** Lost in Turinia **

You are placed in a 2D world. You have to find your way out.

'''

'''
Level 1: 
  Blocking / non blocking entity
  Player is passive
  World manipulates player on command
  Player has fn to get status
  Exit condition by the world

'''

class World(object):

    def load_world(self, map_dict):
        map_2d = map_dict['2d_map']
        encodings = map_dict['encodings']
        #print(repr(map_2d))
        map_2d_list = [ v.strip() for v in map_2d.strip().split('!') ]
        #print(map_2d_list)
        map_2d_w_objects = []

        for row in range(len(map_2d_list)):
            map_2d_w_objects.append([])
            #print(map_2d_list[row])
            for col in range(len(map_2d_list[0])):
                if map_2d_list[row][col] != ' ':
                    map_2d_w_objects[row].append([eval(encodings[map_2d_list[row][col]])()])
                else:
                    map_2d_w_objects[row].append([])
        self.world = map_2d_w_objects

    def __init__(self, map_file_name):
        with open(map_file_name) as f:
            self.load_world(yaml.safe_load(f.read()))
        self.game_over = False

    def place_player(self, player, row,col):
        self.world[row][col].append(player)
        self.player = player
        self.player_location = (row, col)

    def did_the_player_reach_the_door(self):
        current_row, current_col = self.player_location
        entities_in_current_position = self.world[current_row][current_col]
        for entity in entities_in_current_position:
            if entity is not self.player and entity.name == 'door':
                return True
        return False

    def remove_entity_or_player_from_world(self, row, col, entity_name=None, remove_player=False):
        #print(locals())
        entities_in_current_position = self.world[row][col]
        current_entities_without = [ entity for entity in entities_in_current_position
                                     if (entity is not Player if remove_player
                                         else entity.name == entity_name) ]
        self.world[row][col] = current_entities_without
    
    def move_player(self, row_offset, col_offset):
        current_row, current_col = self.player_location
        new_row = current_row + row_offset
        new_col = current_col + col_offset
        entities_in_current_position = self.world[current_row][current_col]
        entities_in_new_position = self.world[new_row][new_col]
        atleast_one_entity_is_blocking = False
        blocking_entity = None
        for entity in entities_in_new_position:
            if entity is not self.player and entity.blocking is True:
                atleast_one_entity_is_blocking = True
                blocking_entity = entity
                break
        if atleast_one_entity_is_blocking:
            print(f"You cannot move that way. You are blocked by a {blocking_entity.name}")
        else:
            # we actually move the player
            self.remove_entity_or_player_from_world(current_row, current_col, remove_player=True)
            self.world[new_row][new_col].append(self.player)
            self.player_location = (new_row, new_col)

            # do the interaction
            for entity in entities_in_new_position:
                if entity is self.player:
                    continue
                #print(locals())
                entity.interact(self.player, self)
        
    def do_command(self, command):
        if command == 'move north':
            self.move_player(-1, 0)
        elif command == 'move south':
            self.move_player(1, 0)
        elif command == 'move east':
            self.move_player(0, 1)
        elif command == 'move west':
            self.move_player(0, -1)
        else:
            print(f"What do you mean, '{command}'?")
        
'''
[Wall] [Wall] [] [] []
[Wall] []  []  [] [] [Wall]
'''

            
class Entity(object):
    
    def interact(self, player):
        pass

class Door(object):
    name = 'door'
    blocking = False
    def interact(self, player, world):
        print(player.bag)
        for entity in player.bag:
            if entity.name == 'key':
                world.game_over = True
                print("You have found the door! Good Bye!")

class Wall(object):
    name = 'wall'
    blocking = True
    pass

class Key(object):
    name = 'key'
    blocking = False
    def interact(self, player, world):
        current_row, current_col = world.player_location
        world.remove_entity_or_player_from_world(current_row, current_col, entity_name = 'key')
        player.bag.append(self)
        print("You picked up a rusty key from the floor. It looks important. You put it in your bag.")

class Player(object):
    name = 'player'

    def __init__(self):
        self.bag = []

def main():
    world = World("map.yaml")
    player = Player()
    world.place_player(player, 1, 1)
    print(introduction)
    done = False
    while not done:
        print("> ",end='')
        command = input()
        world.do_command(command)
        if world.game_over:
            done = True
    
if __name__ == '__main__':
    test()
    #main()
