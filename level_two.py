import TMMC_Wrapper
import rclpy
#Start Process
def checkForStopSigns(image):
    """Takes an NP image and returns whether or not a stopsign in is in view"""
    print("In SS Function")
    try:   
        print("starting SS search")
        image = red_filter(image)
        image = add_contour(image)
        model = YOLO('yolo8n.pt')
        isStopSign = ML_predict_stop_sign(model,image)

        if isStopSign:
            print("stop sign")
            return True
        else:
            print("no stop sign")
            return False
    except Exception as err:
        print (err)

__all__ = ['checkForStopSigns']
