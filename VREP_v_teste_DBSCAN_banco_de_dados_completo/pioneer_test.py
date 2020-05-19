"""pioneer_test controller"""

from controller import Robot
import pandas as pd

TIME_STEP = 32

robot = Robot()

lidar = robot.getLidar("Sick LMS 291")
lidar.enable(TIME_STEP)
lidar.enablePointCloud()

left_wheel = robot.getMotor("left wheel")
left_wheel.setPosition(float('inf'))
left_wheel.setVelocity(3.0)

right_wheel = robot.getMotor("right wheel")
right_wheel.setPosition(float('inf'))
right_wheel.setVelocity(3.0)

robot.step(TIME_STEP)
robot.step(TIME_STEP)
robot.step(TIME_STEP)

rangeImageComplete = []
robot.step(TIME_STEP)
rangeImage = lidar.getRangeImage()
corredor = rangeImage[0]

while robot.step(TIME_STEP) != -1:
    rangeImage = lidar.getRangeImage()
    rangeImageComplete.append(rangeImage)
    if rangeImage[0] < corredor:
        left_wheel.setVelocity(3.1)
        right_wheel.setVelocity(3.0)
    else:
        left_wheel.setVelocity(3.0)
        right_wheel.setVelocity(3.1)

rangeImageCompleteDf = pd.DataFrame(rangeImageComplete)
rangeImageCompleteDf.to_csv('teste.csv')
