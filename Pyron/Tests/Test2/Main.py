import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from Object import ObjLoader

class Item (object):
    def __init__ (self, _Model):
        self.Angle = 0
        self.Vertices = []
        self.Faces = []
        self.Coordinates = [0, 0, -65]
        self.Model = ObjLoader ()
        self.Model.Load (_Model)
        self.Position = [0, 0, -50]

    def Render (self):
        glBegin (GL_TRIANGLES)

        glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearColor (0.902, 0.902, 1, 0.0)
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity ()
        gluLookAt (0, 0, 0, math.sin (math.radians (self.Angle)), 0, math.cos (math.radians (self.Angle)) * -1, 0, 1, 0)
        glTranslatef (self.Coordinates[0], self.Coordinates[1], self.Coordinates[2])

        glEnd ()

    def MoveForward (self):
        self.Coordinates[2] += 10 * math.cos (math.radians (self.Angle))
        self.Coordinates[0] -= 10 * math.sin (math.radians (self.Angle))

    def MoveBack (self):
        self.Coordinates[2] -= 10 * math.cos (math.radians (self.Angle))
        self.Coordinates[0] += 10 * math.sin (math.radians (self.Angle))

    def MoveLeft (self, _Amount):
        self.Coordinates[0] += _Amount * math.cos (math.radians (self.Angle))
        self.Coordinates[2] += _Amount * math.sin (math.radians (self.Angle))

    def MoveRight (self, _Amount):
        self.Coordinates[0] -= _Amount * math.cos (math.radians (self.Angle))
        self.Coordinates[2] -= _Amount * math.sin (math.radians (self.Angle))

    def Rotate (self, _Amount):
        self.Angle += _Amount

    def FullRotate (self):
        for I in range (0, 36):
            self.Angle += 10
            self.MoveLeft (10)
            self.Render ()
            self.Model.Render ()
            pygame.display.flip ()

def Run ():
    pygame.init ()
    pygame.display.set_mode ((640, 480), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption ('Pyron Model Viewer')
    Clock = pygame.time.Clock ()

    glDisable (GL_TEXTURE_2D)
    glEnable (GL_DEPTH_TEST)
    glEnable (GL_BLEND)
    glEnable (GL_CULL_FACE)
    glMatrixMode (GL_PROJECTION)
    gluPerspective (45.0, float (800) / 600, .1, 1000.)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity ()

    Object = Item ('Model.obj')

    Done = False
    while not Done:
        for Event in pygame.event.get ():
            if Event.type == pygame.QUIT:
                Done = True

            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_LEFT or Event.key == pygame.K_a:
                    Object.MoveLeft (10)

                elif Event.key == pygame.K_RIGHT or Event.key == pygame.K_d:
                    Object.MoveRight (10)

                elif Event.key == pygame.K_UP or Event.key == pygame.K_w:
                    Object.MoveForward ()

                elif Event.key == pygame.K_DOWN or Event.key == pygame.K_s:
                    Object.MoveBack ()

                elif Event.key == pygame.K_1:
                    Object.Rotate (10)
                    Object.MoveLeft (10)

                elif Event.key == pygame.K_2:
                    Object.Rotate (-10)
                    Object.MoveRight (10)

                elif Event.key == pygame.K_3:
                    Object.FullRotate ()

        Object.Render ()
        Object.Model.Render ()
        pygame.display.flip ()
        Clock.tick (30)

    pygame.quit ()

#Run ()
