# Based on:
# https://github.com/treeform/obj2egg/blob/master/obj2egg.py
# By: treeform

import os
import sys
import math
import string
import getopt
from DavesLogger import Logs
from pandac.PandaModules import *

def Floats (_FloatList):
    return [float (Number) for Number in _FloatList]

def Ints (_IntList):
    return [int (Number) for Number in _IntList]

class ObjMaterial:
    def __init__ (self):
        self.FileName = None
        self.Name = 'default'
        self.EggDiffuseTexture = None
        self.EggMaterial = None
        self.Attrib = {}
        self.Attrib['Ns'] = 100.0
        self.Attrib['d'] = 1.0
        self.Attrib['illum'] = 2
        self.Attrib['Kd'] = [1.0, 0.0, 1.0]
        self.Attrib['Ka'] = [0.0, 0.0, 0.0]
        self.Attrib['Ks'] = [0.0, 0.0, 0.0]
        self.Attrib['Ke'] = [0.0, 0.0, 0.0]

    def Put (self, _Key, _Value):
        self.Attrib[_Key] = _Value

        return self

    def Get (self, _Key):
        if _Key in self.Attrib:
            return self.Attrib[_Key]

        return None

    def HasKey (self, _Key):
        return _Key in self.Attrib

    def IsTextured (self):
        if 'map_kd' in self.Attrib:
            return True

        return False

    def GetEggTexture (self):
        if self.EggDiffuseTexture:
            return self.EggDiffuseTexture

        if not self.IsTextured ():
            return None

        Texture = EggTexture (self.Name + '_diffuse', self.Get ('map_Kd'))
        Texture.setFormat (EggTexture.FRgb)
        Texture.setMagfilter (EggTexture.FTLinearMipmapLinear)
        Texture.setMinfilter (EggTexture.FTLinearMipmapLinear)
        Texture.setWrapU (EggTexture.WMRepeat)
        Texture.setWrapV (EggTexture.WMRepeat)
        self.EggDiffuseTexture = Texture

        return self.EggDiffuseTexture

    def GetEggMaterial (self):
        if self.EggMaterial:
            return self.EggMaterial

        Material = EggMaterial (self.Name + '_mat')

        RGB = self.Get ('Kd')
        if RGB is not None:
            Material.setDiff (Vec4 (RGB[0], RGB[1], RGB[2], 1.0))

        RGB = self.Get ('Ka')
        if RGB is not None:
            Material.setAmb (Vec4 (RGB[0], RGB[1], RGB[2], 1.0))

        RGB = self.Get ('Ks')
        if RGB is not None:
            Material.setSpec (Vec4 (RGB[0], RGB[1], RGB[2], 1.0))

        NS = self.Get ('Ns')
        if NS is not None:
            Material.setShininess (NS)

        self.EggMaterial = Material

        return self.EggMaterial

class MtlFile:
    def __init__ (self, FileName = None):
        self.FileName = None
        self.Materials = {}
        self.Comments = {}

        if FileName is not None:
            self.Read (FileName)

    def Read (self, _FileName, _Verbose = False):
        self.FileName = _FileName
        self.Materials = {}
        self.Comments = {}

        try:
            File = open (_FileName)
            Lines = File.readlines ()

        except:
            return self

        LineNumber = 0
        Material = None
        for Line in Lines:
            Line = Line.strip ()
            LineNumber += 1

            if not Line:
                continue

            if Line[0] == '#':
                self.Comments[LineNumber] = Line
                #print (Line)

                continue

            Tokens = Line.split ()
            if not Tokens:
                continue

            if _Verbose:
                print ('tokens[0]:', Tokens)

            if Tokens[0] == 'newmtl':
                Material = ObjMaterial ()
                Material.FileName = _FileName
                Material.Name = Tokens[1]
                self.Materials[Material.Name] = Material

                if _Verbose:
                    print ('newmtl:', Material.Name)

                continue

            if Tokens[0] in ('Ns', 'd', 'Tr'):
                Material.Put (Tokens[0], float (Tokens[1]))

                continue

            if Tokens[0] == 'illum':
                Material.Put (Tokens[0], int (Tokens[1]))

                continue

            if Tokens[0] in ('Kd', 'Ka', 'Ks', 'Ke'):
                Material.Put (Tokens[0], Floats (Tokens[1:]))

                continue

            if Tokens[0] in ('map_Kd', 'map_Bump', 'map_Ks', 'map_bump', 'bump'):
                Material.Put (Tokens[0], Pathify (Tokens[1]))

                if _Verbose:
                    print ('map:', Material.Name, Tokens[0], Material.Get (Tokens[0]))

                continue

            if Tokens[0] == 'Ni':
                Material.Put (Tokens[0], float (Tokens[1]))

                continue

            print (f'file \'{_FileName}\': line {str (LineNumber)}: unrecognized:', Tokens)

        File.close ()

        if _Verbose:
            print (f'{len (self.Materials)} materials', 'loaded from', _FileName)

        return self

