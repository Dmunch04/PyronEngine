import glfw
#from ObjLoader import ObjLoader
#from TestRender import Draw
from OpenGL.GL import *

Vertices = []
Faces = []
def Load (fileName):
    try:
        f = open(fileName)
        for line in f:
            if line[:2] == "v ":
                index1 = line.find(" ") + 1
                index2 = line.find(" ", index1 + 1)
                index3 = line.find(" ", index2 + 1)

                vertex = (float(line[index1:index2]), float(line[index2:index3]), float(line[index3:-1]))
                vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))
                Vertices.append(vertex)

            elif line[0] == "f":
                string = line.replace("//", "/")
                i = string.find(" ") + 1
                face = []
                for item in range(string.count(" ")):
                    if string.find(" ", i) == -1:
                        face.append(string[i:-1])
                        break
                    face.append(string[i:string.find(" ", i)])
                    i = string.find(" ", i) + 1
                Faces.append(tuple(face))

        f.close()
    except IOError:
        print(".obj file not found.")

Load ('Test.obj')

def Run (_Title, _Width, _Height):
    if not glfw.init ():
        return

    Window = glfw.create_window (_Width, _Height, _Title, None, None)

    if not Window:
        glfw.terminate ()
        return

    while not glfw.window_should_close (Window):
        # Render here, e.g. using pyOpenGL
        glPolygonMode (GL_FRONT_AND_BACK, GL_LINE)
        glBegin ()

        for Face in Faces:
            for F in Face:
                Vertex = Vertices[int (F) - 1]

                if int (F) % 3 == 1:
                    glColor4f (0.282, 0.239, 0.545, 0.35)

                elif int (F) % 3 == 2:
                    glColor4f (0.729, 0.333, 0.827, 0.35)

                else:
                    glColor4f (0.545, 0.000, 0.545, 0.35)

                glVertex3fv(Vertex)

        glEnd ()

        # Swap front and back buffers
        glfw.swap_buffers (Window)

        # Poll for and process events
        glfw.poll_events ()

    glfw.terminate ()

Run ('Test', 800, 600)
