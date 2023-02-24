# Make Robomaster fire his blaster every time he sees a person. Set the vision marker
# detection distance from 0.5 to 3 for farther distances.

def detect_and_fire():

    led1=0
    led2=255
    blink_rate=6,8
    
    robot_ctrl.set_mode(rm_define.robot_mode_free)

    vision_ctrl.enable_detection(rm_define.vision_detection_people)
    vision_ctrl.set_marker_detection_distance(1)

    led_ctrl.set_top_led(rm_define.armor_top_all,led2,led2,led1,rm_define.effect_breath)
    led_ctrl.set_bottom_led(rm_define.armor_bottom_all,led2,led2,1,rm_define.effect_breath)
    
    num_people_detected = 0
    num_blaster_shots = 0
        
    while True:            
        vision_ctrl.cond_wait(rm_define.cond_recognized_people)
        
        # Increment the number of people detected
        num_people_detected += 1
        
        while True:
            randgimbal_speed=random.randint(20,100)
            randup=random.randint(1,55)

            gimbal_ctrl.set_rotate_speed(randgimbal_speed)
            
            media_ctrl.play_sound(rm_define.media_sound_gimbal_rotate,wait_for_complete_flag=False)

            led_ctrl.set_flash(rm_define.armor_all,blink_rate[0])
            led_ctrl.set_top_led(rm_define.armor_top_all,led2,led1,led1,rm_define.effect_marquee)
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all,led2,led1,led1,rm_define.effect_flash)

            # MODIFY - get the dimensions of the bounding box around the detected person using the S1 API
            # if orientation == "right":
            #     gimbal_ctrl.rotate_with_degree(rm_define.gimbal_right, 10)
            # elif orientation == "left":
            #     gimbal_ctrl.rotate_with_degree(rm_define.gimbal_left, 10)
            # elif orientation == "up":
            #     gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up, 10)
            # elif orientation == "down":
            #     gimbal_ctrl.rotate_with_degree(rm_define.gimbal_down, 10)

            gimbal_ctrl.rotate_with_degree(rm_define.gimbal_up,randup)

            led_ctrl.set_flash(rm_define.armor_all,blink_rate[1])
            led_ctrl.set_top_led(rm_define.armor_top_all,led1,led2,led2,rm_define.effect_flash)
            led_ctrl.set_bottom_led(rm_define.armor_bottom_all,led1,led2,led2,rm_define.effect_flash)

            media_ctrl.play_sound(rm_define.media_sound_shoot,wait_for_complete_flag=True)
            media_ctrl.play_sound(rm_define.media_sound_shoot,wait_for_complete_flag=True)
            
            # Increment the number of blaster shots fired
            num_blaster_shots += 1

            commands_exit=random.randint(1,2)
            
            if commands_exit==1:
                continue
            elif commands_exit==2:
                led_ctrl.set_flash(rm_define.armor_all,blink_rate[0])
                led_ctrl.set_top_led(rm_define.armor_top_all,led2,led1,led1,rm_define.effect_marquee)
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all,led2,led1,led1,rm_define.effect_flash)
                
                gimbal_ctrl.recenter()

                led_ctrl.set_top_led(rm_define.armor_top_all,led2,led2,led1,rm_define.effect_breath)
                led_ctrl.set_bottom_led(rm_define.armor_bottom_all,led2,led2,1,rm_define.effect_breath)                        
                break
        
        # Print out the number of people detected and blaster shots fired
        print(f"Number of people detected: {num_people_detected}")
        print(f"Number of blaster shots fired: {num_blaster_shots}")

def start():
    detect_and_fire()
