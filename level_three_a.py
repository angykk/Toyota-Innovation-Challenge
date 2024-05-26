# Start with imports, ie: import the wrapper
#import other libraries as needed
import TMMC_Wrapper
import rclpy
import math
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

        # #start stop sign code
        image = robot.rosImg_to_cv2()
        model = YOLO('yolov8n.pt')
        stop_status = robot.ML_predict_stop_sign(model,image)
        
        if (stop_status[0]):
            print("stop sign detected")
            robot.set_cmd_vel(0,0,5)
        # end stop sign code

        #crash detection and movement controls
        if(ranges[0] > 0.0 and ranges[0] < 0.3):
            print("distance from collision: ", ranges[0])
            print("angle from collision: ", ranges[1])
            robot.set_cmd_vel(-0.15,0,1)
           
            print("turning 90 degrees: ", -1*(math.pi/2))
            robot.set_cmd_vel(0,-1*(math.pi/2), 1)
        else:
            robot.set_cmd_vel(0.5,0,1)

        #Add looping functionality here
        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    #add functionality to ending processes here

    robot.destroy_node()
    rclpy.shutdown()
