import TMMC_Wrapper
import rclpy

#Start Process
def checkForStopSign(self,image):
    """Takes, self and an NP image and returns whether or not a stopsign in is in view"""
    print("starting SS search")
    image = self.red_filter(image)
    image = self.add_contour(image)
    model = YOLO('yolo8n.pt')
    isStopSign = self.ML_predict_stop_sign(model,image)

    if isStopSign:
        print("stop sign")
        return True
    else:
        print("no stop sign")
        return False