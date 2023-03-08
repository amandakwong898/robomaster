"""
movement_patterns_prototype.py:

A collection of functions that move the RoboMaster in one of four different patterns:

Circle pattern: Moves the RoboMaster in a circle.
X-shaped pattern: Moves the RoboMaster in an X-shaped pattern.
Cross-shaped pattern: Moves the RoboMaster in an cross-shaped pattern.
Square pattern: Moves the RoboMaster in a square-shaped pattern.

The client program moves the RoboMaster in one of the four movement patterns and then exits.
"""

import math

def move_in_circle_pattern(velocity, radius, seconds):
    """
    Moves the RoboMaster in a circle pattern.
  
    Parameters:
    velocity (int): The velocity of the Robomaster's wheels in RPM.
    radius (int): The radius of the circle in dimensionless units.
    seconds (int): The duration of the movement pattern in seconds.
  
    Returns:
    void
    """
    front_left_wheel_speed  = velocity - (velocity / radius)
    front_right_wheel_speed = velocity + (velocity / radius)
    rear_left_wheel_speed = front_left_wheel_speed
    rear_left_wheel_speed = front_right_wheel_speed

    tools.timer_ctrl(rm_define.timer_start)

    while tools.timer_current() < seconds:
        chassis_ctrl.set_wheel_speed(front_left_wheel_speed, front_right_wheel_speed,
        rear_left_wheel_speed, rear_left_wheel_speed)
        time.sleep(0.05)

def move_in_x_pattern(seconds):
    """
    Moves the Robomaster in an X-shaped pattern.
  
    Parameters:
    seconds (int): The duration of the movement pattern in seconds.
  
    Returns:
    void
    """
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.move_with_time(90, math.sqrt(seconds))
    chassis_ctrl.move_with_time(-45, seconds)
    chassis_ctrl.move_with_time(90, math.sqrt(seconds))
    chassis_ctrl.move_with_time(-135, seconds)
    chassis_ctrl.stop()

def move_in_cross_pattern(distance):
    """
    Moves the Robomaster in an cross-shaped pattern.
  
    Parameters:
    distance (int): The vertical and horizontal distance in to travel in m. Has a range of [0, 5] m.
  
    Returns:
    void
    """
    chassis_ctrl.set_trans_speed(1.5)
    chassis_ctrl.move_with_distance(0, distance)
    chassis_ctrl.move_with_distance(180, distance / 2)
    chassis_ctrl.move_with_distance(-90, distance / 2)
    chassis_ctrl.move_with_distance(90, distance)

def move_in_square_pattern(velocity, wait):
    """
    Moves the Robomaster in an square-shaped pattern.
  
    Parameters:
    velocity (int): The velocity of the Robomaster's wheels in RPM.
    wait (int): The waiting period in seconds before completing another side of the square.
  
    Returns:
    void
    """
    chassis_ctrl.set_wheel_speed(velocity,-velocity,-velocity,velocity)
    time.sleep(wait)
    chassis_ctrl.set_wheel_speed(velocity,velocity,velocity,velocity)
    time.sleep(wait)
    chassis_ctrl.set_wheel_speed(-velocity,velocity,velocity,-velocity)
    time.sleep(wait)
    chassis_ctrl.set_wheel_speed(-velocity,-velocity,-velocity,-velocity)

def start():
    """
    The entry-point method for the program.

    Moves the Robomaster in a movement pattern.
    """
    move_in_circle_pattern(130, 1, 15)
    #move_in_x_pattern(2)
    #move_in_cross_pattern(1)
    #move_in_square_pattern(100, 2)
