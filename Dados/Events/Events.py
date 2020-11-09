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

from typing import Union, List

from Dados.Events.Evento.Evento import Evento
from Dados.Events.Formato.Formato import Formato
from Dados.SimpleLine.SimpleLine import SimpleLine


class Events:

    """
    Format:
        field names can be as follow: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
        The sequence of values may change, but 'Text' must always be the last one

    This will store a single list that will have either SimpleLine or Evento for every loaded Line.
    If the line is a valid event, store it as Evento, otherwise, store it as SimpleLine.
    If the input is a textfile or string, it will have SimpleLines.
    """

    def __init__(self) -> None:
        """ Construct an empty Events instance."""

        # How Events will read "[Events]" Section
        # Add all lines as SimpleLine
        # If it find the "Format" Line, read it
        # After finding the "Format" Line, go back to the start, rechecking all the SimpleLines stored up to this point
        # Replace any SimpleLine that is a valid event with an Evento instance
        # Go all the way to the end of the file, adding the remaining lines

        self.__lines = []
        self.__formato = None

    def __repr__(self) -> str:
        """ Return Events section as a formatted String.

        Used for saving. Called when using the String version of this object. f"{NAME!r}"

        :return: String.
        """

        saida = f"[Events]\n"
        if self.getformat() is not None:
            saida += f"{self.getformat()}"
        for _ in self.__lines:
            saida += f"{_}"
        return saida

    def __str__(self) -> str:
        """ Return unformatted string version of this object.

        Used for checking which values to edit.

        :return: String.
        """

        saida = f"[Events]\n"
        if self.getformat() is not None:
            saida += f"{self.getformat()}"
        for _ in range(len(self.__lines)):
            saida += f"({_}) - {self.__lines[_]}"
        return saida

    def getlen(self) -> int:
        """ :return: The number of lines stored."""
        return len(self.__lines)

    @staticmethod
    def getalleventtypes() -> List[str]:
        """ Return all types of events available.

        Values will be:

        ["dialogue", "comment", "picture", "sound", "movie", "command"]
        """

        return Evento.getalleventtypes()

    def __checkline(self, argline: SimpleLine) -> Union[Evento, SimpleLine]:
        """ Checks if argline is a valid event. Returns it as Evento if true. Otherwise, return the same object.

        if format is not set, raise an assert error.

        :param argline: SimpleLine instance.
        :return: SimpleLine instance or Evento instance.
        """

        assert self.__formato is not None, f"Formato is not set."
        if isinstance(argline, SimpleLine) is False:
            raise TypeError(f"{argline} has to be a SimpleLine.")

        if argline.gettipo() is None:
            return argline

        # if the text before the first ":" is an event type
        if ((argline.gettipo()).strip()).lower() in self.getalleventtypes():
            # Create an event, set format, then set event type and values with readevent
            return (Evento().setformato(self.__formato.getformat())).readevent(argline)
        # Just store it as SimpleLine. Treating it as a comment
        return argline

    def readline(self, arg: Union[str, SimpleLine]) -> 'Events':
        """ Read a line and append a "SimpleLine" or an Evento to the list.

        If format is not set, only append "SimpleLine" instances.

        If it finds format, set format, then check previous lines for every valid Evento.

        If format is set, and line is a valid event, it will always append an "Evento" instance.

        :param arg: String or SimpleLine.
        :return: self.
        """

        def comparing(arg1, arg2):
            if arg1 is None:
                if arg2 is None:
                    return True
                return False
            if arg2 is None:
                return False
            if (isinstance(arg1, str) or isinstance(arg2, str)) is False:
                raise TypeError(f"{arg} must be a String")
            return ((arg1.strip()).lower()).startswith(arg2.lower())

        if (isinstance(arg, str) or isinstance(arg, SimpleLine)) is False:
            raise TypeError(f"{arg} must be a SimpleLine or String.")

        __value = SimpleLine(arg)

        if self.getformat() is None:
            # If it starts with:
            if comparing(__value.gettipo(), "format"):
                self.setformat(__value)
                # print(f"{type(self.getformat())}{self.getformat()}")
                replacement = []
                for _ in self.__lines:
                    # Will become Evento if valid.
                    __x__ = self.__checkline(_)
                    if isinstance(__x__, Evento):
                        # Replace all SimpleLine with Evento
                        replacement.append(__x__)

        # check if it starts with any of the valid event types
        if True in {comparing(__value.gettipo(), _) for _ in self.getalleventtypes()}:
            if self.getformat() is not None:
                __x__ = self.__checkline(__value)
                # print(f"__x__ = {__x__}          __value = {__value}")
                # print(f"__x__ = {__x__}          __value = {type(__value)}")
                # print(f"__x__ = {__x__}          type = {type(__x__)}")
                if isinstance(__x__, Evento):
                    self.__lines.append(self.__checkline(__value))
            else:
                self.__lines.append(__value)

        return self

    def getformat(self) -> Union[Formato, None]:
        """ Return Format.

        :return: Formato instance or None.
        """

        if self.__formato is None:
            return None
        return Formato(self.__formato)

    def setformat(self, arg: Union[SimpleLine, Formato]) -> 'Events':
        """ Set format.

        :param arg: String, SimpleLine instance or Formato instance.
        :return: self
        """

        if isinstance(arg, SimpleLine) or isinstance(arg, str) or isinstance(arg, Formato):
            self.__formato = Formato(arg)
        else:
            raise TypeError(f"{arg} must be a SimpleLine, String, or Formato object.")
        return self

    def getlineall(self) -> List[Union[SimpleLine, Evento]]:
        """ Return all lines, "SimpleLine" instances and "Evento"s

        :return: list with "SimpleLine" instances and "Evento" instances.
        """

        if len(self.__lines) == 0:
            return []
        saida = []
        for _ in self.__lines:
            # If formato is None, it will never try to copy an Evento instance to the output
            if isinstance(_, SimpleLine) or isinstance(_, str) or (self.__formato is None):
                saida.append(SimpleLine(_))
            else:
                saida.append(Evento(_))
        return saida

    def getlineevents(self):
        """ Return only Evento instances from the lines.

        :return: list with Evento instances.
        """

        return [Evento(x) for x in self.__lines if isinstance(x, Evento)]

    def clearinvalidlines(self) -> 'Events':
        """ Loop through the list and clear all lines that aren't event lines.

        :return: self.
        """

        self.__lines = self.getlineevents()
        return self

    def setline(self, line: Union[SimpleLine, str, Evento], pos: int) -> 'Events':
        """ Replace a line in position 'pos'.

        :param line: SimpleLine, String or Evento. Line to set.
        :param pos: Integer. Index position to set.
        :return: self.
        """

        if True not in {isinstance(line, _) for _ in [str, SimpleLine, Evento]}:
            raise TypeError(f"{line} has to be string, SimpleLine or Evento.")

        if isinstance(pos, int) is False:
            raise TypeError(f"{pos} has to be an Integer.")

        lista = self.getlineall()
        if len(lista) < pos:
            raise ValueError(f"There is no line in position {pos}.")

        if isinstance(line, Evento):
            if self.__formato is not None:
                __value = Evento(line)
                __value.setformato(self.__formato.getformat())
            else:
                __value = SimpleLine(f"{line}")
            self.__lines[pos] = __value
            return self

        __value = SimpleLine(line)
        if self.__formato is not None:
            # __checkline: Set it as event if valid, else set as SimpleLine
            self.__lines[pos] = self.__checkline(__value)
        else:
            self.__lines[pos] = __value
        return self

    def getline(self, pos: int) -> Union[SimpleLine, Evento]:
        """ Return the line in position pos.

        :param pos: Integer. Index position of line.
        :return: SimpleLine or Evento instance.
        :raise ValueError: If there position is larger than the size stored.
        """

        if isinstance(pos, int) is False:
            raise TypeError(f"{pos} has to be an Integer.")

        if len(self.__lines) <= pos:
            raise ValueError(f"There is no line in position {pos}.")

        return self.__lines[pos]
