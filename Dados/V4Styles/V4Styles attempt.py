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


# Reminder: The only uses this object has for v4styles are the methods readline, __str__ and __repr__
# Time to rewrite the whole module

from typing import Union, List
from Dados.SimpleLine.SimpleLine import SimpleLine


class V4Styles:
    def __init__(self, v4stylescopy: Union[None, 'V4Styles'] = None, copyreference: bool = False):
        """ Constructs empty V4Styles.

        :param v4stylescopy: optional V4Styles instance to copy.
        :param copyreference: If true. Stored values will be references from the v4stylecopy instance.
        """

        # Need to remember to add the copy case as well
        if v4stylescopy is not None:
            if isinstance(v4stylescopy, V4Styles) is False:
                raise TypeError(f"Argument v4stylescopy has to be a V4Styles instance or omitted. Currently it is "
                                + f"{v4stylescopy} of type {type(v4stylescopy)}.")

        self.lines = []
        self.formatline = None

        # If you want to store every single available line,
        # instead of just those in the format "type: text", make storeall = True
        self.storeall = False

        # Make unformatted print ('__str__') all lines, including invalid ones
        self.sprintall = False
        # Make formatted print ('__repr__') all lines, including invalid ones
        self.rprintall = False

        if v4stylescopy is not None:
            self.setformato(v4stylescopy.getformato(copyreference))
            self.setlines(v4stylescopy.getlines(copyreference), copyreference)

    def __str__(self) -> str:
        """ Print unformatted version of this instance.

        Used for debugging. Will also print the index of the line.

        :return: String.
        """

        saida = ""
        if self.formatline is not None:
            saida = f"{self.formatline!s}\n"
        for _ in range(len(self.lines)):
            __ = self.lines[_]
            if isinstance(__, SimpleLine):
                if self.sprintall:
                    saida = f"{saida}({_}){__!s}\n"
            if isinstance(__, Estilo):
                saida = f"{saida}({_}){__!s}\n"
        return saida

    def __repr__(self) -> str:
        """ Print formatted version of this instance.

        Used for saving.

        :return: String.
        """

        saida = ""
        if self.formatline is not None:
            saida = f"{self.formatline!r}\n"
        for _ in self.lines:
            if isinstance(_, SimpleLine):
                if self.rprintall:
                    saida = f"{saida}{_!r}\n"
            if isinstance(_, Estilo):
                saida = f"{saida}{_!r}\n"
        return saida

    def readline(self, line: Union[str, SimpleLine]) -> 'V4Styles':
        """ Read the line given, store the value then return itself. Method is not case-sensitive.

        :param line: String or SimpleLine. Only lines that start with 'format:' or 'style:' are considered valid.
        :returns: self
        """

        if (isinstance(line, str) or isinstance(line, SimpleLine) or line is not None) is False:
            raise TypeError(f"{line} type ({type(line)}) is not compatible with V4Styles")
        newline = SimpleLine(line)
        # if line read isn't in the format '{type}: {text}'
        if newline.gettipo() is None:
            # It will store if set beforehand
            if self.storeall:
                self.lines.append(newline)
            return self

        # if line read starts with 'Format:'
        if (newline.gettipo().strip()).lower() == "format":
            # self.lines.append(Formato(newline))
            newline = Formato(newline)
            self.formatline = newline

            # run through all the Estilos previously read and tell them what is this file's format
            self.lines = [_.setformato(newline) if isinstance(_, Estilo) else _ for _ in self.lines]
            return self

        # if line starts with 'Style:'
        if (newline.gettipo().strip()).lower() == "style":
            if self.formatline is not None:
                self.lines.append(Estilo(newline, self.formatline))
            else:
                self.lines.append(Estilo(newline))
            return self

        # Won't do anything if it is a line in the format '{type}:{text}' if type is not format or style
        # self.lines.append(newline)
        return self

    def isstoreall(self) -> bool:
        """ Tells instance to store invalid lines. Default value is False."""
        if isinstance(self.storeall, bool) is False:
            raise TypeError(f"Something changed formatline to a value other than boolean: {self.storeall}"
                            + f"{type(self.storeall)}")
        return self.storeall

    def issprintall(self) -> bool:
        """ Tells instance to f'unformatted print!s' (__str__) invalid lines. Default value is False."""
        if isinstance(self.sprintall, bool) is False:
            raise TypeError(f"Something changed sprintall to a value other than boolean: {self.sprintall}"
                            + f"{type(self.sprintall)}")
        return self.sprintall

    def isrprintall(self) -> bool:
        """ Tells instance to f'formatted print!r' (__repr__) invalid lines. Default values is False."""
        if isinstance(self.rprintall, bool) is False:
            raise TypeError(f"Something changed rprintall to a value other than boolean: {self.rprintall}"
                            + f"{type(self.rprintall)}")
        return self.rprintall

    def getformato(self, copyreference: bool = True) -> Union['Formato', None]:
        """ Return Styles format. Or None if it wasn't loaded.

        :param copyreference: if set to True, returns a reference for the instance. Else, returns a copy of the object.
        :return: Formato instance, or None if it isn't set.
        """

        if self.formatline is not None:
            if not copyreference:
                return Formato(self.formatline)
            return self.formatline
        return None

    def getline(self, pos: int, copyreference: bool = True) -> Union["Estilo", SimpleLine, None]:
        """ Retrieve a reference for a line from this instance's style list.

        If invalid lines are enabled ('storeall'), they can be disabled completely by calling the method
        'clearinvalidlines'

        :param pos: index to retrieve.
        :param copyreference: if set to True. Returns a reference of the object, instead of a copy.
        :return: Estilo instance mostly. If storeall = True, may also include invalid SimpleLine instances. None if
        index is invalid.
        """
        if isinstance(pos, int) is False:
            raise TypeError(f"Argument 'pos' has to be int. Currently it is {pos} of type {type(pos)}")
        if (pos < 0) or (pos >= len(self.lines)):
            return None
        if (isinstance(self.lines[pos], Estilo) or isinstance(self.lines[pos], SimpleLine)) is False:
            raise TypeError(f"Value found wasn't Estilo or SimpleLine somehow. Value in {pos} is {self.lines[pos]} of "
                            + f"type {type(self.lines[pos])}")

        if copyreference is False:
            if isinstance(self.lines[pos], SimpleLine):
                return SimpleLine(self.lines[pos])
            elif isinstance(self.lines[pos], Estilo):
                return Estilo(self.lines[pos])

        return self.lines[pos]

    def getlines(self, copyreference: bool = True) -> List[Union['Estilo', SimpleLine]]:
        """ Returns a reference to this instance's list.

        If invalid lines are enabled ('storeall'), they can be disabled completely by calling the method
        'clearinvalidlines'

        :param copyreference: if set to True, returns a reference to the object. Else returns a copy of the object.
        :return reference to a list of Estilo and SimpleLine instances.
        """

        __ = []
        if not copyreference:
            for _ in self.lines:
                if isinstance(_, SimpleLine):
                    __.append(SimpleLine(_))
                if isinstance(_, Estilo):
                    __.append(Estilo(_))
            return __
        return self.lines

    def setstoreall(self, arg: bool) -> 'V4Styles':
        """ Tells instance to store invalid lines. Default value is False."""

        if isinstance(arg, bool) is False:
            raise TypeError(f"arg can only be a boolean. Currently is {arg} of type {type(arg)}")
        self.storeall = arg
        return self

    def setsprintall(self, arg: bool) -> 'V4Styles':
        """ Tells instance to f'unformatted print!s' (__str__) invalid lines. Default value is False."""

        if isinstance(arg, bool) is False:
            raise TypeError(f"arg can only be a boolean. Currently is {arg} of type {type(arg)}")
        self.sprintall = arg
        return self

    def setrprintall(self, arg: bool) -> 'V4Styles':
        """ Tells instance to f'formatted print!r' (__repr__) invalid lines. Default value is False."""

        if isinstance(arg, bool) is False:
            raise TypeError(f"arg can only be a boolean. Currently is {arg} of type {type(arg)}")
        self.rprintall = arg
        return self

    def clearinvalidlines(self) -> 'V4Styles':
        """ Clear all lines that aren't recognized by the object.

        Doesn't need to be called if self.storeall is False. Which is the default.

        Also tells the object to stop storing and printing invalid lines.

        :return: self
        """

        # This should seen as a set for multiple values
        self.lines = [_ for _ in self.lines if isinstance(_, Estilo)]
        self.storeall, self.sprintall, self.rprintall = False, False, False
        return self

    def setformato(self, formato: Union['Formato', str, None]) -> 'V4Styles':
        """ Set Style's format.

        :param formato: Formato instance or a String for it to read. None erases stored value.
        :return: self
        """

        if formato is None:
            self.formatline = None
            return self
        elif (isinstance(formato, Formato) or isinstance(formato, str)) is False:
            raise TypeError(f"Argument formato has to be a Formato instance, String or None. Currently it is {formato} "
                            + f"of type {type(formato)}.")
        # Creating a copy of the instance to avoid storing a reference.
        self.formatline = Formato(formato)
        return self

    def setline(self, newline: Union['Estilo', str, SimpleLine], pos: Union[int, None] = None) -> 'V4Styles':
        """ Replace the specific line with newline.

        If 'storeall' was set to true. The invalid SimpleLine lines can be cleared with the method 'clearinvalidlines'.

        :param newline: Estilo instance for copying. String or SimpleLine to attempt to read.
        :param pos: index to set the value. If not given, or if it is larger than the length of the list, method will
            append instead. Negative will still raise ValueError.
        :return: self.
        """

        if True not in {isinstance(newline, _) for _ in (Estilo, str, SimpleLine)}:
            raise TypeError(f"'newline' has to be Estilo, String or SimpleLine. Currently it is  {newline} of type "
                            + f"{type(newline)}")
        if pos is not None:
            if isinstance(pos, int) is False:
                raise TypeError(f"'pos' must be an integer or omitted. Currently it is {pos} of type {type(pos)}")

        if pos < 0:
            raise ValueError(f"Index pos is currently negative: ({pos}).")

        line = Estilo(newline)
        if pos is None:
            self.lines.append(line)
        else:
            if pos >= len(self.lines):
                self.lines.append(line)
            else:
                self.lines[pos] = line

        return self

    def setlines(self, newlines: List[Union['Estilo', SimpleLine, str]], copyreference: bool = False,
                 useformat: bool = False) -> 'V4Styles':
        """ Replace all the lines stored with the given list.

        :param newlines: the list to set. It may have Estilo, SimpleLine or String instances.
        :param copyreference: default False. If True, it will store the references, not copies of the objects. Not
            recommended.
        :param useformat: default False. If True, it will set each event to the stored format. If False, it must be set
            later.
        :return: self
        """

        if isinstance(newlines, list) is False:
            raise TypeError(f"'newlines' has to be a list with 'Estilo', 'String' or 'SimpleLine' values. Currently it "
                            + f"is {newlines} of type {type(newlines)}")
        for _ in newlines:
            if True not in {isinstance(_, __) for __ in (Estilo, SimpleLine, str)}:
                # set doesn't have duplicates. So this set comprehension will have one class of each type.
                __typesfound = {type(___) for ___ in newlines}
                raise TypeError(f"'newlines' has to be a list with 'Estilo', 'SimpleLine' or str instances. Currently,"
                                + f" it is {newlines} and contain these classes{__typesfound}.")

        # validating args done, time for the actual copy
        self.lines = []
        for _ in newlines:
            if copyreference:
                # Append the reference only.
                self.lines.append(_)
            else:
                if isinstance(_, SimpleLine) or isinstance(_, str):
                    self.readline(_)
                if isinstance(_, Estilo):
                    self.lines.append(Estilo(_))
        if useformat:
            if self.formatline is None:
                raise ValueError(f"Tried to use format when it's not read yet.")
            for _ in self.lines:
                if isinstance(_, Estilo):
                    # Giving each 'Estilo' a reference to format so they can track changes.
                    _.setformato(self.formatline)
        return self


# These 2 classes are here just to help me remember what is essential for them. They will get their own modules soon.
class Estilo:
    def __init__(self, line: Union['Estilo', str, SimpleLine] = None, formato: 'Formato' = None):
        pass

    @staticmethod
    def readline(line: Union[str, SimpleLine]):
        pass

    def setformato(self, arg: 'Formato') -> 'Estilo':
        """ Used for printing.

        So Estilo knows in what order should it prints it's values.

        :param arg:
        :return:
        """
        return self


class Formato:
    def __init__(self, line: Union[str, SimpleLine, 'Formato']):
        if (isinstance(line, str) or isinstance(line, SimpleLine) or (line, Formato)) is False:
            raise TypeError(f"Argument has to be a string, 'SimpleLine' instance or another 'Formato' instance.")
        self.cols = []

    def readline(self, line: Union[str, SimpleLine]):
        pass
