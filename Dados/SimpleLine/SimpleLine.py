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


class SimpleLine:
    """ A single line of the text file.

        Used in Script_Info. Also used when reading the file."""

    # Position in the text file.
    posicao = 0

    # Argument name. If tipo == f'null', the line will be treated as a comment line.
    tipo = ""

    # Argument value.
    texto = ""

    def __init__(self, texto=None, posicao=None, speaking=False):
        """ Starts the object with a line from the text file. Formatted as f'{tipo}: {texto}'.

        :param texto: String. The line loaded from the file. If it is undeclared. This object will be f'{tipo}: {texto}'
            and position = 0.
        :param posicao: Integer. Position of the line. Used when saving the file. If it is undeclared, posicao = 0.
        :param speaking: Boolean. Used for debugging. Tells processarLinha to print what it is reading."""

        # print(f"texto: ({texto})  posicao: ({posicao})")
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
                if isinstance(posicao, int):
                    TypeError(f"{posicao} must be int or omitted")
                self.setposicao(posicao)
                self.processarlinha(f"{texto}", speaking)

    def __repr__(self):
        """Prints the line in the same format it can be found in a SSA file. Used when saving.

        :return: if tipo=='null', return f"{tipo}: {texto}"
            else f"{texto}" """

        if self.tipo is None:
            return f"{self.texto}"
        else:
            return f"{self.tipo}: {self.texto}"

    def processarlinha(self, texto, speaking=False):
        """ Read a line and assign it's values to this object. Called by the constructor. Position isn't set here.

        :param texto: string. The line to be read. Formatted as f'{tipo}: {texto}'
        :param speaking: Boolean. Debugging parameter. The method prints what it is reading in the output.
        :return: None.

        comments are SimpleLine with tipo = 'null' values.
        tipo is None when:
            -starts with ';'
            -starts with '!:'
            -starts with 'comment:'

        If speaking == true. Print f"[{self.getPosicao()}]{self.getTipo()}: {self.getTexto()}" """

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
                chop = [_.strip() for _ in chop]
                if(len(chop) == 1) or (chop[0] == "!") or (chop[0].lower() == "comment"):
                    self.settipo(None)
                    self.settexto(texto)
                else:
                    # Sets the first index from list to tipo from saida,
                    # Sets the second index from list to texto from saida
                    # Strip() will clear out every empty space at the start/end of each string

                    self.settipo(chop[0])
                    self.settexto(chop[1].strip())

        if speaking:
            # For Debugging. Prints what it read.
            print(f"[{self.getposicao()}]{self.gettipo()}: {self.gettexto()}")

    def gettipo(self):
        """ Return tipo. From the format f'{tipo}: {texto}'

            :return: String tipo"""
        return self.tipo

    def gettexto(self):
        """ Return texto. From the format f'{tipo}: {texto}'

        :return: String texto"""
        return self.texto

    def getposicao(self):
        """ Return posicao. The position of this line in the text file.

        :return: Integer posicao"""
        return self.posicao

    def setposicao(self, posicao):
        """ Set posicao. The position of this line in the text file

        :param posicao: Integer
        :return: self
        """
        if isinstance(posicao, int) is False:
            raise TypeError(f"{posicao} must be an integer")

        self.posicao = posicao
        return self

    def settipo(self, tipo):
        """ Set tipo. From the format f'{tipo}: {texto}'.

        :param tipo: String
        :return: self"""
        if tipo is None:
            self.tipo = None
            return self

        if isinstance(tipo, str) is False:
            raise TypeError(f"{tipo} must be a string or None")

        self.tipo = tipo
        return self
    
    def settexto(self, texto):
        """ Set Texto. From the format f'{tipo}: {texto}'.

        :param texto: String
        :return: self"""
        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string")
        self.texto = texto
        return self


# debugging
if __name__ == "__main__":
    # I used a subtitle file generated by the website aegisub, which is 100x better than myne. Please consider
    # supporting them. I'm only making this project to add to my curriculum. No intention of finishing
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
