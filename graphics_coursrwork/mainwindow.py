from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QCheckBox

from ui.form import Ui_MainWindow
from glwidget import glWidget, GL_FILL, GL_LINE, GL_POINT


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.glwidget = glWidget(self)
        self.glwidget.setMinimumSize(700, 100)
        self.widget_layout.addWidget(self.glwidget)

        def check1F():
            self.glwidget.isViewingCamera = self.check1.isChecked()
        self.check1.stateChanged.connect(check1F)
        self.sliderLightIntensive.valueChanged.connect(self.changeLightIntensive)
        self.comboBoxStyle.currentIndexChanged.connect(self.changeDrawStyle)
        self.comboBoxTexture.currentTextChanged.connect(self.changeTexture)

        self.sliderLightPosX.valueChanged.connect(self.changeLightPosX)
        self.sliderLightPosY.valueChanged.connect(self.changeLightPosY)
        self.sliderLightPosZ.valueChanged.connect(self.changeLightPosZ)

        self.sliderViewPosX.valueChanged.connect(self.changeViewPosX)
        self.sliderViewPosY.valueChanged.connect(self.changeViewPosY)
        self.sliderViewPosZ.valueChanged.connect(self.changeViewPosZ)

        self.pushButton.clicked.connect(self.changeColor)
        self.pushButton_2.clicked.connect(self.changeColor2)

        self.spinBox.valueChanged.connect(self.changeStepCount)

        self.glwidget.setFocus()

    def changeStepCount(self, value):
        self.glwidget.changeStepCount(value)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeColor2(self):
        self.glwidget.changeColor((0.2, 0.2, 0.2, 1))
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeColor(self):
        self.glwidget.changeColor()
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def keyPressEvent(self, event):
        self.glwidget.keyboardCallBack(event)
        if event.key() % 32 == 0:
            self.check1.setChecked(not self.check1.isChecked())
        self.glwidget.updateGL()

    def changeLightIntensive(self, val):
        self.glwidget.LightIntensity.setX(val / 100)
        self.glwidget.LightIntensity.setY(val / 100)
        self.glwidget.LightIntensity.setZ(val / 100)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeDrawStyle(self, value):
        if value is 1:
            type_draw = GL_LINE
        elif value is 2:
            type_draw = GL_POINT
        else:
            type_draw = GL_FILL

        self.glwidget.polygon_mode = type_draw
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeTexture(self, value):
        if value == 'дерево':
            self.glwidget.currentTexture = self.glwidget.woodTexture
        if value == 'камень':
            self.glwidget.currentTexture = self.glwidget.stoneTexture
        if value == 'асфальт':
            self.glwidget.currentTexture = self.glwidget.roadTexture
        if value == 'кирпич':
            self.glwidget.currentTexture = self.glwidget.brickTexture
        if value == 'без текстуры':
            self.glwidget.currentTexture = -1

        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeLightPosX(self, value):
        self.glwidget.LightPosition.setX(value / 5 - 5)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeLightPosY(self, value):
        self.glwidget.LightPosition.setY(value / 5 - 5)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeLightPosZ(self, value):
        self.glwidget.LightPosition.setZ(value / 5 - 5)
        self.glwidget.setFocus()
        self.glwidget.updateGL()


    def changeViewPosX(self, value):
        self.glwidget.cameraPos.setX(value / 2.5 - 20)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeViewPosY(self, value):
        self.glwidget.cameraPos.setY(value / 2.5 - 20)
        self.glwidget.setFocus()
        self.glwidget.updateGL()

    def changeViewPosZ(self, value):
        self.glwidget.cameraPos.setZ(value / 2.5 - 20)
        self.glwidget.setFocus()
        self.glwidget.updateGL()







if __name__ == '__main__':
    pass
