import trimesh
from pyrender import Mesh

def Render (_Model = ''):
    if _Model == 'TEST_':
        ModelTrimesh = trimesh.load ('Data/Models/Test Models/LegoMan.obj')
        ModelMesh = Mesh.from_trimesh (ModelTrimesh)

        with open ('Data/Models/Test Models/LegoMan.obj', 'r') as File:
            Data = File.read ().strip ()

        return ModelTrimesh, ModelMesh, Data

    else:
        ModelTrimesh = trimesh.load (_Model)
        ModelMesh = Mesh.from_trimesh (ModelTrimesh)

        with open (_Model, 'r') as File:
            Data = File.read ().strip ()

        return ModelTrimesh, ModelMesh, Data
