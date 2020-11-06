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

# import sys
# if r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA""" in sys.path:
#     pass
# else:
#     sys.path.append(r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA""")
#
# import EditorSSA
# from Dados.ErrorEditorSSA import ErrorEditorSSA
from Dados.ErrorPackage.ErrorPackage import Estilogeterror


class Estilo:
    """ Estilo object represents a single "Style" line found on the text file. Created by 'Dados.V4Styles', used by
    'Dados.Events' and 'Dados.Events.Evento'.

        methods:
            Estilo(colunas, texto): constructor.

            __repr__: used for printing or saving the file. The string format of this object will be 'Style: ' + every
            value from this object + '\n'

            readEstilo(texto): no need to call this method. It is used by the constructor already.
            Receives 'texto' string, split all the ',' and associate all values to this object using setattr.

            getFormato(): returns a list of strings referencing the columns read from the text file. This
            object receives these values through the constructor, no other method for changing them.

            getValue(texto): returns the value with name 'texto'. Raises 2 custom errors to help debugging.
                ErrorV4Styles_Estilo: Format found on list, but value was not assigned
                ErrorV4Styles_Estilo2: value not found on format list

            getValueList(): returns a list with all read values from the constructor. Calls getValue, so it may raise
            the same exceptions."""

    # Formato Contains the list of values/columns this object stores. The values are case-sensitive. So, during
    # comparison, use method .lower() for both values.
    Formato = []

    def getformato(self):
        """ Returns a list with every column of this list.

        If the columns in this object were created invalid. Please make a call for this object again using:

        __init__(colunas, texto): colunas is a list of strings containing every loaded Column from Format Line in
        V4Styles section of the text file.

        :return:
        """
        saida = []
        for _ in self.Formato:
            saida.append(f"{_}")
        return saida

    # colunas = Format string list. Must have been read before creating this object. The number of elements associated
    # in texto will be the same as colunas.
    # texto = String with the elements that must be processed and stored. Values will be stored

    def __init__(self, colunas, texto):
        """ Constructor. Called by 'Dados.V4Styles.V4Styles.V4Styles'.

        :param colunas: list of strings that have the names of each column read in 'Format' line on '[V4+ Styles]'
        section of the text file.
        :param texto: the 'line itself' read from the text file. String, """

        if isinstance(colunas, list) is False:
            raise TypeError(f"{colunas} must be a list.")
        # assert (type(colunas) == list), "formato <- must be a list"
        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string.")
        # assert (type(texto) == str), "texto <- must be a string"
        if len(colunas) != len(texto.split(',')):
            raise ValueError(f"{texto} doesn't have {len(colunas)} columns.")
        # assert (len(colunas) <= len(texto.split(','))), "texto <- not enough columns on this line"

        self.Formato = []

        for _ in colunas:
            self.Formato.append(f"{_}")
        
        # assign the values associated with each column
        self.readestilo(texto)

    def __repr__(self):
        """ String version of this object. Used for saving/printing the text file.

        :return: "Style: " + (Every format value from this object) + "\n" """

        saida = "Style: "
        for _ in range(len(self.Formato)):
            piece = f"{getattr(self, self.Formato[_].lower())}"
            saida = f"{saida}{piece}"
            if _ < (len(self.Formato)-1):
                saida = f"{saida}, "
        saida = f"{saida}\n"
        return saida

    def readestilo(self, texto):
        """ Reads a String line containing the values for a Style. Called by the constructor.

        :param texto: String. Formatted as "Style: {var1}, {var2}, {var3}, ... , {varN}\n"
        :return: None."""

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} must be a string.")
        # assert (isinstance(texto, str)), f"{texto} must be a string."
        if len(self.Formato) < 1:
            raise ValueError(f"({len(self.Formato)})Empty Formato")
        # assert (len(self.Formato) >= 1), f"({len(self.Formato)})Empty Formato"

        if texto.startswith("Style:"):
            entrada = texto[6:].strip()
        else:
            entrada = texto.strip()

        # split the same number of columns as "Formato" .
        entrada = (entrada.split(",", len(self.Formato)-1))

        # Getting rid of all empty spaces at the start and end of each section of the string list.
        for _ in range(len(entrada)):
            entrada[_] = entrada[_].strip()
        
        # Assigning each value to this object.
        for _ in range(len(entrada)):
            setattr(self, self.Formato[_].lower(), entrada[_])

    def getvalue(self, texto):
        """ Does the same as getattr(self, texto). But checks only the format list. And raise it's own exceptions.

        :param texto: String. What column to return. Must be one of the strings from 'Dados.V4Styles.Formato'. Get the
        list with getFormato()
        :return: String. The value stored.
        :raise Dados.ErrorEditorSSA.ErrorV4Styles_Estilo: Format found on list, but value was not assigned.
        :raise Dados.ErrorEditorSSA.ErrorV4Styles_Estilo2: Value not found on format list."""

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} has to be a string.")
        # assert(isinstance(texto, str)), f"{texto} has to be a string."

        if texto in self.getformato():
            for _ in self.getformato():
                if f"{texto}".lower() == f"{_}".lower():
                    if hasattr(self, _.lower()):
                        saida = getattr(self, _.lower())
                        return saida
                    else:
                        # Format found on list, but value was not assigned
                        raise Estilogeterror(f"{texto}")
        else:
            # value not found on format list
            return None
            # raise ErrorEditorSSA.ErrorV4Styles_Estilo2(f"{texto}")

    def getvaluelist(self):
        """ Returns a list with every value stored in this object.

        :return: list. Values are string.
        :raise ErrorEditorSSA.ErrorV4Styles_Estilo: Format found on list, but value was not assigned."""

        saida = []
        for _ in self.getformato():
            saida.append(self.getvalue(_))
        return saida
