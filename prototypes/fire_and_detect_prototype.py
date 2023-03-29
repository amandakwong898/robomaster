"""
fire-and-detect-prototype.py:
The Robomaster S1's gimbal is first set to wake mode, enabling robot 
identification and clapping. The gimble switches to red and begins to 
detect another Robomaster S1 in front when the Robomaster S1 hears 
two claps. The Robomaster S1 fires four times if it detects another
robot; else, it will emit a C-sharp sound.
"""

#pylint: disable=unused-argument
def sound_recognized_applause_twice(msg):
    """
    When RoboMaster detects another RoboMaster, it will fire 4 times.
    The gimbal color will change to red and make a C-sharp sound, indicating
    the detection.

    Parameters:
    msg - supplied by the RoboMaster and invoked automatically
  
    Returns:
    void
    """
    led_ctrl.set_top_led(rm_define.armor_top_all, 255, 0, 0, rm_define.effect_always_on)
    if vision_ctrl.check_condition(rm_define.cond_recognized_car):
        gun_ctrl.set_fire_count(4)
        gun_ctrl.fire_once()
        chassis_ctrl.enable_stick_overlay()
        chassis_ctrl.move_and_rotate(135, rm_define.clockwise)
        robot_ctrl.set_mode(rm_define.robot_mode_free)
        time.sleep(4)
        if chassis_ctrl.is_impact() :
            media_ctrl.play_sound(rm_define.media_sound_attacked)
            media_ctrl.play_sound(rm_define.media_sound_solmization_1DSharp)
    else:
        media_ctrl.play_sound(rm_define.media_sound_solmization_3C)
    time.sleep(8)

def start():
    """
    The entry-point method for the program.
    Configures flash, sound recognition, and detection before sleeping for 8 seconds.
    """
    led_ctrl.set_flash(rm_define.armor_all, 1)
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    vision_ctrl.enable_detection(rm_define.vision_detection_car)
    gimbal_ctrl.resume()
    time.sleep(8)
