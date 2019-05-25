from GUI import RenderWindow

class Editor (RenderWindow):
    def __init__ (self, Title, Version, Width, Height):
        super ().__init__ (Title, Version, Width, Height)

        self.HistoryList = []
        self.HistoryIndex = 0

    @proberty
    def CanUndo (self):
        return self.HistoryIndex > 0

    @proberty
    def CanRedo (self):
        return self.HistoryIndex < len (self.HistoryList)

    def Undo (self):
        if not self.CanUndo:
            return

        self.HistoryIndex -= 1
        # Undo

    def Redo (self):
        if not self.CanRedo:
            return

        # Redo
        self.HistoryIndex += 1

    def AddHistory (self, _Data):
        self.HistoryList = self.HistoryList[: self.HistoryIndex]
        self.HistoryList.append (_Data)
        self.HistoryIndex += 1
