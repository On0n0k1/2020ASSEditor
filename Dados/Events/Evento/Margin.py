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

# from Dados.ErrorEditorSSA import ErrorEditorSSA
from typing import Union, List


class Margin:
    """ Margin in pixels used in "MarginL", "MarginR" and "MarginV" of "Dados.Events.Evento"

    Extends 'Dados.Events.Evento.Evento'.

    Acts as integer most of the times. But string format has at least 4 digits. Supports most integer operations.
    But mostly recommended to just use int({objectname}) and then Margin ({result}) when using this object.

    Methods:

    __init__: Sets self.margin when constructing.

    __repr__: has at least 4 digits, as in "0000" for self.margin == 0.

    setmargin: margin is integer (margin >=0).

    __int__: returns self.margin as an integer.
    """

    def __dir__(self) -> List[str]:
        return ['__abs__', '__add__', '__dir__', '__divmod__', '__eq__', '__float__', '__floordiv__', '__ge__',
                '__gt__', '__iadd__', '__ifloordiv__', '__imod__', '__imul__', '__init__', '__int__', '__invert__',
                '__ipow__', '__isub__', '__itruediv__', '__le__', '__lt__', '__mod__', '__mul__', '__ne__', '__neg__',
                '__pos__', '__pow__', '__radd__', '__rdivmod__', '__repr__', '__rfloordiv__', '__rmod__', '__rmul__',
                '__rpow__', '__rsub__', '__rtruediv__', '__sub__', '__truediv__', 'setmargin']

    def __init__(self, margin: Union[int, float, str, 'Margin'] = 0) -> None:
        """ Construct margin.

        :param margin: Non-negative Integer, float, string or another Margin instance.
        """
        self.margin = 0

        if isinstance(margin, int):
            self.setmargin(margin)
        elif isinstance(margin, str):
            try:
                x = int(margin)
                self.setmargin(x)
            except ValueError:
                raise ValueError(f"{margin} isn't a valid string.")
        elif isinstance(margin, Margin):
            self.setmargin(int(margin))
        else:
            raise TypeError(f"{margin} isn't a valid margin type")

    def setmargin(self, margin: Union [int, float, str, 'Margin']) -> 'Margin':
        """ Set the object's main value 'margin'

        :param margin: Non-negative integer, float, string or another Margin instance.
        :return: self.
        """

        # inefficient way to check conditions, changing eventually
        if True not in {isinstance(margin, _) for _ in (int, float, str, Margin)}:
            raise TypeError
        if isinstance(margin, int):
            if margin < 0:
                # margin can't be negative
                raise ValueError
        self.margin = int(margin)
        return self

    def __repr__(self) -> str:
        num = int(self.margin)
        if num == 0:
            saida = "0000"
        elif num < 10:
            saida = f"000{num}"
        elif num < 100:
            saida = f"00{num}"
        elif num < 1000:
            saida = f"0{num}"
        else:
            saida = f"{num}"

        return saida

    def __int__(self) -> int:
        return int(self.margin)

    def __float__(self) -> float:
        return float(self.margin)

    def __lt__(self, other) -> bool:
        return int(self.margin) < other

    def __gt__(self, other) -> bool:
        return self.margin > other

    def __le__(self, other) -> bool:
        return self <= other

    def __ge__(self, other) -> bool:
        return self.margin >= other

    def __eq__(self, other) -> bool:
        return self.margin == other

    def __ne__(self, other) -> bool:
        return self.margin != other

    def __add__(self, other) -> int:
        return self.margin + other

    def __sub__(self, other) -> int:
        return self.margin - other

    def __mul__(self, other) -> int:
        return self.margin * other

    def __truediv__(self, other) -> Union[int, float]:
        return self.margin / other

    def __floordiv__(self, other) -> int:
        return self.margin // other

    def __mod__(self, other) -> int:
        return self.margin % other

    def __divmod__(self, other):
        return divmod(self.margin, other)

    def __pow__(self, other, modulo=None) -> int:
        return pow(self.margin, other, modulo)

    def __radd__(self, other) -> int:
        return self.margin + other

    def __rsub__(self, other) -> int:
        return other - self.margin

    def __rmul__(self, other) -> int:
        return self.margin * other

    def __rtruediv__(self, other) -> Union[int, float]:
        return other / self.margin

    def __rfloordiv__(self, other) -> Union[int, float]:
        return other // self.margin

    def __rmod__(self, other) -> int:
        return other % self.margin

    def __rdivmod__(self, other):
        return divmod(other, self.margin)

    def __rpow__(self, other, modulo=None) -> int:
        return pow(other, self.margin, modulo)

    def __iadd__(self, other) -> int:
        try:
            self.margin = self.margin + other
            return int(self.margin)
        except TypeError as ee:
            raise TypeError(ee.args)
        except ValueError as eee:
            raise ValueError(eee.args)

    def __isub__(self, other) -> int:
        try:
            self.margin = self.margin - other
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __imul__(self, other):
        try:
            self.margin = self.margin * other
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __itruediv__(self, other) -> Union[int, float]:
        try:
            self.margin = self.margin / other
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __ifloordiv__(self, other):
        try:
            self.margin = self.margin // other
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __imod__(self, other) -> int:
        try:
            self.margin = self.margin % other
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __ipow__(self, other, modulo=None) -> int:
        try:
            self.margin = pow(self.margin, other, modulo)
            return int(self.margin)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as eee:
            raise TypeError(eee.args)

    def __neg__(self) -> int:
        return -self.margin

    def __pos__(self) -> int:
        return self.margin

    def __abs__(self) -> int:
        return self.margin

    def __invert__(self) -> int:
        return -self.margin


# testing
if __name__ == "__main__":
    for _ in range(1, 100):
        # print(Margin(_))
        for __ in range(1, 100):
            print(f"Margin({_}) + {__} = {Margin(_) + __}")
            assert (Margin(_) + __ == Margin(_ + __)), f"Not equals: (Margin(_) + __ == Margin(_ + __))"
            print(f"Margin({_}) - {__} = {Margin(_) - __}")
            if (_ - __) >= 0:
                assert (Margin(_) - __ == Margin(_ - __)), f"Not equals: (Margin(_) - __ == Margin(_ - __))"
            print(f"Margin({_}) * {__} = {Margin(_) * __}")
            assert(Margin(_)*__ == Margin(_*__)), f"Not equals: (Margin(_) * __ == Margin(_ * __))"
            print(f"Margin({_}) / {__} = {Margin(_) / __}")
    # assert(Margin(Margin(_)/__) == Margin(float(_)/__)), f"Not equals: ({Margin(Margin(_) / __)} != {Margin(_ / __)})"
    # print(f"Margin({_}) // {__} = {Margin(_) // __}")
            assert(Margin(_) // __ == Margin(_ // __)), f"Not equals: (Margin(_) // __ == Margin(_ // __))"
            print(f"Margin({_}) % {__} = {Margin(_) % __}")
            assert(Margin(_) % __ == Margin(_ % __)), f"Not equals: (Margin(_) % __ == Margin(_ % __))"

    c = Margin(150)
    print(f"{c}")
    print(f"{dir(c)}")
