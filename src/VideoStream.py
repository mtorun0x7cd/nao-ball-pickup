import threading
import logging
import time
import cv2
import numpy as np
import vision_definitions
from PIL import Image
from EventHook import EventHook

class VideoStream(threading.Thread):
    # Initialize the camera by subscribing the camera proxy object
    def __init__(self, camProxy, camIndex, name):
        self.isStopped = False
        super(VideoStream, self).__init__()
        self.alProyx = camProxy
        self.alIndex = camIndex
        self.name = name
        resolution = vision_definitions.kVGA
        colorSpace = vision_definitions.kRGBColorSpace
        fps = 30
        self.videoClient = camProxy.subscribeCamera(name, self.alIndex, resolution, colorSpace, fps)
        self.ImageEvent = EventHook()
        print(self.videoClient)

    # The Thread will fetch images until the isStopped flag is set
    # Each image triggers the onNewPic (*.fire) event
    def run(self):
        while self.isStopped is False:
            image, imageWidth, imageHeight, acq_time = self.__getImage__()
            
            if image is not None:
                self.ImageEvent.fire(image, imageWidth, imageHeight, acq_time)
                
        self.alProyx.unsubscribe(self.videoClient)

    def stop(self, stop=True):
        self.isStopped = stop

    # Get Image from Stream
    # Get a NAOqi image in remote and convert the retrieved image in a PIL (Python Image Library) format
    def __getImage__(self):
        image = self.alProyx.getImageRemote(self.videoClient)
        
        if image == None:
            print('error with Stream')
            self.alProyx.releaseImage(self.videoClient)
            
            return None, 0, 0
        else:
            print("Got Image from NAO")
            # Each image is in an array format
            imageWidth = image[0]
            imageHeight = image[1]
            array = image[6]
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)
            self.alProyx.releaseImage(self.videoClient)
            
            return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR), imageWidth, imageHeight
