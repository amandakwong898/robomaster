'''
clap_turn_left_right_prototype.py:

The client program waits for the user to clap twice before turning the RoboMaster right.

Afterwards, the client program waits for the user to clap three times before turning
the RoboMaster left.
'''

def sound_recignition_applause_twice(msg):
    """
    Waits for the user to clap twice before turning left.
    Afterwards, waits for the user to clap three times before turning right.

    Paramaters: msg (unused)

    Returns:
    void
    """
    # pylint: disable=unused-argument
    ir_blaster_ctrl.fire_continuous()
    gimbal_ctrl.recenter()
    if media_ctrl.check_condition(rm_define.cond_cound_recognized_applause_twice):
        gimbal_ctrl.rotate_with_degree(rm_define.gimbal_right,90)
    elif media_ctrl.check_condition(rm_define.cond_cound_recognized_applause_thrice):
        gimbal_ctrl.rotate_with_degree(rm_define.gimbal_left,90)
    else:
        gun_ctrl.fire_once()

def start():
    """
    The entry-point method for the program.

    Enables sound detection and sets the RoboMaster's chassis to follow mode.

    """
    media_ctrl.enable_sound_recognition(rm_define.sound_detection_applause)
    robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)
    time.sleep(8)
