import glfw
from Main import Item
import TestRender as TR
from OpenGL.GL import *
from OpenGL.GLU import *

def Test (_Title, _Width, _Height):
    Object = Item ('Model.obj')

    if not glfw.init ():
        return

    Window = glfw.create_window (_Width, _Height, _Title, None, None)

    if not Window:
        glfw.terminate ()
        return

    gluPerspective (45, (_Width / _Height), 0.1, 50)
    glTranslatef (0, 0, -5)

    while not glfw.window_should_close (Window):
        glRotatef (2, 1, 1, 3)
        glClear (GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        TR.Draw (TR.Vertices, TR.Edges)
        # Render here, e.g. using pyOpenGL
        #glBegin ()

        #Object.Render ()
        #Object.Model.Render ()

        #glEnd ()

        # Swap front and back buffers
        glfw.swap_buffers (Window)

        # Poll for and process events
        glfw.poll_events ()

    glfw.terminate ()

Test ('Test', 800, 600)
