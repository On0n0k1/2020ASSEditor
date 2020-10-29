"""
Extends Effect. Contains Banner, one of the 3 effects that the subtitle can use.

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

# from Dados.ErrorEditorSSA.ErrorEditorSSA import ErrorEvents_Evento_Effect


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.1.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Banner:
    """ Text will be displayed in one line; Scrolling from  right to left  or right to left accross the screen.

        Extends 'Dados.Events.Evento.Effect.Effect'.

        Methods:

        __init__(str1 = None): constructs the object based on a string or another Banner object.

        __repr(): the string version of banner.

        getdelay(): returns delay. integer.

        getlefttoright(): returns lefttoright. None or integer.

        getfadeawaywidth(): returns fadeawaywidth. None or integer.

        setdelay(int1): int1 must be an integer from 0 to 100.

        setlefttoright(int1): int1 must be 1 or 0."""

    def __init__(self, str1=None):
        """ Constructor. Text will be displayed in one line; Scrolling from  right to left  or right to left accross
            the screen.

            Use a string or another Banner object to setup it's values. If str1 is None. Delay will be 0.

            String format: f"Banner;{delay};{lefttoright};{fadeawaywidth}"

            lefttoright and fadeawaywidth are optional.

            delay: integer from 0 to 100.

            lefttoright: integer 1 or 0.

            fadeawaywidth: integer.

            :param str1: String or another Banner object."""

        # Adding a None case for the constructor
        if str1 is None:
            self.delay, self.lefttoright, self.fadeawaywidth = [0, 0, None]
        else:
            # Adding a copy case for the constructor
            if isinstance(str1, Banner):
                self.setdelay(int(str1.getdelay()))
                if str1.getlefttoright() is None:
                    self.lefttoright = None
                else:
                    self.setlefttoright(str1.getlefttoright())
                if str1.getfadeawaywidth() is None:
                    self.fadeawaywidth = None
                else:
                    self.setfadeawaywidth(str1.getfadeawaywidth())
            else:
                # string case for the constructor
                _ = f"{str1} has to be a string or a Dados.Events.Evento.Effect.Banner.Banner object."
                # assert (isinstance(str1, str)), f"{_}"
                if isinstance(str1, str) is False:
                    raise TypeError(_)
                leitura = str1
                leitura = leitura.strip()
                # turning leitura into a list
                leitura = leitura.split(";")
                # since the first character in the list should be ";" the first index is trash
                del leitura[0]

                if(len(leitura) < 1) or (len(leitura) > 3):
                    raise ValueError(f"Banner {str1} invalid arguments for Banner effect.")

                for _ in range(len(leitura)):
                    try:
                        leitura[_] = int(leitura[_])
                    except ValueError:
                        __ = f"Banner {str1} all arguments for Banner effect must be integers"
                        raise ValueError(f"{__}")

                # reading delay
                self.delay = int(leitura[0])
                if (self.delay < 0) or (self.delay > 100):
                    _ = f"Banner {str1} -> ({self.delay}): delay must be a value from 0 to 100"
                    raise ValueError(f"{_}")

                # lefttoright is 0 by default
                if len(leitura) == 1:
                    # this value is set on the second parameter (optional)
                    self.lefttoright = 0

                if len(leitura) >= 2:
                    self.lefttoright = int(leitura[1])
                    if (self.lefttoright < 0) or (self.lefttoright > 1):
                        _ = f"Banner {str1} -> ({self.lefttoright}) lefttoright can only be 1 or 0"
                        raise ValueError(f"{_}")

                if len(leitura) < 3:
                    # this value is set on the third parameter (optional)
                    self.fadeawaywidth = None

                if len(leitura) == 3:
                    # "fadeawayheight and fadeawaywidth parameters can be used to make the scrolling text at the sides
                    # transparent."

                    # The documentation doesn't seem to explain very well how 'fadeawaywidth' works. So just reading it.
                    self.fadeawaywidth = int(leitura[2])

    def __repr__(self):
        """ Return the string version of this object.

            Used for saving.

            lefttoright and fadeawaywidth are optional values. lefttoright will be included as '0' when None,
            fadeawaywidth will not be included when None.

            :return: String. Formatted as f"{delay};{lefttoright};{fadeawaywidth}" """

        saida = f"Banner ;"
        saida = f"{saida}{self.delay}; {self.lefttoright}"
        if self.fadeawaywidth is not None:
            saida = f"{saida}; {self.fadeawaywidth}"
        return saida

    def getdelay(self):
        """ Get the delay of the Banner Effect.

            Integer from 0 to 100. The higher the value, the slower it scrolls.

            Calculated as 1000/delay second/pixel.

            0: no delay.

            100: 0.1 second per pixel.

            :return: integer. Value from 0 to 100."""

        return int(self.delay)

    def getlefttoright(self):
        """ Set the lefttoright value of the Banner Effect.

            0 or 1. 1 makes the scrolling moves from left to right.

            :return: integer (0 or 1) or None (not set)."""

        if self.lefttoright is None:
            return None
        return int(self.lefttoright)

    def getfadeawaywidth(self):
        """ Get the fadeawaywidth value of this object.

            The distance from the corners where the text fades away.

            Developer comment: 'Couldn't find much info about how this attribute works. Therefore just storing an int.'

            :return: integer, or None. Since it's optional."""

        if self.fadeawaywidth is None:
            return None
        return int(self.fadeawaywidth)

    def setdelay(self, int1):
        """ Set the delay of the Banner Effect.

            Integer from 0 to 100. The higher the value, the slower it scrolls.

            Calculated as 1000/delay second/pixel.

            0: no delay.

            100: 0.1 second per pixel.

            :param int1: integer. Value from 0 to 100
            :return: self."""

        if isinstance(int1, int) is False:
            raise TypeError(f"{int1} has to be an integer.")
        # assert (isinstance(int1, int)), f"{int1} has to be an integer."
        if (int1 < 0) or (int1 > 100):
            raise ValueError(f"{int1} must be a value from 0 to 100")
        # assert (int1 >= 0) and (int1 <= 100), f"{int1} must be a value from 0 to 100"

        self.delay = int(int1)
        return self

    def setlefttoright(self, int1):
        """ Set the lefttoright value of the Banner Effect.

            0 or 1. 1 makes the scrolling moves from left to right.

            :param int1: integer. 0 or 1.
            :return: self."""

        if isinstance(int1, int) is False:
            raise TypeError(f"{int1} has to be an integer.")
        # assert (isinstance(int1, int)), f"{int1} has to be an integer."
        if ((int1 == 0) or (int1 == 1)) is False:
            raise ValueError(f"{int1} can only be 0 or 1.")
        # assert (int1 == 0) or (int1 == 1), f"{int1} can only be 0 or 1."

        self.lefttoright = int1
        return self

    def setfadeawaywidth(self, int1):
        """ Set the fadeawaywidth value of this object.

            The distance from the corners where the text fades away.

            Developer comment: 'Couldn't find much info about how this attribute works. Therefore just reading an int.'

            :param int1: integer.
            :return: self."""

        if isinstance(int1, int) is False:
            raise TypeError(f"{int1} has to be an integer.")
        # assert (isinstance(int1, int)), f"{int1} has to be an integer."

        self.fadeawaywidth = int1
        return self
