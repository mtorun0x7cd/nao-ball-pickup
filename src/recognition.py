# import the necessary packages
import time
import cv2
import imutils
from EventHook import EventHook
from Controller import PD

class Recognition():
    # Init with HSV from init PIC Script
    # Thus initialize the recognition part by setting up all event listeners and defining the default HSV color 
    # that the robot will search for
    def __init__(self, robot):
        self.HSV_MIN = (165, 130, 116)
        self.HSV_MAX = (255, 255, 255)
        self.controller_x = PD(0.005, 0, 0.15)
        self.controller_y = PD(0.005, 0, 0.15)
        self.robot = robot
        robot.videoBottom.ImageEvent += self.checkBallInImage
        self.CanPickup = EventHook()
        self.CanPickup += robot.initPickup

    # Listens at the event onNewPic (Fire) so that after each received image of the NAOqi this method is fired
    def checkBallInImage(self, image, imgWidth, imgHeight):
        x, y, radius = self.maskImage(image)
        
        if radius > 0:
            self.followBall(x, y)
            
        cv2.imshow("Detection", image)

    # Finds the largest Shape in Image
    # The largest shape is the largest contour in the mask, then it's used to compute 
    # the minimum enclosing circle and centroid
    def getPositionofBall(self, center, cnts):
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        moments = cv2.moments(c)
        # Find centroid cx and cy
        center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"]))
        
        return center, radius, x, y

    # Mask the image and find the target
    # This is done by filtering the image and determining the position of the target
    # If the found target area has a radius of 3, we will draw a circle to make the detection visible
    def maskImage(self, frame):
        mask = self.createMaskforBall(frame)
        center, cnts = self.findPosOfBallinsideImage(mask)
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            center, radius, x, y = self.getPositionofBall(center, cnts)
            
            # check if circle is larger then X (thus if circle meets minimum radius x)
            if radius > 2:
                # Draw the circle and the centroid on the frame
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 0), 2)
                cv2.circle(frame, center, 1, (0, 0, 255), -1)
                print("center: " + str(center) + " radius: " + str(radius))
                
                return x, y, radius
                
        return 0, 0, 0

    # Create a mask for the ball 
    # This means, that we create a mask that holds only the target properties (ball)
    def createMaskforBall(self, frame):
        imageWithBlur = cv2.GaussianBlur(frame, (5, 5), 0)
        
        # convert the image to hsv color space, blur it, and detect edges
        hsv = cv2.cvtColor(imageWithBlur, cv2.COLOR_BGR2HSV)
        
        # Remove MIN MAX HSV
        # construct a mask for the color "orange", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, self.HSV_MIN, self.HSV_MAX)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        return mask

    # Find contours of the ball inside the image and initialize the current 
    # (x, y) center of the ball
    # We simply find the contours in the edged image and keep the largest one;
    # we'll assume that this is our ball in the image
    def findPosOfBallinsideImage(self, mask):
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        return None, contours

    # Check if Ball is in view, then move if not in center by delta x 
    # This will only be executed if a suitable ball is found 
    # This method controls the robot's head angles to that the robot can keep the target centered when tracked
    def followBall(self, x, y):
        yaw, pitch = self.robot.getHeadAngle()
        self.checkBallFound(pitch, x, y, yaw)
        targetyaw = yaw
        targetpitch = pitch
        
        if not (310 <= x <= 330):
            diff= x - 320
            targetyaw = yaw + 0.007 * diff
            
        if not (230 <= y <= 250):
            diff = y - 240
            targetpitch = pitch - + 0.007 * diff
            
        self.robot.setHeadAngle(targetyaw, targetpitch)

    # Check if the ball can be picked up
    # When the ball is placed in an optimal position and fire the event onBallInPos so that the NAOqi can start a pickup movement
    def checkBallFound(self, pitch, x, y, yaw):
        print("x: " + str(x) + " y: " + str(x))
        print("yaw: " + str(yaw) + " pitch: " + str(pitch))
        
        if -0.20 >= yaw >= -0.30:
            print ("yaw right")
            
        if 0.46 <= pitch <= 0.49:
            print ("pitch right")
            
        if 310 <= x <= 330:
            print ("x right")
            
        if 310 <= y <= 360:
            print ("y right")
            
        if 310 <= x <= 330 and -0.20 >= yaw >= -0.30 and 0.46 <= pitch <= 0.49:
            self.CanPickup.fire()







