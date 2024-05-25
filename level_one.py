# Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import numpy as np
import math
import cv2
from level_two import checkForStopSigns
from ultralytics import YOLO

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
        rclpy.spin_once(robot, timeout_sec=0.1)

        print("starting SS search")
        #image = robot.rosImg_to_cv2()
        image = cv2.imread("STOP_sign.jpeg",mode="RGB")
        model = YOLO('yolo8n.pt')

        if robot.ML_predict_stop_sign(model,image):
            print("stop sign")
            robot.set_cmd_vel(0,0,1)
        else:
            print("no stop sign")
  

        if((robot.detect_obstacle(robot.checkScan().ranges)[0]) < 0.1):
            print("back")
            robot.set_cmd_vel(-0.25,0,1)
            print("wait")
            robot.set_cmd_vel(0,0,5)
            print("turn")
            robot.set_cmd_vel(0,0.25*3.14, 4)


        #Add looping functionality here
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()
