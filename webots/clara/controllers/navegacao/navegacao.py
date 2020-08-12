"""pioneer_180 controller"""

from controller import Robot, Motor, Lidar
import time


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



#inicializar o cluster
saida_direita = pd.read_csv('saida_direita.csv', index_col='object')
saida_esquerda = pd.read_csv('saida_esquerda.csv', index_col = 'object')
saida_direita_esquerda = pd.read_csv('saida_direita_esquerda.csv', index_col='object')
encruzilhada_esquerda = pd.read_csv('encruzilhada_esquerda.csv', index_col='object')
encruzilhada_direita = pd.read_csv('encruzilhada_direita.csv', index_col='object')
encruzilhada = pd.read_csv('encruzilhada.csv', index_col='object')
corredor = pd.read_csv('corredor.csv', index_col='object')

dataset = pd.concat([saida_direita, saida_esquerda, saida_direita_esquerda, encruzilhada_esquerda, encruzilhada_direita, encruzilhada, corredor], axis=0, ignore_index=True)
dataset.head()

dataset['label'] = dataset['label'].replace('saida_direita',0)
dataset['label'] = dataset['label'].replace('saida_esquerda',1)
dataset['label'] = dataset['label'].replace('saida_direita_esquerda',2)
dataset['label'] = dataset['label'].replace('encruzilhada_esquerda',3)
dataset['label'] = dataset['label'].replace('encruzilhada_direita',4)
dataset['label'] = dataset['label'].replace('encruzilhada',5)
dataset['label'] = dataset['label'].replace('corredor',6)


datasetNoLabel = dataset.drop(columns=['label'])
print(datasetNoLabel)

datasetNoLabel = normalize(datasetNoLabel)


plt.figure(figsize=(25, 20))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dend = shc.dendrogram(shc.linkage(datasetNoLabel, method='ward'), truncate_mode='lastp', leaf_rotation=45., leaf_font_size=10., show_contracted=True )
plt.axhline(y=10, color='r', linestyle='--')

cluster = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='ward')
cluster.fit_predict(datasetNoLabel)
print(cluster.labels_)


rangeImageComplete = []
rangeImagemAux = []
cont = 0

def Navegacao():
    estado = 6
    while robot.step(TIME_STEP) != -1:
        for cont in 50:
            rangeImage = lidar.getRangeImage()#Pega os dados de cada ponto
            rangeImageAux.append(rangeImage)
        cont = 0
        rangeImageComplete.append(rangeImage)
        distDir = rangeImage[2]
        estado = leEstadoAtual(rangeImageAux);#50 pontos
        if estado == 6:
            seguirParedeDir(distDir, rangeImage);
            print("corredor")
        else:
            executarAcao(estado);

    
def seguirParedeDir (distDir):
    dirAtual = rangeImage[2];
    if(dirAtual > distDir):
        left_wheel.setVelocity(3.0)
        right_wheel.setVelocity(4.0)
    else:
        left_wheel.setVelocity(4.0)
        right_wheel.setVelocity(3.0)
        
def executarAcao (estado):
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
         
         
def leEstadoAtual (rangemImage):
    


#retorna -1 quando o Webots finalizar o controlador
while robot.step(TIME_STEP) != -1:#Sincroniza os dados do controlador com o simulador
    rangeImage = lidar.getRangeImage()#Pega os dados de cada ponto
    rangeImageComplete.append(rangeImage)


rangeImageCompleteDf = pd.DataFrame(rangeImageComplete)
rangeImageCompleteDf.to_csv('certo.csv')
