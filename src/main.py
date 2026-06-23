# Author: Mert Torun (mtorun0x7cd)
from time import sleep
from robot import Robot
from recognition import Recognition

def main():
    # Replace with your NAO robot's IP address
    robot = Robot("<robot-ip>", 9559)
    robot.start()
    robotrecog = Recognition(robot)

if __name__ == "__main__":
    main()
