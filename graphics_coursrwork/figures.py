from OpenGL.raw.GL.VERSION.GL_1_1 import GL_TRIANGLES


class Cube:
    def __init__(self, width, height, length, texture, color=(0.2, 0.2, 0.2, 1)):
        self.x = width
        self.y = height
        self.z = length
        self.count = 36
        self.type = GL_TRIANGLES
        self.texture = texture
        self.color = color

    def generate(self):
        return [
            -self.x, -self.y, -self.z, 0.0, 0.0, -1.0, 0.0, 0.0, *self.color,
            self.x, -self.y, -self.z, 0.0, 0.0, -1.0, 1.0, 0.0, *self.color,
            self.x, self.y, -self.z, 0.0, 0.0, -1.0, 1.0, 1.0, *self.color,
            self.x, self.y, -self.z, 0.0, 0.0, -1.0, 1.0, 1.0, *self.color,
            -self.x, self.y, -self.z, 0.0, 0.0, -1.0, 0.0, 1.0, *self.color,
            -self.x, -self.y, -self.z, 0.0, 0.0, -1.0, 0.0, 0.0, *self.color,

            -self.x, -self.y, self.z, 0.0, 0.0, 1.0, 0.0, 0.0, *self.color,
            self.x, -self.y, self.z, 0.0, 0.0, 1.0, 1.0, 0.0, *self.color,
            self.x, self.y, self.z, 0.0, 0.0, 1.0, 1.0, 1.0, *self.color,
            self.x, self.y, self.z, 0.0, 0.0, 1.0, 1.0, 1.0, *self.color,
            -self.x, self.y, self.z, 0.0, 0.0, 1.0, 0.0, 1.0, *self.color,
            -self.x, -self.y, self.z, 0.0, 0.0, 1.0, 0.0, 0.0, *self.color,

            -self.x, self.y, self.z, -1.0, 0.0, 0.0, 1.0, 0.0, *self.color,
            -self.x, self.y, -self.z, -1.0, 0.0, 0.0, 1.0, 1.0, *self.color,
            -self.x, -self.y, -self.z, -1.0, 0.0, 0.0, 0.0, 1.0, *self.color,
            -self.x, -self.y, -self.z, -1.0, 0.0, 0.0, 0.0, 1.0, *self.color,
            -self.x, -self.y, self.z, -1.0, 0.0, 0.0, 0.0, 0.0, *self.color,
            -self.x, self.y, self.z, -1.0, 0.0, 0.0, 1.0, 0.0, *self.color,

            self.x, self.y, self.z, 1.0, 0.0, 0.0, 1.0, 0.0, *self.color,
            self.x, self.y, -self.z, 1.0, 0.0, 0.0, 1.0, 1.0, *self.color,
            self.x, -self.y, -self.z, 1.0, 0.0, 0.0, 0.0, 1.0, *self.color,
            self.x, -self.y, -self.z, 1.0, 0.0, 0.0, 0.0, 1.0, *self.color,
            self.x, -self.y, self.z, 1.0, 0.0, 0.0, 0.0, 0.0, *self.color,
            self.x, self.y, self.z, 1.0, 0.0, 0.0, 1.0, 0.0, *self.color,

            -self.x, -self.y, -self.z, 0.0, -1.0, 0.0, 0.0, 1.0, *self.color,
            self.x, -self.y, -self.z, 0.0, -1.0, 0.0, 1.0, 1.0, *self.color,
            self.x, -self.y, self.z, 0.0, -1.0, 0.0, 1.0, 0.0, *self.color,
            self.x, -self.y, self.z, 0.0, -1.0, 0.0, 1.0, 0.0, *self.color,
            -self.x, -self.y, self.z, 0.0, -1.0, 0.0, 0.0, 0.0, *self.color,
            -self.x, -self.y, -self.z, 0.0, -1.0, 0.0, 0.0, 1.0, *self.color,

            -self.x, self.y, -self.z, 0.0, 1.0, 0.0, 0.0, 1.0, *self.color,
            self.x, self.y, -self.z, 0.0, 1.0, 0.0, 1.0, 1.0, *self.color,
            self.x, self.y, self.z, 0.0, 1.0, 0.0, 1.0, 0.0, *self.color,
            self.x, self.y, self.z, 0.0, 1.0, 0.0, 1.0, 0.0, *self.color,
            -self.x, self.y, self.z, 0.0, 1.0, 0.0, 0.0, 0.0, *self.color,
            -self.x, self.y, -self.z, 0.0, 1.0, 0.0, 0.0, 1.0, *self.color]
