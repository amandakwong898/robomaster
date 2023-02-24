import math

# Height of the Robomaster in mm.
ROBOMASTER_HEIGHT_MM = 270.0
# Height of the Robomaster in in.
ROBOMASTER_HEIGHT_IN = 10.6
# Camera focal length for the Robomaster.
ROBOMASTER_CAMERA_FOCAL_LENGTH = 1.0
# Camera DPI for the Robomaster.
ROBOMASTER_CAMERA_DPI = 72.0
# Enum code for targeting a person.
TARGET_PERSON = 1.0
# Enum code for targeting a car.
TARGET_CAR = 2.0

def distance_in_mm(height):
    """
    Returns distance to an object in mm.
  
    Parameters:
    height (int): Height of the object's bounding box in mm.
  
    Returns:
    float: Distance to an object in mm.
    """
    return (ROBOMASTER_CAMERA_FOCAL_LENGTH * ROBOMASTER_HEIGHT_MM) / height

def pixels_to_mm(pixels):
    """
    Converts pixels to mm based on the DPI for the Robomaster's camera.
  
    Parameters:
    pixels (int): Pixel length from the Robomaster's camera.
  
    Returns:
    float: Pixel length from the Robomaster's camera in mm.
    """
    return (pixels * 25.4) / ROBOMASTER_CAMERA_DPI

def move_to_closest_target(target_type=TARGET_PERSON, speed=1.5):
    """
    Wait for targets to appear and then moves to the closest target.
  
    Parameters:
    target_type (int): The type of target to move to.
    
    TARGET_PERSON targets a person.
    TARGET_CAR targets a car.
  
    Returns:
    void
    """
    chassis_ctrl.set_trans_speed(speed)
    target = None
    hits = None

    if target_type == TARGET_PERSON:
        target = rm_define.vision_detection_people
    else:
        target = rm_define.vision_detection_car
    
    # Enable target detection
    vision_ctrl.enable_detection(target)

    print("Waiting for the target to be visible...")

    # Wait for a person to become visible on screen.

    if target_type == TARGET_PERSON:
        vision_ctrl.cond_wait(rm_define.cond_recognized_people)
    else:
        vision_ctrl.cond_wait(rm_define.cond_recognized_car)

    print("Recognized a target...")

    # Get the people detection information.
    if target_type == TARGET_PERSON:
        hits = vision_ctrl.get_people_detection_info()
    else:
        hits = vision_ctrl.get_car_detection_info()

    # Number of people detected
    targets_hit = hits[0]
    
    # Height of the bounding box for the closest target.
    bounding_box_height = get_closest_target_height(hits)

    # Height of the bounding box in mm.
    height_in_mm = pixels_to_mm(bounding_box_height)
    # Distance from the Robomaster to the target in m.
    distance_in_m = distance_in_mm(height_in_mm) / 1000

    print("Hits: " + str(hits))
    print("Number of targets found: " + str(targets_hit))
    print("Height of the bounding box: " + str(height_in_mm) + " mm")
    print("Distance to target: " + str(distance_in_m) + " m")

    print("Driving to target...")
    # Drive to the person based on the estimated distance to that person.
    chassis_ctrl.move_with_distance(0, distance_in_m)

def get_closest_target_height(hits):
    """
    Finds the bounding box height for the closest target in a list of targets.
  
    Parameters:
    hits (List): A list of detected targets from vision_ctrl.
  
    Returns:
    int: Pixel length for the closest target.
    """
    targets_hit = hits[0]
    closest = math.inf

    for i in range(4, len(hits), 4):
        if hits[i] < closest:
            closest = hits[i]
    
    return closest

def start():
    """
    The entry-point method for the program.

    Moves to the closest target.
    """
    move_to_closest_target()