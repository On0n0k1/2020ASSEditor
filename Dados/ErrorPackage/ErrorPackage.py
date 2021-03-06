"""
Contains all custom exceptions of this project. Doesn't include ValueError and TypeError, which are local.

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

__all__ = ["ErrorPackage", "Timingnegativeerror", "Manyeffectserror", "Estilogeterror", "V4stylesgeterror",
           "Effectgetvalue"]


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.2.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class ErrorPackage(Exception):
    """Base Error Module from which others inherit."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class Timingnegativeerror(ErrorPackage):
    """ Operation led to Timing becoming a negative value.

    Raised by 'aftersub' in method '__sub__' from class Timing in 'Dados.Events.Evento.Effect.Timing.py'.
    """

    def __init__(self, titulo: str, message="Operation led to Timing becoming a negative value."):
        self.titulo = titulo
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.titulo} -> {self.message}"


class Manyeffectserror(ErrorPackage):
    """ Operation led to Timing becoming a negative value.

    Raised by 'aftersub' in method '__sub__' from class Timing in 'Dados.Events.Evento.Effect.Timing.py'.
    """

    def __init__(self, titulo: str, message="Operation led to Timing becoming a negative value.") -> None:
        self.titulo = titulo
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.message}"


class Estilogeterror(ErrorPackage):
    """ Tried to get a format that existed, but wasn't set.

    Raised by method 'getvalue' from class Estilo in 'Dados.V4Styles.Estilo.Estilo.py'.
    """

    def __init__(self, titulo: str, message="Tried to get a format that existed, but wasn't set.") -> None:
        self.titulo = titulo
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.message}"


class V4stylesgeterror(ErrorPackage):
    """ Attempted to retrieve Format when it wasn't set.

    Raised by methods 'getestilolist' and 'getestilo' from class V4Styles in 'Dados.V4Styles.V4Styles.py'.
    """

    def __init__(self, titulo: str, message="Attempted to retrieve Format, but it wasn't set.") -> None:
        self.titulo = titulo
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.message}"


class Effectgetvalue(ErrorPackage):
    """ Detected more than 1 simultaneous error.

    Raised by method 'getvalue' from class Effect in 'Dados.Events.Evento.Effect.Effect.py'.
    """

    def __init__(self, titulo: str, message="Can only have 1 effect set max.") -> None:
        self.titulo = titulo
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"{self.titulo} -> {self.message}"
