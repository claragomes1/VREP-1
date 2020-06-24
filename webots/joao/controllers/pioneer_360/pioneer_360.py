"""pioneer_360 controller"""

from controller import Robot
import pandas as pd
from csv import writer

def appendListAsRow(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

TIME_STEP = 32
robot = Robot()
lidar = robot.getLidar("LDS-01")
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
range_image = lidar.getRangeImage()
range_image_df = pd.DataFrame([range_image])
range_image_df.to_csv('corredor.csv')

counter = 1
lado = 90
corredor = range_image[lado]
while robot.step(TIME_STEP) != -1:
    range_image = lidar.getRangeImage()
    if range_image[lado] < corredor:
        left_wheel.setVelocity(3.1)
        right_wheel.setVelocity(3.0)
    else:
        left_wheel.setVelocity(3.0)
        right_wheel.setVelocity(3.1)
    appendListAsRow('corredor.csv', [counter] + range_image)
    counter += 1
