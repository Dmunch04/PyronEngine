from OpenGL.GL import *

class ObjLoader (object):
    def __init__ (self):
        self.Vertices = []
        self.Faces = []

    def Load (self, _Filename):
        try:
            with open (_Filename, 'r') as File:
                Lines = File.readlines ()

        except IOError:
            print ('.obj file not found!')
            return

        for Line in Lines:
            if Line[:2] == 'v ':
                Index1 = Line.find (' ') + 1
                Index2 = Line.find (' ', Index1 + 1)
                Index3 = Line.find (' ', Index2 + 1)

                Vertex = (float (Line[Index1 : Index2]), float (Line[Index2 : Index3]), float (Line[Index3 : -1]))

                Vertex = (round (Vertex[0], 2), round (Vertex[1], 2), round (Vertex[2], 2))
                self.Vertices.append (Vertex)

            elif Line[0] == 'f':
                String = Line.replace ('//', '/')
                Index = String.find (' ') + 1
                Face = []

                for Item in range (String.count (' ')):
                    if String.find (' ', Index) == -1:
                        Face.append (String[Index : -1])
                        break

                    Face.append (String[Index : String.find (' ', Index)])
                    Index = String.find (' ', Index) + 1

                self.Faces.append (tuple (Face))

    def Render (self):
        if len (self.Faces) > 0:
            glPolygonMode (GL_FRONT_AND_BACK, GL_LINE)
            glBegin (GL_TRIANGLES)

            for Face in self.Faces:
                for F in Face:
                    Vertex = self.Vertices[int (F) - 1]

                    if int (F) % 3 == 1:
                        glColor4f (0.282, 0.239, 0.545, 0.35)

                    elif int (F) % 3 == 2:
                        glColor4f (0.729, 0.333, 0.827, 0.35)

                    else:
                        glColor4f (0.545, 0.000, 0.545, 0.35)

                    glVertex3fv (Vertex)

            glEnd ()
