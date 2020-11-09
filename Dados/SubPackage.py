#!/usr/bin/env python3
"""
Extends 2020ASSEditor. Contains all the Data that will be stored about the SSA file.

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

import os

# Own Modules
from Dados.ScriptInfo.ScriptInfo import ScriptInfo
from Dados.V4Styles.V4Styles import V4Styles
from Dados.Events.Events import Events
from Dados.SimpleLine.SimpleLine import SimpleLine

# Search for Epydoc, MIT LICENSE, Python Packages, PEP 0440 and RestructuredText
# Reminder: The only uses this object has for v4styles are the methods readline, __str__ and __repr__
# Time to rewrite the whole module


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.2.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class SubPackage:
    def __init__(self) -> None:
        self.scriptinfo = ScriptInfo()
        self.v4styles = V4Styles()
        self.events = Events()

        self.__defaulttitles__ = [f"{_}" for _ in SimpleLine().__defaulttitles__]
        self.__lowertitles__ = [f"{_}" for _ in SimpleLine().__lowertitles__]
        self.__readers__ = (self.scriptinfo.readline, self.v4styles.readline, self.events.readline)

        self.__readerpos__ = None

    def __repr__(self) -> str:
        """ Called when printing the formatted version of this object.

        Used for saving. Called with f'{NAME!r}'

        :return: String.
        """
        return f"{self.scriptinfo!r}\n{self.v4styles!r}\n{self.events!r}\n"

    # Must change this later to check for absolute paths instead of just strings
    def savefile(self, arg: str, overwrite: bool = False) -> bool:
        """ Save file into location 'arg'.

        :param arg: String. File Path to save. Will not replace existing file. Unless overwrite == True.
        :param overwrite: Forces method to overwrite existing file.
        :return: True if Save was successful. False if file already exists.
        """

        if isinstance(arg, str) is False:
            raise TypeError(f"{arg} must be a file address (String).")
        try:
            with open(arg, "x") as f:
                f.write(f"{self!r}")
                return True
        except FileExistsError:
            if overwrite:
                if os.path.exists(arg):
                    os.remove(arg)

                    with open(arg, "x") as f:
                        f.write(f"{self!r}")
                        return True
                else:
                    raise ValueError(f"File exists, but file doesn't exist. This exception shouldn't ever happen...")
            else:
                return False

    def __str__(self) -> str:
        """ Unformatted string Version of the file.

        Used for checking what lines to edit. Called with f'{NAME!s}'

        :return: String.
        """

        return f"{self.scriptinfo!s}\n{self.v4styles!s}\n{self.events!s}\n"

    # Must change this later to check for absolute paths instead of just strings
    def loadfile(self, arg: str) -> 'SubPackage':
        """ Load an SSA text file into this object.

        :param arg: String. Local Address of file.
        :return: self.
        """

        if isinstance(arg, str) is False:
            raise TypeError(f"{arg} must be a file address (String).")
        try:
            with open(arg, "r") as f:
                for _ in f:

                    __line = SimpleLine(_)
                    __linelower = f"{__line}".lower()
                    __checking__ = [__ in __linelower for __ in self.__lowertitles__]
                    if True in __checking__:
                        self.__readerpos__ = __checking__.index(True)
                    else:
                        if self.__readerpos__ is not None:
                            # Call the reading function for the current section
                            (self.__readers__[self.__readerpos__])(__line)

        except FileNotFoundError:
            raise ValueError(f"{arg} file could not be found.")
        return self
