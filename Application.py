import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from Misc import GetArgument, OpenFileDialog
import GlobalControl
import ContextMenu



class Settings_class:
    #These settings are Tkinter objects (not normal bools). You need to use get() to obtain the actual values.
    def __init__(self):
        self.deleteOriginal    = tk.BooleanVar()
        self.deleteTemp        = tk.BooleanVar()
        self.smartResize       = tk.BooleanVar()
        self.onlyReduce        = tk.BooleanVar()
        self.closeWhenFinished = tk.BooleanVar()




class Application:

    def __init__(self):

        self.argument = GetArgument()       #Get argument (file or folder name) if program was executed from a context menu

        self.window = tk.Tk()               #Create main window
        
        self.settings = Settings_class()    #This object holds settings from the different user inputs

       

        #    _____ _    _ _____ 
        #   / ____| |  | |_   _|
        #  | |  __| |  | | | |  
        #  | | |_ | |  | | | |  
        #  | |__| | |__| |_| |_ 
        #   \_____|\____/|_____|

        #GUI uses the Tkinter framework. The elements are positioned using pack(), rather than grid(),
        #as I found it easier for correct alignments as long as inline elements are grouped inside frames

        ''' ----- Main window ----- '''
        self.window.geometry("300x350")
        self.window.title("Comic Resizer")

        ''' ----- Source ----- '''
        self.frameSource = tk.Frame(self.window)
        self.frameSource.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.label = tk.Label(self.frameSource, text="Source")
        self.label.pack(side=tk.TOP, fill=tk.NONE, expand=True, padx=5, pady=0, anchor='sw')

        self.pathTextBox = tk.Entry(self.frameSource, width=42)
        self.pathTextBox.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=0, anchor='nw')
        self.pathTextBox.insert(0, self.argument)

        self.dirDialogButton = tk.Button(self.frameSource, text="...", height=1, command=lambda:OpenFileDialog(self.pathTextBox))
        self.dirDialogButton.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=0)
       

        ''' ----- Width ----- '''
        self.frameWidth = tk.Frame(self.window)
        self.frameWidth.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.label = tk.Label(self.frameWidth, text="Width (px)")
        self.label.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=5, anchor="w")

        self.widthTextBox = tk.Entry(self.frameWidth, width=5)
        self.widthTextBox.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=5)
        self.widthTextBox.insert(0, '1280')
        

        ''' ----- Settings ----- '''
        self.separ = ttk.Separator(self.window, orient=tk.HORIZONTAL)
        self.separ.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=5, pady=0)

        self.frameSett = tk.Frame(self.window)  #Frame for all checkboxes
        self.frameSett.pack(side=tk.TOP, fill=tk.BOTH, expand=False, anchor='n')

        self.frame1 = tk.Frame(self.frameSett)  #Subframe to put the first two checboxes on same row 
        self.frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        self.checkBoxDelete = tk.Checkbutton(self.frame1, text="Delete original", variable=self.settings.deleteOriginal)
        self.checkBoxDelete.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=0, anchor="w")
        
        self.checkBoxDeleteTemp = tk.Checkbutton(self.frame1, text="Delete temp folder", variable=self.settings.deleteTemp)
        self.checkBoxDeleteTemp.pack(side=tk.RIGHT, fill=tk.NONE, expand=False, padx=5, pady=0, anchor="w")

        self.checkBoxSmart = tk.Checkbutton(self.frameSett, text="Smart resizing (detect doublepages, etc.)", variable=self.settings.smartResize)
        self.checkBoxSmart.select()
        self.checkBoxSmart.pack(side=tk.TOP, fill=tk.NONE, expand=False, padx=5, pady=0, anchor="w")

        self.checkBoxOnlyReduce = tk.Checkbutton(self.frameSett, text="Only reduce size, don't increase", variable=self.settings.onlyReduce)
        self.checkBoxOnlyReduce.select()
        self.checkBoxOnlyReduce.pack(side=tk.TOP, fill=tk.NONE, expand=False, padx=5, pady=0, anchor="w")

        self.separ = ttk.Separator(self.window, orient=tk.HORIZONTAL)
        self.separ.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=5, pady=5)


        ''' ----- Buttons ----- '''
        self.frameStartBtns = tk.Frame(self.window)
        self.frameStartBtns.pack(side=tk.TOP, fill=tk.BOTH, expand=False, anchor='n')

        self.font1 = font.Font(size=20)
        self.buttonResize = tk.Button(self.frameStartBtns, text="Resize", font=self.font1, height=1, command=lambda:GlobalControl.ResizeComic(self.pathTextBox.get() , int(self.widthTextBox.get()) , self.settings))
        self.buttonResize.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=10, pady=5)

        self.frame1 = tk.Frame(self.frameStartBtns)
        self.frame1.pack(side=tk.TOP, fill=tk.BOTH, expand=False, anchor='n')
        
        self.label = tk.Label(self.frame1, text="Substeps:")
        self.label.pack(side=tk.LEFT, fill=tk.NONE, expand=True, padx=0, pady=0)

        self.buttonExtractAndPreview = tk.Button(self.frame1, text="1/2\nExtract & preview", height=2, command=lambda:GlobalControl.ExtractAndPreview(self.pathTextBox.get() , self.settings))
        self.buttonExtractAndPreview.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=0, pady=5)
        
        self.buttonResize = tk.Button(self.frame1, text="2/2\nResize & compress", height=2, command=lambda:GlobalControl.ResizeAndCompress(self.pathTextBox.get() , int(self.widthTextBox.get()) , self.settings))
        self.buttonResize.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=5)

        self.separ = ttk.Separator(self.window, orient=tk.HORIZONTAL)
        self.separ.pack(side=tk.TOP, fill=tk.BOTH, expand=False, padx=5, pady=5)


        ''' ----- Footer ----- '''
        self.frameFooter = tk.Frame(self.window)
        self.frameFooter.pack(side=tk.TOP, fill=tk.BOTH, expand=False, anchor='n')

        self.checkBoxClose = tk.Checkbutton(self.frameFooter, text="Close when finished", variable=self.settings.closeWhenFinished)
        self.checkBoxClose.pack(side=tk.LEFT, fill=tk.NONE, expand=False, padx=5, pady=0, anchor="w")
        self.checkBoxClose.select()

        self.buttonContextMenu = tk.Button(self.frameFooter, text="Add context\nmenu item", command=ContextMenu.AddToContextMenu)
        self.buttonContextMenu.pack(side=tk.RIGHT, fill=tk.NONE, expand=False, padx=5, pady=5)




    ''' Main loop: runs the application '''
    def run(self):
        self.window.mainloop()