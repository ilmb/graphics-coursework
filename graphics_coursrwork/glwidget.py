import copy
import numpy as np
import ctypes
import random
from math import cos, sin, radians

from OpenGL.GL import *
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *

from figures import *


class glWidget(QGLWidget):

    def __init__(self, parent):

        QGLWidget.__init__(self, parent)
        self.rotationX = 0
        self.rotationY = 0
        self.rotationZ = 0

        self.is_pressed = False
        self.firstMouse = True
        self.isViewingCamera = True

        self.yaw = -100.0
        self.pitch = -10.0
        self.scale = 5.0

        fx = cos(radians(self.yaw)) * cos(radians(self.pitch))
        fy = sin(radians(self.pitch))
        fz = sin(radians(self.yaw)) * cos(radians(self.pitch))
        self.cameraFront = QVector3D(fx, fy, fz)
        self.cameraPos = QVector3D(5.0, 4.0, 16.0)
        self.cameraUp = QVector3D(0.0, 1.0, 0.0)

        self.LightIntensity = QVector3D(1.0, 1.0, 1.0)
        self.LightPosition = QVector4D(9.0, 5.0, 13.0, 0.0)

        self.polygon_mode = GL_FILL

        self.projection_matrix = QMatrix4x4()
        self.projection_matrix.perspective(45.0, self.width() / self.height(), 0.1, 100.0)
        self.current_view = QMatrix4x4()
        self.current_model = QMatrix4x4()

        self.changeColor((0.2, 0.2, 0.2, 1))
        self.changeStepCount(5)

    def resizeGL(self, w, h):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # очистка буферов

        glEnable(GL_DEPTH_TEST)

        self.shaderProgram.setUniformValue('light.position', self.LightPosition)
        self.shaderProgram.setUniformValue('light.direction', self.cameraFront)
        self.shaderProgram.setUniformValue('ViewPosition', self.cameraPos)
        self.shaderProgram.setUniformValue('LightIntensity', self.LightIntensity)

        self.updateMatrices()

        glPointSize(4)
        glLineWidth(2)
        glPolygonMode(GL_FRONT_AND_BACK, self.polygon_mode)
        self.drawLight()

        self.drawScene()

        glDisable(GL_DEPTH_TEST)

    def drawScene(self):
        step_width = 4
        step_height = 0.3
        step_length = 1

        self.drawFigure(Cube(3, 0.3, 8, self.currentTexture, self.current_color))
        for i in range(self.step_count):
            self.drawFigure(Cube(step_length, step_height, step_width, self.currentTexture, self.current_color),
                            offset=(2 * step_length * (i + 2),
                                    2 * step_height * (i + 1),
                                    step_width))
            self.drawFigure(Cube(step_length, step_height, step_width, self.currentTexture, self.current_color),
                            offset=(2 * step_length * (i + 2),
                                    -2 * step_height * (i + 1),
                                    -step_width))
        self.drawFigure(Cube(3 * step_length * self.step_count, 0.3, 3 * step_length * self.step_count,
                             -1, (0.25, 0.25, 0.25, 1)),
                        offset=(step_length * self.step_count / 2, -2 * step_height * (self.step_count + 1), 0))

    def initializeGL(self):
        glClearColor(0.133, 0.5, 0.7, 1.0)

        # VBO
        self._vertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertexBuffer)
        # IBO
        self._indexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._indexBuffer)

        self.shaderProgram = self.initShaderProgram()

        self.attribVertexColor = self.shaderProgram.attributeLocation("color_vertex")
        self.attribVertexPosition = self.shaderProgram.attributeLocation("position_vertex")
        self.attribVertexNormal = self.shaderProgram.attributeLocation("normal_vertex")
        self.attribVertexTexCoord = self.shaderProgram.attributeLocation("texcoord_vertex")

        glEnable(GL_TEXTURE_2D)
        self.woodTexture = self.bindTexture(QPixmap("textures/дерево.jpg"))
        self.brickTexture = self.bindTexture(QPixmap("textures/кирпич.jpg"))
        self.stoneTexture = self.bindTexture(QPixmap("textures/камень.jpg"))
        self.roadTexture = self.bindTexture(QPixmap("textures/асфальт.jpg"))

        self.currentTexture = self.woodTexture

    def changeStepCount(self, value):
        self.step_count = value

    def changeColor(self, color=None):
        if color:
            self.current_color = color
        else:
            self.current_color = (random.random(), random.random(), random.random(), 1)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        self.is_pressed = True

    def mouseReleaseEvent(self, event):
        self.is_pressed = False

    def mouseMoveEvent(self, event):
        if self.isViewingCamera:
            self.viewingCameraMode(event.x(), event.y())
        else:
            self.spinMode(event)
        self.updateGL()

    def wheelEvent(self, event):
        self.LightPosition.setY(self.LightPosition.y() + event.angleDelta().y() / 120)
        self.updateGL()

    def viewingCameraMode(self, x, y):
        sensitivity = 0.15

        dx = (x - self.lastPos.x()) * sensitivity
        dy = (self.lastPos.y() - y) * sensitivity

        self.lastPos = QPointF(x, y)

        self.yaw += dx
        self.pitch += dy

        if (self.pitch > 89.0):
            self.pitch = 89.0
        if (self.pitch < -89.0):
            self.pitch = -89.0

        self.cameraFront.setX(cos(radians(self.yaw)) * cos(radians(self.pitch)))
        self.cameraFront.setY(sin(radians(self.pitch)))
        self.cameraFront.setZ(sin(radians(self.yaw)) * cos(radians(self.pitch)))
        self.cameraFront.normalize()

    def spinMode(self, event):
        speed = 180
        if self.is_pressed:
            dx = (event.x() - self.lastPos.x()) / self.width()
            dy = (event.y() - self.lastPos.y()) / self.height()
            if (event.buttons() == Qt.LeftButton):
                self.rotationX += speed * dy
                self.rotationY += speed * dx
            elif (event.buttons() == Qt.RightButton):
                self.rotationX += speed * dy
                self.rotationZ += speed * dx
        self.lastPos = event.pos()

    def keyboardCallBack(self, event):
        cameraSpeed = 0.5
        if event.key() == ord('W') or event.key() == 1062:
            self.cameraPos += cameraSpeed * self.cameraFront
        if event.key() == ord('A') or event.key() == 1060:
            cross = QVector3D.crossProduct(self.cameraFront, self.cameraUp)
            cross.normalize()
            self.cameraPos -= cross * cameraSpeed
        if event.key() == ord('S') or event.key() == 1067:
            self.cameraPos -= cameraSpeed * self.cameraFront
        if event.key() == ord('D') or event.key() == 1042:
            cross = QVector3D.crossProduct(self.cameraFront, self.cameraUp)
            cross.normalize()
            self.cameraPos += cross * cameraSpeed
        if event.key() == 16777235:  # ^
            self.LightPosition.setZ(self.LightPosition.z() - 1)
        if event.key() == 16777234:  # <-
            self.LightPosition.setX(self.LightPosition.x() - 1)
        if event.key() == 16777237:  # v
            self.LightPosition.setZ(self.LightPosition.z() + 1)
        if event.key() == 16777236:  # ->
            self.LightPosition.setX(self.LightPosition.x() + 1)

    def initShaderProgram(self):
        shaderProgram = QOpenGLShaderProgram()
        shaderProgram.addShaderFromSourceFile(QOpenGLShader.Vertex, "shaders/shader.vert")
        shaderProgram.addShaderFromSourceFile(QOpenGLShader.Fragment, "shaders/shader.frag")
        shaderProgram.link()
        shaderProgram.bind()

        # light
        shaderProgram.setUniformValue('light.ambient', QVector3D(0.2, 0.2, 0.2))
        shaderProgram.setUniformValue('light.diffuse', QVector3D(0.5, 0.5, 0.5))
        shaderProgram.setUniformValue('light.specular', QVector3D(0.1, 0.1, 0.1))
        shaderProgram.setUniformValue('light.constant', 1.0)
        shaderProgram.setUniformValue('light.linear', 0.014)
        shaderProgram.setUniformValue('light.quadratic', 0.0007)
        shaderProgram.setUniformValue('light.cutOff', cos(radians(12.5)))
        shaderProgram.setUniformValue('light.outerCutOff', cos(radians(17.5)))
        # material
        shaderProgram.setUniformValue('material.specular', QVector3D(0.5, 0.5, 0.5))
        shaderProgram.setUniformValue('material.shininess', 10.0)

        return shaderProgram

    def updateMatrices(self):

        view, model = QMatrix4x4(), QMatrix4x4()

        view.lookAt(self.cameraPos, self.cameraPos + self.cameraFront, self.cameraUp)

        model.rotate(self.rotationX, QVector3D(1.0, 0.0, 0.0))
        model.rotate(self.rotationY, QVector3D(0.0, 1.0, 0.0))
        model.rotate(self.rotationZ, QVector3D(0.0, 0.0, 1.0))

        self.current_view = view
        self.current_model = model

        self.setUniformMatrix(model, view)

    def setUniformMatrix(self, model, view):
        modelview = view * model
        self.shaderProgram.setUniformValue("MVP", self.projection_matrix * modelview)
        self.shaderProgram.setUniformValue("NormalMatrix", model.normalMatrix())
        self.shaderProgram.setUniformValue("ModelMatrix", model)

    def drawFigure(self, figure, offset=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        self.setDefaultAttribPointers()
        self.enableAttributeArrays()
        model = copy.deepcopy(self.current_model)
        model.translate(*offset)
        model.rotate(rotate[0], QVector3D(1.0, 0.0, 0.0))
        model.rotate(rotate[1], QVector3D(0.0, 1.0, 0.0))
        model.rotate(rotate[2], QVector3D(0.0, 0.0, 1.0))
        model.scale(*scale)
        self.setUniformMatrix(model, self.current_view)

        glBindTexture(GL_TEXTURE_2D, figure.texture)
        glBufferData(GL_ARRAY_BUFFER, np.array(figure.generate(), dtype='float32'), GL_STATIC_DRAW)
        glDrawArrays(figure.type, 0, figure.count)
        self.disableAttributeArrays()

        self.setUniformMatrix(self.current_model, self.current_view)

    def drawLight(self):
        self.drawFigure(Cube(0.1, 0.1, 0.1, -1, (1, 1, 0, 1)),
                        offset=(self.LightPosition.x(), self.LightPosition.y(), self.LightPosition.z()))

    def enableAttributeArrays(self):
        self.shaderProgram.enableAttributeArray(self.attribVertexPosition)
        self.shaderProgram.enableAttributeArray(self.attribVertexTexCoord)
        self.shaderProgram.enableAttributeArray(self.attribVertexNormal)
        self.shaderProgram.enableAttributeArray(self.attribVertexColor)

    def disableAttributeArrays(self):
        self.shaderProgram.disableAttributeArray(self.attribVertexPosition)
        self.shaderProgram.disableAttributeArray(self.attribVertexTexCoord)
        self.shaderProgram.disableAttributeArray(self.attribVertexNormal)
        self.shaderProgram.disableAttributeArray(self.attribVertexColor)

    def setDefaultAttribPointers(self):
        stride = 12 * ctypes.sizeof(ctypes.c_float)
        glVertexAttribPointer(self.attribVertexPosition, 3, GL_FLOAT, GL_FALSE, stride, None)
        glVertexAttribPointer(self.attribVertexNormal, 3, GL_FLOAT, GL_FALSE, stride,
                              ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glVertexAttribPointer(self.attribVertexTexCoord, 2, GL_FLOAT, GL_FALSE, stride,
                              ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
        glVertexAttribPointer(self.attribVertexColor, 4, GL_FLOAT, GL_FALSE, stride,
                              ctypes.c_void_p(8 * ctypes.sizeof(ctypes.c_float)))
