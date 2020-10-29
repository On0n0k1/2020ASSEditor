"""
Extends Events. Contains Evento, which represents a single subtitle in the file.

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


# Libs
import types

# Own modules
from Dados.SimpleLine.SimpleLine import SimpleLine
from Dados.Events.Formato.Formato import Formato
from Dados.Events.Evento.Timing import Timing
from Dados.Events.Evento.Margin import Margin
from Dados.Events.Evento.Effect.Effect import Effect
from Dados.Events.Evento.Text.Text import Text
# from Dados.V4Styles import V4Styles
# from Dados.ErrorPackage import ErrorPackage


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.1.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]


class Evento:
    """ Stores an Event for SSA.

        Extend 'Dados.Events.Events'.

        Attribute names: ["layer", "marked", "start", "end", "style", "name", "marginl", "marginr", "marginv", "effect",
        "text"]

        List above is retrievable with gettiposdisponiveis() method.

        These attributes will be stored in a dict from which the values can be get and set with getdictvalue and
        setdictvalue respectively. There's also gets and sets for each attribute separately, for the sake of ease.
        E.G. : setlayer, setmarked, getlayer, getmarked...

        The values can also be loaded using a string with readevent. A list can be loaded with setvalues, but it must be
        following the same order as this object's getformat.

        Use setformat before reading any string, setting with any list, or printing this object.

        seteventtype set this event type. All possible types can be checked with getalleventtypes(), which is abstract.

        Below is a list of all methods used:

        getalleventtypes(): Static Method. Returns a string list with all possible types this object can set.

        gettiposdisponiveis(): Not Static. Returns a string list with all attribute names usable.

        __init__(arg = None): constructs this object and set itself to arg.

        __repr__(): called when printing formatted version of this object. Will return "" if format is not set.

        seteventtype(str1): set event type to the string 'str1' informed. String must be in 'getalleventtypes()'.

        geteventtype(): Return event type. String. "" if it wasn't set. Will be a value from 'getalleventtypes()' if
        set.

        __convertvalue__(name, value): Meant to be used by the instance. 'name' must be in 'gettiposdisponiveis()'.
        Converts 'value' to the expected type for that 'name'.

        setdictvalue(name, value): 'name' is String. 'name' must be in 'gettiposdisponiveis()'. Set attribute 'name' to
        a copy of object 'value'.

        getdictvalue(name): Return value of attribute 'name'. 'name' must be in 'gettiposdisponiveis()'. Return None if
        value isn't set.

        setvalues(args): Set attributes following format order. args is a list containing all 10 attributes to set.

        getvalues(): Return a list of size 10 containing each attribute value. Values will be ordered according to
        'format'.

        setformato(args): Set format to the list of strings args. args must have size 10. And be a valid format list,
        containing only elements that can be found in 'gettiposdisponiveis()'.

        getformato(): Returns format. None if it wasn't set, list of 10 strings if it is set.

        readevent(arg): Read an event line and store it's values. 'arg' is String or 'SimpleLine' instance.

        (gets and sets for each attribute name)..."""

    def __dir__(self):
        """ Displays everything from this object that is useful for outsiders, and doesn't break anything when used.

            :return: list of all useful attributes in this class."""

        return ["__dir__", "condition", "updatetime", "getalleventtypes", "gettiposdisponiveis", "__init__", "__repr__",
                "seteventtype", "geteventtype", "__convertvalue__", "setdictvalue", "getdictvalue", "setvalues",
                "getvalues", "setformato", "getformato", "readevent", "getlayer", "setlayer", "getmarked", "setmarked",
                "getstart", "setstart", "getend", "setend", "getstyle", "setstyle", "getname", "setname", "getmarginl",
                "setmarginl", "getmarginr", "setmarginr", "getmarginv", "setmarginv", "geteffect", "seteffect",
                "gettext", "settext"]

    def condition(self, method):
        """ Run method using arguments [layer, name, start, end].

            if it returns True or False. Returns the value.

            Else, raise ValueError.

            :param method: function.
            :return: True, False."""

        if isinstance(method, type(types.FunctionType)) is False:
            raise TypeError(f"{method!r} has to be a method or lambda.")
        args = [self.getlayer(), self.getname(), self.getstart(), self.getend()]
        result = method(args)
        if (result is not True) and (result is not False):
            raise ValueError(f"{result!r}: result was not boolean.")
        else:
            return result

    @staticmethod
    def condtest(a=None, b=None):

        if a is not None:
            if True not in {isinstance(a, _) for _ in {int, float, Timing}}:
                raise TypeError(f"{a} must be an Integer, Floating or Timing instance.")

        if b is not None:
            if True not in {isinstance(b, _) for _ in {int, float, Timing}}:
                raise TypeError(f"{b} must be an Integer, Floating or Timing instance.")

        if a == b:
            f"{a} == {b} no valid intervals to acquire"
        argmin = a
        argmax = b

        def cond(value):
            xmin = argmin
            xmax = argmax

            # test1 operation between value and xmin
            # test2 operation between value and xmax
            # returned value will be (test1) and (test2)

            if (xmin is None) and (xmax is None):
                raise ValueError(f"Both arguments are empty.")
            if xmin is None:
                test1 = True
            else:
                test1 = value > xmin
            if xmax is None:
                test2 = True
            else:
                test2 = value < xmax

            return test1 and test2

        return cond

    def updatetime(self, arg, condition=None, pos=None):
        """ Sum or subtract start and end by the value arg.

            Reminder that integer are treated as centiseconds, and floats are treated as seconds.

            :param arg: Integer or Float. Positive or negative.
            :param condition: lambda or function that returns True or False based on what time it is currently at.
            :param pos: index of the line used.
            :return: self."""

        if (isinstance(arg, int) or isinstance(arg, float)) is False:
            raise TypeError(f"{arg} has to be integer or float")

        __saida__ = f"{self.getdictvalue('start')} : {self.getdictvalue('end')}     ->      "
        # __saida__ = f"{self.getstart()} : {self.getend()}    ->  "
        # if condition is not None:
        #     if condition(self.getstart()) is False:
        #         return self

        # print(f"{self.getstart()}")
        if arg > 0:
            newstart = Timing(Timing(self.getstart()) + arg)
            newend = Timing(Timing(self.getend()) + arg)
        elif arg < 0:
            newstart = Timing(Timing(self.getstart()) - (-arg))
            newend = Timing(Timing(self.getend()) - (-arg))
        else:
            return self

        self.setdictvalue('start', newstart)
        self.setdictvalue('end', newend)
        # self.setstart(newstart)
        # self.setend(newend)
        __saida__ = f"{__saida__}{self.getdictvalue('start')} : {self.getdictvalue('end')}\n arg = {arg}    "
        __saida__ = f"{__saida__} condition = {self.condtest(condition)(self.getstart())}"
        # __saida__ = f"{__saida__}{self.getstart()} : {self.getend()}"
        # if condition is not None:
        #     print(__saida__)
        if pos is not None:
            return pos
        return self

    @staticmethod
    def getalleventtypes():
        return ["dialogue", "comment", "picture", "sound", "movie", "command"]

    def gettiposdisponiveis(self):
        return list(self.tiposdisponiveis)

    def __init__(self, arg=None, argformato=None):
        """ Initialize the attributes.

            tiposdisponiveis: String list that stores every attribute name that can be stored. Used by dictvalues

            alleventtypes: String list that stores every event type that can be used.

            formato: String list that stores the order of the columns used. Uses tiposdisponiveis strings.

            dictvalues: Dict that associates each string name to it's object.

                key 'layer': integer non-negative.

                key 'marked': integer, 1 or 0.

                key 'start': 'Timing' stance from 'Dados.Events.Evento.Timing'

                key 'end': 'Timing stance from 'Dados.Events.Evento.Timing'

                key 'style': String

                key 'name': String

                key 'marginl': 'Margin' stance from 'Dados.Events.Evento.Margin'

                key 'marginr': 'Margin' stance from 'Dados.Events.Evento.Margin'

                key 'marginv': 'Margin' stance from 'Dados.Events.Evento.Margin'

                key 'effect': 'Effect' stance from 'Dados.Events.Evento.Effect.Effect'

                key 'text': 'Text' stance from 'Dados.Events.Evento.Text.Text'

            eventtype: String.

            :param arg: Evento instance for copying only."""

        # Checking these 3 conditions to raise the error without going through all that is down there
        if arg is None or isinstance(arg, Evento):
            pass
        elif isinstance(argformato, Formato) and (isinstance(arg, str) or isinstance(arg, list)):
            pass
        else:
            raise TypeError

        # tiposdisponiveis will be:
        # ["layer", "marked", "start", "end", "style", "name", "marginl", "marginr", "marginv", "effect", "text"]
        # Calling it from format so it can keep up with any future changes that may happen
        self.tiposdisponiveis = []
        for _ in Formato.gettiposdisponiveis():
            # Lowering each string so they are not case sensitive
            self.tiposdisponiveis.append(_.lower())

        # formato will store the order of columns
        self.formato = []

        # This dict will store all this object's values, unordered.
        self.dictvalues = {}
        for _ in self.tiposdisponiveis:
            # documentation is for debugging: Explains the column
            # conditions is a list of lists.
            # every list will be [one condition lambda expression, the error it raises, text for the error]
            # constructor is the type of object used to store it. Will be used as constructor by the get and set methods
            # value is the value itself stored. Will be used by the get method.
            self.dictvalues[_] = {
                "documentation": "",
                "conditions": [],
                # "type": None,
                "value": None
            }

        self.alleventtypes = self.getalleventtypes()
        self.eventtype = ""

        # setlayer
        # make 800 lines of code, or make an unreadable cinderblock of chaos
        # this seems more fun. But I definitely won't do it at work.

        cond = "conditions"
        # cons = "type"
        # doc = "documentation"
        name = 'layer'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # first values are the lambdas for condition testing, last element is the message of the error to raise
        # the element before the last is the error to be raised.
        # this can be scaled a lot, even though it doesn't need to.
        _ = [(lambda x: (x >= 0)), ValueError, "Layer can not be negative"]
        ((self.dictvalues[name])[cond]).append(_)
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'marked'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        _ = [(lambda x: (x == 0) or (x == 1)), ValueError, "Marked can only be 0 or 1."]
        ((self.dictvalues[name])[cond]).append(_)
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'start'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # no condition to check
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'end'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'style'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'name'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'marginl'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'marginr'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'marginv'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'effect'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        name = 'text'
        assert name in self.tiposdisponiveis, f"{name} missing from {self.tiposdisponiveis}"
        # ((self.dictvalues[name])[doc]) = """Used to have a reference for the main docs here. Took it out to avoid
        # copyright issues."""

        # Initializing these values to avoid some issues
        self.setmarked(0)
        self.setlayer(0)

        if isinstance(arg, Evento):
            # These 2 sets should work even if arg doesn't have them set. What matters is that this is a copy of arg.
            self.seteventtype(arg.geteventtype())
            self.setformato(arg.getformato())
            # Using every attribute name to set

            # for _ in arg.getformato():
            for _ in self.gettiposdisponiveis():
                # setting every attribute using the names for both objects
                self.setdictvalue(_, arg.getdictvalue(_))
            # as a string, it is expected that it is a full line containing all 10 values and it's type
            # these constraints will be checked by readevent.
        elif isinstance(arg, str) and isinstance(argformato, Formato):
            self.setformato(argformato.getformat())
            self.readevent(arg)
        elif isinstance(arg, list) and isinstance(argformato, Formato):
            self.setformato(argformato.getformat())
            self.setvalues(arg)
        elif arg is None:
            pass
        else:
            raise TypeError

    def __repr__(self):
        """ Prints formatted version of Evento.

            Used for saving the file and debugging.

            Values will follow 'self.getformat()' order.

            :return: String."""

        _type = self.geteventtype()
        # Use the index of type to get the camelcase version of the same String.
        # _type = ["Dialogue", "Comment", "Picture", "Sound", "Movie", "Command"][self.getalleventtypes().index(_type)]

        _values = self.getvalues()
        # Will not print or save invalid events
        if _type is None:
            return ""
        _saida = f"{_type}: "
        for _ in range(9):
            if _values[_] is None:
                return ""
            _saida += f"{_values[_]},"
        # last element shouldn't have ',' at the end
        _saida += f"{_values[9]}\n"
        return _saida

    def seteventtype(self, str1):
        """ Set this object's event type.

            types can be:

            self.getalleventtypes() == ["dialogue", "comment", "picture", "sound", "movie", "command"]

            :param str1: String. This method is not case-sensitive.
            :return: self"""

        if isinstance(str1, str) is False:
            raise TypeError(f"{str1} has to be a String.")

        _ = (str1.strip()).lower()
        if _ in self.alleventtypes:
            self.eventtype = f"{_}".capitalize()
            return self
        # invalid event type
        raise ValueError(f"Arg: {_}, Acceptable values:{self.alleventtypes}")
        # raise ErrorEditorSSA.ErrorEvents_Evento_Evento_SetEventType(f"Arg: {_}, Acceptable values:{self.alleventtypes
        # }")

    def geteventtype(self):
        """ Return event type.

            types can be every element from self.getalleventtypes() but capitalized.

            ["Dialogue", "Comment", "Picture", "Sound", "Movie", "Command"]

            :return: String if set. Empty String "" if it wasn't set."""

        return f"{self.eventtype}"

    def __convertvalue__(self, name, value):
        """ Return a converted type of value based on what name it has.

            Used by gets and sets.

            :param name: String. Must be in self.tiposdisponiveis
            :param value: any type valid for the name used. Call f"{(self.dictvalues[name])['documentation']}" for more
                info.
            :return: converted value"""

        _name = (name.strip()).lower()
        assert _name in self.tiposdisponiveis, f"{name} - > {_name} must be in {self.tiposdisponiveis}."
        # [layer, marked, start, end, style, name, marginl, marginr, marginv, effect, text]
        # [int, int, Timing, Timing, str, str, Margin, Margin, Margin, Effect, Text]
        if _name in ["layer", "marked"]:
            if value is not None:
                _value = int(value)
            else:
                _value = None
        elif _name in ["start", "end"]:
            _value = Timing(value)
        elif _name in ["style", "name"]:
            _value = f"{value}"
        elif _name in ["marginl", "marginr", "marginv"]:
            _value = Margin(value)
        elif _name == "effect":
            _value = Effect(value)
        elif _name == "text":
            _value = Text(value)
        else:
            raise ValueError
        return _value

    def setdictvalue(self, name, value):
        """ Set the atribute with name to value.

            :param name: String. Must be in 'self.tiposdisponiveis'.
            :param value: valid arg for that value constructor.
            :return: self.
            :raise ValueError: When 'layer' or 'marked' values are invalid."""

        if isinstance(name, str) is False:
            raise TypeError(f"{name} has to be a string.")
        # assert isinstance(name, str), f"{name} has to be a string."
        _name = (name.strip()).lower()
        __cond = "conditions"
        __val = "value"

        if _name not in self.tiposdisponiveis:
            raise ValueError(f"{name} - > {_name} must be in {self.tiposdisponiveis}.")
        # assert _name in self.tiposdisponiveis, f"{name} - > {_name} must be in {self.tiposdisponiveis}."
        # converts value into the type that will be stored.
        _value = self.__convertvalue__(name, value)
        # Time for the giant overkill for testing conditions
        if len((self.dictvalues[_name])[__cond]) == 0:
            (self.dictvalues[_name])[__val] = _value
        else:
            # getting the list of lists to check conditions
            __clists = (self.dictvalues[_name])[__cond]
            # looping through the list of lists
            for __clist in __clists:
                # looping through the list, but the last 2 elements [error, errorarg]
                siz = len(__clist)
                # list should have at least 1 condition, and then the last element will be a message
                # and before the last will be the error to raise
                # so siz can be 0, 3 and higher only
                assert (siz != 1) and (siz != 2), f"{__clist} has {siz} elements. Coder mistake!"
                for _ in range(siz - 2):
                    # if the lambda returns false (like an assert), raise the error at the end of the list
                    if ((__clist[_])(_value)) is False:
                        if __clist[siz - 1] is None:
                            raise __clist[siz - 2]
                        else:
                            raise (__clist[siz - 2])(f"{__clist[siz - 1]}")
            else:
                (self.dictvalues[_name])[__val] = _value
        return self

    def getdictvalue(self, name):
        """ Returns value with key 'name'.

            :param name: String. Must be in 'self.tiposdisponiveis'.
            :return: a copy of the stored value."""

        if isinstance(name, str) is False:
            raise TypeError(f"{name} has to be a string.")
        # assert isinstance(name, str), f"{name} has to be a string."
        _name = (name.strip()).lower()
        if _name not in self.tiposdisponiveis:
            raise ValueError(f"{_name} -> {name} not in {self.tiposdisponiveis}")
        # assert _name in self.tiposdisponiveis, f"{_name} -> {name} not in {self.tiposdisponiveis}"

        _value = (self.dictvalues[_name])['value']
        return self.__convertvalue__(_name, _value)

    def setvalues(self, args):
        """ Sets the values using a list following this object's format order.

            :param args: list with 10 elements. Each element must be appropriate for that specific value.
            :return: self."""
        if isinstance(args, list) is False:
            raise TypeError(f"{args} has to be a list.")
        if len(args) != 10:
            raise ValueError(f"{args} must have 10 elements")
        assert self.getformato() is not None, f"Format is not set for this instance."
        _format = self.getformato()
        # I know __convertvalue__ is being called twice for the same object
        # just trying to follow the practice of making sure that the output is never a reference to the input
        # _values = [self.__convertvalue__(_format[_], args[_]) for _ in range(10)]
        # changed my mind, just calling args instead of _values
        for _ in range(10):
            self.setdictvalue(_format[_], args[_])
        return self

    def getvalues(self):
        """ Return a list of values stored following the same order as format.

        :return: list with 10 elements. Different object types involved."""

        _format = self.getformato()
        return [self.getdictvalue(_format[_]) for _ in range(10)]

    def setformato(self, args):
        """ Sets formato to the list of strings.

            :param args: list of 10 strings. Each String must be in 'self.gettiposdisponiveis()'.
            :return: self."""
        __value = args
        if isinstance(args, str) or isinstance(args, SimpleLine):
            __value = [_.strip() for _ in ((SimpleLine(f"{__value}").gettexto()).strip()).split(",")]
            if len(__value) != 10:
                raise ValueError(f"{__value} must have 10 columns")
            for _ in __value:
                if _.lower() not in [__.lower() for __ in self.tiposdisponiveis]:
                    raise ValueError(f"{_}: Invalid format type.")
        if isinstance(__value, list) is False:
            raise TypeError(f"{args} must be a list of Strings")
        if len(__value) != 10:
            raise ValueError(f"{__value} must have 10 elements ({len(__value)})")
        for _ in __value:
            if isinstance(_, str) is False:
                raise ValueError(f"{__value} all elements must be Strings")
        # creating trimmed and lowered version of the string using list comprehension
        __values = [(_.strip()).lower() for _ in __value]
        for _ in range(10):
            if __values[_] not in self.tiposdisponiveis:
                raise ValueError(f"{__value[_]} -> {__values[_]} not in {self.tiposdisponiveis}")
            # assert __values[_] in self.tiposdisponiveis, f"{args[_]} -> {__values[_]} not in {self.tiposdisponiveis}"

        # checking duplicates very inneficiently, since each combination will be checked twice
        # easier to read though
        for _ in range(10):
            for __ in range(10):
                if _ != __:
                    if __values[_] == __values[__]:
                        raise ValueError(f"{__values} -> duplicates found in index {_} and {__}")

        # setting the list using list comprehension
        self.formato = [f"{_}" for _ in __values]
        return self

    def getformato(self):
        """ Return format.

            :return: None if it wasn't set. String list with 10 elements if it is set."""

        if isinstance(self.formato, list) is False:
            raise TypeError(f"{self.formato} is not even a list. Something else changed it.")
        # assert isinstance(self.formato, list), f"{self.formato} is not even a list. Something else changed it."
        if len(self.formato) == 0:
            return None
        return [f"{_}" for _ in self.formato]

    # string
    # simpleline
    def readevent(self, arg):
        """ Read an event line and stores it's columns.

            :param arg: String or SimpleLine instance.
            :return: self."""
        assert self.getformato() is not None, f"Format is not set"
        if (isinstance(arg, str) or isinstance(arg, SimpleLine)) is False:
            raise TypeError(f"{arg} must be a string or a 'SimpleLine' instance")

        # If it's a string, splits type from the text. If it's a SimpleLine, remains the same.
        __event = SimpleLine(arg)
        if __event.gettipo() is None:
            raise ValueError("Invalid Event")
        # This will raise ValueError if it is invalid
        self.seteventtype(__event.gettipo())

        __values = [_.strip() for _ in __event.gettexto().split(",", 9)]
        if len(__values) != 10:
            raise ValueError(f"{len(__values)}: number of columns has to be 10.")
        return self.setvalues(__values)

    # Everything below are unessential gets and sets, created with the intent of making this object easyer to use
    # self.getdictvalue already works as a get for all names
    # self.setdictvalue already works as set for all names
    # [layer, marked, start, end, style, name, marginl, marginr, marginv, effect, text]

    def getlayer(self):
        """ Return layer.

            Subtitles having different layer number will be ignored during the collusion detection. Higher numbered
            layers will be drawn over the lower numbered.

            Can be Layer or Marked. One of the two is chosen in Format.

            :return: non-negative integer."""

        _name = 'layer'
        return self.getdictvalue(_name)

    def setlayer(self, arg):
        """ Set layer.

            Each layer have it's own collision areas.

            Subtitles with higher layers will be drawn over lower layer ones.

            Can be Layer or Marked. One of the two is chosen in Format.

            :param arg: non-negative integer. Or integer in string format.
            :return: self."""

        _name = 'layer'
        return self.setdictvalue(_name, arg)

    def getmarked(self):
        """ Return marked.

            Marked=0 means the line is not shown as "marked" in SSA.

            Marked=1 means the line is shown as "marked" in SSA.

            :return: Integer. 1 or 0."""

        _name = 'marked'
        return self.getdictvalue(_name)

    def setmarked(self, arg):
        """ Set marked.

            Marked=0 means the line is not shown as "marked" in SSA.

            Marked=1 means the line is shown as "marked" in SSA.

            :param arg: Integer. 1 or 0.
            :return: self."""

        _name = 'marked'
        return self.setdictvalue(_name, arg)

    def getstart(self):
        """ Return Start.

            Starting time for the event.

            0:00:00:00 format as Hrs:Mins:Secs:hundredths.

            :return: Timing object. From 'Dados.Events.Evento.Timing'. """

        _name = 'start'
        return self.getdictvalue(_name)

    def setstart(self, arg):
        """ Set Start.

            Starting time for the event.

            0:00:00:00 format as Hrs:Mins:Secs:hundredths.

            :param arg: No value, Integer, Float, String, Integer List or another Timing instance.
            :return: self. """

        _name = 'start'
        return self.setdictvalue(_name, arg)

    def getend(self):
        """ Return end.

            Ending time for the event.

            0:00:00:00 format as Hrs:Mins:Secs:hundredths.

            :return: Timing object. From 'Dados.Events.Evento.Timing.Timing'."""

        _name = 'end'
        return self.getdictvalue(_name)

    def setend(self, arg):
        """ Set end.

            Ending time for the event.

            0:00:00:00 format as Hrs:Mins:Secs:hundredths.

            :param arg: No value, Integer, Float, String, Integer List or another Timing instance.
            :return: self."""

        _name = 'end'
        return self.setdictvalue(_name, arg)

    def getstyle(self):
        """ Return style.

            The name of the style used by this event. String.

            The string is a reference to one of the names in V4Styles. If there's no style with this name, it will not
            raise an error.

            The issue of not having a reference should be found and solved by the upper classes.

            :return: String."""

        _name = 'style'
        return self.getdictvalue(_name)

    def setstyle(self, arg):
        """ Set style.

            The name of the style used by this event.

            The string is a reference to one of the names in V4Styles. If there's no style with this name, it will not
            raise an error.

            The issue of not having a reference should be found and solved by the upper classes.

            :param arg: String.
            :return: self."""

        _name = 'style'
        return self.setdictvalue(_name, arg)

    def getname(self):
        """ Return name.

            Character that is speaking the line. Meant to help scripting/editing the file.

            Optional value.

            :return: String."""

        _name = 'name'
        return self.getdictvalue(_name)

    def setname(self, arg):
        """ Set name.

            Character that is speaking the line. Meant to help scripting/editing the file.

            Optional value.

            :param arg: String.
            :return: self."""

        _name = 'name'
        return self.setdictvalue(_name, arg)

    def getmarginl(self):
        """ Return marginl.

            Left margin. Instanced by it's own class with valid operations and conversion with integers. String version
            has 4 digits, at least.

            :return: Margin instance from 'Dados.Events.Evento.Margin.Margin'."""

        _name = 'marginl'
        return self.getdictvalue(_name)

    def setmarginl(self, arg):
        """ Set marginl.

            Left margin. Instanced by it's own class with valid operations and conversion with integers. String version
            has 4 digits, at least.

            :param arg: Non-negative Integer.
            :return: self."""

        _name = 'marginl'
        return self.setdictvalue(_name, arg)

    def getmarginr(self):
        """ Return marginr.

            Right margin. Instanced by it's own class with valid operations and conversion with integers. String version
            has 4 digits, at least.

            :return: Margin instance from 'Dados.Events.Evento.Margin.Margin'"""

        _name = 'marginr'
        return self.getdictvalue(_name)

    def setmarginr(self, arg):
        """ Set marginr.

            Right margin. Instanced by it's own class with valid operations and conversion with integers. String version
            has 4 digits, at least.

            :param arg: Non-negative Integer.
            :return: self."""

        _name = 'marginr'
        return self.setdictvalue(_name, arg)

    def getmarginv(self):
        """ Return marginv.

            Bottom margin. Instanced by it's own class with valid operations and conversion with integers. String
            version has 4 digits, at least.

            :return: Margin instance from 'Dados.Events.Evento.Margin.Margin'"""

        _name = 'marginv'
        return self.getdictvalue(_name)

    def setmarginv(self, arg):
        """ Set marginv.

            Bottom margin. Instanced by it's own class with valid operations and conversion with integers. String
            version has 4 digits, at least.

            :param arg: Non-negative Integer.
            :return: self."""

        _name = 'marginv'
        return self.setdictvalue(_name, arg)

    def geteffect(self):
        """ Return effect.

            Usually empty. But can have one of 3 transition effects from SSA v4.x

            :return: Effect instance from 'Dados.Events.Evento.Effect.Effect'."""

        _name = 'effect'
        return self.getdictvalue(_name)

    def seteffect(self, arg):
        """ Set effect.

            Usually empty. But can have one of 3 transition effects from SSA v4.x

            :param arg: None, String or Effect instance from 'Dados.Events.Evento.Effect.Effect'. "" and None means no
                value to be read.

            :return: self."""

        _name = 'effect'
        return self.setdictvalue(_name, arg)

    def gettext(self):
        """ Return 'text'.

            Subtitle Text. It will always be in the last column of the text file. Can have special override functions.

            Functions haven't been properly implemented for this yet. So treating the string from this section raw.

            :return: Text instance from 'Dados.Events.Evento.Text.Text'."""

        _name = 'text'
        return self.getdictvalue(_name)

    def settext(self, arg):
        """ Set 'text'.

            Subtitle Text. It will always be in the last column of the text file. Can have special override functions.

            'Functions haven't been properly implemented for this yet. So treating the string from this section raw.

            :param arg: String or Text instance from 'Dados.Events.Evento.Text.Text'.
            :return: self."""

        _name = 'text'
        return self.setdictvalue(_name, arg)