class ObjFile:
    def __init__ (self, FileName = None):
        self.FileName = None
        self.Objects = ['defaultobject']
        self.Groups = ['defaultgroup']
        self.Points = []
        self.UVS = []
        self.Normals = []
        self.Faces = []
        self.PolyLines = []
        self.MatLibs = []
        self.MaterialsByName = {}
        self.Comments = {}
        self.CurrentObject = self.Objects[0]
        self.CurrentGroup = self.Groups[0]
        self.CurrentMaterial = None

        if FileName is not None:
            self.Read (FileName)

    def Read (self, _FileName, _Verbose = False):
        if _Verbose:
            print ('ObjFile.Read:', 'filename:', _FileName)

        self.FileName = _FileName
        self.Objects = ['defaultobject']
        self.Groups = ['defaultgroup']
        self.Points = []
        self.UVS = []
        self.Normals = []
        self.Faces = []
        self.PolyLines = []
        self.MatLibs = []
        self.MaterialsByName = {}
        self.Comments = {}
        self.CurrentObject = self.Objects[0]
        self.CurrentGroup = self.Groups[0]
        self.CurrentMaterial = None

        try:
            File = open (_FileName)
            Lines = File.readlines ()

        except:
            return self

        LineNumber = 0
        for Line in Lines:
            Line = Line.strip()
            LineNumber += 1

            if not Line:
                continue

            if Line[0] == '#':
                self.Comments[LineNumber] = Line
                #print (Line)

                continue

            Tokens = Line.split ()
            if not Tokens:
                continue

            if Tokens[0] == 'mtllib':
                if _Verbose:
                    print ('mtllib:', Tokens[1:])

                Path = os.path.dirname (self.FileName)
                MtlLib = MtlFile (Path + '/' + Tokens[1])
                self.MatLibs.append (MtlLib)
                self.IndexMaterials (MtlLib)

                continue

            if Tokens[0] == 'g':
                if _Verbose:
                    print ('g:', Tokens[1:])

                self.__NewGroup (''.join (Tokens[1:]))

                continue

            if Tokens[0] == 'o':
                if _Verbose:
                    print ('o:', tokens[1:])

                self.__NewObject (''.join (Tokens[1:]))

                continue

            if Tokens[0] == 'usemtl':
                if _Verbose:
                    print ('usemtl:', Tokens[1:])

                self.__UseMaterial (Tokens[1])

                continue

            if Tokens[0] == 'v':
                if _Verbose:
                    print ('v:', Tokens[1:])

                self.__NewV (Tokens[1:])

                continue

            if Tokens[0] == 'vn':
                if _Verbose:
                    print ('vn:', Tokens[1:])

                self.__NewNormal (Tokens[1:])

                continue

            if Tokens[0] == 'vt':
                if _Verbose:
                    print ('vt:', Tokens[1:])

                self.__NewUV (Tokens[1:])

                continue

            if Tokens[0] == 'f':
                if _Verbose:
                    print ('f:', Tokens[1:])

                self.__NewFace (Tokens[1:])

                continue

            if Tokens[0] == 's':
                Logs.Warning (f'{_FileName} @ {str (LineNumber)}: Ignoring: ' + ''.join (Tokens))

                continue

            if Tokens[0] == 'l':
                if _Verbose:
                    print ('l:', Tokens[1:])

                self.__NewPolyLine (Tokens[1:])

                continue

            print (f'{_FileName}:{str (LineNumber)}:', 'Unknown:', Tokens)

        File.close ()

        return self

    def __VertList (self, _Verticies):
        Result = []

        for Verticy in _Verticies:
            Info = Verticy.split ('/')
            Length = len (Info)
            Vertex = {'v': None, 'vt': None, 'vn': None}

            if Length == 1:
                Vertex['v'] = int (Info[0])

            elif Length == 2:
                if Info[0] != '':
                    Vertex['v'] = int (Info[0])

                if vinfo[1] != '':
                    Vertex['vt'] = int (Info[1])

            elif Length == 3:
                if Info[0] != '':
                    Vertex['v'] = int (Info[0])

                if Info[1] != '':
                    Vertex['vt'] = int (Info[1])

                if Info[2] != '':
                    Vertex['vn'] = int (Info[2])

            else:
                print ('Aborting...')

            Result.append (Vertex)

        if False:
            print (Result)

        return Result

    def __Enclose (self, _List):
        Data = (self.CurrentObject, self.CurrentGroup, self.CurrentMaterial)

        return (_List, Data)

    def __NewPolyLine (self, _Line):
        PolyLine = self.__VertList (_Line)

        if False:
            print ('__newline:', PolyLine)

        self.PolyLines.append (self.__Enclose (PolyLine))

        return self

    def __NewFace(self, _Face):
        Face = self.__VertList (_Face)

        if False:
            print (Face)

        self.Faces.append (self.__Enclose (Face))

        return self

    def __NewUV(self, _UV):
        self.UVS.append (Floats (_UV))

        return self

    def __NewNormal (self, _Normal):
        self.Normals.append (Floats (_Normal))

        return self

    def __NewV (self, _Verticy):
        VerticyData = Floats (_Verticy)
        Data = (self.CurrentObject, self.CurrentGroup, self.CurrentMaterial)
        Info = (VerticyData, Data)

        self.Points.append (Info)

        return self

    def IndexMaterials (self, _MtlLib, _Verbose = False):
        for Name in _MtlLib.Materials:
            Obj = _MtlLib.Materials[Name]
            self.MaterialsByName[Obj.Name] = Obj

        if _Verbose:
            print ('indexmaterials:', _MtlLib.FileName, 'materials:', self.MaterialsByName.keys ())

        return self

    def __CloseObject (self):
        self.CurrentObject = 'defaultobject'

        return self

    def __NewObject (self, _Object):
        self.__CloseObject ()

        if False:
            print ('__newobject:', 'object:', _Object)

        self.CurrentObject = _Object
        self.Objects.append (_Object)

        return self

    def __CloseGroup (self):
        self.CurrentGroup = 'defaultgroup'

        return self

    def __NewGroup (self, _Group):
        self.__CloseGroup ()

        if False:
            print ('__newgroup:', 'group:', _Group)

        self.CurrentGroup = _Group
        self.Groups.append (_Group)

        return self

    def __UseMaterial (self, _Material):
        if False:
            print ('__usematerial:', 'material:', _Material)

        if _Material in self.MaterialsByName:
            self.CurrentMaterial = _Material

        else:
            Logs.Error ('__UseMaterial: Unkown Material ' + _Material)

        return self

    def __ItemsBy (self, _ItemList, _ObjectName, _GroupName):
        Result = []

        for Item in _ItemList:
            List, Data = Item
            Object, Group, Material = Data

            if (Object == _ObjectName) and (Group == _GroupName):
                Result.append (Item)

        return Result

    def __FacesBy (self, _ObjectName, _GroupName):
        return self.__ItemsBy (self.Faces, _ObjectName, _GroupName)

    def __LinesBy(self, _ObjectName, _GroupName):
        return self.__ItemsBy (self.PolyLines, _ObjectName, _GroupName)

    def __EggifyVerticies (self, _Eprim, _Evpool, _List):
        for Vertex in _List:
            ItemXYZ = Vertex['v']
            Info = self.Points[ItemXYZ - 1]
            VerticyXYZ, VerticyMeta = Info
            _EggVertex = EggVertex ()
            _EggVertex.setPos (Point3D (VerticyXYZ[0], VerticyXYZ[1], VerticyXYZ[2]))

            ItemUV = Vertex['vt']
            if ItemUV is not None:
                VerticyUV = self.UVS[ItemUV - 1]
                _EggVertex.setUv (Point2D (VerticyUV[0], VerticyUV[1]))

            ItemNormal = Vertex['vn']
            if ItemNormal is not None:
                VerticyNormal = self.Normals[ItemNormal - 1]
                _EggVertex.setNormal (Vec3D (VerticyNormal[0], VerticyNormal[1], VerticyNormal[2]))

            _Evpool.addVertex (_EggVertex)
            _Eprim.addVertex (_EggVertex)

        return self

    def __EggifyMaterials (self, _Eprim, _Material):
        if _Material in self.MaterialsByName:
            Material = self.MaterialsByName[_Material]

            if Material.IsTextured ():
                _Eprim.setTexture (Material.GetEggTexture ())
                _Eprim.setMaterial (Material.GetEggMaterial ())

            RGB = Material.Get ('Kd')
            if RGB is not None:
                _Eprim.setColor (Vec4 (RGB[0], RGB[1], RGB[2], 1.0))

            if False:
                _Eprim.setMaterial (Material.GetEggMaterial ())

        return self

    def __FacesToEgg(self, _Egg, _ObjectName, _GroupName):
        SelectedFaces = self.__FacesBy (_ObjectName, _GroupName)
        if len (SelectedFaces) == 0:
            return self

        EggObject = EggGroup (_ObjectName)
        _Egg.addChild (EggObject)
        _EggGroup = EggGroup (_GroupName)
        EggObject.addChild (_EggGroup)
        Evpool = EggVertexPool (_GroupName)
        _EggGroup.addChild (Evpool)

        for Face in SelectedFaces:
            List, Data = Face
            Object, Group, Material = Data

            _EggPolygon = EggPolygon ()
            _EggGroup.addChild (_EggPolygon)
            self.__EggifyMaterials (_EggPolygon, Material)
            self.__EggifyVerticies (_EggPolygon, Evpool, List)

        return self

    def __PolyLinesToEgg (self, _Egg, _ObjectName, _GroupName):
        SelectedLines = self.__LinesBy (_ObjectName, _GroupName)
        if len (SelectedLines) == 0:
            return self

        EggObject = EggGroup (_ObjectName)
        _Egg.addChild (EggObject)
        _EggGroup = EggGroup (_GroupName)
        EggObject.addChild (_EggGroup)
        Evpool = EggVertexPool (_GroupName)
        EggGroup.addChild (Evpool)

        for Line in SelectedLines:
            List, Data = Line
            Object, Group, Material = mdata
            _EggLine = EggLine ()
            EggGroup.addChild (_EggLine)
            self.__EggifyMaterials (_EggLine, Material)
            self.__EggifyVerticies (_EggLine, Evpool, List)

        return self

    def ToEgg (self, _Verbose = True):
        if _Verbose:
            print ('Converting...')

        Egg = EggData ()

        if len (self.Faces) > 0:
            for ObjectName in self.Objects:
                for GroupName in self.Groups:
                    self.__FacesToEgg (Egg, ObjectName, GroupName)

        if len (self.PolyLines) > 0:
            for ObjectName in self.Objects:
                for GroupName in self.Groups:
                    self.__PolyLinesToEgg (Egg, ObjectName, GroupName)
        return Egg

def Pathify (_Path):
    if os.path.isfile(_Path):
        return _Path

    Path = _Path.lower ()
    Path = Path.replace ('\\', '/')
    Head, Tail = os.path.split (Path)

    if os.path.isfile (Tail):
        return Tail

    print ('warning: can\'t make sense of this map file name:', _Path)

    return Tail

def Convert (Files = None):
    if isinstance (Files, str):
        Files = [Files]

    for InFile in Files:
        try:
            if not InFile.endswith ('.obj'):
                Logs.Warning (InFile + ' Does not look like to be a valid obj file!')
                continue

            Object = ObjFile (InFile)
            Egg = Object.ToEgg ()
            Root, Ext = os.path.splitext (InFile)
            OutFile = Root + '.egg'

            Egg.removeUnusedVertices (GlobPattern (''))

            if True:
                Egg.triangulatePolygons (EggData.TConvex & EggData.TPolygon)

            if True:
                Egg.recomputePolygonNormals ()

            return Egg

        except Exception as Error:
            print (Error)
