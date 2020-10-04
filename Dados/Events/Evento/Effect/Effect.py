"""
Extends Evento. Contains Effect, which is one of the columns of each event.

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

# from Dados.ErrorPackage import ErrorPackage
from Dados.ErrorPackage.ErrorPackage import Effectgetvalue
from Dados.Events.Evento.Effect.Karaoke import Karaoke
from Dados.Events.Evento.Effect.Banner import Banner
from Dados.Events.Evento.Effect.Scroll import Scroll


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.0.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Effect:
    """ Effect column of every event in 'Event' section.

        Extends 'Dados.Events.Evento.Evento'.

        Usually empty. But can have one of 3 transition effects from SSA v4.x

        Names are case sensitive. Effects are Banner, Karaoke and Scroll. Check each file for more info about the names
        and args.

        Developer's Note: Not properly tested up to this day (01-10-2020)

        Use dir to check methods."""

    def __dir__(self):
        return ["__dir__", "__doc__", "__init__", "__repr__", "clearvalue", "getvalue", "setvalue"]

    def __init__(self, str1):
        """ Construct the object with a String or another Effect object.

            None: equals no no value.

            String: "" equals to no value. Otherwise attempts to read it.

            Effect: copy the values into this new one.

            :param str1: Effect instance, String or None.
            :raise Dados.ErrorPackage.ErrorPackage.Effectgetvalue: There are 2 or more values set, somehow..."""

        if isinstance(str1, Effect):
            # getvalue returns a list with an object and the string name of the object.
            # Using this object as arg for setvalue.
            self.setvalue(str1.getvalue()[0])
        else:
            self.transitioneffect = ""
            self.karaoke = None
            self.banner = None
            self.scroll = None
            _ = f"{str1} has to be a string, another Dados.Events.Evento.Effect.Effect instance or None."
            if str1 is not None:
                if isinstance(str1, str) is False:
                    raise TypeError(_)
                # assert (isinstance(str1, str)), _
                if str1 == "":
                    pass
                else:
                    self.setvalue(f"{str1}")

    def __repr__(self):
        """ String in the same format as the text file.

            Used for saving.

            :return: '' if there is no stored value. Banner, Karaoke or Scroll string format otherwise."""

        _ = self.getvalue()[0]
        if _ is None:
            return ""
        return f"{_}"

    def __del__(self):
        self.clearvalue()

    def getvalue(self):
        """ Returns the effect value as a list with 2 elements.

            First element is the object itself. Second is the lowercase name of the object.

            [None, ""] No value stored.

            [Karaoke, "Karaoke"] Karaoke from 'Dados.Events.Evento.Effect.Karaoke'

            [Banner, "Banner"]  Banner from 'Dados.Events.Evento.Effect.Banner'

            [Scroll, "Scroll"]  Scroll from 'Dados.Events.Evento.Effect.Scroll'

            :return: list with 2 values. First element is the effect object. Second element is the effect string name.
            :raise Dados.ErrorPackage.ErrorPackage.Effectgetvalue: There are 2 or more values set, somehow..."""

        values = [self.karaoke, self.banner, self.scroll]
        if values.count(None) == 3:
            return [None, ""]

        # If there are 2 or more effects set simultaneously
        if values.count(None) < 2:
            raise Effectgetvalue(f"{values} ")
        if self.karaoke is not None:
            return [Karaoke(self.karaoke), "Karaoke"]
        if self.banner is not None:
            return [Banner(self.banner), "Banner"]
        if self.scroll is not None:
            return [Scroll(self.scroll), "Scroll"]

    def clearvalue(self):
        """ Delete stored effect value.

            :return: self."""

        # del self.scroll
        # del self.banner
        # del self.karaoke
        self.scroll, self.karaoke, self.banner, self.transitioneffect = [None, None, None, ""]
        return self

    def setvalue(self, arg):
        """ Sets the effect value.

            None: Clear present value.

            Karaoke, Banner or Scroll object: Copy the object.

            String: Read the string value.

            :param arg: String, Banner, Scroll or Karaoke object. Can also be a None object to clear it.
            :return: self."""

        if arg is None:
            return self.clearvalue()
        elif isinstance(arg, Karaoke):
            # print("_____asdfadshfa") #testing
            self.clearvalue()
            self.karaoke = Karaoke()
            self.transitioneffect = "Karaoke"
            return self
        elif isinstance(arg, Banner):
            self.clearvalue()
            self.banner = Banner(arg)
            self.transitioneffect = "Banner"
            return self
        elif isinstance(arg, Scroll):
            self.clearvalue()
            self.scroll = Scroll(arg)
            self.transitioneffect = "Scroll"
            return self
        elif isinstance(arg, str):
            switcharg = {
                "banner": Banner,
                "scroll": Scroll,
                "karaoke": Karaoke
            }
            # clear empty spaces at the start and end of the argument, then turn all characters lowercase.
            __ = (arg.strip()).lower()
            # checks through switcharg keys for the one arg starts with
            for _ in switcharg:
                # if arg starts with this key
                if __.startswith(f"{_}"):
                    # create the object found in switcharg.
                    ___ = switcharg[_](__)
                    # Recall this method, but this time, using one of the three objects as parameter.
                    return self.setvalue(___)
            else:
                # Invalid string argument.
                raise ValueError(f"{arg} Invalid String argument.")
        # Invalid argument type.
        raise TypeError(f"{arg} can be 'None', 'Karaoke', 'Banner', 'Scroll' or 'String' only.")

# "[ ]" means the argument is optional
# Banner;delay;[lefttoright;fadeawaywidth]
# Scroll down;y1;y2;delay[;fadeawayheight]
# Scroll up;y1;y2;delay[;fadeawayheight]
# Karaoke


# testing
if __name__ == "__main__":
    a = "Banner   ;   0   ; 1;   100   "
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    a = "Banner   ;   0   ; 1"
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    # according to the docs, lefttoright (second argument)  has default = 0 for backwards compatibility.
    # So this object will always print it, just to be safe.
    a = "Banner   ;   0"
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    a = "Scroll    down   ;     100   ;   50   ;  100   ;    1000"
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    a = "Scroll    down   ;     100   ;   50   ;  100   "
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    a = "Scroll       up     ;      10    ;    0    ;    0    ;    0    "
    c = Effect(a)
    print(f"{Effect(a).__dict__}")
    print(f"{c}")
    print(f"{c.__dict__}")

    a = "Karaoke"
    c = Effect(a)
    print(f"{c}")
    print(f"{c.__dict__}")
    # print(f"{dir(c)}")
    # try:
    # a = "Karaoke  "
    # b = Effect(a)
    # print(f"{b}")
    # except ErrorEditorSSA.ErrorEvents_Evento_Effect as name:
    #   print(f"{name}")
