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

from typing import Union


class SimpleLine:
    """ A single line of the text file.

    Used in Script_Info. Also used when reading the file.

    Used for treating strings formatted as f'{tipo}: {texto}'

    If read string is not in that format, {tipo} will be None, and {texto} will be the whole line.

    'posicao' is an optional attribute that could be used for tracking it's index in a list, for instance.

    Methods:

        processarlinha: read a line and store the value

        __repr__: this object as a formatted string. Used for saving.

        __init__: construct this object with no args, another SimpleLine or a string to read.

        gettipo: returns tipo as string or None.

        gettexto: returns texto as string.

        getposicao: returns posicao as integer.

        settipo: set tipo with a string or None.

        settexto: set texto with a string.

        setposicao: set posicao with an integer.
    """

    def __init__(self, texto: Union[None, 'SimpleLine', str] = None, posicao: Union[None, int] = None, speaking: bool
                 = False):
        """ Starts the object with a line from the text file. Formatted as f'{tipo}: {texto}'.

        :param texto: String or SimpleLine. The line loaded from the file. If it is undeclared. This object will be
        f'{tipo}: {texto}' and position = 0.

        :param posicao: Integer. Position of the line. Used when saving the file. If it is undeclared, posicao = 0.

        :param speaking: Boolean. Used for debugging. Tells processarLinha to print what it is reading.
        """

        if (isinstance(texto, SimpleLine) or isinstance(texto, str) or (texto is None)) is False:
            raise TypeError(f"Invalid type for texto: {texto}({type(texto)})")
        if ((posicao is None) or isinstance(posicao, int)) is False:
            raise TypeError(f"Invalid type for posicao: {posicao}({type(posicao)})")
        if isinstance(speaking, bool) is False:
            raise TypeError(f"Invalid type for speaking: {speaking}({type(speaking)})")

        self.posicao, self.tipo, self.texto = 0, None, ""

        self.__defaulttitles__ = ("[Script Info]", "[V4+ Styles]", "[Events]")
        self.__lowertitles__ = (_.lower() for _ in self.__defaulttitles__)
        if texto is None:
            self.setposicao(0)
            self.settipo(None)
            self.settexto("")
        elif isinstance(texto, SimpleLine):
            self.setposicao(texto.getposicao())
            self.settipo(texto.gettipo())
            self.settexto(texto.gettexto())
        else:
            if isinstance(texto, str) is False:
                raise TypeError(f"{texto} must be string or omitted")
            if posicao is None:
                self.setposicao(0)
                self.processarlinha(f"{texto}")
            else:
                if isinstance(posicao, int) is False:
                    TypeError(f"{posicao} must be int or omitted")
                self.setposicao(posicao)
                self.processarlinha(f"{texto}", speaking)

    def __repr__(self) -> str:
        """Prints the line in the same format it can be found in a SSA file.

        Used when saving. Can be called with f'{NAME!r}'

        :return: if tipo is not None (therefore comment), return f"{tipo}: {texto}" else f"{texto}"
        """

        if self.tipo is None:
            return f"{self.texto}"
        else:
            return f"{self.tipo}: {self.texto}"

    def processarlinha(self, texto: str, speaking: bool = False) -> 'SimpleLine':
        """ Read a line and assign it's values to this object. Called by the constructor. Position isn't set here.

        :param texto: string. The line to be read. Formatted as f'{tipo}: {texto}'
        :param speaking: Boolean. Debugging parameter. The method prints what it is reading in the output.
        :return: self.

        comments are SimpleLine with tipo = 'null' values.

        tipo is None when:
            -starts with ';'

            -starts with '!:'

            -starts with 'comment:'

        If speaking == true, Print f"[{self.getPosicao()}]{self.getTipo()}: {self.getTexto()}"
        """

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string value.")

        texto = texto.strip()
        if texto.startswith(";"):
            self.settipo(None)
            self.settexto(texto)
        else:
            checking = [(_ in texto.lower()) for _ in self.__lowertitles__]
            if True in checking:
                self.settipo(None)
                self.settexto(self.__defaulttitles__[checking.index(True)])
            else:
                chop = texto.split(":", 1)
                # Strip() will clear out every empty space at the start/end of each string
                chop = [_.strip() for _ in chop]
                if(len(chop) == 1) or (chop[0] == "!") or (chop[0].lower() == "comment"):
                    self.settipo(None)
                    self.settexto(texto)
                else:
                    # Sets the first index from list to tipo from saida,
                    # Sets the second index from list to texto from saida
                    self.settipo(chop[0])
                    self.settexto(chop[1].strip())

        if speaking:
            # For Debugging. Prints what it read.
            print(f"[{self.getposicao()}]{self.gettipo()}: {self.gettexto()}")
        return self

    def gettipo(self) -> str:
        """ Return tipo. From the format f'{tipo}: {texto}'

        :return: String tipo
        """

        return self.tipo

    def gettexto(self) -> str:
        """ Return texto. From the format f'{tipo}: {texto}'

        :return: String texto
        """

        return self.texto

    def getposicao(self) -> int:
        """ Return posicao. The position of this line in the text file.

        :return: Integer posicao
        """

        return self.posicao

    def setposicao(self, posicao: int) -> 'SimpleLine':
        """ Set posicao. The position of this line in the text file

        :param posicao: Integer
        :return: self
        """

        if isinstance(posicao, int) is False:
            raise TypeError(f"{posicao} must be an integer")

        self.posicao = posicao
        return self

    def settipo(self, tipo: Union[str, None]) -> 'SimpleLine':
        """ Set tipo.

        From the format f'{tipo}: {texto}'.

        :param tipo: String
        :return: self
        """

        if tipo is None:
            self.tipo = None
            return self
        if isinstance(tipo, str) is False:
            raise TypeError(f"{tipo} must be a string or None")

        self.tipo = tipo
        return self
    
    def settexto(self, texto: str) -> 'SimpleLine':
        """ Set Texto. From the format f'{tipo}: {texto}'.

        :param texto: String
        :return: self
        """

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string")
        self.texto = texto
        return self


# debugging
if __name__ == "__main__":
    x = [
            "[script info]",
            "; Script generated by Aegisub 2.1.9",
            "; http://www.aegisub.org/",
            "Title: Default Aegisub file",
            "ScriptType: v4.00+",
            "WrapStyle: 0",
            "PlayResX: 1280",
            "PlayResY: 720",
            "ScaledBorderAndShadow: yes",
            "Video Aspect Ratio: 0",
            "Video Zoom: 6",
            "Video Position: 3640",
            "Video File: jorg-01-premux-7cdb5f6a.mkv",
            "Last Style Storage: Default",
            "Audio File: ?video",
            "Keyframes File: jorg-01-keyframes.txt]"]

    potato = []
    for _ in x:
        potato.append(SimpleLine(_))
    for _ in potato:
        """saida+=f"{_}"""
        print(f"({_})" + "       --------tipo: " + f"({_.gettipo()})    ------Texto: ({_.gettexto()})")
