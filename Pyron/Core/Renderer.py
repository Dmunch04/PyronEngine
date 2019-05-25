import trimesh
from pyrender import Mesh
from Core.Convert import Convert

def Render (_Model = ''):
    EggData = Convert (_Model)

    Path = 'Temp/Model.egg'
    EggData.writeEgg (Path)

    with open (Path, 'r') as File:
        Data = File.read ()

    return Path, Data
