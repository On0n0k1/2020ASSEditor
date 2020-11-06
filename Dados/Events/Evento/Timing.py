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

__all__ = ["Timing"]

# from Dados.ErrorEditorSSA import ErrorEditorSSA
from Dados.ErrorPackage.ErrorPackage import Timingnegativeerror


class Timing:
    """ Time format for SSA files f'{h}:{mm}:{ss}.{cs}'.

        Extends 'Dados.Events.Evento.Evento'.

        Usable methods:

        Timing(texto): constructor. Accepts String, list, Timing object, int, float or None as parameter.

        readTiming(string): static method. Receives a string representation of timing and return a list with the values.

        getTimes(): returns a list with each value of this object. [hours, minutes, seconds, centiSeconds]

        setTimes(list): assign this 4-integer list's values unto this object.

        setHours(int): set hours.

        setMinutes(int): set minutes.

        setSeconds(int): set seconds.

        setCentiSeconds(int): set centiSeconds.

        secondsToTime(valor): Abstract. Valor is an integer or float in seconds. Returns a list on this object's format.

        Operations:

        sum: self + other, other + self, self+=other. other can be Timing, list, integer or float.

        sub: self - other, other - self, self-=other. other can be Timing, list, integer or float.

        sub raises 'ErrorPackage.Timingnegativeerror' if subtraction results in a negative
        time."""

    def __dir__(self):
        """ Modified __dir__ to display only user-defined functions of this object."""

        return ['__add__', '__dir__', '__eq__', '__float__', '__ge__', '__gt__', '__hash__', '__iadd__', '__init__',
                '__int__', '__isub__', '__le__', '__lt__', '__ne__', '__radd__', '__repr__', '__rsub__', '__sub__',
                '_aftersum', '_fitlista', 'checknegativeunset', 'chechnegativeset', 'centiseconds', 'gettimes', 'hours',
                'minutes', 'readtiming', 'seconds', 'secondstotime', 'setcentiseconds', 'sethours', 'setminutes',
                'setseconds', 'settimes']

    def checknegativeset(self):
        """ Any operation that turns this object into a negative time will turn it into 0 instead.

            This method make it raise an error whenever it happens. Default state is "not raise the error".

            :return: self."""
        self.checknegative = True

    def checknegativeunset(self):
        """ Any operation that turns this object into a negative time will turn it into 0 instead.

            This method makes it not raise an error whenever it happens. Which is already the default state.

            :return: self."""
        self.checknegative = False

    @staticmethod
    def readtiming(texto):
        """ Read a Time format of '0:00:00.00' and assign it's values to hours, minutes, seconds and centiseconds.

            Abstract Method.

            :param texto: String. f'{h}:{mm}:{ss}.{cs}'. Only 'hours' is allowed to have more digits.
            :return: Integer list with size 4. As in [0, 0, 0, 0]. With each respective value.

            Called by __init__. Receive a string line representing timing. Check if it is readable, then convert the 4
            values (hours, minutes, seconds, centiseconds) into a list. Before returning the list."""

        if isinstance(texto, str) is False:
            raise TypeError(f"{texto} not a String.")

        if (len(texto) < 9) or (":" not in texto):
            raise ValueError(f"{texto} invalid Timing arg")

        # anexar will become f"[{hh}, {mm}, {ss}.{cs}]" seconds and centiseconds together
        anexar = texto.split(":")
        if len(anexar) != 3:
            raise ValueError(f"{texto} - > {anexar} invalid Timing format.")

        # now anexar will become f"[{hh}, {mm}, {ss}, {cs}]"
        ___ = anexar[2]
        anexar.pop(2)
        for _ in ___.split("."):
            anexar.append(f"{_}")

        if len(anexar) != 4:
            raise ValueError(f"{texto} -> {anexar} was divided into {len(anexar)} elements instead of 4")

        # second, third and fourth values must have 2 digits
        for _ in range(1, 4):
            if(len(anexar[_])) != 2:
                raise ValueError(f"{texto} not a valid timing string")

        try:
            anexar = [int(anexar[_]) for _ in range(4)]
        except ValueError:
            raise ValueError(f"{anexar} could not be converted from string to integer values.")

        if anexar[1] >= 60 or anexar[2] >= 60:
            raise ValueError(f"{texto} -> {anexar} not valid Timing values.")

        return anexar

    @staticmethod
    def secondstotime(valor):
        """ Turn 'valor' in seconds to [h, mm, ss, cs] list format.

        :param valor: positive integer or float. Integer will be centiseconds. Float will be centiseconds.
        :return: [h, mm, ss, cs] list of integers."""

        if (isinstance(valor, int) or isinstance(valor, float)) is False:
            raise TypeError(f"{valor} must be an integer or float.")
        if valor < 0:
            raise ValueError(f"{valor} must be a positive value.")

        # resto is 'remainder' in portuguese
        hours, minutes, seconds, centiseconds, resto = (0, 0, 0, 0, 0)
        if isinstance(valor, float):
            # float means that valor is in seconds
            centiseconds = int(valor * 100.0) % 100
            resto = int(valor)
        elif isinstance(valor, int):
            # int means that valor is in centiseconds
            centiseconds = valor % 100
            resto = int((valor - centiseconds)/100)

        # resto is seconds minutes and hours now
        seconds = resto % 60
        resto = resto - seconds
        resto = int(resto / 60)

        # resto is minutes and hours now
        minutes = resto % 60
        resto = resto - minutes
        resto = int(resto / 60)
        # resto is hours now
        hours = resto

        return [hours, minutes, seconds, centiseconds]

    @staticmethod
    def _fitlista(lista):
        """ Turns an integer list into a [h, mm, ss, cs] time format.

            :param lista: Integer list. length between 0 and 4, inclusive.
            :return: Integer list [hours, minutes, seconds, centiseconds].

            Called by __init__()

            lista               ->      return

            []                  ->      [0, 0, 0, 0]

            [x1]                ->      [0, 0, x1, 0]

            [x1, x2]            ->      [0, x1, x2, 0]

            [x1, x2, x3]        ->      [x1, x2, x3, 0]

            [x1, x2, x3, x4]    ->      [x1, x2, x3, x4]"""

        if isinstance(lista, list) is False:
            raise TypeError(f"{lista} must be a list.")
        if len(lista) > 4:
            raise ValueError(f"{lista} may only have 0 to 4 values.")
        for _ in lista:
            if isinstance(_, int) is False:
                raise ValueError(f"{lista} all elements must be Integers.")

        # if len(lista) == 0
        saida = [0, 0, 0, 0]
        if len(lista) == 4:
            saida = [lista[_] for _ in range(4)]
        elif len(lista) == 3:
            saida = [lista[0], lista[1], lista[2], 0]
        elif len(lista) == 2:
            saida = [0, lista[0], lista[1], 0]
        elif len(lista) == 1:
            saida = [0, 0, lista[0], 0]
        return saida

    def __init__(self, texto=None):
        """ Constructor. Can receive 4 different types of arguments, or none at all.

                If 'texto' is String: it will read the String in the same format as the text file.

                If 'texto' is a list: it may have 1 to 4 integers. Being treated as:
                    [0, 0, texto[0], 0]
                    [0, texto[0], texto[1], 0]
                    [texto[0], texto[1], texto[2], 0]
                    [texto[0], texto[1], texto[2], texto[3]]

                If 'texto' is the same type of object as this: It will copy it's values.

                If 'texto' is an integer, consider the value to be in centiseconds.

                If 'texto' is not in arguments: all values start with 0."""

        if texto is not None:
            if True not in {isinstance(texto, _) for _ in (str, list, Timing, int, float)}:
                raise TypeError(f"Type {type(texto)} is unsupported for Timing.")
        # Checknegative raises an error whenever an operation is about to turn this object into a negative timing
        # False means it will just become 0
        self.checknegative = False
        entrada = [0, 0, 0, 0]
        self.hours, self.minutes, self.seconds, self.centiseconds = entrada
        # Mouseover the functions to see their documentation.
        if texto is None:
            pass
        elif isinstance(texto, str):
            entrada = self.readtiming(f"{texto}")
        elif isinstance(texto, list):
            entrada = self._fitlista(texto)
        elif isinstance(texto, Timing):
            entrada = texto.gettimes()
        elif isinstance(texto, int) or isinstance(texto, float):
            entrada = self.secondstotime(texto)
        self.settimes(entrada)

    def gettimes(self):
        """ Return an integer list with this object values.

        :return: [hours, minutes, seconds, centiSeconds]"""

        return [self.hours, self.minutes, self.seconds, self.centiseconds]

    def settimes(self, lista):
        """ Set this object's values to the integer list 'lista'.

            :param lista: Integer lista. [hours, minutes, seconds, centiSeconds]
            :return: self."""

        if isinstance(lista, list) is not True:
            raise TypeError(f"{lista} -- must be of list type")
        if len(lista) != 4:
            raise ValueError(f"{lista} -- must have 4 elements")

        for _ in (range(len(lista))):
            if isinstance(lista[_], int) is False:
                raise ValueError(f"{lista} all values must be integers")

        self.sethours(lista[0])
        self.setminutes(lista[1])
        self.setseconds(lista[2])
        self.setcentiseconds(lista[3])
        return self

    def sethours(self, horas):
        """ Set hours.

            :param horas: integer.
            :return: self."""

        if isinstance(horas, int) is False:
            raise TypeError(f"{horas} must be an integer")
        if horas < 0:
            if self.checknegative:
                raise ValueError(f"{horas} must be a positive value")
            return self.settimes([0, 0, 0, 0])
        self.hours = horas
        return self

    def setminutes(self, minutos):
        """ Set minutes.

            :param minutos: integer.
            :return: self."""

        if isinstance(minutos, int) is False:
            raise TypeError(f"{minutos} must be an integer")
        if (minutos < 0) or (minutos > 59):
            raise ValueError(f"{minutos} must be a value between 0 and 59")
        self.minutes = minutos
        return self

    def setseconds(self, segundos):
        """ Set seconds.

            :param segundos: integer.
            :return: self."""

        if isinstance(segundos, int) is False:
            raise TypeError(f"{segundos} must be an integer")
        if (segundos < 0) or (segundos > 59):
            raise ValueError(f"{segundos} must be a value between 0 and 59")
        self.seconds = segundos
        return self

    def setcentiseconds(self, centisegundos):
        """ Set centiseconds.

            :param centisegundos: integer.
            :return: self."""

        if isinstance(centisegundos, int) is False:
            raise TypeError(f"{centisegundos} must be an integer")
        if (centisegundos < 0) or (centisegundos > 99):
            raise ValueError(f"{centisegundos} must be a positive integer of up to 2 digits")
        self.centiseconds = centisegundos
        return self

    def __hash__(self):
        return hash(int(self))

    def __add__(self, other):
        """ The result of a sum operation with another object.

            :param other: the other object. Can be Timing, list, integer or float.
            :return: a new Timing object with the resulting values.

            If other is a Timing object, sum both the object's values into the new one.

            If other is a list, the sum method changes with the length (1 to 4):

            other = [x1]                [self.hours, self.minutes, self.seconds +x1, self.centiseconds]

            other = [x1, x2]            [self.hours, self.minutes + x1, self.seconds + x2, self.centiseconds]

            other = [x1, x2, x3]        [self.hours + x1, self.minutes + x2, self.seconds + x3, self.centiseconds]

            other = [x1, x2, x3, x4]    [self.hours + x1, self.minutes + x2, self.seconds + x3, self.centiseconds + x4]

            Other as an integer gets translated into centiseconds before incrementing.

            Other as a float gets translated into seconds before incrementing."""

        # If other is not one of these types, raise an error
        if True not in {isinstance(other, _) for _ in (Timing, list, int, float)}:
            raise TypeError(f"{type(other)} is unsupported for this function.")
        somatimes = self.gettimes()
        # If other is a Timing object, sum both the object's values into the new one.
        if isinstance(other, Timing):
            newtimes = other.gettimes()
        elif isinstance(other, list):
            # Change other into a 4 element list
            newtimes = self._fitlista(other)
        elif isinstance(other, int) or isinstance(other, float):
            # as integer, consider the value to be in centiseconds
            newtimes = self.secondstotime(other)
        else:
            # This line should be unreachable
            raise TypeError(f"{other} Invalid type for operation.")
        somatimes = [somatimes[_] + newtimes[_] for _ in range(4)]
        # Some values will go past their limits. I.E: minutes or seconds > 59, centiseconds > 99
        # aftersum fixes that.
        self._aftersum(somatimes)
        return Timing(somatimes)

    @staticmethod
    def _aftersum(somatimes):
        """ Check minutes, seconds and centiseconds for values that went above their limit. Used after sum operation.

            :param somatimes: integer list (4 elements). Resembling [h, mm, ss, cs].
            :return: integer list. Resembling [h, mm, ss, cs]. Same object as somatimes.

            Called by __add__() method.

            Returns fixed list:

            Assertains:

            hours >= 0

            0 <= minutes <= 59

            0 <= seconds <= 59

            0 <= centiseconds <=99."""

        if isinstance(somatimes, list) is False:
            raise TypeError(f"{somatimes} has to be a list.")
        if len(somatimes) != 4:
            raise ValueError(f"{somatimes} must have 4 elements.")
        for _ in somatimes:
            if isinstance(_, int) is False:
                raise ValueError(f"{somatimes} must have only integers.")

        def remainder(firstarg, secondarg, maxarg):
            """ Checks if secondarg is above it's max, send the excess to firstarg."""
            if secondarg >= maxarg:
                firstarg = firstarg + int((secondarg - (secondarg % maxarg))/maxarg)
                secondarg = secondarg % maxarg
            return [firstarg, secondarg]

        for _ in [3, 2, 1]:
            limitarg = 60
            if _ == 3:
                # centiseconds go all the way to 99
                limitarg = 100
            somatimes[_ - 1], somatimes[_] = remainder(somatimes[_ - 1], somatimes[_], limitarg)
        # somatimes[2], somatimes[3] = remainder(somatimes[2], somatimes[3], 100)
        # somatimes[1], somatimes[2] = remainder(somatimes[1], somatimes[2], 60)
        # somatimes[0], somatimes[1] = remainder(somatimes[0], somatimes[1], 60)
        return somatimes

    def __radd__(self, other):
        """ Operation other + self

            :param other: the object this was summed with.
            :return: self + other.

            This operation is commutative with all objects in which 'self + other' is implemented."""

        return self + other

    def __iadd__(self, other):
        """ Operation self+=other

            :param other: another object.
            :return: self + other

            Does self = self + other. Then return another object with the same values as self. Doesn't return self."""

        try:
            saida = Timing(self + other)
        except TypeError as typething:
            raise TypeError(typething.args)
        except ValueError as thingy:
            # Using the same args used for the error
            raise ValueError(thingy.args)
        self.settimes(saida.gettimes())
        return saida

    def __sub__(self, other):
        """ The result of a subtraction operation with another object.

            :param other: the other object. Can be Timing, list, integer or float.
            :return: a new Timing object with the result values.

            If other is a Timing object, subtract both the object's values into the new one.

            If other is a list, the sum method changes with the length(1 to 4):
                other = [x1]                [self.hours, self.minutes, self.seconds - x1, self.centiSeconds]
                other = [x1, x2]            [self.hours, self.minutes - x1, self.seconds - x2, self.centiSeconds]
                other = [x1, x2, x3]        [self.hours - x1, self.minutes - x2, self.seconds - x3, self.centiSeconds]
                other = [x1, x2, x3, x4]    [self.hours - x1, self.minutes - x2, self.seconds-x3, self.centiSeconds- x4]

            Other as an integer will be treated as centiseconds.

            Other as float will be treated as seconds.

            :raise ErrorPackage.Timingnegativeerror by _afterSub(): If time becomes negative (hours < 0)."""

        # Checking if valid
        if True not in {isinstance(other, _) for _ in (Timing, list, int, float)}:
            raise TypeError(f"Operation only valid with Timing, list, integer or float.")

        def aftersub(arg):
            """ Checks every column in the list for negative values and fix them.

                :param arg: The Timing list to check. [h, mm, ss, cs] format.
                :return: a fixed list.
                :raise ErrorPackage.Timingnegativeerror: If time becomes negative (hours < 0)."""

            # Not sure if using this function is making the  code more readable
            # It used to be an independent function of this object,
            # so I made it local since it is intended to be used just here
            rangenum = 60

            def nonnegative(firstnum, secondnum):
                """ While the digit is negative, pull 1 from the next 'house' and increment the digit by 'range'."""
                while secondnum < 0:
                    secondnum += rangenum
                    firstnum -= 1
                return [firstnum, secondnum]

            for _ in [3, 2, 1]:
                rangenum = 60
                if _ == 3:
                    rangenum = 100
                arg[_-1], arg[_] = (nonnegative(arg[_-1], arg[_]))
            # arg[2], arg[3] = nonnegative(arg[2], arg[3], 100)
            # arg[1], arg[2] = nonnegative(arg[1], arg[2], 60)
            # arg[0], arg[1] = nonnegative(arg[0], arg[1], 60)
            if arg[0] < 0:
                self.settimes([0, 0, 0, 0])
                if self.checknegative:
                    raise Timingnegativeerror(f"{arg}")
            return arg

        # Back to the __sub__ function
        # first and second will be used in subtracting function, the result will be used in aftersub
        first = self.gettimes()
        if isinstance(other, Timing):
            second = other.gettimes()
        elif isinstance(other, list):
            if len(other) > 4:
                raise ValueError(f"{other} can't have more than 4 elements")
            if False in {isinstance(_, int) for _ in other}:
                raise ValueError(f"{other} must have only integers")
            second = self._fitlista(other)
        elif isinstance(other, int) or isinstance(other, float):
            second = self.secondstotime(other)
        else:
            raise TypeError(f"Operation only valid with Timing, list, integer or float.")
        saida = [first[_] - second[_] for _ in range(4)]
        saida = aftersub(saida)
        return saida

    def __rsub__(self, other):
        """ Operation other - self.

            Operation is commutative. Therefore, other - self = self - other

            :param other: the object self is subtracting with.
            :return: self - other."""
        return self - other

    def __isub__(self, other):
        """ Operation self-=other.

            :param other: Another object used for this operation.
            :return: self - other."""

        try:
            saida = Timing(self - other)
        except TypeError as thingy:
            raise TypeError(thingy.args)
        except ValueError as otherthingy:
            raise ValueError(otherthingy.args)
        self.settimes(saida.gettimes())
        return saida

    def __int__(self):
        """ Integer representation of this object (centiseconds).

            :return: Integer. This object's value in centiseconds."""

        tempo = self.gettimes()
        seconds = tempo[0] * 360000 + tempo[1] * 6000 + tempo[2] * 100 + tempo[3]
        return int(seconds)

    def __float__(self):
        """ Float representation of this object (seconds).

            :return: Float. This object's value in seconds."""

        tempo = self.gettimes()
        seconds = float(tempo[0] * 3600 + tempo[1] * 60 + tempo[2]) + float(tempo[3])/100.0
        return seconds

    def __eq__(self, other):
        """ Operation self == other.

            :param other: Timing, Integer (seconds) or Float (seconds).
            :return: Boolean."""

        if True not in {isinstance(other, _) for _ in [Timing, int, float]}:
            raise TypeError(f"{type(self)} - {type(other)}  ->   operation is not supported.")

        _a = self.gettimes()
        _b = Timing(other).gettimes()
        # (If all comparisons are True) is the same as (If none of the comparisons are False)
        # (a and b) is the same as (!a or !b)
        if False not in {_a[_] == _b[_] for _ in range(4)}:
            return True
        return False

    def __lt__(self, other):
        """ Operation self < other.

            :param other: Timing, Integer(centiseconds) or Float (seconds).
            :return: Boolean."""

        if True not in {isinstance(other, _) for _ in [Timing, int, float]}:
            raise TypeError(f"{type(self)} - {type(other)}  ->  operation not supported for these types.")

        _a = self.gettimes()
        try:
            _b = Timing(other).gettimes()
        except ValueError as thingy:
            raise ValueError(thingy.args)
        except TypeError as typethingy:
            raise TypeError(typethingy.args)
        for _ in range(4):
            if _a[_] != _b[_]:
                if _a[_] < _b[_]:
                    return True
                return False
        # reaching here means that a == b
        return False

    def __le__(self, other):
        """ Operation self <= other.

            :param other: Timing, Integer (centiseconds) or Float (seconds)
            :return: Boolean."""
        try:
            return (self == other) or (self < other)
        except ValueError as ee:
            raise ValueError(ee.args)
        except TypeError as ettt:
            raise TypeError(ettt.args)

    def __ne__(self, other):
        """ Operation self != other

            :param other: Timing, Integer (centiseconds) or Float (seconds).
            :return: Boolean."""
        try:
            return not(self == other)
        except ValueError as thingg:
            raise ValueError(thingg.args)
        except TypeError as tasukete:
            raise TypeError(tasukete.args)

    def __gt__(self, other):
        """ Operation self > other.

            :param other: Timing, Integer (centiseconds) or Float (seconds).
            :return: Boolean"""

        if True not in {isinstance(other, _) for _ in [Timing, int, float]}:
            raise TypeError(f"{type(self)} > {type(other)}  ->  Invalid types for this operation.")
        _a = self.gettimes()
        try:
            _b = Timing(other).gettimes()
        except ValueError as thingy:
            raise ValueError(thingy.args)

        for _ in range(4):
            if _a[_] != _b[_]:
                if _a[_] > _b[_]:
                    return True
                return False
        # a == b
        return False

    def __ge__(self, other):
        """ Operation self >= other.

            :param other: Timing, Integer (centiseconds) or Float (seconds).
            :return: Boolean."""

        if True not in {isinstance(other, _) for _ in (Timing, int, float)}:
            raise TypeError(f"{type(self)} >= {type(other)} ->  Operation not valid for given types.")
        try:
            # saving processing by testing one at a time
            if self > other:
                return True
            else:
                return self == other
        except ValueError as thingy:
            raise ValueError(thingy.args)

    def __repr__(self):
        """ Return the string representation of this object. Used for saving.

            :return: f"{h:mm:ss.cs}

            hours: 1 digit at least
            minutes: 2 digits only
            seconds: 2 digits only
            centiseconds: 2 digits only."""

        def digito(arg):
            """ Make sure that even values with 1 digit are printed with 2 digits."""
            _ = ""
            if arg < 10:
                _ += f"0"
            return f"{_}{arg}"

        saida = f"{self.hours}:{digito(self.minutes)}:{digito(self.seconds)}.{digito(self.centiseconds)}"
        return saida


