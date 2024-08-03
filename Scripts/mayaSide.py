'''This class is used to connect to an Arduino through the serial port'''

import time
import threading
import serial

from maya import cmds


class ArduinoConnection:
    ''' This class is used to connect to an Arduino through the serial port
	    @param arduinoPort: port to read. In windows format is "COM1", "COM9", etc.
	    @param baudRate: baud Rate in which the Arduino is emitting the signal.
    '''

    def __init__(self, arduinoPort, mayaAttribute, callbackFunction):
        self.arduinoPort = arduinoPort
        self.mayaAttribute = mayaAttribute
        self.callbackFunction = callbackFunction
        self.communicationThread = None
        self.stopEvent = threading.Event()

        self.baudRate = 115200


    def start(self):
        '''This method initializes the connection in a separate thread'''

        serialComm = self.initSerialConnection()

        if serialComm:
            self.communicationThread = threading.Thread(target = self.communicateWithArduino, args=(serialComm,))
            self.communicationThread.daemon = True
            self.communicationThread.start()


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

        if not serialComm:
            return

        try:
            while not self.stopEvent.is_set():
                if serialComm.in_waiting > 0:
                    arduinoMessage = serialComm.readline().decode('utf-8').strip()
                    self.callbackFunction(self.mayaAttribute, int(arduinoMessage))

                time.sleep(0.05)

        except serial.SerialException as error:
            cmds.warning(f"Error in Arduino comunication: {error}")

        finally:
            serialComm.close()


    def stop(self):
        '''This method stops the connection and the thread'''

        self.stopEvent.set()

        if self.communicationThread:
            self.communicationThread.join()
        cmds.warning("Serial communication stopped")
