import math

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

# Enable person detection
vision_ctrl.enable_detection(rm_define.vision_detection_people)

print("Waiting for a person to be visible...")

# Wait for a person to become visible on screen.
vision_ctrl.cond_wait(rm_define.cond_recognized_people)

print("Recognized a person...")

# Get the people detection information.
hits = vision_ctrl.get_people_detection_info()
# Number of people detected
people_hit = hits[0]
# Height of the bounding box for the first person detected.
bounding_box_height = hits[4]
# Height of the bounding box in mm.
height_in_mm = pixels_to_mm(bounding_box_height)
# Distance from the Robomaster to the person in m.
distance_in_m = distance_in_mm(height_in_mm) / 1000

print("Hits: " + str(hits))
print("Number of people found: " + str(people_hit))
print("Height of the bounding box: " + str(height_in_mm) + " mm")
print("Distance to person: " + str(distance_in_m) + " m")

print("Driving to person...")
# Drive to the person based on the estimated distance to that person.
chassis_ctrl.move_with_distance(0, distance_in_m)