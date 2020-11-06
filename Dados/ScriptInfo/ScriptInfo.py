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

from Dados.SimpleLine.SimpleLine import SimpleLine
# from Dados.ErrorEditorSSA import ErrorEditorSSA


class ScriptInfo:
    """ Stores and prints all the data loaded from the [Script Info] section of the sub file.

        Subclass of Dados. Imports SimpleLine. Text format: f"{tipo}: {texto}".

        Methods(args):
            __init__(): Creates an empty object of this class.

            __repr__(): Prints all the data stored in this object in the same format as the loaded file.

            readline(linha):  Reads the values from the text line loaded from the [Script Info] section
            of the loaded file. linha is SimpleLine.

            gettexto(titulo): titulo is string. Get the value stored with name 'titulo'.

            getvaluelist(): returns a SimpleLine list with all stored values.

            gettipos(): returns a String list with all stored 'tipo' values.

            gettextolist(): returns a String list with all stored 'texto' values.

        Developer comment:
        I couldn't find every possible information that can be stored here.
        So this is just a bin to keep every single line to be edited or loaded.
        Not sure about what values these are and what they do. Recognize a few but not all."""

    def __init__(self):
        """ Constructs the object. Doesn't do anything other than that."""
        self.linelist = []

    def __repr__(self):
        """ The formatted string representation of the object.

            First line is '[Script Info]'.

            Following lines are f'{tipo}: {texto}'.

            :return: String."""

        saida = f"[Script Info]\n"
        for _ in self.linelist:
            saida = f"{saida}{_}\n"
        return saida

    # Not sure how to properly implement more than 1 string representation, gonna study it more later...
    def __str__(self):
        """ Return unformatted string version of this object.

            Used for checking which values to edit.

            :return: String."""
        saida = f"[Script Info]\n"
        for _ in range(len(self.linelist)):
            saida = f"{saida}({_}) - {self.linelist[_]}\n"
        return saida

    def readline(self, linha):
        """ Read the values from the text line loaded from the [Script Info] section of the loaded file.

            :param linha: SimpleLine object to be read. (Linha.gettipo() is None) means that line is a comment.
            :return: self."""

        if (isinstance(linha, SimpleLine) or isinstance(linha, str)) is False:
            raise TypeError(f"{linha} has to be SimpleLine or String.")

        newlinha = SimpleLine(linha)

        if(f"{linha}".strip()).lower() == "[Script Info]".lower():
            pass
        elif newlinha.gettipo() is None:
            pass
        else:
            for _ in range(len(self.linelist)):
                if isinstance(self.linelist[_], SimpleLine):
                    if ((self.linelist[_].gettipo()).strip()).lower() == ((newlinha.gettipo()).strip()).lower():
                        self.linelist[_] = newlinha
                        break
            else:
                self.linelist.append(newlinha)
        return self

    def getline(self, tipo):
        """ Return line with name "tipo".

            :param tipo: String. "tipo" of the object to acquire
            :return: SimpleLine."""

        if isinstance(tipo, str) is False:
            raise TypeError(f"{tipo} has to be String.")

        newline = None
        for _ in self.linelist:
            if isinstance(_, SimpleLine):
                if ((_.gettipo()).strip()).lower() == (tipo.strip()).lower():
                    newline = _
        return newline

    def gettexto(self, tipo):
        """ Returns the value with name 'tipo'.

            :param tipo: String.
            :return: String if found. None if not found."""
        if isinstance(tipo, str):
            raise TypeError(f"{tipo} has to be a string.")

        newline = self.getline(tipo)
        if newline is None:
            return None
        else:
            return newline.gettexto()

    def getvaluelist(self):
        """ Return a SimpleLine list with all stored values.

            :return: list with 'Dados.SimpleLine' elements."""

        listaderetorno = []
        for _ in self.linelist:
            if isinstance(_, SimpleLine):
                listaderetorno.append(SimpleLine(_))
        return listaderetorno

    def gettipos(self):
        """ Return a string list with all stored 'tipo' values.

            :return: list with String elements."""
        listaderetorno = []
        for _ in self.linelist:
            if isinstance(_, SimpleLine):
                listaderetorno.append(f"{_.gettipo()}")
        return listaderetorno

    def gettextolist(self):
        """ Return a string list with all stored 'texto' values.

            :return: list of string elements."""

        listaderetorno = []
        for _ in self.linelist:
            if isinstance(_, SimpleLine):
                listaderetorno.append(f"{_.gettexto()}")
        return listaderetorno
