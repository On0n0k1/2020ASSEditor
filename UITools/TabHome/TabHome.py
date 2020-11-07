"""
Copyright 2020 Lucas Alessandro do Carmo Lemos

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:


The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.2.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from FileManagement.FileManagement import FileManagement as File
from Dados.SubPackage import SubPackage


class TabHome:
    """
        Frame that represents the first tab in UITools user interface.
    """

    def __init__(self, parentframe, ssaobject, initialsavedir=f"{__file__}", initialloaddir=f"{__file__}"):
        """
            Creates a home Frame using parentframe as parent widget.
            Args:
                parentframe: tk.TK instance or Frame instance.
                ssaobject: Dados.SubPackage instance. Must be a reference for loading and saving.
                initialsavedir: path for a save directory. Expected to be "InputOutput/Output"
                initialloaddir: path for a load directory. Expected to be "InputOutput/Input"
        """

        # There must be a better way for checking if parentframe is a valid parent
        if (isinstance(parentframe, tk.Tk) or isinstance(parentframe, tk.Frame) or
                isinstance(parentframe, ttk.Frame)) is False:
            raise TypeError(f"parentframe is {type(parentframe)}. Expected tk.Tk or tk.Frame instead.")

        if File.exists(initialsavedir) is False:
            raise TypeError(f"Invalid path argument: {initialsavedir}")
        if File.exists(initialloaddir) is False:
            raise TypeError(f"Invalid path argument: {initialsavedir}")
        if isinstance(ssaobject, SubPackage) is False:
            raise TypeError(f"Invalid ssaobject type: {type(ssaobject)}")

        self.initialsavedir = initialsavedir
        self.initialloaddir = initialloaddir
        self.ssaobject = ssaobject
        # Default file name for saving, will be replaced when another is loaded
        self.savefilename = "output"

        frame = tk.Frame(parentframe)
        frame.pack()

        loadbutton = tk.Button(frame, text='Open File', command=self.openfilebuttom)
        loadbutton.pack(fill=tk.X, side=tk.TOP)
        savebutton = tk.Button(frame, text='Save File', command=self.savefilebuttom)
        savebutton.pack(fill=tk.X, side=tk.TOP)
        printbutton = tk.Button(frame, text='Print loaded SSA Object', command=self.printfilebuttom)
        printbutton.pack(fill=tk.X, side=tk.TOP)

    def openfilebuttom(self):
        name = fd.askopenfilename(parent=None, initialdir=self.initialloaddir, filetypes=(("SSA Files", "*.ass"),))
        if name == "" or name == ():
            pass
        else:
            # Back when I wrote the method, I didn't know how to manage paths through os. So turning it into a string
            # instead
            self.ssaobject.loadfile(f"{name}")
            # Will take loaded file name to use when saving
            self.savefilename = File.lastpathname(f"{name}")

    def savefilebuttom(self):
        name = fd.asksaveasfilename(parent=None, initialdir=self.initialsavedir, initialfile=self.savefilename,
                                    filetypes=(("SSA Files", "*.ass"),))
        # print(name)
        # Not sure why. Pressing cancel sometimes return an empty tuple.
        if name == () or name == "":
            pass
        else:
            self.ssaobject.savefile(name, overwrite=True)

    def printfilebuttom(self):
        # By checking the __repr__ method, it's visible that the object will call all it's children __repr__ methods.
        # This isn't just printing the file. I will add edit tools to this window as soon as I'm able to make a rest
        # project. Which is currently a priority in terms of "hirability" for me.
        print(self.ssaobject)


if __name__ == "__main__":
    x = SubPackage()
    root = tk.Tk()
    root.resizable(False, False)
    root.eval('tk::PlaceWindow . Center')

    frame2 = tk.Frame(root)
    # Add contents inside of frame2
    TabHome(parentframe=frame2, ssaobject=x)
    frame2.pack()

    tk.mainloop()
