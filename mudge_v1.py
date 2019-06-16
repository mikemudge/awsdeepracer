import math

def reward_function(params):
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = params['steering_angle'] # Only need the absolute steering angle
    heading = params['heading']
    speed = params['speed']

    close_waypoints = params['closest_waypoints']
    # Look at up coming waypoints to make sure your turning when needed?
    prev_point = params['waypoints'][close_waypoints[0]]
    next_point = params['waypoints'][close_waypoints[1]]
    next_next = params['waypoints'][(close_waypoints[1] + 1) % len(params['waypoints'])]

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    track_direction = math.degrees(track_direction)

    # This could be -179 and 179 which is actually pretty close.
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # If the car is going toward the next waypoint thats ok as well.
    next_point_direction = math.atan2(next_point[1] - params['x'], next_point[0] - params['y']) 
    next_point_direction = math.degrees(next_point_direction)

    # This could be -179 and 179 which is actually pretty close.
    direction_diff2 = abs(next_point_direction - heading)
    if direction_diff2 > 180:
        direction_diff2 = 360 - direction_diff2

    # If the track curves ahead we should encourage steering.
    track_next_direction = math.atan2(next_next[1] - next_point[1], next_next[0] - next_point[0]) 
    track_next_direction = math.degrees(track_next_direction)

    car_heading_offset = track_direction - heading
    # -10 = 0 - 10 Right
    # 10 = 10 - 0 Left
    # -350 = -175 - 175 # Left
    # 350 = 175 - -175 # Right
    if car_heading_offset < -180:
        car_heading_offset += 360
    if car_heading_offset > 180:
        car_heading_offset -= 360

    if car_heading_offset > 5:
        if steering > 0:
            # Steering in the right direction is good.
            steering_reward = .8
        else: 
            steering_reward = .1
    elif car_heading_offset < -5:
        if steering < 0:
            # Steering in the right direction is good.
            steering_reward = .8
        else: 
            steering_reward = .1
    else:
        # Track is pretty straight so make steering less valuable.
        if steering == 0:
            # Going straight is good.
            steering_reward = 1
        else:
            # punish steering based on the direction the car is going.
            steering_reward = abs(car_heading_offset / 5.0)

    # Use the smaller of the 2 diff's.
    direction_diff = min(direction_diff, direction_diff2)
    if direction_diff < 10:
        # reward for being closer to the tracks direction
        direction_reward = 1 - (direction_diff / 10.0)
    else:
        direction_reward = .1

    # TODO look further ahead at more waypoints?

    # reward for going faster (0-1)
    speed_reward = speed / 8.0

    offtrack_reward = 1
    # Being too close to the track edge is bad, but we do want to encourage some movement for racing lines.
    if distance_from_center > 0.5 * track_width:
        offtrack_reward = .1  # likely crashed/ close to off track

    print(offtrack_reward, speed_reward, direction_reward, steering_reward, steering, track_direction, heading)
    return float(offtrack_reward * speed_reward * direction_reward * steering_reward)