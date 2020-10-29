"""
Extends Evento. Contains Text, which is the last column of each event.

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

# No time at the moment to implement all the available functions or style override codes.
# Treating the strings raw for the moment.
# from EditorSSA.Dados.ErrorEditorSSA import ErrorEditorSSA


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.1.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Text:
    def __init__(self, str1):
        """ Just printing and saving this as a String for now. Too many special functions here to worry about.

            Extends 'Dados.Events.Evento.Evento'.

            :param str1: String or Text instance."""

        assert(isinstance(str1, str) or isinstance(str1, Text)), f"{str1} has to be a String or Text object."

        if isinstance(str1, Text):
            self.texto = self.readtexto(f"{str1}")
        else:
            self.texto = self.readtexto(str1)

    # for the moment just copying the string to the string line
    @staticmethod
    def readtexto(str1):
        """ Receives a string. Returns the same string.

            At the moment, Text doesn't do anything besides storing a string value.

            Functions will be implemented later.

            :param str1: String
            :return: String. """
        if isinstance(str1, str) is False:
            raise TypeError(f"{str1} has to be a string")
        return f"{str1}"

    def __repr__(self):
        return self.texto