# testing
if __name__ == "__main__":

    formatting = f"Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    formatobject = Formato(formatting)
    # _event = Evento()
    # _event.setformato(formatobject.getformat())
    # print(_event.getformato())

    lines = [
        r"Dialogue: 0,0:00:28.06,0:00:31.34,Default,,0000,0000,0000,,{\be1}Though I devour the five lands",
        r"Dialogue: 0,0:00:31.86,0:00:34.97,Default,,0000,0000,0000,,{\be1}and drink the three oceans dry,",
        r"Dialogue: 0,0:00:35.73,0:00:39.63,Default,,0000,0000,0000,,{\be1}I am powerless against the sky,",
        r"Dialogue: 0,0:00:42.06,0:00:46.23,Default,,0000,0000,0000,,{\be1}for I have neither wings, nor legs, nor hand"
        + r"s.",
        r"Dialogue: 0,0:00:55.88,0:00:58.57,Default,,0000,0000,0000,,{\be1}I am the world snake.",
        r"Dialogue: 0,0:01:00.51,0:01:04.88,Default,,0000,0000,0000,,{\be1}My name is Jormungand.",
        r"Dialogue: 0,0:03:05.29,0:03:12.46,Default,,0000,0000,0000,,{\be1}A state-of-the-art fighter just like that on"
        + r"e killed my parents with its payload of high-tech bombs.",
        r"Dialogue: 0,0:03:14.57,0:03:16.64,Default,,0000,0000,0000,,{\be1}There are those who invent new weapons,",
        r"Dialogue: 0,0:03:16.64,0:03:18.29,Default,,0000,0000,0000,,{\be1}those who manufacture them,",
        r"Dialogue: 0,0:03:18.29,0:03:20.27,Default,,0000,0000,0000,,{\be1}those who sell them,",
        r"Dialogue: 0,0:03:20.27,0:03:21.47,Default,,0000,0000,0000,,{\be1}and those who use them.",
        r"Dialogue: 0,0:03:22.82,0:03:26.65,Default,,0000,0000,0000,,{\be1}I will hate them for all eternity.",
        r"Dialogue: 0,0:03:28.69,0:03:32.76,Default,,0000,0000,0000,,{\be1}I wonder if God knows how I feel.",
        r"Dialogue: 0,0:03:34.01,0:03:36.36,Default,,0000,0000,0000,,{\be1}Move your feet, soldier!",
        r"Dialogue: 0,0:03:36.62,0:03:41.53,Default,,0000,0000,0000,,{\be1}Come on! One, two! One, two!",
        r"Dialogue: 0,0:03:42.49,0:03:45.66,Default,,0000,0000,0000,,{\be1}She's Koko Hekmatyar, a young arms dealer.",
        r"Dialogue: 0,0:03:47.22,0:03:51.59,Default,,0000,0000,0000,,{\be1}I travel with an arms dealer."
    ]
    _events = [(Evento().setformato(formatobject.getformat())).readevent(_) for _ in lines]
    saida = ""
    for _ in _events:
        line = _.getvalues()
        print([f"{line[_]}({type(line[_])})" for _ in range(10)])
        saida += f"{_}"
    print(f"{saida}")

    print(dir(_events[0]))
