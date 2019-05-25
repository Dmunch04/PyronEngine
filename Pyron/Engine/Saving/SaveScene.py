import os

def SaveScene (_Scene, _Path = ''):
    """
        Saves the given window/scene into a folder called 'Build'
        Files in the folder:
            Scene.eve
            Models
                - Model1.obj
                - Model2.obj
                - etc.
    """

    if _Path.endswith ('/'):
        Path = _Path + 'Build'

    elif _Path == '' or _Path == ' ':
        Path = _Path + 'Build'

    else:
        Path = _Path + '/Build'

    if not os.path.exists (Path):
        os.makedirs (Path)

    ModelPath = Path + '/Models'
    if not os.path.exists (ModelPath):
        os.makedirs (ModelPath)

    Models = []

    Index = 1
    for Model in _Scene.ModelMeshes:
        ModelSavePath = ModelPath + f'/Model{str (Index)}.egg'

        with open (ModelSavePath, 'w+') as File:
            File.write (Model)

        Models.append (f"'{ModelSavePath}'")

        Index += 1

    Models = ', '.join (Models)

    """
    Camera = [
        f"'{_Scene.Camera.znear}'",
        f"'{_Scene.Camera.zfar}'",
        f"'{_Scene.Camera.name}'",
        f"'{_Scene.Camera.yfov}'",
        f"'{_Scene.Camera.aspectRatio}'"
    ]
    Camera = ', '.join (Camera)

    Light = [
        f"'{_Scene.Light.name}'",
        #f'{_Scene.Light.color}',
        f"'{_Scene.Light.intensity}'",
        f"'{_Scene.Light._shadow_camera}'",
        f"'{_Scene.Light._shadow_texture}'"
    ]
    Light = ', '.join (Light)

    Data = "[\n  'Title' :: '{0}'\n  'Version' :: '{1}'\n  'Camera' :: ({2})\n  'Lighting' :: ({3})\n  'Models' :: ({4})\n];".format (
        _Scene.Title,
        _Scene.Version,
        Camera,
        Light,
        Models
    )
    """

    Data = "[\n  'Title' :: '{0}'\n  'Version' :: '{1}'\n  'Models' :: ({4})\n];".format (
        _Scene.Title,
        _Scene.Version,
        Models
    )

    Path += '/Scene.eve'
    with open (Path, 'w+') as File:
        File.write (Data)
