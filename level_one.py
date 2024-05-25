# Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math
from level_two import checkForStopSigns

#Start ros with initializing the rclpy object
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #Specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#Debug messaging 
print("running main")

#start processes
robot.start_keyboard_control()
#add starter functions here

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

#run control functions on loop
try:
    print("Entering the robot loop which cycles until the script is stopped")
    while True:
        print("A")
        #rclpy,spin_once is a function that updates the ros topics once
        #rclpy.spin_once(robot, timeout_sec=0.1)

        # robot.checkImage()
        # print("B", robot.checkImage())
        # print("C",rosImg_to_cv2())
        # checkForStopSigns(rosImg_to_cv2())

        if(robot.detect_obstacle(robot.checkScan().range)) < 0.3):
            print("back")
            set_cmd_vel(0.5,0,1)
            print("wait")
            set_cmd_vel(0,0,5)
            print("turn")
            set_cmd_vel(0,0.5*3.14, 2)


        #Add looping functionality here
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()
