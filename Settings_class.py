import tkinter as tk

class Settings_class:
    def __init__(self):
        self.deleteOriginal    = tk.BooleanVar()
        self.deleteTemp        = tk.BooleanVar()
        self.smartResize       = tk.BooleanVar()
        self.onlyReduce        = tk.BooleanVar()
        self.closeWhenFinished = tk.BooleanVar()

    def ChangeToNormalVars(self):
        '''Convert tkinter vars to normal vars that can be used by the rest of the application'''
        self.deleteOriginal    = self.deleteOriginal.get()
        self.deleteTemp        = self.deleteTemp.get()
        self.smartResize       = self.smartResize.get()
        self.onlyReduce        = self.onlyReduce.get()
        self.closeWhenFinished = self.closeWhenFinished.get()