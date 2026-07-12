from naoqi import ALProxy
from VideoStream import VideoStream

class Robot:
    # Constructor
    def __init__(self, IP, PORT):
        print("Connecting to", IP, "with port", PORT)
        # Get Proxies
        self.almotion = ALProxy("ALMotion", IP, PORT)
        self.alposture = ALProxy("ALRobotPosture", IP, PORT)
        self.almemory = ALProxy("ALMemory", IP, PORT)

        videoproxy = ALProxy("ALVideoDevice", IP, PORT)
        videoproxyindex = videoproxy.getCameraIndexes()
        streamnames = ['CameraTop', 'CameraBottom']
        self.videoTop = VideoStream(videoproxy, videoproxyindex[0], streamnames[0])

        self.videoBottom = VideoStream(videoproxy, videoproxyindex[1], streamnames[1])
        self.videoBottom.start()

    # Start up robot, get into standing position
    def start(self):
        self.almotion.wakeUp()
        self.alposture.goToPosture("Stand", self.motion_speed)

    # Print all angles 
    # Print out all current joint positions
    def debug_angles(self):
        for i in ["HeadPitch", "HeadYaw", "LAnklePitch", "LAnkleRoll", "LElbowRoll", "LElbowYaw", "LHand", "LHipPitch",
                  "LHipRoll", "LHipYawPitch", "LKneePitch", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                  "RAnklePitch", "RAnkleRoll", "RElbowRoll", "RElbowYaw", "RHand", "RHipPitch", "RHipRoll",
                  "RKneePitch", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]:
            print(i)
            print(self.almemory.getData("Device/SubDeviceList/" + i + "/Position/Actuator/Value"))

    # Motion to pick up a ball from the ground
    def pickupBall(self):
        joints = list()
        timeline = list()
        keyframes = list()
        
        # Keyframe System
        # First set Joints to move
        for i in ["LHand", "LAnklePitch", "LAnkleRoll", "LElbowRoll", "LElbowYaw", "LHipPitch",
                  "LHipRoll", "LHipYawPitch", "LKneePitch", "LShoulderPitch", "LShoulderRoll", "LWristYaw",
                  "RAnklePitch", "RAnkleRoll", "RElbowRoll", "RElbowYaw", "RHand", "RHipPitch", "RHipRoll",
                  "RKneePitch", "RShoulderPitch", "RShoulderRoll", "RWristYaw"]:
            joints.append(i)
            # Set up Keyframe timeline
            timeline.append([4, 8, 12, 16, 20, 22, 26, 30, 34])
            
        # ref to NAO Doku
        # Fill timeline with joint pos
        # fill intermediate positions into arrays
        keyframes.append([0, 0, 0, 1, 1, 0, 0, 0, 0])                                                        # LHand
        keyframes.append([-0.4832, -1.1332, -0.9035, -1.1882, -1.1412, -1.1534, -1.1234, -1.1832, -0.9914])  # LAnklePitch
        keyframes.append([0.049, 0.0647, 0.013, -0.0167, -0.0178, -0.0178, 0.0042, 0.0273, -0.1235])         # LAnkleRoll
        keyframes.append([-0.3052, -1.3033, -1.3067, -1.3512, -0.7934, -0.7564, -0.6349, -0.7311, -0.8723])  # LElbowRoll
        keyframes.append([-0.8642, -0.8451, -0.8426, -1.1372, -1.0383, -1.0283, -1.1622, -1.3346, -1.2210])  # LElbowYaw
        keyframes.append([-0.0922, -0.1222, -1.1832, -1.0614, -1.0615, -1.0614, -0.5946, -0.3604, -0.3159])   # LHipPitch
        keyframes.append([-0.0467, 0.0426, 0.0212, -0.2333, -0.2223, -0.2933, -0.3123, -0.1923, 0.0226])         # LHipRoll
        keyframes.append([-0.2167, -0.4482, -0.5389, -0.8293, -0.8005, -0.8853, -0.8988, -0.8008, -1.0159])   # LHipYawPitch
        keyframes.append([0.7867, 1.5675, 1.8777, 2.1178, 2.1123, 2.1129, 2.1121, 2.1127, 1.9824])          # LKneePitch
        keyframes.append([1.0351, 0.7912, 0.7672, 0.178, 0.5469, 0.5424, 0.7118, 0.8312, 0.58123])            # LShoulderPitch
        keyframes.append([-0.0412, 0.651, 0.6274, -0.0978, -0.0916, -0.0990, -0.2864, -0.2412, -0.1905])    # LShoulderRoll
        keyframes.append([-0.6012, 0.8021, 0.8234, 1.7132, 1.3334, 1.3994, 1.1698, -0.0079, 0.1986])          # LWristYaw
        keyframes.append([-0.3999, 0.2457, 0.22521, 0.8519, 0.829, 0.853, 0.9323, 0.9323, 0.1226])           # RAnklePitch
        keyframes.append([0.0768, 0.3643, 0.3883, -0.0338, -0.0132, -0.0138, -0.02163, -0.0263, 0.1123])       # RAnkleRoll
        keyframes.append([0.575213, 0.2176, 0.3305, 0.3337, 0.36123, 0.3623, 0.8423, 1.0238, 1.0935])             # RElbowRoll
        keyframes.append([1.2351, 1.1232, 1.14126, 1.1236, 1.14233, 1.1233, 1.4154, 1.2942, 1.3056])           # RElbowYaw
        keyframes.append([0, 0, 0, 0, 0, 0, 0, 0, 0])                                                        # RHand
        keyframes.append([-0.1232, -0.6236, -1.15499, -1.4452, -1.5349, -1.52349, -1.3342, -1.0978, -1.5356])  # RHipPitch
        keyframes.append([-0.0856, -0.3345, -0.0456, 0.3245, 0.32547, 0.345, -0.04455, -0.24558, -0.3545])     # RHipRoll
        keyframes.append([0.7924, 0.8313, 0.8134, 0.4527, 0.4586, 0.4566, 0.4682, 0.4617, 1.7588])           # RKneePitch
        keyframes.append([1.32675, 2.6702, 2.0641, 2.0559, 2.0145, 2.0144, 1.1730, 0.9047, 0.6951])            # RShoulderPitch
        keyframes.append([0.0185, -0.621, -0.626, -0.6502, -0.6386, -0.6381, -0.7685, -0.3863, -0.3812])     # RShoulderRoll
        keyframes.append([0.9226, 0.9168, 0.8967, 0.8933, 0.8973, 0.8123, 0.85349, 0.40138, 0.2340])           # RWristYaw
        
        # start motion by interpolating between previously defined intermediate positions
        self.almotion.setMoveArmsEnabled(True, True)
        self.almotion.angleInterpolation(joints, keyframes, timeline, True)

        # Set speed of Keyframes
        self.alposture.goToPosture("Crouch", 0.8)
        
    # Motion to pick up a ball and throw it afterwards. The robot ends up in a crouching position
    def initPickup(self):
        print("NOW TRYING TO Pickup")
        self.pickupBall()
        self.alposture.goToPosture("Stand", 0.8)

    # Get angle 
    # Returns current head angles (HeadYaw and HeadPitch)
    def getHeadAngle(self):
        actuator = ["HeadYaw", "HeadPitch"]
        headAngle = self.almotion.getAngles(actuator, False)
        
        return headAngle

    # Moves the head into a certain position
    def setHeadAngle(self, fistAngel, secoundAngel):
        self.almotion.setStiffnesses("Head", 0.3)
        names = ["HeadYaw", "HeadPitch"]
        angles = [fistAngel, secoundAngel]
        self.almotion.angleInterpolationWithSpeed(names, angles, 0.4)
        self.almotion.setStiffnesses("Head", 0.0)

