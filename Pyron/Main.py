from GUI import RenderWindow
from Core import Render
from Engine import SaveScene
from Scripting import Input

# -- Test / Debug Functions --
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

    pass

def RunTest2 ():
    # -- Simple Example --
    #Window = RenderWindow ()
    #Window.Draw (Render ('Data/Models/Test Models/Car.obj'))
    #Window.SpinCamera ()
    #Window.RotateCamera (180)
    #Window.ShowFPS (True)
    #Window.Run ()

    pass

# -- Test / Debug Function Calls --
#RunTest1 ()
RunTest2 ()
