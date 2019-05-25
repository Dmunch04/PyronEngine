__version__ = '0.0.1'

import sys
from App import App
from Core import Renderer
from Scripting import Input
from GUI import RenderWindow

def Init (_Title: str, _Width: int, _Height: int) -> None:
    Module = sys.modules[__name__]

    App (Module, _Title, _Width, _Height)
