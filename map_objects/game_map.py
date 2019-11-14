from random import randint

from map_objects.tile import Tile
from map_objects.rectangle import Rect
import math

class GameMap:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()
        self.rooms = []

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
        return tiles

    def room_facts(self):
        return self.rooms


    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        # Create two rooms for demonstration purposes
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    rand_int = randint(0,2)

                    if rand_int == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    elif rand_int == 0:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                    else:
                        self.create_r_tunnel(prev_x, new_x, prev_y, new_y)

                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1
        self.rooms = rooms

    def create_floor_tile(self, x, y):
        self.tiles[x][y].blocked = False
        self.tiles[x][y].block_sight = False


    # def assign_owner_to_tile(self, x, y, owner):


    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                # self.assign_owner_to_tile(x,y)
                self.create_floor_tile(x,y)

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.create_floor_tile(x,y)

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.create_floor_tile(x,y)

    def create_r_tunnel(self, x1, x2, y1, y2):

        dx = x2 - x1
        dy = y2 - y1

        abs_dx = int(abs(dx))
        abs_dy = int(abs(dy))

        if abs_dx != 0:
            norm_dx = int(dx / abs_dx)
        else:
            norm_dx = 0

        if abs_dy != 0:
            norm_dy = int(dy / abs_dy)
        else:
            norm_dy = 0

        x = int(x1)
        y = int(y1)

        while (x != x2 and y != y2):
            # print(x,y)
            rx = randint(0, abs_dx)
            ry = randint(0, abs_dy)

            if (rx == 0 and ry == 0) or (rx != 0 and ry != 0):
                if randint(0,1) == 0:
                    x += norm_dx
                else:
                    y += norm_dy
            elif rx == 0:
                y += norm_dy
            elif ry == 0:
                x += norm_dx

            self.create_floor_tile(x,y)

        while (x == x2 and y != y2):
            y += norm_dy
            self.create_floor_tile(x,y)


        while (x != x2 and y == y2):
            x += norm_dx
            self.create_floor_tile(x,y)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True
        return False