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
    if rect1_x1 < rect2_x2 and rect2_x1 < rect1_x2:
        in_x = True
    if rect1_y1 < rect2_y2 and rect2_y1 < rect1_y2:
        in_y = True
    if in_x and in_y:
        result = True

    return result


def circle_circle_intersection(circle1_list, circle2_list):
    result = False
    circle1_x_center = circle1_list[0]
    circle1_y_center = circle1_list[1]
    circle1_radius = circle1_list[2]
    circle2_x_center = circle2_list[0]
    circle2_y_center = circle2_list[1]
    circle2_radius = circle2_list[2]

    distance = math.sqrt(math.pow(circle1_x_center - circle2_x_center, 2) +
                         math.pow(circle1_y_center - circle2_y_center, 2))

    if distance <= circle1_radius + circle2_radius:
        result = True

    return result


def line_circle_intersection(line_type, circle_list, min_x=0, min_y=0, max_x=0, max_y=0, x=0, y=0):
    circle_x_center = circle_list[0]
    circle_y_center = circle_list[1]
    circle_radius = circle_list[2]
    # r^2 = (x-xc)^2 + (y-yc)^2
    # y = +/-sqrt(r^2 - (x-xc)^2) + yc
    # x = +/-sqrt(r^2 - (y-yc)^2) + xc

    if line_type == 'horizontal':
        factor = math.sqrt(circle_radius*circle_radius - math.pow(y-circle_y_center, 2))
        xi_1 = circle_y_center + factor
        xi_2 = circle_y_center - factor
        if min_x <= xi_1 <= max_x:
            return True, xi_1, xi_2
        elif min_x <= xi_2 <= max_x:
            return True, xi_1, xi_2
        else:
            return False
    elif line_type == 'vertical':
        factor = math.sqrt(circle_radius * circle_radius - math.pow(x - circle_x_center, 2))
        yi_1 = circle_x_center + factor
        yi_2 = circle_x_center - factor
        if min_y <= yi_1 <= max_y:
            return True
        elif min_y <= yi_2 <= max_y:
            return True
        else:
            return False
    else:
        pass


def rectangle_circle_intersection(rect_list, circle_list):
    rect_x_min = rect_list[0]
    rect_x_max = rect_list[0] + rect_list[2]
    rect_y_min = rect_list[1]
    rect_y_max = rect_list[1] + rect_list[3]
    rectangle_polygon_x = [rect_x_min, rect_x_max, rect_x_max, rect_x_min, rect_x_min]
    rectangle_polygon_y = [rect_y_min, rect_y_min, rect_y_max, rect_y_max, rect_y_min]

    circle_x_center = circle_list[0]
    circle_y_center = circle_list[1]
    circle_radius = circle_list[2]

    # check center + radius being beyond min/max limits
    if circle_x_center + circle_radius < rect_x_min:
        return False
    elif circle_y_center + circle_radius < rect_y_min:
        return False
    elif circle_x_center - circle_radius > rect_x_max:
        return False
    elif circle_y_center - circle_radius > rect_y_max:
        return False
    elif point_in_polygon(circle_x_center, circle_y_center, rectangle_polygon_x, rectangle_polygon_y):
        return True
    else:
        # After removing the other cases, the remaining are intersections with the 4 sides of the rectangle
        if line_circle_intersection('horizontal', circle_list, min_x=rect_x_min, max_x=rect_x_max, y=rect_y_min):
            return True
        elif line_circle_intersection('horizontal', circle_list, min_x=rect_x_min, max_x=rect_x_max, y=rect_y_max):
            return True
        if line_circle_intersection('vertical', circle_list, min_y=rect_y_min, max_y=rect_y_max, y=rect_x_min):
            return True
        elif line_circle_intersection('vertical', circle_list, min_y=rect_y_min, max_y=rect_y_max, y=rect_x_max):
            return True
        else:
            return False


def point_in_polygon(x0, y0, polygon_x, polygon_y):
    # Use ray-casting algorithm to determine if point is inside polygon
    # If there is an odd number of intersections, the point is inside
    polygon_len = len(polygon_x) - 1
    counter = 0
    for k in range(polygon_len):
        x1 = polygon_x[k]
        x2 = polygon_x[k + 1]
        y1 = polygon_y[k]
        y2 = polygon_y[k + 1]
        if y0 > min(y1, y2):
            if y0 <= max(y1, y2):
                if x0 <= max(x1, x2):
                    # To reach here, the point must be in between y1 and y2 and less than x2
                    # As long as y1 doesn't equal y2, a horizontal line can be drawn to the right of the point and
                    # intersect this line segment of the polygon
                    if y1 != y2:
                        # inv_segment_slope is 1/slope of the polygon segment
                        inv_segment_slope = (x2 - x1) / (y2 - y1)
                        # the ray-cast has equation y = y0
                        # setting y = y0 = m*x_intersection+b of the polygon segment reduces to this intersection:
                        x_intersection = (y0-y1) * inv_segment_slope + x1
                        if x1 == x2 or x0 <= x_intersection:
                            counter = counter+1

    if counter % 2 == 0:
        return False
    else:
        return True


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
