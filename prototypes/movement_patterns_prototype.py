import math

def move_in_circle_pattern(velocity, radius, seconds):
    """
    Moves the Robomaster in a circle pattern.
  
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

def move_in_cross_pattern(seconds):
    """
    Moves the Robomaster in a cross pattern.
  
    Parameters:
    seconds (int): The duration of the movement pattern in seconds.
  
    Returns:
    void
    """
    chassis_ctrl.set_trans_speed(1)
    chassis_ctrl.move_with_time(90,math.sqrt(seconds))
    chassis_ctrl.move_with_time(-45,seconds)
    chassis_ctrl.move_with_time(90,math.sqrt(seconds))
    chassis_ctrl.move_with_time(-135,seconds)
    chassis_ctrl.stop()

def start():
    """
    The entry-point method for the program.

    Moves the Robomaster in a movement pattern.
    """
    move_in_circle(130, 1, 15)
    #move_in_cross_pattern(2)