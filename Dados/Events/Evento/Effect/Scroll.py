"""
Extends Effect. Contains Scroll, which is one the 3 effects employed by the event.

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

# from Dados.ErrorEditorSSA import ErrorEditorSSA
# from Dados.ErrorPackage.ErrorPackage import ErrorPackage


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.2.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Scroll:
    """ Scroll makes the event (image or message) scroll vertically through the screen.

        Extends 'Dados.Events.Evento.Effect.Effect'.

        Methods:

        __init__(entrada = None, subtitlerplugin = None): Create the object with no parameters, a String, or another
        Scroll object to copy. String reading format changes according to subtitlerplugin.

        gety1(): returns y1. Non-negative Integer.

        gety2(): returns y2. Non-negative Integer.

        getdelay(): returns delay. Integer, value from 0 to 100.

        getfadeawayheight(): returns fadeawayheight. Non-negative Integer.

        issubtitlerplugin(): returns subtitlerplugin. True or False.

        getdirection(): returns direction. String. "up" or "down".

        sety1(y1): set y1. Non-negative integer.

        sety2(y2) set y2. Non-negative integer.

        setdelay(delay) set delay. Integer. From 0 to 100, inclusive.

        setfadeawayheight(fadeawayheight): set fadeawayheight. Non-negative integer.

        setsubtitlerplugin(subtitlerplugin) set subtitlerplygin. Which decides how to read and print this object.

        setdirection(direction): set direction. "up" or "down".

        __repr__(): String format changes according to subtitlerplugin."""

    # self.direction: 'up' or 'down'
    # self.subtitlerplugin: True or False. If it is using Avery Lee's Subtitler plugin order or not.
    # self.y1: Integer. First height. In pixels.
    # self.y2: Integer. Second height. In pixels.
    # (doesn't matter the order between y1 and y2)
    # self.delay: Integer. From 0 to 100. How much will the scrolling be delayed.
    # self.fadeawayheight: Integer. Optional. The documentation doesn't explain well how to treat this value,
    # so I won't care much about it.

    def __init__(self, entrada=None, subtitlerplugin=None):
        """ Constructs the object. Can use a string or copy from a similar object.

            :param entrada: String, Dados.Events.Evento.Effect.Scroll.Scroll object, or None. String is used for loading
                a SSA file. Scroll object will have copied values. None will start with direction, y1, y2, delay,
                fadeawayheight and subtitlerplugin as "up", 0, 0, 0, None and False, respectively.
            :param subtitlerplugin: True or False. True means the format will be read and written as
                f"Scroll {direction}; {delay}; {y1}; {y2}; {fadeawayheight}". False means the format will be read and
                written as f"Scroll {direction}; {y1}; {y2}; {delay}; {fadeawayheight}".

                """

        if entrada is None:
            self.direction, self.y1, self.y2, self.delay, self.fadeawayheight = ["up", 0, 0, 0, None]
            self.subtitlerplugin = False
        elif isinstance(entrada, Scroll):
            self.direction, self.y1, self.y2 = [entrada.getdirection(), entrada.gety1(), entrada.gety2()]
            self.delay, self.fadeawayheight = [entrada.getdelay(), entrada.getfadeawayheight()]
            self.setsubtitlerplugin(entrada.issubtitlerplugin())
        else:
            if isinstance(entrada, str) is False:
                raise TypeError(f"{entrada} has to be a string or Scroll object.")
            # assert(isinstance(entrada, str)), f"{entrada} has to be a string or Scroll object."
            _ = f"{subtitlerplugin} must be a boolean or omitted."
            if subtitlerplugin is not None:
                if isinstance(subtitlerplugin, bool) is False:
                    raise TypeError(_)
            # assert((subtitlerplugin is None) or isinstance(subtitlerplugin, bool)), _

            texto = (entrada.strip()).lower()
            if texto.startswith("scroll"):
                texto = texto[6:].strip()
            if texto.startswith("up"):
                self.direction = "up"
                texto = texto[2:]
            elif texto.startswith("down"):
                self.direction = "down"
                texto = texto[4:]
            else:
                _ = f"{entrada} : 'up' or 'down' Not Found after Scroll."
                raise ValueError(f"{_}")

            parameters = texto.split(";")
            # since the section starts with ';', the first value of the list must be removed
            del parameters[0]

            if len(parameters) < 3:
                # Line too long
                _ = f"{entrada} : too few arguments after Scroll {self.direction}({len(parameters)} "
                raise ValueError(_)
            if len(parameters) > 4:
                # Line too long
                _ = f"{entrada} : too many arguments after Scroll {self.direction}({len(parameters)}) "
                raise ValueError(_)

            try:
                if len(parameters) == 3:
                    parameters = [int(parameters[0]), int(parameters[1]), int(parameters[2])]
                else:
                    parameters = [int(parameters[0]), int(parameters[1]), int(parameters[2]), int(parameters[3])]
            except ValueError:
                raise ValueError(f"{entrada} the arguments aren't integers.")

            # Here comes another messup of this format
            # SSA reads Scroll up/down parameters as y1;y2;delay[;fadeawayheight]
            # But 'Avery Lee's "Subtitler" plugin' reads the parameters as 'delay;y1;y2[;fadeawayheight]'
            # The reader will try to guess which of the styles is being used based on the values. It will focus on using
            # ';y1;y2;delay' normally though.

            # if subtitlerplugin was not defined
            if subtitlerplugin is not None:
                self.subtitlerplugin = subtitlerplugin
            else:
                # try to guess if the order is ';delay;y1;y2' based on constraints
                # delay has to be a value that goes from 0 to 100, so  at least one of the values will be in that range
                if (0 <= parameters[0]) and (parameters[0] <= 100) and parameters[2] > 100:
                    self.subtitlerplugin = True
                else:
                    self.subtitlerplugin = False

            if self.subtitlerplugin:
                if len(parameters) == 3:
                    self.delay, self.y1, self.y2 = parameters
                    self.fadeawayheight = None
                else:
                    self.delay, self.y1, self.y2, self.fadeawayheight = parameters
            else:
                if len(parameters) == 3:
                    self.y1, self.y2, self.delay = parameters
                    self.fadeawayheight = None
                else:
                    self.y1, self.y2, self.delay, self.fadeawayheight = parameters

    def gety1(self):
        """ Y1 and Y2 are the height values where the text will scroll.

            There's no respective order for both values. Any of the two can be the highest or lowest.

            :return: Non-negative integer."""

        return int(self.y1)

    def gety2(self):
        """ Y1 and Y2 are the height values where the text will scroll.

            There's no respective order for both values. Any of the two can be the highest or lowest.

            :return: Non-negative integer."""

        return int(self.y2)

    def getdelay(self):
        """ Return the delay value of this object.

            Integer from 0 to 100. The higher the value, the slower it scrolls.

            Calculated as 1000/delay second/pixel.

            0: no delay.

            100: 0.1 second per pixel.

            :return: Integer. From 0 to 100."""
        return int(self.delay)

    # Not sure if fadeawayheight is the distance that the scroll has to cover before fading,
    # or the position on the screen where it starts fading.
    # should return 0 be ok?
    def getfadeawayheight(self):
        """ Get fadeawayheight value of this object.

            :return: Integer. Non-negative value."""

        return self.fadeawayheight

    def issubtitlerplugin(self):
        """ Get subtitlerplugin value.

            True: f"Scroll {direction}; {delay}; {y1}; {y2}; {fadeawayheight}"

            False: f"Scroll {direction}; {y1}; {y2}; {delay}; {fadeawayheight}"

            :return: True or False."""

        return self.subtitlerplugin

    def getdirection(self):
        """ Get direction.

            :return: String. "up" or "down" only."""

        return self.direction

    def sety1(self, y1):
        """ Set y1 value of this object.

            :param y1: Integer. Non-negative value.
            :return: self."""

        if isinstance(y1, int) is False:
            raise TypeError(f"{y1} must be an integer.")
        if y1 < 0:
            raise ValueError(f"{y1} must be a non-negative value")
        # assert (isinstance(y1, int)), f"{y1} must be an integer."
        # assert (y1 >= 0), f"{y1} must be a non-negative value"
        self.y1 = y1
        return self

    def sety2(self, y2):
        """ Set y2 value of this object.

            :param y2: Integer. Non-negative value.
            :return: self."""

        if isinstance(y2, int) is False:
            raise TypeError(f"{y2} must be an integer.")
        # assert (isinstance(y2, int)), f"{y2} must be an integer."
        if y2 < 0:
            raise ValueError(f"{y2} must be a non-negative value")
        # assert (y2 >= 0), f"{y2} must be a non-negative value"
        self.y2 = y2
        return self

    def setdelay(self, delay):
        """ Set delay value of this object.

            Integer from 0 to 100. The higher the value, the slower it scrolls.

            Calculated as 1000/delay second/pixel.

            0: no delay.

            100: 0.1 second per pixel.

            :param delay: Integer. From 0  to 100.
            :return: self."""

        if isinstance(delay, int) is False:
            raise TypeError(f"{delay} must be an integer")
        # assert (isinstance(delay, int)), f"{delay} must be an integer"
        if (delay < 0) or (delay > 100):
            raise ValueError(f"{delay} must be a value from 0 to 100")
        # assert (0 <= delay) and (delay <= 100), f"{delay} must be a value from 0 to 100"
        self.delay = delay
        return self

    def setfadeawayheight(self, fadeawayheight):
        """ Set fadeawayheight value of this object.

            :param fadeawayheight: Integer. Non-negative value.
            :return: self."""

        if isinstance(fadeawayheight, int) is False:
            raise TypeError(f"{fadeawayheight} must be an integer")
        # assert(isinstance(fadeawayheight, int)), f"{fadeawayheight} must be an integer"
        if fadeawayheight < 0:
            raise ValueError(f"{fadeawayheight} must be a positive value")
        # assert (fadeawayheight >= 0), f"{fadeawayheight} must be a positive value"
        self.fadeawayheight = fadeawayheight
        return self

    def setsubtitlerplugin(self, subtitlerplugin):
        """ Set subtitlerplugin value.

            If True:

            f"Scroll {direction}; {delay}; {y1}; {y2}; {fadeawayheight}"

            if False:

             f"Scroll {direction}; {y1}; {y2}; {delay}; {fadeawayheight}"

            :param subtitlerplugin:
            :return: self."""

        if isinstance(subtitlerplugin, bool) is False:
            raise TypeError(f"{subtitlerplugin} must be True or False")
        # assert(isinstance(subtitlerplugin, bool)), f"{subtitlerplugin} must be True or False"
        self.subtitlerplugin = subtitlerplugin
        return self

    def setdirection(self, direction):
        """ Set Scroll direction.

            :param direction: String. "up" or "down" only.
            :return: self."""

        if isinstance(direction, str) is False:
            raise TypeError(f"{direction} must be 'up' or 'down'.")
        # assert(isinstance(direction, str)), f"{direction} must be 'up' or 'down'."
        if (direction.lower() != "up") and (direction.lower() != "down"):
            raise ValueError(f"{direction} must be 'up' or 'down'.")
        # assert(direction.lower() == "up") or (direction.lower() == "down"), f"{direction} must be 'up' or 'down'."
        self.direction = direction.lower()
        return self

    def __repr__(self):
        """ Returns this object string format.

            If subtitlerplugin is set to true. The return will be:

            f"Scroll {direction}; {delay}; {y1}; {y2}; {fadeawayheight}"


            if subtitlerplugin is set to false. The return will be:

            f"Scroll {direction}; {y1}; {y2}; {delay}; {fadeawayheight}"

            :return: This object string in SSA format"""

        saida = f"Scroll {self.direction.lower()};"
        if self.subtitlerplugin:
            saida = f"{saida} {self.delay}; {self.y1}; {self.y2}"
        else:
            saida = f"{saida} {self.y1}; {self.y2}; {self.delay}"
        if self.fadeawayheight is None:
            return saida
        else:
            return f"{saida}; {self.fadeawayheight}"
