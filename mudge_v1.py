import math

def reward_function(params):
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    heading = params['heading']
    speed = params['speed']

    close_waypoints = params['closest_waypoints']
    # Look at up coming waypoints to make sure your turning when needed?
    prev_point = params['waypoints'][close_waypoints[0]]
    next_point = params['waypoints'][close_waypoints[1]]

    steering_reward = 1
    # In general going straight is better than turning (faster).
    if steering > 1:
        steering_reward = 0.8


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

    # Use the smaller of the 2 diff's.
    direction_diff = math.min(direction_diff, direction_diff2)
    if direction_diff < 10:
        # reward for being closer to the tracks direction
        direction_reward = direction_diff / 10
    else:
        direction_reward = .1
        # Steering when the direction is wrong is a good thing.
        steering_reward = 1

    # TODO look further ahead at more waypoints?

    # reward for going faster (0-1)
    speed_reward = speed / 8

    offtrack_reward = 1
    # Being too close to the track edge is bad, but we do want to encourage some movement for racing lines.
    if distance_from_center > 0.5 * track_width:
        offtrack_reward = .1  # likely crashed/ close to off track

    return float(offtrack_reward * speed_reward * direction_reward * steering_reward)