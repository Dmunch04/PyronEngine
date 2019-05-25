import glfw
import time
import math

class App:
    def __init__ (self, Module, Title, Width, Height):
        global Pyron
        Pyron = Module

        self.Module = Module
        self.Title = Title
        self.Width = Width
        self.Height = Height

        # Change the FPS later idk
        FPS = 100
        self._NextUpdateTime = 0
        self._OneFrameTime = 1 / FPS
        self._Update = None
        self._Draw = None

        Monitor = glfw.get_primary_monitor ()
        DisplayWidth, DisplayHeight = glfw.get_video_mode (Monitor)[0]

        self._Window = glfw.create_window (_Width, _Height, _Title, None, None)
        if not self._Window:
            glfw.terminate ()

        glfw.set_window_pos (
            self._Window,
            (DisplayWidth - _Width) // 2,
            (DisplayHeight - _Height) // 2
        )

    def Run (self, _Update, _Draw):
        self._Update = _Update
        self._Draw = _Draw

        def MainLoop ():
            while not glfw.window_should_close (self._Window):
                glfw.poll_events ()

                self._UpdateFrame ()
                self._DrawFrame ()

                glfw.swap_buffers (self._Window)

            glfw.terminate ()

        MainLoop ()

    def _UpdateFrame (self):
        while True:
            CurTime = time.time ()
            WaitTime = self._NextUpdateTime - CurTime

            if WaitTime > 0:
                time.sleep (WaitTime)

            else:
                break

            UpdateCount = math.floor (-WaitTime / self._OneFrameTime) + 1
            self._NextUpdateTime += UpdateCount * self._OneFrameTime

    def _DrawFrame (self):
        DrawStartTime = time.time ()
