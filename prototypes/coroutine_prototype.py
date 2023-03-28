"""
coroutine_prototype.py:

Implements a data class that holds all of the possible states for
the RoboMaster and a collection of coroutines that implement
a few of the possible states.

The client program randomly changes the Robomaster's state before
running the corresponding coroutine for that state.
"""
# These checks must be disabled due to the restrictions of the RoboMaster app.
# pylint: disable=unnecessary-dunder-call, unsubscriptable-object, no-self-argument
# All class methods are static but are not denoted as such since the RoboMaster app
# does not support function decorators.

import math

class RoboMasterDimensions:
    """
    A collection of function that estimates the distance between the RoboMaster
    and a target using the camera's focal length and DPI.
    """

    # Height of the Robomaster in mm.
    ROBOMASTER_HEIGHT_MM = 270.0
    # Height of the Robomaster in in.
    ROBOMASTER_HEIGHT_IN = 10.6
    # Camera focal length for the Robomaster.
    ROBOMASTER_CAMERA_FOCAL_LENGTH = 1.0
    # Camera DPI for the Robomaster.
    ROBOMASTER_CAMERA_DPI = 72.0

    def distance_in_mm(height):
        """
        Returns distance to an object in mm.
  
        Parameters:
        height (int): Height of the object's bounding box in mm.
  
        Returns:
        float: Distance to an object in mm.
        """
        return (RoboMasterDimensions.ROBOMASTER_CAMERA_FOCAL_LENGTH *
                RoboMasterDimensions.ROBOMASTER_HEIGHT_MM) / height

    def pixels_to_mm(pixels):
        """
        Converts pixels to mm based on the DPI for the Robomaster's camera.
  
        Parameters:
        pixels (int): Pixel length from the Robomaster's camera.
  
        Returns:
        float: Pixel length from the Robomaster's camera in mm.
        """
        return (pixels * 25.4) / RoboMasterDimensions.ROBOMASTER_CAMERA_DPI

    def get_closest_target_height(hits):
        """
        Finds the bounding box height for the closest target in a list of targets.
  
        Parameters:
        hits (List): A list of detected targets from vision_ctrl.
  
        Returns:
        int: Pixel length for the closest target.
        """
        closest = math.inf

        for i in range(4, len(hits), 4):
            if hits[i] < closest:
                closest = hits[i]

        return closest

    def distance_to_robomaster_in_m(hits):
        """
        Returns the distance from the closest detected object to the RoboMaster in m.
  
        Parameters:
        distance (int): The vertical and horizontal distance in to travel in m.
        Has a range of [0, 5] m.
  
        Returns:
        void
        """
        # Height of the bounding box for the closest target.
        bounding_box_height = RoboMasterDimensions.get_closest_target_height(hits)

        # Height of the bounding box in mm.
        height_in_mm = RoboMasterDimensions.pixels_to_mm(bounding_box_height)
        # Distance from the Robomaster to the target in m.
        distance_in_m = RoboMasterDimensions.distance_in_mm(height_in_mm) / 1000

        return distance_in_m

class RoboMasterMovements:
    """
    A collection of functions that move the RoboMaster in one of two different ways:
    Cross-shaped movement pattern: Moves the RoboMaster in an cross-shaped pattern.
    Target following: Moves the RoboMaster to a detected target.
    """

    # An inch in meters.
    INCH_IN_M = 0.0254
    # A foot in meters.
    FOOT_IN_M = 0.3048
    # A yard in meters.
    YARD_IN_M = 0.9144

    def move_in_cross_pattern(distance):
        """
        Moves the Robomaster in an cross-shaped pattern.
  
        Parameters:
        distance (int): The vertical and horizontal distance in to travel in m.
        Has a range of [0, 5] m.
  
        Returns:
        void
        """
        chassis_ctrl.set_trans_speed(1.5)

        while True:
            chassis_ctrl.move_with_distance(0, distance)
            yield
            chassis_ctrl.move_with_distance(180, distance / 2)
            yield
            chassis_ctrl.move_with_distance(-90, distance / 2)
            yield
            chassis_ctrl.move_with_distance(90, distance)
            yield

    def move_to_target(hits):
        """
        Moves to the closest target.
  
        Parameters:
        hits (List): A list of detected objects.
  
        Returns:
        void
        """

        targets_hit = hits[0]

        if targets_hit > 0:
            # Height of the bounding box for the closest target.
            bounding_box_height = RoboMasterDimensions.get_closest_target_height(hits)

            # Height of the bounding box in mm.
            height_in_mm = RoboMasterDimensions.pixels_to_mm(bounding_box_height)

            # Distance from the Robomaster to the target in m.
            distance_in_m = RoboMasterDimensions.distance_in_mm(height_in_mm) / 1000

            # Move to the target.
            chassis_ctrl.move_with_distance(0, distance_in_m)

