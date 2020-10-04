"""
Extends Effect. Contains Karaoke, which is one of the 3 effects the subtitle can use.

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

# from EditorSSA.Dados.ErrorEditorSSA import ErrorEditorSSA


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.0.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Karaoke:
    """ 'Karaoke' effect on 'effect' column of 'Events section'.

        Extends 'Dados.Events.Evento.Effect.Effect'.

        I don't know what to do with this. According to the files "Karaoke as an effect is obsolete'

        So this object just reads and print 'Karaoke'. It will stay as object in case someone decides to implement it.

        Methods:

        __init__(): Constructs the object.

        __repr__(): Returns 'Karaoke'."""

    def __init__(self, str1=""):
        # 'Nothing' to do here.
        if isinstance(str1, Karaoke):
            # No values to copy
            self.value = "Karaoke"

    def __repr__(self):
        return "Karaoke"