if __name__ == "__main__":
    x = [1, 0, 0, 0]
    print(f"Timing({x}) - Timing([0, 59, 59, 0]) = {Timing(x) - Timing([0, 59, 59, 0])}")
    print(f"Timing({x}) - [0, 59, 59, 0] = {Timing(x) - [0, 59, 59, 0]}")
    print(f"Timing({x}) - [0, 59, 59] = {Timing(x) - [0, 59, 59]}")
    print(f"Timing({x}) - [59, 59] = {Timing(x) - [59, 59]}")
    print(f"Timing({x}) - [59] = {Timing(x) - [59]}")
    y = 1
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 59
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 120
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 3599
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 0.01
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 3599.99
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")
    y = 119.5
    # y = 3601
    print(f"Timing({x}) - {y} = {Timing(x) - y}     ->>>    Timing({x}) - Timing({y}) = {Timing(x) - Timing(y)}")

    x = [0, 0, 1, 0]
    print(f"Timing({x}) + Timing([0, 59, 59, 0]) = {Timing(x) + Timing([0, 59, 59, 0])}")
    print(f"Timing({x}) + [0, 59, 59, 0] = {Timing(x) + [0, 59, 59, 0]}")
    print(f"Timing({x}) + [0, 59, 59] = {Timing(x) + [0, 59, 59]}")
    print(f"Timing({x}) + [59, 59] = {Timing(x) + [59, 59]}")
    print(f"Timing({x}) + [59] = {Timing(x) + [59]}")
    y = 1
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 59
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 120
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 3599
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 0.01
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 3599.99
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")
    y = 119.5
    print(f"Timing({x}) + {y} = {Timing(x) + y}     ->>>    Timing({x}) + Timing({y}) = {Timing(x) + Timing(y)}")

    # testing int(Timing) and float(Timing) for 369999 values
    for _ in range(0, 3700):
        if _ % 100 == 0:
            print(f"testing int and float {_}.00 - > {int(_ / 100)}99.99")
        # assert(_ == int(Timing(_)), f"Integer error ({_})")
        # for __ in range(0, 99):
        #     _tempo = float(_) + float(__) / 100
        #     assert(_tempo == float(Timing(_tempo)), f"Float error ({_tempo})")
        #     assert(int(_tempo*100) == int(Timing(_tempo)), f"Float error ({_tempo})")
        # assert(int(Timing(_)) == Timing.secondstotime(_))

    print((Timing(0) == (Timing([0, 0, 0, 0]))))
    print((Timing(0) <= (Timing([0, 0, 1, 0]))))
    print((Timing(0) > (Timing([0, 1, 0, 0]))))
    print((Timing([0, 0, 0, 0]) < (Timing([1, 0, 0, 0]))))
    # testing comparisons
    for _ in range(0, 1802):
        if _ % 100 == 0:
            print(f"Testing comparisons {int(_ * 2 / 100)}00 -> {int((_ * 2) / 100 + 1)}99")
        # from 3604 to 0 increment -2
        _x = (3604 - _ * 2) * 100
        # from 0 to 3604 increment 2
        _y = (_ * 2) * 100
        # The operations must have the same results in seconds and in Timing format

        # print(f"({Timing(_x)}) and ({Timing(_y)})")
        assert ((Timing(_x) == Timing(_y)) == (_x == _y)), f"{_x} failed = with {_y}"
        assert ((Timing(_x) < Timing(_y)) == (_x < _y)), f"{_x} failed < with {_y}"
        assert ((Timing(_x) <= Timing(_y)) == (_x <= _y)), f"{_x} failed with {_y}"
        assert ((Timing(_x) > Timing(_y)) == (_x > _y)), f"{_x} failed > with {_y}"
        assert ((Timing(_x) >= Timing(_y)) == (_x >= _y)), f"{_x} failed >= with {_y}"

    x = Timing()
    print(dir(x))
