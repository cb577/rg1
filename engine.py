import tcod as libtcod
import tcod.event
import json

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder


def main():
    screen_width = 80
    screen_height = 50

    # Size of the map
    map_width = 80
    map_height = 45

    # Some variables for the rooms in the map
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    # MONSTERS
    max_monsters_per_room = 3

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10
    # reg colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # debug colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }

    # Components and Entities
    fighter_component = Fighter(hp=30, defense=2, power=5)

    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,  fighter=fighter_component)



    entities = [player]

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(screen_width, screen_height,  'libtcod tutorial revised', False, vsync= True, renderer = libtcod.RENDERER_SDL2)

    con = libtcod.console.Console(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room )
    print("{}: {}".format("Rooms", len(game_map.rooms)))




    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    # can't get this code to work the way it's supposed to, so whateves
    # while not tcod.event.get() == 'QUIT':
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, entities, player, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit = action.get('exit')
        command = action.get('command')

        if command == 'p':
            print("{} {}".format("Rooms:", len(game_map.rooms)))
            gm = game_map
            gm_tiles = gm.tiles
            xt = 0
            yt = 0


            for xdex, xtem in enumerate(gm.tiles):
                for ydex, ytem in enumerate(xtem):
                    print("{}{} {}{} {}".format("Tile (", xdex, ydex, "):", json.dumps(gm.tiles[xdex][ydex].__dict__)))

                # print(index, item)

            # for row in gm.tiles:

            #     for abc in row:
            #         print(abc)

                # for c in row:
                    # if c.explored == True:
                        # print("{}{} {}{} {}".format("Tile (", xt, yt, "):", json.dumps(gm.tiles[xt][yt].__dict__)))

            # print("{}{} {}{} {}".format("Tile (", xt, yt, "):", json.dumps(gm.tiles[xt][yt].__dict__)))

        if command == 'o':
            print("{}: {}".format("Rooms", len(game_map.rooms)))

        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN


        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN



if __name__ == '__main__':
     main()
