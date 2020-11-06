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
from tkinter import filedialog as fd

from FileManagement.FileManagement import FileManagement as File
from Dados.SubPackage import SubPackage


class UITools:
    """ Have some tools that use the module tkinter in it."""
    def __init__(self, ssaobject=SubPackage(), initialsavedir=f"{__file__}", initialloaddir=f"{__file__}"):
        # This functions just calls os.path.lexists
        # Using this so the code doesn't mix FileManagement and os.path together
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

        self.root = tk.Tk()
        # root.geometry("200x100")
        self.root.resizable(False, False)
        # Executes a tk language command to center the window
        self.root.eval('tk::PlaceWindow . center')
        frame = tk.Frame(self.root)
        frame.pack()

        upperframe = tk.Frame(self.root)
        upperframe.pack(side=tk.TOP)

        bottomframe = tk.Frame(self.root)
        bottomframe.pack(side=tk.BOTTOM)

        label = tk.Label(upperframe, text="Control Panel (More will be added later)")
        label.pack(fill=tk.X)

        loadbutton = tk.Button(bottomframe, text='Open File', command=self.openfilebuttom)
        loadbutton.pack(fill=tk.X, side=tk.TOP)
        savebutton = tk.Button(bottomframe, text='Save File', command=self.savefilebuttom)
        savebutton.pack(fill=tk.X, side=tk.TOP)
        printbutton = tk.Button(bottomframe, text='Print loaded SSA Object', command=self.printfilebuttom)
        printbutton.pack(fill=tk.X, side=tk.TOP)
        closebutton = tk.Button(bottomframe, text='Exit', command=self.close)
        closebutton.pack(fill=tk.X, side=tk.BOTTOM)
        tk.mainloop()

    def openfilebuttom(self):
        name = fd.askopenfilename(parent=None, initialdir=self.initialloaddir, filetypes=(("SSA Files", "*.ass"),))
        if name == "":
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
        # Not sure why. Pressing cancel returns an empty tuple. While load just returns an empty string.
        if name == () or name == "":
            pass
        else:
            self.ssaobject.savefile(name, overwrite=True)

    def printfilebuttom(self):
        # By checking the __repr__ method, it's visible that the object will call all it's children __repr__ methods.
        # This isn't just printing the file. I will add edit tools to this window as soon as I'm able to make a rest
        # project. Which is currently a priority in terms of "hirability" for me.
        print(self.ssaobject)

    def close(self):
        self.root.destroy()


if __name__ == "__main__":
    IOpaths = File()
    x = UITools(initialloaddir=IOpaths.getinputpath(), initialsavedir=IOpaths.getoutputpath())
    # x.callback()
