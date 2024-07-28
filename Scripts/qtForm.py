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

        self.setWindowTitle("Arduino Connection")
        self.setGeometry(100, 100, 300, 300)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.createWidgets()
        self.createLayout()
        self.createConnections()


    def createWidgets(self):
        '''Widgets setup'''

        self.label = QtWidgets.QLabel('COM')
        self.label.setFixedWidth(50)

        self.textCom = QtWidgets.QLineEdit()
        self.textCom.setValidator(QtGui.QIntValidator())
        self.textCom.setFixedWidth(50)
        self.textCom.setAlignment(QtCore.Qt.AlignRight)

        self.label_atributos = QtWidgets.QLabel('Attributes')
        self.label_valores = QtWidgets.QLabel('Pinout')

        self.attributeList = QtWidgets.QListWidget()
        self.lista_valores = QtWidgets.QListWidget()
        self.lista_valores.addItems(['A2', 'A3', 'A4'])

        self.btn_start = QtWidgets.QPushButton('Start')
        self.btn_stop = QtWidgets.QPushButton('Stop')


    def createLayout(self):
        '''Layout setup'''

        # Layout para el label y el campo de texto
        form_layout = QtWidgets.QHBoxLayout()
        form_layout.addWidget(self.label)
        form_layout.addWidget(self.textCom)
        form_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes

        # Layout derecho
        right_layout = QtWidgets.QHBoxLayout()
        right_layout.addStretch()  # Agrega espacio flexible a la izquierda
        right_layout.addLayout(form_layout)
        
        layout_valores = QtWidgets.QVBoxLayout()
        layout_valores.addWidget(self.label_valores)
        layout_valores.addWidget(self.lista_valores)

        layout_atributos = QtWidgets.QVBoxLayout()
        layout_atributos.addWidget(self.label_atributos)
        layout_atributos.addWidget(self.attributeList)

        # Layout de listas
        listas_layout = QtWidgets.QHBoxLayout()
        listas_layout.addLayout(layout_valores)
        listas_layout.addLayout(layout_atributos)

        # Layout para los botones
        botones_layout = QtWidgets.QHBoxLayout()
        botones_layout.addStretch()  # Agrega espacio flexible a la izquierda
        botones_layout.addWidget(self.btn_start)
        botones_layout.addWidget(self.btn_stop)

        # Layout principal
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(right_layout)  # Agrega el layout a la derecha
        layout.addLayout(listas_layout)  # Agrega el layout de listas
        layout.addLayout(botones_layout)  # Agrega el layout de botones

        # Establecer el layout al widget principal
        self.setLayout(layout)


    def createConnections(self):
        '''Connections setup'''

        self.script_job = cmds.scriptJob(event=["SelectionChanged", self.actualizar_atributos], protected=True)

        self.actualizar_atributos()


    def closeEvent(self, event):
        # Eliminar el scriptJob cuando se cierra el formulario
        if hasattr(self, 'script_job') and cmds.scriptJob(exists=self.script_job):
            cmds.scriptJob(kill=self.script_job, force=True)
        event.accept()


    def actualizar_atributos(self):
        self.attributeList.clear()
        seleccion = cmds.ls(selection=True)
        if not seleccion:
            return
        
        # Obtener el primer objeto seleccionado
        objeto = seleccion[0]
        
        # Atributos de transformación
        atributos_transformacion = ['translateX', 'translateY', 'translateZ',
                                    'rotateX', 'rotateY', 'rotateZ',
                                    'scaleX', 'scaleY', 'scaleZ']
        
        for atributo in atributos_transformacion:
            if cmds.attributeQuery(atributo, node=objeto, exists=True):
                self.attributeList.addItem(f"{atributo}")


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
