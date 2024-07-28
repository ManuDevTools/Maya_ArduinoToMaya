'''This class is used to connect to an Arduino through the serial port'''
import maya.api.OpenMaya as om
import time
import threading
import serial

from maya import cmds


class ArduinoConnection:
    ''' This class is used to connect to an Arduino through the serial port
	    @param arduinoPort: port to read. In windows format is "COM1", "COM9", etc.
	    @param baudRate: baud Rate in which the Arduino is emitting the signal.
    '''

    def __init__(self, arduinoPort, baudRate):
        self.arduinoPort = arduinoPort
        self.baudRate = baudRate


    def start(self):
        '''This method initializes the connection in a separate thread'''

        serialComm = self.initSerialConnection()

        if serialComm:
            communicationThread = threading.Thread(target = self.communicateWithArduino, args=(serialComm,))
            communicationThread.daemon = True
            communicationThread.start()


    def initSerialConnection(self):
        '''This method starts the serial comunication'''

        try:
            serialComm = serial.Serial(self.arduinoPort, self.baudRate, timeout=1)
            time.sleep(2)

            return serialComm

        except serial.SerialException as error:
            cmds.warning(f"Can't initialize connection: {error}")
            return None


    def communicateWithArduino(self, serialComm):
        '''Loop for Read/Write that will be executed in a thread to not block Maya's UI'''

        if serialComm:
            try:
                while True:
                    if serialComm.in_waiting > 0:
                        arduinoMessage = serialComm.readline().decode('utf-8').strip()
                        #cmds.setAttr("pCube1.translateX", int(arduinoMessage))
                        cmds.setAttr("ambientLight1.intensity", regla_de_tres(int(arduinoMessage)))
                        #cambiar_posicion_x(int(arduinoMessage))

                    time.sleep(0.05)

            except serial.SerialException as error:
                cmds.warning(f"Error in Arduino comunication: {error}")
            finally:
                serialComm.close()




def cambiar_posicion_x(nueva_posicion_x):
    objeto = 'pCube1'
    
    # Verifica si el objeto existe en la escena
    if cmds.objExists(objeto):

        # Obtén el MObject del objeto
        selection_list = om.MSelectionList()
        selection_list.add(objeto)
        dag_path = selection_list.getDagPath(0)
        transform_node = dag_path.transform()
        
        # Accede a la función de transformación
        fn_transform = om.MFnTransform(transform_node)
        
        # Cambia la posición en el eje X
        fn_transform.setTranslation(om.MVector(nueva_posicion_x, 0, 0), om.MSpace.kTransform)


def regla_de_tres(valor, minimo=0, maximo=200):
    """
    Realiza una regla de tres simple con los valores dados.

    :param valor: El valor que se desea escalar.
    :param minimo: El valor mínimo (por defecto 0).
    :param maximo: El valor máximo (por defecto 200).
    :return: El valor escalado entre 0 y 1.
    """
    if valor <= minimo:
        return 0
    elif valor >= maximo:
        return 1
    else:
        return (valor - minimo) / (maximo - minimo)