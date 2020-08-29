"""pioneer_180 controller"""

from controller import Robot, Motor, Lidar
import time
import pandas as pd
import leEstadoAtual
import scipy


def executarAcao(estado):
    if estado == 0:
        print("saida direita")
    if estado == 1:
        print("saida_esquerda")
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
    if estado == 7:
        print("Erro ao encontrar o estado !")


TIME_STEP = 32

# Criando o robo

robot = Robot()  # Pioneer 3

# inicializando os dispositivos

lidar = robot.getLidar("Sick LMS 291")  # Alcance de 80 metros e pega os dados em 180 graus
lidar.enable(TIME_STEP)  # O Lidar mede informações em metros da renderização do sensor
lidar.enablePointCloud()

left_wheel = robot.getMotor("left wheel")
left_wheel.setPosition(float('inf'))
left_wheel.setVelocity(3.0)

right_wheel = robot.getMotor("right wheel")
right_wheel.setPosition(float('inf'))
right_wheel.setVelocity(3.0)

robot.step(TIME_STEP)

dataset = leEstadoAtual.create_df()

# DEFINICOES

rangeImageCompleteDf = []
rangeImageAux = []
rangeImage = lidar.getRangeImage()
cont = 0
estado = 6
# Rodando o programa

columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
           '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37',
           '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
           '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73',
           '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91',
           '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '102', '103', '104', '105', '106', '107',
           '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122',
           '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137',
           '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150', '151', '152',
           '153', '154', '155', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167',
           '168', '169', '170', '171', '172', '173', '174', '175', '176', '177', '178', '179']

while robot.step(TIME_STEP) != -1:
    for cont in range(50):
        rangeImage = lidar.getRangeImage()  # Pega os dados de cada ponto
        if not rangeImage:
            cont = cont - 1
        else:
            rangeImageAux.append(rangeImage)

    rangeImageCompleteDf = pd.DataFrame(rangeImageAux)
    #print(rangeImageCompleteDf)
    #print(dataset)

    rangeImageCompleteDf.astype(str)
    rangeImageCompleteDf.columns = columns
    # dataset.columns.aplly(str)
    cols = dataset.columns.tolist()
    #print(cols)
    cols1 = rangeImageCompleteDf.columns.tolist()
    #print(cols1)
    dataset.to_csv('dataset.csv')

    # dataset.columns = columns

    # rangeImageCompleteDf.to_csv('rangeimage.csv')
    # rangeImageCompleteDf.drop([], axis=1, inplace=True)
    # rangeImageCompleteDf.columns = columns
    # dataset = pd.concat(
    #   [dataset, rangeImageCompleteDf], axis=0, ignore_index=True)
    dataset = dataset.append(rangeImageCompleteDf, ignore_index=True)
    #print(dataset)
    # dataset.to_csv('datasetAppend.csv')
    # rangeImageCompleteDf.to_csv('rangeimage.csv')

    estado = leEstadoAtual.leEstado(dataset);  # 50 pontos
    # print(estado)
    executarAcao(estado);
    rangeImageAux = []
