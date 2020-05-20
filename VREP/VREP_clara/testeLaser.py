import vrep
import time

serverIP = '127.0.0.1'
serverPort = 19999
laserScannerHandle = 0

clientID = vrep.simxStart(serverIP, serverPort, True, True, 2000, 5)
if clientID != -1:
    print('Servidor conectado!')

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_streaming)
    if error != vrep.simx_return_novalue_flag:
        print(str(error) + '! signalValue')

    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    print(signalValue)
    data = vrep.simxUnpackFloats(signalValue)
    print(data)
    time.sleep(0.1)
    error, signalValue = vrep.simxGetStringSignal(clientID, 'measuredDataAtThisTime', vrep.simx_opmode_buffer)
    data = vrep.simxUnpackFloats(signalValue)
    print(data)
    time.sleep(0.1)
