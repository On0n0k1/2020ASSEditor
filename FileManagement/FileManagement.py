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

import os


class FileManagement:
    """
        Object for managing file input and output.
    """
    def __init__(self, pathname=None):
        """
            :param pathname: Path for Input/Output folders. If not specified. It will use the default folder. Default
            folder is 2020ASSEditor/Testing/
        """

        if pathname is not None:
            if os.path.isdir(self.upperpath(pathname)) is False:
                raise ValueError(f"Not an existing directory path.")

            self.pathname = self.upperpath(pathname)

            self.__inputlocation__ = self.connectpath(f"{self.pathname}", "Input/")
            self.__outputlocation__ = self.connectpath(f"{self.pathname}", "Output/")
        else:
            # This is expecting that the module wasn't imported by a project outside 2020ASSEditor
            thisplace = FileManagement.upperpath(f"{__file__}")
            thisplace = FileManagement.upperpath(thisplace)
            thisplace = FileManagement.connectpath(thisplace, "InputOutput//")

            self.__inputlocation__ = self.connectpath(f"{thisplace}", "Input/")
            self.__outputlocation__ = self.connectpath(f"{thisplace}", "Output/")

    @staticmethod
    def connectpath(path1, path2):
        """Trying to connect 2 paths in a way compatible for both windows and unix"""
        outpath = os.path.normcase(path1)
        outpath = os.path.join(outpath, os.path.normcase(path2))
        outpath = os.path.normpath(outpath)
        return outpath

    @staticmethod
    def upperpath(path1):
        """ Returns path1 upper directory."""
        return os.path.split(path1)[0]

    @staticmethod
    def lastpathname(path1):
        """ Returns path1 last name. Which will be a filename or an empty String."""
        return os.path.split(path1)[1]

    @staticmethod
    def exists(path1):
        # This is just to avoid a class importing both os.path and this file. Making it easier to read through.
        """ Returns True if path1 is an existing path file."""
        return os.path.lexists(path1)

    def __repr__(self):
        saida = f"{self.__inputlocation__}    {os.path.isdir(self.__inputlocation__)}\n"
        saida += f"{self.__outputlocation__}    {os.path.isdir(self.__outputlocation__)}"
        return saida

    def getinputpath(self):
        """
            Returns: What should be the Input file of 2020ASSEditor project.
        """
        return self.__inputlocation__

    def getoutputpath(self):
        """
            Returns: What should be the output file of 2020ASSEditor project.
        """
        return self.__outputlocation__


if __name__ == "__main__":
    # thisplace = FileManagement.upperpath(f"{__file__}")
    # thisplace = FileManagement.upperpath(thisplace)
    # thisplace = FileManagement.upperpath(thisplace)
    # thisplace = FileManagement.connectpath(thisplace, "Testing//")
    # for _ in range(2):
    #     thisplace = os.path.split(thisplace)[0]
    # x = FileManagement(thisplace)
    # print(thisplace)
    # y = os.path.dirname(thisplace)
    # print(y)
    x = FileManagement()
    print(f"{x}")




