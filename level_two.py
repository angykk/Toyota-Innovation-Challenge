import TMMC_Wrapper
import rclpy

#start ros
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #specify hardware api
    TMMC_Wrapper.use_hardware()
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#debug messaging 
print("running level_two: Stop Sign")

#Start Process
try:
    while True:
        robot.checkScan()
        robot.checkImage()
        currentImg = robot.rosImg_to_cv2()
        currentImg = robot.red_filter(currentImg)
        currentImg = robot.add_contour(currentImg)
        model = YOLO('yolo8n.pt')
        isStopSign = robot.ML_predict_stop_sign(model,currentImg)

        if isStopSign:
            print("stop sign")
        else:
            print("no stop sign")
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
