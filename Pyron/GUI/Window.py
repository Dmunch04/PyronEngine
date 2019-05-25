import Eve
import matplotlib.pyplot as plt
from numpy import array, min, pi, sqrt, ones
from pyrender import PerspectiveCamera, Scene, Node, Viewer, OffscreenRenderer, SpotLight

from Core import Renderer

class Window:
    def __init__ (self, Title = f'Pyron Engine [0.0.1] - Untitled*', Width = 800, Height = 600):
        self.Title = Title
        self.Version = '0.0.1'
        self.Width = Width
        self.Height = Height

        self.Camera = PerspectiveCamera (yfov = (pi / 3.0))
        self.Scene = Scene (ambient_light = array ([0.02, 0.02, 0.02, 1.0]))

    def Draw (self, _Object):
        ObjectNode = Node (mesh = _Object[1], translation = array ([0.1, 0.15, -min (_Object[0].vertices[:, 2])]))
        self.Scene.add_node (ObjectNode)

    def LoadScene (self, _Path):
        Data = Eve.Load (_Path)

        # General
        self.Title = Data['Title']
        self.Version = Data['Version']

        # Camera
        ZNear = Data['Camera'][0]
        ZFar = Data['Camera'][1]
        Name = Data['Camera'][2]
        YFov = Data['Camera'][3]
        AspectRatio = Data['Camera'][4]

        if ZNear != 'None':
            self.Camera.znear = float (ZNear)

        if ZFar != 'None':
            self.Camera.zfar = float (ZFar)

        if Name != 'None':
            self.Camera.name = str (Name)

        if YFov != 'None':
            self.Camera.yfov = float (YFov)

        if AspectRatio != 'None':
            self.Camera.aspectRatio = float (AspectRatio)

        # Models
        for ModelPath in Data['Models']:
            self.Draw (Renderer.Render (ModelPath))

    def Run (self):
        self.Viewer = Viewer (self.Scene, use_raymond_lighting = True, shadows = True, width = self.Width, height = self.Height, title = 'a')

class TestWindow:
    def __init__ (self, Title = f'Pyron Engine [0.0.1] - Untitled*', Width = 800, Height = 600):
        self.Title = Title
        self.Version = '0.0.1'
        self.Width = Width
        self.Height = Height

        self.Scene = Scene ()
        self.Camera = PerspectiveCamera (yfov = pi / 3.0, aspectRatio = 1.0)
        S = sqrt (2) / 2
        self.CameraPose = array ([
            [0.0, -S, S, 0.3],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, S, S, 0.35],
            [0.0, 0.0, 0.0, 1.0]
        ])
        self.Scene.add(self.Camera, pose = self.CameraPose)
        self.Light = SpotLight (color = ones (3), intensity = 3.0, innerConeAngle = pi / 16.0, outerConeAngle = pi / 6.0)
        self.Scene.add (self.Light, pose = self.CameraPose)

        self.ModelMeshes = []

    def __repr__ (self):
        return self.Scene

    def Draw (self, _Object):
        self.Scene.add (_Object[1])
        self.ModelMeshes.append (_Object[2])

    def LoadScene (self, _Path):
        Data = Eve.Load (_Path)

        # General
        self.Title = Data['Title']
        self.Version = Data['Version']

        # Camera
        ZNear = Data['Camera'][0]
        ZFar = Data['Camera'][1]
        Name = Data['Camera'][2]
        YFov = Data['Camera'][3]
        AspectRatio = Data['Camera'][4]

        if ZNear is not None:
            self.Camera.znear = float (ZNear)

        if ZFar != 'None':
            self.Camera.zfar = float (ZFar)

        if Name != 'None':
            self.Camera.name = str (Name)

        if YFov != 'None':
            self.Camera.yfov = float (YFov)

        if AspectRatio != 'None':
            self.Camera.aspectRatio = float (AspectRatio)

        # Lighting
        Name = Data['Lighting'][0]
        Intensity = Data['Camera'][1]
        ShadowCamera = Data['Camera'][2]
        ShadowTexture = Data['Camera'][3]

        if Name != 'None':
            self.Camera.name = str (Name)

        if Intensity != 'None':
            self.Camera.intensity = float (Intensity)

        if ShadowCamera != 'None':
            self.Camera._shadow_camera = float (ShadowCamera)

        if ShadowTexture != 'None':
            self.Camera._shadow_texture = float (ShadowTexture)

        # Models
        for ModelPath in Data['Models']:
            self.Draw (Renderer.Render (ModelPath))

    def Run (self):
        Renderer = OffscreenRenderer (400, 400)
        Color, Depth = Renderer.render (self.Scene)
        plt.figure ()
        plt.subplot (1, 2, 1)
        plt.axis ('off')
        plt.imshow (Color)
        plt.subplot (1, 2, 2)
        plt.axis ('off')
        plt.imshow (Depth, cmap = plt.cm.gray_r)
        plt.show ()
