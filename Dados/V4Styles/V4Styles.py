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
__version__ = "0.1.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]

from Dados.V4Styles.Formato.Formato import Formato
from Dados.V4Styles.Estilo.Estilo import Estilo
from Dados.SimpleLine.SimpleLine import SimpleLine
# from Dados.ErrorEditorSSA import ErrorEditorSSA
from Dados.ErrorPackage.ErrorPackage import V4stylesgeterror


# Developer Note: I should change getestilolist to create a estilo object instead of returning it's own.
class V4Styles:
    """ Object containing info about the loaded file column format

        Methods:

        readformat(texto) :
            texto is string. Receives the "Format" line read from the text file, section "[V4+ Styles]", and saves each
            column and their order in "formatTypesList" list

            raises "Dados.ErrorEditorSSA.ErrorV4Styles_checkFormat1" if one of the columns has a value not found in
            the formatTypes dictionary

            raises "Dados.ErrorEditorSSA.ErrorV4Styles_checkFormat2" if it read the same value twice. Resulting in
            duplicate column values.

        getformat() :
            returns a list of strings containing each of the columns used by the "Style" objects in their expected
            order. Returns an empty list if there was a file reading issue, or if it wasn't read.

        readline(texto):
            texto is string or SimpleLine. Receives the "Style" line read from the text file, section "[V4+ Styles],
            creates an object "Estilo", with each value and append it to "V4Style" list

        getestilolist():
            returns a V4Style list from this object, called by getEstilo(nome)

            raise ErrorEditorSSA.ErrorV4Styles_Estilo3: if Format is not set before attempting to retrieve the list.

        getestilo(nome):
            nome is string. Returns a V4Style in which f'{name}'==f'{nome}'. (There's no error or replacing for V4Styles
            with the same or no name. Maybe I should change that later...)

            raise Dados.ErrorPackage.V4stylesgeterror: if Format is not set before attempting to retrieve the list.

            """

    Format = Formato()

    def __init__(self, copy=None):
        """ Constructs the object with default values, or copy another V4Styles 'copy' values.

            :param copy: V4Styles object for this constructor to copy. Optional."""

        if copy is None:
            self.Format = Formato()
            self.V4Style = []

        elif isinstance(copy, V4Styles):
            self.Format = Formato().setformat(copy.getformat())
            self.V4Style = []
            for _ in copy.getestilolist():
                self.V4Style.append(Estilo(copy.getformat(), f"{_}"))
        else:
            raise TypeError(f"{copy} must be a Dados.V4Styles.V4Styles or None")

    def __repr__(self):
        """ Return the entire string version of [V4+ Styles] section stored in this object.

            :return: String."""

        _saida = f"[V4+ Styles]\n"
        _saida += f"{self.Format}"
        for _ in self.V4Style:
            _saida += f"{_}"
        _saida += f"\n"
        return _saida

    def __str__(self):
        """ Return unformatted string version of this object.

            Used for checking which values to edit.

            :return: String."""

        _saida = f"[V4+ Styles]\n"
        _saida += f"{self.Format}"
        for _ in range(len(self.V4Style)):
            _saida += f"({_}) - {self.V4Style[_]}"
        _saida += f"\n"
        return _saida

    def getformat(self):
        """ Returns a list of the column names stored in this object.

            :return: List of Strings."""

        return self.Format.getformat()

    def readformat(self, texto):
        """ Receives the "Format" line read from the text file, section "[V4+ Styles]", and saves each column and their
            order in "formatTypesList" list

            :param texto: String
            :return: None"""

        self.Format.readformat(texto)

    V4Style = []

    def readline(self, argline):
        """ Store argline as Estilo if it is valid. SimpleLine if it isn't

            :param argline: String or SimpleLine instance.
            :return: self."""

        if (isinstance(argline, str) or isinstance(argline, SimpleLine)) is False:
            raise TypeError(f"{argline} must be a string or SimpleLine instance.")

        # f"{}" will turn the SimpleLine into a String
        # Until format is read, everything will be stored as SimpleLine instances
        # When format is read, replace the list with only valid events

        novov4style = SimpleLine(argline)
        if len(self.Format.getformat()) == 0:
            if (((novov4style.gettipo()).strip()).lower()).startswith("format"):
                self.readformat(f"{novov4style}")
                replacement = []

                for _ in self.V4Style:
                    if isinstance(_, Estilo):
                        replacement.append(_)
                    elif isinstance(_, SimpleLine):
                        if ((_.gettipo()).lower()).startswith("style"):
                            replacement.append(Estilo(self.getformat(), f"{_}"))
                self.V4Style = replacement
            else:
                self.V4Style.append(novov4style)
        else:
            if novov4style.gettipo() is not None:
                if (((novov4style.gettipo()).strip()).lower()).startswith("style"):
                    novov4style = Estilo(self.getformat(), f"{argline}")
                    self.V4Style.append(novov4style)
        return self

    def getestilolist(self):
        """ Returns a list with every Estilo stored in this object.

            :return: List of 'Dados.V4Styles.Estilo.Estilo' objects."""

        if len(self.getformat()) == 0:
            raise V4stylesgeterror(f"Format = {self.getformat()}   ")

        __saida__ = []
        for _ in self.V4Style:
            if isinstance(_, Estilo):
                __saida__.append(Estilo(self.getformat(), _))
        return __saida__

    def getestilo(self, nome):
        """ Find a V4Style with name == nome, then return it.

            :param nome: string. The V4Style required.
            :return: 'Dados.V4Style.Estilo.Estilo' if object was found. None otherwise."""

        if isinstance(nome, str) is False:
            raise TypeError(f"{nome} has to be a string.")

        if len(self.getformat()) == 0:
            raise V4stylesgeterror(f"Format = {self.getformat()}   ")

        # estilolista = self.getestilolist()
        for _ in self.V4Style:
            if _.getvalue("name") == nome:
                return _
        else:
            return None


# for debugging
if __name__ == "__main__":

    x = V4Styles()
    _ = "Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic,"
    _ += "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL,"
    _ += " MarginR, MarginV, Encoding"
    x.readformat(_)
    _ = "Default,H_Canaan_Main,45,&H00DCDCDC,&H000000FF,&H001D1D1D,&H001E1E1E,0,0,0,0,100,100,0,0,1,2,1,2,100,100,45,1"
    __ = "Title,DEATH FONT ver1.0,70,&H00D7D3D6,&H001D0121,&H0025012A,&H0025012A,0,0,0,0,100,100,0,0,1,0,6,2,10,10,10,1"
    s = [_, __]

    for _ in s:
        x.readline(_)

    print(x)

    teste = x.getformat()
    saida = "Format: "
    for _ in teste:
        saida += f"{_}, "
    print(saida)

    """
    saida = ""
    hhhhh = True

    for _ in x.getestilolist():
        print(f"{_.getformato()}")

        saida = "Style: "
        for testando in _.getvaluelist():
            saida = f"{saida}{testando}, "

        saida = f"{_.getformato()}"
        print(saida)

        saida += f"{_}"
    """
    print(x)
