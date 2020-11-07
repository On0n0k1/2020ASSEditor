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
# from tkinter import filedialog as fd

from FileManagement.FileManagement import FileManagement as File
from Dados.SubPackage import SubPackage
from UITools.TabHome.TabHome import TabHome


class UserInterface:
    """ Have some tools that use the module tkinter in it."""
    def __init__(self, ssaobject=SubPackage(), initialsavedir=f"{__file__}", initialloaddir=f"{__file__}"):
        # This functions just calls os.path.lexists
        # Using this so the code doesn't mix FileManagement and os.path together
        # if File.exists(initialsavedir) is False:
        #     raise TypeError(f"Invalid path argument: {initialsavedir}")
        # if File.exists(initialloaddir) is False:
        #     raise TypeError(f"Invalid path argument: {initialsavedir}")
        if isinstance(ssaobject, SubPackage) is False:
            raise TypeError(f"Invalid ssaobject type: {type(ssaobject)}")

        self.initialsavedir = initialsavedir
        self.initialloaddir = initialloaddir
        self.ssaobject = ssaobject

        self.root = tk.Tk()
        self.root.geometry("400x300")
        # self.root.resizable(False, False)
        # Executes a tk language command to center the window
        self.root.eval('tk::PlaceWindow . center')
        frame = tk.Frame(self.root)
        # TabHome(parentframe=frame, ssaobject=self.ssaobject, initialsavedir=initialsavedir,
        #         initialloaddir=initialloaddir)
        self.tabs(frame)
        frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        frame2 = tk.Frame(self.root)
        closebutton = tk.Button(frame2, text='Exit', command=self.close)
        closebutton.pack(fill=tk.X, side=tk.BOTTOM)
        frame2.pack(side=tk.BOTTOM)
        tk.mainloop()

    def tabs(self, parentframe):
        """

        Args:
            parentframe: tk.Tk instance or tk.Frame instance to adopt this frame.

        Returns: tab reference

        """

        tabcontrol = ttk.Notebook(parentframe)

        tabhome = ttk.Frame(tabcontrol)
        tabscriptinfo = ttk.Frame(tabcontrol)
        tabv4styles = ttk.Frame(tabcontrol)
        tabevents = ttk.Frame(tabcontrol)

        tabcontrol.add(tabhome, text="Home")
        tabcontrol.add(tabscriptinfo, text="ScriptInfo")
        tabcontrol.add(tabv4styles, text="V4Styles")
        tabcontrol.add(tabevents, text="Events")
        tabcontrol.pack(expand=1, fill="both")

        TabHome(parentframe=tabhome, ssaobject=self.ssaobject, initialsavedir=self.initialsavedir,
                initialloaddir=self.initialloaddir)

    def close(self):
        self.root.destroy()


if __name__ == "__main__":
    IOpaths = File()
    x = UserInterface(initialloaddir=IOpaths.getinputpath(), initialsavedir=IOpaths.getoutputpath())
    # x.callback()
