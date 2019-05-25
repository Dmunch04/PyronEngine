import numpy as np

class ObjLoader:
    def __init__ (self):
        self.VertexCoords = []
        self.TextureCoords = []
        self.NormalCoords = []

        self.VertexIndex = []
        self.TextureIndex = []
        self.NormalIndex = []

        self.Model = []

    def Load (self, _File):
        with open (_File, 'r') as File:
            Lines = File.readlines ()

        for Line in Lines:
            Line = Line.strip ()
            Values = Line.split ()

            if Line.startswith ('#') or not Values:
                continue

            if Values[0] == 'v':
                self.VertexCoords.append (Values[1 : 4])

            elif Values[0] == 'vt':
                self.TextureCoords.append (Values[1 : 3])

            elif Values[0] == 'vn':
                self.NormalCoords.append (Values[1 : 4])

            elif Values[0] == 'f':
                FaceI = []
                TextureI = []
                NormalI = []

                for Value in Values[1 : 4]:
                    W = Value.split ('/')
                    # Error here:
                    # TextureI.append (int (W[1]) - 1)
                    # ValueError: invalid literal for int() with base 10: ''
                    try:
                        FaceI.append (int (W[0]) - 1)
                        TextureI.append (int (W[1]) - 1)
                        NormalI.append (int (W[2]) - 1)

                    except:
                        pass

                self.VertexIndex.append (FaceI)
                self.TextureIndex.append (TextureI)
                self.NormalIndex.append (NormalI)

        self.VertexIndex = [Y for X in self.VertexIndex for Y in X]
        self.TextureIndex = [Y for X in self.TextureIndex for Y in X]
        self.NormalIndex = [Y for X in self.NormalIndex for Y in X]

        for Index in self.VertexIndex:
            self.Model.extend (self.VertexCoords[Index])

        for Index in self.TextureIndex:
            self.Model.extend (self.TextureCoords[Index])

        for Index in self.NormalIndex:
            self.Model.extend (self.NormalCoords[Index])

        self.Model = np.array (self.Model, dtype = 'float32')

Loader = ObjLoader ()
Loader.Load ('Test.obj')
print (Loader.Model[1401])
