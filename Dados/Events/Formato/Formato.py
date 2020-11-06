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

from Dados.ErrorPackage import ErrorPackage
from Dados.SimpleLine.SimpleLine import SimpleLine


class Formato:
    """ Stores the values from the Line 'Format: ' found at the start of '[Events]' section.

        Methods:
            readFormat(texto):
                texto is string. texto is the 'Format:' line on the ssa text file
                This is the main loading method. Stores all the values in self.listaTipos.
            getFormat():
                returns the string list with every loaded Format on the proper order.
            setformat(*args):
                set this object's values to the list strings.

        Constraints:
            There are 10 columns to be read. The last one has to be 'Text', but all the others may have varied order.

            The order chosen for the loaded text file needs to be maintained.

            The code will not load the file in a case sensitive manner. But the saved file will have proper
            capitalization.

            'Marked' or 'Layer' occupy the same column. These behave differently from one another, and which is used
            depends on the user."""

    @staticmethod
    def gettiposdisponiveis():
        """ Returns what strings format can use.

            Used by this object and each individual event to know how to name it's values.

            :return: ["Layer", "Marked", "Start", "End", "Style", "Name", "MarginL", "MarginR", "MarginV", "Effect",
                "Text"]"""
        return ["Layer", "Marked", "Start", "End", "Style", "Name", "MarginL", "MarginR", "MarginV", "Effect", "Text"]

    def __init__(self, arg=None):
        """ Start the instance empty or as a Formato copy.

            :param arg: instance of this class from 'Dados.Events.Formato.Formato.Formato' or String to read."""

        self.listaTipos = []
        self.tiposDisponiveis = self.gettiposdisponiveis()

        if isinstance(arg, Formato):
            # assert , f"{copy} has to be another instance of this object if used as argument."
            self.setformat(arg.getformat())
        elif isinstance(arg, str) or isinstance(arg, SimpleLine):
            self.readformat(arg)
        else:
            raise TypeError

    def __repr__(self):
        """ String representation of this object. On the same format as the text files. Used for saving.

        :return: 'Format' line with the columns in stored order."""

        saida = "Format: "
        x = self.getformat()
        for _ in range(len(x)):
            saida = f"{saida}{x[_]}"
            if _ < len(x)-1:
                saida += ", "
        saida += "\n"
        return saida

    def __checkcolumns(self, lista):
        """ Check the list to see if it fulfills all the requirements for 'Format' section.

            Used by readFormat

            :param lista: string list with 10 elements. Not case-sensitive. Last element has to be 'Text'. All the other
            9 columns can be in any order, but they have to be ["Layer" or "Marked", "Start", "End", "Style", "Name",
            "MarginL", "MarginR", "MarginV", "Effect"]. "Layer" and "Marked" can replace one another, but these cannot
            be together in the same list."""

        if isinstance(lista, list) is False:
            raise TypeError(f"{lista} has to be a list.")
        if len(lista) != 10:
            raise ValueError(f"{lista} must have 10 columns")
        # assert(isinstance(lista, type([]))), f"lista parameter must be a list"
        # assert(len(lista) == 10), f"lista must have 10 columns"
        errorlista = []
        # Regarding 'self.tiposDisponiveis',
        # Layer and Marked happens on the same column.
        # if there is 'layer', 'marked' won't show up, and viceversa.
        # Therefore 'self.tiposDisponiveis' is a list with 11 elements. While 'lista' is a list with 10 elements.

        for _ in lista:
            # searching for 'Layer'
            if self.tiposDisponiveis[0].lower() == _.lower():
                break
        else:
            # if 'Layer' wasn't found, searching for 'Marked'
            for _ in lista:
                if self.tiposDisponiveis[1].lower() == _.lower():
                    break
            else:
                # If none of the two are present on the line, add to the error list
                errorlista.append("Layer Or Marked")
        
        # repeat the search for all the remaining required values"""
        for _ in range(2, len(self.tiposDisponiveis)-1):
            for x in lista:
                if x.lower() == self.tiposDisponiveis[_].lower():
                    break
            else:
                # Didn't find this column in the list
                errorlista.append(f"{self.tiposDisponiveis[_]}")

        # Raising the errors, if any occurred.
        if len(errorlista) > 0:
            raise ValueError(f"{errorlista} <- These columns are missing from format.")
            # raise ErrorEditorSSA.ErrorEvents_Formato_checkColumn(f"{errorlista}")

        # Last column has to be 'Text'
        if lista[9].lower() != self.tiposDisponiveis[10].lower():
            raise ValueError(f"{lista[9]} last element has to be 'Text'.")
            # raise ErrorEditorSSA.ErrorEvents_Formato_checkColumn2(f"{lista[9]}")
        
        return True

    def readformat(self, texto):
        """ Process a 'Format: ' line into this object.

            Receive the line 'Format:' found in '[Events]' section of the SSA file, check if the line is readable, and
            save it in this object. Use self.getFormat() to retrieve the result.

            :param texto: String or SimpleLine. The 'Format: ' line to be read.
            :return: self."""

        if isinstance(texto, SimpleLine):
            if ((texto.gettipo()).strip()).lower() != "format":
                raise ValueError(f"{((texto.gettipo()).strip()).lower()} 'Tipo' must be 'format' (case not sensitive)")
            return self.readformat(texto.gettexto())
        else:
            if isinstance(texto, str) is False:
                raise TypeError(f"{texto} has to be a string.")

            linha = f"{texto}"

            # If line starts with 'Format:', cuts it out from the string.
            if(linha.lower()).startswith("Format:".lower()):
                linha = f"{texto}"[7:]
            lista = linha.split(",")

            # Number of columns has to be 10 ('marked' and 'layer' swap within a single column)
            if len(lista) != 10:
                raise ValueError(f"Columns have to be 10 ({len(lista)})")
                # raise ErrorEditorSSA.ErrorEvents_Formato_readFormat(f"columns: {len(lista)}")

            # Cleaning empty spaces on start/end of each fragment
            for _ in range(len(lista)):
                lista[_] = lista[_].strip()

            # Checking for errors and raising them.
            if self.__checkcolumns(lista):
                # Using the properly capitalized values (self.tiposDisponiveis) to the final list.
                for _ in lista:
                    for x in self.tiposDisponiveis:
                        if _.lower() == x.lower():
                            self.listaTipos.append(f"{x}")
                            break
                    else:
                        # Gonna make this properly raise an error when the object has been finished.
                        # print(f"{_} from {lista} doesnt match with {self.tiposDisponiveis}")
                        raise ValueError(f"{_} Invalid Column.")
                        # raise ErrorEditorSSA.ErrorEvents_Formato_readFormat2(f"{_}")
        return self
                
    def getformat(self):
        """ Get a string list with the stored values in it's loaded order.

            :return: String list. Length 10. [] if it wasn't set.
            :raises ErrorPackage.Formatogeterror: When format is not set or invalid."""

        if isinstance(self.listaTipos, list) is False:
            raise ErrorPackage.Formatogeterror(f"{self.listaTipos}#WRONG TYPE({type(self.listaTipos)})")
        if len(self.listaTipos) != 10:
            raise ErrorPackage.Formatogeterror(f"{self.listaTipos}#WRONG SIZE({len(self.listaTipos)})")
        # assert(len(self.listaTipos) == 10), f"{self.listaTipos}Stored format wasn't loaded or is invalid"

        saida = []
        for _ in self.listaTipos:
            saida.append(f"{_}")
        return saida

    def setformat(self, args):
        """ Set this object's format to the list given.

            :param args: list with 10 string elements.
            :return: self."""

        if isinstance(args, list) is False:
            raise TypeError(f"{args} has to be a list.")
        # assert isinstance(args, list), f"{args} has to be a list."
        for _ in args:
            if isinstance(_, str) is False:
                checking = [isinstance(__, str) for __ in args]
                raise TypeError(f"{args} all elements from the list must be string. Results: {checking}")

        # for _ in args:
        #     assert isinstance(_, str), f"{args} all elements from the list must be string."

        # checkcolumns is what raises all the exceptions
        if self.__checkcolumns(args):
            self.listaTipos = []
            for _ in args:
                self.listaTipos.append(f"{_}")
        return self


# test

# if __name__ == "__main__":
#     x = Formato().readformat(" Start,  Style,End, Name, MarginL, MarginR, MarginV,Layer, Effect, Text")
#     print(x)
