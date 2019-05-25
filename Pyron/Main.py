# Window Controls (This is controlled by pyrender):
# - a: Toggles rotational animation mode.
# - c: Toggles backface culling.
# - f: Toggles fullscreen mode.
# - h: Toggles shadow rendering.
# - i: Toggles axis display mode (no axes, world axis, mesh axes, all axes).
# - l: Toggles lighting mode (scene lighting, Raymond lighting, or direct lighting).
# - m: Toggles face normal visualization.
# - n: Toggles vertex normal visualization.
# - o: Toggles orthographic camera mode.
# - q: Quits the viewer.
# - r: Starts recording a GIF, and pressing again stops recording and opens a file dialog.
# - s: Opens a file dialog to save the current view as an image.
# - w: Toggles wireframe mode (scene default, flip wireframes, all wireframe, or all solid).
# - z: Resets the camera to the default view.



from GUI import Window, TestWindow
from Core import Renderer
from Engine import SaveScene
from Scripting import Input

def RunTest1 ():
    # -- Simple Drawing Example --
    #TestWindow = Window ()
    #TestWindow.Draw (Renderer.Render ('TEST_'))
    #TestWindow.Draw (Renderer.Render ('Data/Models/Test Models/Car.obj'))
    #TestWindow.Run ()

    # -- Save Example --
    #Window = TestWindow ()
    #Window.Draw (Renderer.Render ('TEST_'))
    #Window.Draw (Renderer.Render ('Data/Models/Test Models/Car.obj'))
    #SaveScene (Window)

    # -- Load Example --
    #xWindow = Window ()
    #xWindow.LoadScene ('Build/Scene.eve')
    #xWindow.Run ()

RunTest1 ()
