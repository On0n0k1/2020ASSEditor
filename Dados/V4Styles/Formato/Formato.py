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


class Formato:
    """ Object that represents 'Format:' from [V4+ Styles] section of the loaded file. Extends Dados.V4Styles.Formato.

    methods:
    __init__(): Constructs the object with no arguments.

    readformat(str): Receives the 'Format:' line from the file (V4+ Styles section) and stores it's values.

    getformat(): returns a string list with all loaded string values.

    gettam(): returns how many format names are stored here."""

    # formattypes:
    # Dict containing the available 'format names' and their order in the text file.
    # Used for loading and saving. Keys are all in lower characters. Values are integers:
    # -1 = not on file.
    # x = position x on formatTypesList[x].
    # the 'format' line can not have values other than these.
    formatTypes = {}

    # formatForPrint:
    # All key values from the dictionary above, but properly capitalized. Used for saving files and printing.
    # E.G:
    # formattype:       formatforprint:
    # primarycolour     primarycolour
    formatForPrint = []

    # tam:
    #   size variable. Indicates how many elements are loaded in V4Styles
    tam = 0

    # formatTypesList:
    # The elements loaded from the text file on their own sequence. Starts with no elements until the file has been
    # read.
    formatTypesList = []

    def gettam(self):
        """ Returns how elements are stored here.

            :return: Integer."""

        return self.tam

    def getformat(self):
        """ Returns a list with the columns for each format type loaded from the text file.

            :return: list containing Strings."""

        saida = []
        for _ in self.formatTypesList:
            # appends the variable names to the list, using proper capital letters
            texto = self.formatForPrint[_.lower()]
            saida.append(f"{texto}")
        return saida

    def setformat(self, newformat):
        """ Copy 'newformat' values to this object.

            Checks 'newformat'. Reset previous values. Copy the new values.

            :param newformat: list of strings.
            :return: self.
            :raise ErrorEditorSSA.ErrorV4Styles_checkFormat2(topico): If there is a duplicate in the list.

            :raise ErrorEditorSSA.ErrorV4Styles_checkFormat1(topico): If the format name is invalid."""

        if isinstance(newformat, list) is False:
            raise TypeError(f"{newformat} has to be a list of strings.")
        for _ in newformat:
            if isinstance(_, str) is False:
                raise TypeError(f"{newformat} must have only string values.")
            if _.lower() in self.formatForPrint is False:
                raise ValueError(f"{_} invalid format value.")

        saida = list(newformat)
        # Clearing empty spaces at start and end of each element.
        for _ in range(len(saida)):
            saida[_] = (saida[_]).strip()

        # reverting any previously loaded values from this object
        for _ in self.formatTypes:
            self.formatTypes[_] = -1
        self.tam = 0
        self.formatTypesList = []

        for _ in saida:
            if self._checkformat(_) is True:
                self.formatTypesList.append(_)
                self.formatTypes[_.lower()] = self.gettam()
                self.tam += 1
        return self

    def getformattypes(self):
        """ returns a dict with the Non-case sensitive format names with the case sensitive ones.

        :return: dict of strings for strings."""

        saida = {}
        for x, y in self.formatForPrint.items():
            saida[f"{x}"] = f"{y}"
        return saida

    def _checkformat(self, topico):
        """ Check if topic exists or is already used on formatTypes.

        Called by self.readFormat()

        :param topico: String.
        :return: True if topico is available to set. False if already set. None if topico doesn't exist."""

        if isinstance(topico, str) is False:
            raise TypeError(f"{topico} must be string.")
        __checking__ = (topico.strip()).lower()
        if __checking__ in self.formatTypes:
            saida = self.formatTypes.get(__checking__)
            if saida == -1:
                return True
            else:
                # error: duplicate format found
                return False
        else:
            # error: format type non-existent
            return None

    def readformat(self, texto):
        """ Receives a 'Format:' line from V4+ Styles section of the loaded file. Save the values on this object.

        Get the resulting list with self.getformat() after this.

        :param texto: String.
        :return: Self."""

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string.")

        if (texto.lower()).startswith("format:"):
            saida = texto[7:].split(",")
        else:
            saida = (texto.split(","))

        # Getting rid of all empty spaces at the start and end of each section of the string list
        for _ in range(len(saida)):
            saida[_] = saida[_].strip()
        
        for _ in saida:
            # if key exists and is not duplicated
            if self._checkformat(_) is True:
                # print(f"_:{_}   tam: {self.getTam()}    List: {self.formatTypesList}    +   {_}")
                self.formatTypesList.append(_)
                self.formatTypes[_.lower()] = self.gettam()
                self.tam += 1
        return self

    def __init__(self):
        """ Creates this object and set it's default values.

        Must read the line afterward with method readformat(str)"""

        # lower characters used for reading the file
        self.formatTypes = {}

        # Capital Characters used for saving the file
        self.formatForPrint = {}

        # the algorithm will read format on a non-case-sensitive method
        # but it will save the files with the proper capital letters
        # formatTypes has lower characters, used for reading files
        # formatForPrint is a dictionary that associates the lower names with the proper names

        # List Used for creating the dictionary
        creatingprintinglist = ["Name", "Fontname", "Fontsize", "PrimaryColour", "SecondaryColour", "OutlineColour"]
        creatingprintinglist.extend(["BackColour", "Bold", "Italic", "Underline", "Strikeout", "ScaleX", "ScaleY"])
        creatingprintinglist.extend(["Spacing", "Angle", "BorderStyle", "Outline", "Shadow", "Alignment", "MarginL"])
        creatingprintinglist.extend(["MarginR", "MarginV", "AlphaLevel", "Encoding"])

        for _ in creatingprintinglist:
            # associating lower characters with printing form
            self.formatForPrint[_.lower()] = _
            # associating lower characters with position on the loaded list (list has not been loaded yet, therefore -1)
            self.formatTypes[f"{_}".lower()] = -1

        self.tam = 0
        self.formatTypesList = []
    
    def __repr__(self):
        """ The string representation of this object.

        Used when saving or printing the object.

        :return: f'Format: ' + all elements in this object + '\n' """

        saida = "Format: "
        x = self.getformat()
        for _ in range(len(x)):
            saida = f"{saida}{x[_]}"
            if _ < len(x)-1:
                saida = f"{saida}, "
        saida = f"{saida}\n"
        return saida


# Testing block
if __name__ == "__main__":
    parametro = "Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
    parametro += "Underline, Strikeout, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
    parametro += "MarginL, MarginR, MarginV, Encoding"
    _ = Formato()
    # try:
    _.readformat(parametro)
    print(_.getformattypes())
    print(_.getformat())
    # except ErrorEditorSSA.ErrorV4Styles_checkFormat1 as e:
    #     print(f"{e}")
    # except ErrorEditorSSA.ErrorV4Styles_checkFormat2 as e:
    #     print(f"{e}")
