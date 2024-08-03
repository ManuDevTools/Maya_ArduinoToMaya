''' User interface for connect some attribute with the selected Arduino pinout
    IMPORTANT: For older versions of Maya 2025, you may want to change the version
    from PySide to Pyside2
'''

from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from shiboken6 import wrapInstance

from maya import cmds
import maya.OpenMayaUI as omui
from MayaToArduino.Scripts.mayaSide import ArduinoConnection


def mayaMainWindow():
    """
    Return the Maya main window widget as a Python object
    """
    mainWindowPtr = omui.MQtUtil.mainWindow()

    return wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)


class QtForm(QtWidgets.QDialog):
    '''User interface for connect some attribute with the selected Arduino pinout'''

    def __init__(self, parent = mayaMainWindow()):
        super(QtForm, self).__init__(parent)

        self.connection = None

        self.setWindowTitle("Arduino Connection")
        self.setGeometry(100, 100, 300, 300)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()

        self.scriptJob = cmds.scriptJob(event = ["SelectionChanged", self.updateAttributes], protected = True)
        self.updateAttributes()


    def createWidgets(self):
        '''Widgets setup'''

        self.labelCom = QtWidgets.QLabel('COM')
        self.labelCom.setFixedWidth(50)

        self.textCom = QtWidgets.QLineEdit()
        self.textCom.setValidator(QtGui.QIntValidator())
        self.textCom.setFixedWidth(50)
        self.textCom.setAlignment(QtCore.Qt.AlignRight)

        self.labelAttributes = QtWidgets.QLabel('Attributes')
        self.labelPinout = QtWidgets.QLabel('Pinout')

        self.attributeList = QtWidgets.QListWidget()
        self.listPinout = QtWidgets.QListWidget()
        self.listPinout.addItems(['Analog2'])

        self.btnStart = QtWidgets.QPushButton('Start')
        self.btnStop = QtWidgets.QPushButton('Stop')


    def createLayout(self):
        '''Layout setup'''

        layoutCom = QtWidgets.QHBoxLayout()
        layoutCom.addWidget(self.labelCom)
        layoutCom.addWidget(self.textCom)
        layoutCom.setContentsMargins(0, 0, 0, 0)

        layoutRight = QtWidgets.QHBoxLayout()
        layoutRight.addStretch()
        layoutRight.addLayout(layoutCom)

        layoutPinout = QtWidgets.QVBoxLayout()
        layoutPinout.addWidget(self.labelPinout)
        layoutPinout.addWidget(self.listPinout)

        layoutAttributes = QtWidgets.QVBoxLayout()
        layoutAttributes.addWidget(self.labelAttributes)
        layoutAttributes.addWidget(self.attributeList)

        layoutLists = QtWidgets.QHBoxLayout()
        layoutLists.addLayout(layoutPinout)
        layoutLists.addLayout(layoutAttributes)

        layoutButtons = QtWidgets.QHBoxLayout()
        layoutButtons.addStretch()
        layoutButtons.addWidget(self.btnStart)
        layoutButtons.addWidget(self.btnStop)

        layoutMain = QtWidgets.QVBoxLayout()
        layoutMain.addLayout(layoutRight)
        layoutMain.addLayout(layoutLists)
        layoutMain.addLayout(layoutButtons)

        self.setLayout(layoutMain)


    def createConnections(self):
        '''Connections setup'''

        self.btnStart.clicked.connect(self.startClicked)
        self.btnStop.clicked.connect(self.stopClicked)


    def closeEvent(self, event):
        '''Stop the ScriptJob when the form is closed'''

        if hasattr(self, 'scriptJob') and cmds.scriptJob(exists = self.scriptJob):
            cmds.scriptJob(kill = self.scriptJob, force = True)

        event.accept()


    def updateAttributes(self):
        '''Updates the values in the attributes list, depending on what you have selected'''

        self.attributeList.clear()
        selection = cmds.ls(selection = True)

        if not selection:
            return

        selectedObject = selection[0]

        attributesToList = ['translateX', 'translateY', 'translateZ',
                            'rotateX', 'rotateY', 'rotateZ',
                            'scaleX', 'scaleY', 'scaleZ', 'intensity']

        for attribute in attributesToList:
            try:
                cmds.getAttr(f"{selectedObject}.{attribute}")
                self.attributeList.addItem(f"{attribute}")

            except ValueError:
                continue


    def startClicked(self):
        '''What will happend when we press the start button'''

        selection = cmds.ls(selection = True)

        if not selection:
            return

        selectedObject = selection[0]

        attributeSelected = self.attributeList.currentItem().text()

        self.connection = ArduinoConnection(f"COM{self.textCom.text()}", f"{selectedObject}.{attributeSelected}", funtionToExectute)
        self.connection.start()


    def stopClicked(self):
        '''What will happend when we press the stop button'''

        if self.connection:
            self.connection.stop()


    @classmethod
    def showUI(cls):
        '''Shows the UI'''

        try:
            qtTemplateDialog.close() # pylint: disable=E0601
            qtTemplateDialog.deleteLater()

        except NameError:
            pass

        qtTemplateDialog = QtForm()
        qtTemplateDialog.show()

QtForm.showUI()


def funtionToExectute(connectionObject, portValue):
    '''Write here all the thing you want to execute on every loop'''

    cmds.setAttr(connectionObject, portValue)
