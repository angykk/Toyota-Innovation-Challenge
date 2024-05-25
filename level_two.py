import TMMC_Wrapper
import rclpy
from ultralytics import YOLO

#Start Process
def checkForStopSigns(image):
    """Takes an NP image and returns whether or not a stopsign in is in view"""
    print("In SS Function")
    try:   
        print("starting SS search")
        model = YOLO('yolov8n.pt')
        isStopSign = ML_predict_stop_sign(model,image)

        if isStopSign:
            print("stop sign")
            return True
        else:
            print("no stop sign")
            return False
    except Exception as err:
        print (err)
        return False

__all__ = ['checkForStopSigns']
