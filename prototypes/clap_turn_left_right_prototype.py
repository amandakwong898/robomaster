def sound_recignition_applause_twice(msg):
  ir_blaster_ctrl.fire_continuous()
  gimbal_ctrl.recenter()
  if media_ctrl.check_condition(rm_define.cond_cound_recognized_applause_twice) :
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_right,90)
  else:
      if media_ctrl.check_condition(rm_define.cond_cound_recognized_applause_thrice) :
    gimbal_ctrl.rotate_with_degree(rm_define.gimbal_left,90)
      else:
        gun_strl.fire_once()
def start():
  media_strl.enable_sound_recognition(rm_define.sound_detection_applause)
  robot_ctrl.set_mode(rm_define.robot_mode_chassis_follow)
  time.sleep(8)