# pylint: disable=too-few-public-methods
# This warning is diabled because the only purpose
# of this class is to hold data. This could be
# accomplished with an enum, but the RoboMaster
# does not support enums.
class RoboMasterState:
    """
    A data class that holds all of the possible states for the RoboMaster.

    PATROL: Patrols an area.
    CHASE: Chases another RoboMaster.
    ATTACK: Attacks another RoboMaster.
    FLEE: Runs away from another RoboMaster.
    IDLE: Waits and does nothing.
    TAGGED: Once detected by another RoboMaster, transitions to CHASE state.

    CURRENT_STATE: The RoboMaster's current state. The default is IDLE.

    """
    PATROL = "PATROL"
    CHASE = "CHASE"
    ATTACK = "ATTACK"
    FLEE = "FLEE"
    IDLE = "IDLE"
    TAGGED = "TAGGED"

    CURRENT_STATE = CHASE

def get_coroutine():
    """
    Returns a coroutine based on the RoboMaster's current state.

    When the current state is RoboMasterState.IDLE, it returns the idle coroutine.
    When the current state is RoboMasterState.PATROL, it returns the patrol coroutine.
    When the current state is RoboMasterState.CHASE, it returns the chase coroutine.
  
    Parameters:
    none
  
    Returns:
    void
    """
    if RoboMasterState.CURRENT_STATE == RoboMasterState.PATROL:
        return patrol()

    if RoboMasterState.CURRENT_STATE == RoboMasterState.CHASE:
        return chase()

    if RoboMasterState.CURRENT_STATE == RoboMasterState.ATTACK:
        return attack()

    if RoboMasterState.CURRENT_STATE == RoboMasterState.FLEE:
        return flee()

    if RoboMasterState.CURRENT_STATE == RoboMasterState.TAGGED:
        return idle()

    return idle()

def patrol():
    """
    Patrols while the current state is RoboMasterState.PATROL.

    Parameters:
    none
  
    Returns:
    void
    """
    current_movement_pattern = RoboMasterMovements.move_in_cross_pattern(1)

    print(RoboMasterState.CURRENT_STATE)
    while RoboMasterState.CURRENT_STATE == RoboMasterState.PATROL:
        if vision_ctrl.check_condition(rm_define.cond_recognized_people):
            RoboMasterState.CURRENT_STATE = RoboMasterState.CHASE
            yield
        current_movement_pattern.__next__()

    print("Finished Patrol")

def chase():
    """
    Chases another RoboMaster while the current state is RoboMasterState.CHASE.

    Parameters:
    none
    
    Returns:
    void
    """
    print(RoboMasterState.CURRENT_STATE)
    while RoboMasterState.CURRENT_STATE == RoboMasterState.CHASE:
        if not vision_ctrl.check_condition(rm_define.cond_recognized_people):
            chassis_ctrl.stop()
            RoboMasterState.CURRENT_STATE = RoboMasterState.PATROL
            yield
        chassis_ctrl.set_wheel_speed(100,100,100,100)
    print("Finished Chase")

def idle():
    """
    Idles while the current state is RoboMasterState.IDLE.

    Parameters:
    none
  
    Returns:
    void
    """
    print(RoboMasterState.IDLE)
    while RoboMasterState.CURRENT_STATE == RoboMasterState.IDLE:
        yield
    print("Finished Idle")

def attack():
    """
    Attacks while the current state is RoboMasterState.ATTACK.

    Parameters:
    none
  
    Returns:
    void
    """
    print(RoboMasterState.ATTACK)
    while RoboMasterState.CURRENT_STATE == RoboMasterState.ATTACK:
        yield
    print("Finished Attack")

def flee():
    """
    Flees while the current state is RoboMasterState.FLEE.

    Parameters:
    none
  
    Returns:
    void
    """
    print(RoboMasterState.FLEE)
    current_movement_pattern = RoboMasterMovements.move_in_cross_pattern(1)
    while RoboMasterState.CURRENT_STATE == RoboMasterState.FLEE:
        if vision_ctrl.check_condition(rm_define.cond_recognized_people):
            chassis_ctrl.move_with_distance(180, 2)
        else:
            current_movement_pattern.__next__()
    print("Finished Flee")
    chassis_ctrl.stop()

def tagged():
    """
    Determines if RoboMaster is tagged (still ip - physical attack? within range? etc.)

    Parameters:
    none

    Returns:
    void   
    """

    return False

def start():
    """
    The entry-point method for the program.
    Randomly changes the Robomaster's state before running the corresponding
    coroutine for that state.
    """
    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    current_coroutine = get_coroutine()

    while RoboMasterState.CURRENT_STATE != RoboMasterState.IDLE:
        try:
            current_coroutine.__next__()
            # pylint: disable=broad-exception-caught
            # A StopIteration exception is always raised when exiting
            # a coroutine but the RoboMaster does not recognize it.
            # The solution to this problem is catching a
            # general exception.
        except Exception:
            current_coroutine = get_coroutine()
