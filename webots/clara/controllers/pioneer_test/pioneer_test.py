"""pioneer_test controller"""

from controller import Robot, Motor, Lidar
import time
import pandas as pd

TIME_STEP = 32

robot = Robot()#Pioneer 3 

#inicializar os dispositivos

lidar = robot.getLidar("Sick LMS 291")#Alcance de 80 metros e pega os dados em 180 graus
lidar.enable(TIME_STEP)#O Lidar mede informações em metros da renderização do sensor
lidar.enablePointCloud()

left_wheel = robot.getMotor("left wheel")
left_wheel.setPosition(float('inf'))
left_wheel.setVelocity(3.0)

right_wheel = robot.getMotor("right wheel")
right_wheel.setPosition(float('inf'))
right_wheel.setVelocity(3.0)

robot.step(TIME_STEP)

rangeImageComplete = []


#retorna -1 quando o Webots finalizar o controlador
while robot.step(TIME_STEP) != -1:#Sincroniza os dados do controlador com o simulador
    rangeImage = lidar.getRangeImage()#Pega os dados de cada ponto
    rangeImageComplete.append(rangeImage)


rangeImageCompleteDf = pd.DataFrame(rangeImageComplete)
rangeImageCompleteDf.to_csv('corredor_encruzilhada_corredor_esquerda.csv')
