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

#add starter functions here

#rclpy,spin_once is a function that updates the ros topics once
rclpy.spin_once(robot, timeout_sec=0.1)

#run control functions on loop
try:
    print("Entering the robot loop which cycles until the script is stopped")
    while True:
        ranges = robot.detect_obstacle(robot.checkScan().ranges)
        while(ranges[0] == -1):
            robot.set_cmd_vel(1,0,1)

        if(ranges[0] > 0.0 and ranges[0] < 0.3):
            print("dist: ")
            print(ranges[0])
            print("\n")
            print("angle: ")
            print(ranges[1])
            robot.set_cmd_vel(-0.10,0,2)
           
            robot.set_cmd_vel(0,0,1)
            print("turning", math.pi - 0.0174533*ranges[1])
            robot.set_cmd_vel(0,math.pi - 0.0174533*ranges[1], 1)


        #Add looping functionality here
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here

    robot.destroy_node()
    rclpy.shutdown()
