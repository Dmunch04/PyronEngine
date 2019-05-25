import keyboard

class Input:
    def AwaitKey (_Key):
        while True:
            if keyboard.is_pressed (_Key):
                return True

    def GetKeyDown (_Key):
        if keyboard.is_pressed (_Key):
            return True

        else:
            return False
