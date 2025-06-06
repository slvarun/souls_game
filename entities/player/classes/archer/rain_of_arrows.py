import random
import pyglet
from functools import partial
from entities.player.classes.archer.arrow import Arrow

def rain_of_arrows(origin_x, origin_y, tar_x, tar_y, ability_index, window=None, arrows_list=None):
    if arrows_list is None or window is None:
        print("Missing window or arrows list.")
        return
    
    

    num_arrows = 10
    spread_radius = 50
    launch_height = 2000
    strength = 1.0
    base_delay = 1.5
    launch_stagger = 0.08
    fall_stagger = 0.08

    player_x = origin_x + 16
    player_y = origin_y + 16

    cam_x = origin_x - window.width // 2
    cam_y = origin_y - window.height // 2
    real_target_x = tar_x + cam_x
    real_target_y = tar_y + cam_y

    for i in range(num_arrows):
        offset_x = random.uniform(-spread_radius, spread_radius)
        start_x = player_x + offset_x
        start_y = player_y

        # Schedule upward arrow
        launch_delay = i * launch_stagger
        pyglet.clock.schedule_once(
            partial(spawn_arrow,
                    x=start_x,
                    y=start_y,
                    target_x=start_x,
                    target_y=start_y + launch_height,
                    arrows_list=arrows_list),
            launch_delay
        )

        # Schedule downward arrow
        fall_delay = launch_delay + base_delay + (i * fall_stagger)
        fall_offset_x = random.uniform(-spread_radius, spread_radius)
        fall_offset_y = random.uniform(-spread_radius / 2, spread_radius / 2)
        target_fx = real_target_x + fall_offset_x
        target_fy = real_target_y + fall_offset_y

        pyglet.clock.schedule_once(
            partial(spawn_arrow,
                    x=start_x,
                    y=start_y + launch_height,
                    target_x=target_fx,
                    target_y=target_fy,
                    arrows_list=arrows_list),
            fall_delay
        )

def spawn_arrow(dt, x, y, target_x, target_y, arrows_list):
    arrow = Arrow(
        x=x,
        y=y,
        target_x=target_x,
        target_y=target_y,
        strength_factor=1.0
    )
    arrows_list.append(arrow)
