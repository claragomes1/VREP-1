"""pioneer_180 controller"""

from controller import Robot, Motor, Lidar
import time
import pandas as pd


#Como girar 90 graus?
#ramdom que escolhe se vira ou não quando tiver mais de uma opção, pois o objetivo não é chegar ao destino mais rápido

def executarAcao (estado):
    if estado == 0:
        print("saida direita")
        left_wheel.setVelocity(2.0)
        right_wheel.setVelocity(1.0)
      
    if estado == 1:
        print("saida_esquerda")
        left_wheel.setVelocity(1.0)
        right_wheel.setVelocity(2.0)
    if estado == 2:
         print("saida_direita_esquerda")
    if estado == 3:
         print("encruzilhada_esquerda")
    if estado == 4:
         print("encruzilhada_direita")
    if estado == 5:
         print("encruzilhada")
    if estado == 6:
         print("corredor")
         
         
def seguirParedeDir (distDir, rangeImage):
    dirAtual = rangeImage[2];
    if(dirAtual > distDir):
        left_wheel.setVelocity(3.0)
        right_wheel.setVelocity(4.0)
    else:
        left_wheel.setVelocity(4.0)
        right_wheel.setVelocity(3.0)
         



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

#DEFINICOES

rangeImageComplete = []
rangeImageAux = []
rangeImage = lidar.getRangeImage()
cont = 0
estado = 0


while robot.step(TIME_STEP) != -1:
    for cont in range(50):
        rangeImage = lidar.getRangeImage()#Pega os dados de cada ponto
        rangeImageAux.append(rangeImage)


    rangeImageComplete.append(rangeImageAux)
   # print(rangeImageComplete)
    #distDir = rangeImage[2]
    #estado = leEstadoAtual(rangeImageAux);#50 pontos
    
    if estado == 6:
        #seguirParedeDir(distDir, rangeImage);
        print("corredor")
        
    else:
        executarAcao(estado);
    estado = 6
    #rangeImageAux = []

rangeImageCompleteDf = pd.DataFrame(rangeImageAux)
rangeImageCompleteDf.to_csv('auxNovo.csv')


  #Colocar while estado == 6 em tudo. e depois executar ação  
  #Fazer algo dentro do executar acao para completar a curva por exemplo antes de sair
  #Salvar onde estava 
        

         
#def leEstadoAtual (rangemImageAux):
    


#retorna -1 quando o Webots finalizar o controlador
#while robot.step(TIME_STEP) != -1:#Sincroniza os dados do controlador com o simulador
#    rangeImage = lidar.getRangeImage()#Pega os dados de cada ponto
#    rangeImageComplete.append(rangeImage)




