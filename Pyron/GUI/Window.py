import os
import Eve
from direct.task import Task
from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase

from Core import Renderer

class RenderWindow (ShowBase):
    def __init__ (self, Title = 'Untitled', Version = '0.0.1', Width = 800, Height = 600):
        ShowBase.__init__ (self)

        self.Title = Title
        self.Version = Version
        self.Width = Width
        self.Height = Height

        self.Scene = self.loader

        self.ModelMeshes = []
        self.IsShowFPS = False

    def SpinCamera (self):
        self.taskMgr.add (self.SpinCameraTask, 'SpinCameraTask')

    def ShowFPS (self, _Setting = None):
        if _Setting is not None:
            if self.IsShowFPS == False:
                self.IsShowFPS = True
                self.set_frame_rate_meter (True)

            else:
                self.IsShowFPS = False
                self.set_frame_rate_meter (False)

        else:
            self.set_frame_rate_meter (_Setting)

    def SpinCameraTask (self, _Task):
        Degrees = _Task.time * 6.0
        Radians = Degrees * (pi / 180.0)

        self.camera.setPos (20 * sin (Radians), -20.0 * cos (Radians), 3)
        self.camera.setHpr (Degrees, 0, 0)

        return Task.cont

    def RotateCamera (self, _Degrees):
        self.Scene.setH (self.Scene.getH () + _Degrees)

    def Draw (self, _Object):
        self.Scene = self.loader.loadModel (_Object[0])
        self.ModelMeshes.append (_Object[1])

        os.remove ('Temp/Model.egg')

    def Run (self):
        self.Scene.reparentTo (self.render)
        self.Scene.setScale (0.25, 0.25, 0.25)
        self.Scene.setPos (-8, 42, 0)
        self.run ()
