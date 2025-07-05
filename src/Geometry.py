import math


def rectangle_rectangle_intersection(rect1_list, rect2_list):
    result = False
    rect1_x1 = rect1_list[0]
    rect1_x2 = rect1_list[0] + rect1_list[2]
    rect1_y1 = rect1_list[1]
    rect1_y2 = rect1_list[1] + rect1_list[3]
    rect2_x1 = rect2_list[0]
    rect2_x2 = rect2_list[0] + rect2_list[2]
    rect2_y1 = rect2_list[1]
    rect2_y2 = rect2_list[1] + rect2_list[3]
    in_x = False
    in_y = False
    if rect2_x1 <= rect1_x1 <= rect2_x2:
        in_x = True
    if rect2_x1 <= rect1_x2 <= rect2_x2:
        in_x = True
    if rect2_y1 <= rect1_y1 <= rect2_y2:
        in_y = True
    if rect2_y1 <= rect1_y2 <= rect2_y2:
        in_y = True
    if in_x and in_y:
        result = True

    return result


def character_collision(victim, aggressor):
    result = False
    victim_rect = [victim.x, victim.y, victim.width, victim.height]
    aggressor_rect = [aggressor.x, aggressor.y, aggressor.width, aggressor.height]
    if rectangle_rectangle_intersection(victim_rect, aggressor_rect):
        result = True

    return result


def platform_collision(walker, platforms):
    result = False
    collision_platform = None
    wall_collision = 0
    player_rect = [walker.x, walker.y, walker.width, walker.height]
    past_player_bottom = walker.y - walker.vel_y + walker.height
    current_player_bottom = walker.y + walker.height
    # if not walker.on_ground:
    for platform in platforms:
        platform_rect = [platform.rect.x, platform.rect.y, platform.rect.width, platform.rect.height]
        if rectangle_rectangle_intersection(player_rect, platform_rect):
            # Landing on top of platform
            if walker.vel_y > 0 and walker.y < platform.rect.y and past_player_bottom <= platform.rect.y+5:
                result = True
                collision_platform = platform
                return result, collision_platform, wall_collision
            elif walker.x + walker.width - walker.vel_x <= platform.rect.x:
                wall_collision = -1
                collision_platform = platform
                return result, collision_platform, wall_collision
            elif walker.x - walker.vel_x >= platform.rect.x + platform.rect.width:
                wall_collision = 1
                collision_platform = platform
                return result, collision_platform, wall_collision

    # special check for high velocity moving through the platform
    for platform in platforms:
        if abs(walker.vel_y) > platform.rect.height:
            platform_rect = [platform.rect.x, platform.rect.y, platform.rect.width, platform.rect.height]
            platform_top = platform.rect.y
            platform_bottom = platform.rect.y + platform.rect.height

            if past_player_bottom < platform_top and current_player_bottom > platform_bottom:

                num_steps = math.ceil(abs(walker.vel_y) / platform.rect.height)
                x_step = walker.vel_x / num_steps
                y_step = walker.vel_y / num_steps
                for j in range(num_steps - 1):
                    this_x = walker.x - walker.vel_x + x_step * (j + 1)
                    this_y = walker.y - walker.vel_y + y_step * (j + 1)
                    past_player_rect = [this_x, this_y, walker.width, walker.height]
                    if rectangle_rectangle_intersection(past_player_rect, platform_rect):
                        # Landing on top of platform
                        if walker.vel_y > 0 and walker.y < platform.rect.y:
                            result = True
                            collision_platform = platform
                            return result, collision_platform, wall_collision

    return result, collision_platform, wall_collision
