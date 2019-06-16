import sys, pygame
import random
import math

import mudge_v1 as model

pygame.init()

size = width, height = 640, 480
speed = 2.0

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# define a surface (RECTANGLE)  
image_orig = pygame.Surface((35 , 15))  
# for making transparent background while rotating an image  
image_orig.set_colorkey((0 , 0 , 0))  
# fill the rectangle / surface with green color  
image_orig.fill((255 , 13 , 7))  
image = image_orig.copy()  
image.set_colorkey((0, 0, 0))
rect = image.get_rect()

# Start position and angle for car
rect.center = (250, 150)
angle = 0

waypoints = [[250, 150], [400, 150], [400, 350], [200, 350]]
track_width = 30
# The waypoint which we are most recently went passed.
waypoint_idx = 0

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    old_center = rect.center
    new_image = pygame.transform.rotate(image_orig, angle)
    rect = new_image.get_rect()
    rect.center = old_center

    # Calculate a line from one waypoint to the next (the track)
    w1 = waypoints[waypoint_idx]
    w2 = waypoints[waypoint_idx + 1 % len(waypoints)]
    x_diff = w2[0] - w1[0]
    y_diff = w2[1] - w1[1]

    # Caclculate the distance from this line to find our distance_from_center
    num = abs(y_diff * rect.center[0] - x_diff * rect.center[1] + w2[0] * w1[1] - w2[1] * w1[0])
    den = math.sqrt(y_diff**2 + x_diff**2)
    distance_from_center = num / den

    # Look at the line to the next waypoint compared to the line to the cars position.
    # Take the dot product to calculate how far along the waypoint line the car is.
    carx_diff = rect.center[0] - w1[0]
    cary_diff = rect.center[1] - w1[1]

    # We want to use the normalized waypoint line direction so we get a distance along it.
    length = math.sqrt(x_diff ** 2 + y_diff ** 2)
    dotP = x_diff / length * carx_diff + y_diff / length * cary_diff

    if dotP < 0:
        # Haven't actually gone past the first waypoint. Do we need to handle backtracking???
        pass
    elif dotP > length:
        # we have gone further than the length of the line along this waypoint line. Move on to the next one.
        waypoint_idx = waypoint_idx + 1 % len(waypoints)
    else:
        # We are somewhere between the waypoints.
        pass


    closest_waypoints = [waypoint_idx, waypoint_idx + 1 % len(waypoints)]

    params = {
        'x': rect.center[0],
        'y': rect.center[1],
        'distance_from_center': distance_from_center,
        'track_width': track_width,
        'heading': -angle,
        'waypoints': waypoints,
        'closest_waypoints': closest_waypoints,
        'speed': speed,
    }

    # Alter speed/steering_angle params and try reward.
    params.update({'steering_angle': 5})
    left_reward = model.reward_function(params)
    
    params.update({'steering_angle': 0})
    straight_reward = model.reward_function(params)

    params.update({'steering_angle': -5})
    right_reward = model.reward_function(params)

    # Move based on rewards.
    # speed change based on angle?
    if left_reward > straight_reward and left_reward > right_reward:
        # left is max
        turn = "Left"
        angle += 5
        if angle > 180:
            angle -= 360
    elif right_reward > straight_reward and right_reward > left_reward:
        # right is max
        turn = "Right"
        angle -= 5
        if angle < -180:
            angle += 360
    else:
        # straight is max, no turning.
        turn = "Straight"
        pass

    # Status of each tick.
    print(waypoint_idx, dotP, length, distance_from_center, turn, left_reward, straight_reward, right_reward)

    # crash before we move.
    if rect.left < 0 or rect.right > width:
        speed = 0
    if rect.top < 0 or rect.bottom > height:
        speed = 0


    # Move based on the angle we are heading in.
    speed_delta = [
        speed * math.cos(math.radians(angle)),
        -speed * math.sin(math.radians(angle))
    ]             

    # Then move.
    rect = rect.move(speed_delta)

    # Change rotation
    screen.fill([0, 0, 0])

    # Draw the track
    grey = (128,128,128)
    closed = True
    pygame.draw.lines(screen, grey, closed, waypoints, track_width)
    screen.blit(new_image, rect)
    pygame.display.flip()

    # --- Wrap-up
    # Limit to 60 frames per second
    clock.tick(60)
    # Slow down for testing
    clock.tick(10)
