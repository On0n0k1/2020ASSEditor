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
__version__ = "0.1.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]

# from Dados.ErrorEditorSSA import ErrorEditorSSA
# from Dados.V4Styles.V4Styles import V4Styles


from Dados.Events.Evento.Evento import Evento
# from Dados.Events.Evento.Timing import Timing
from Dados.Events.Formato.Formato import Formato
from Dados.SimpleLine.SimpleLine import SimpleLine
# from multiprocessing import Process, Queue, JoinableQueue
import concurrent.futures
import queue
import time
# import os
# import types


class Events:

    """
        Format:
            field names can be as follow: Marked, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
            The sequence of values may change, but 'Text' must always be the last one


            """

    # alleventtypes will be ["dialogue", "comment", "picture", "sound", "movie", "command"]
    def __init__(self):
        """

            """
        # This will store a single list that will have either SimpleLine or Evento for every loaded Line
        # If the line is a valid event, store it as Evento, otherwise, store it as SimpleLine
        # If the input is a textfile or string, it will have SimpleLines
        # If it receives input from other sources that have no 'trash' like json, it will only have Evento instances
        # In other words, it will work the same way regardless of how many invalid lines are on the file
        # And will work the same way with other kinds of inputs.

        # How it will read a file
        # Add all lines as SimpleLine
        # If it find the "Format" Line, read it
        # After finding the "Format" Line, go back to the start, rechecking all the SimpleLines stored up to this point
        # Replace any SimpleLine that is a valid event with an Evento instance
        # Go all the way to the end, adding the remaining lines

        self.__lines = []
        self.__formato = None
        # __q__: queue for executing tasks on this object
        self.__q__ = queue.Queue()
        # used only for counting in updatetimes
        # self.__counter__ = 0

    # def condition(self, method):
    #     """ Loop through events and return a list with each position where condition is True or False.
    #
    #         :param method: lambda or function using [layer, name, start, end]
    #         :return: list (size = number of events stored) with True and False values."""
    #
    #     def packager(pos):
    #         """ Return the condition function that is referenced by pos.
    #
    #             Returns a lambda that always returns False when target doesn't exist."""
    #         if isinstance(pos, int) is False:
    #             raise TypeError(f"{pos} has to be int.")
    #         print(pos)
    #         if pos < len(self.__lines):
    #             return False
    #         # not altering values, so getline is good enough
    #         targetevento = self.getline(pos)
    #         if isinstance(targetevento, Evento) is False:
    #             return False
    #         return targetevento.condition(method)
    #
    #     # if isinstance(method, type(types.FunctionType)) is False:
    #     #     raise TypeError(f"{method!r} has to be a method or lambda.")
    #
    #     with multiprocessing.Pool() as pool:
    #         results = [__ for __ in pool.map(packager, [_ for _ in range(len(self.__lines))])]
    #
    #     return results

    # def updatetimes(self, argcondition, argvalue):
    #     """ Check conditions for every Evento. Alter the ones which return True.
    #
    #         :param argcondition: Conditions to check before altering. List with 4 elements, each containing a lambda
    #         or
    #             function that can only return True or False, to be used for [layer, name, start, end] columns of each
    #             evento.
    #
    #         :param argvalue: value to add in time when condition is True. Float or Integer, positive or negative.
    #
    #         :return: self"""
    #
    #     def packager(pos):
    #         """ Return the updatetime function that is referenced by pos.
    #
    #             Returns a lambda that always returns False when target doesn't exist."""
    #         if isinstance(pos, int) is False:
    #             raise TypeError(f"{pos} has to be int.")
    #         print(pos)
    #         if pos < len(self.__lines):
    #             raise ValueError(f"{pos} out of bounds [0 to {len(self.__lines)}]")
    #         # altering values, so calling self.__lines directly
    #         self.__lines[pos].updatetime(argvalue)
    #         return True
    #
    #     if (isinstance(argvalue, int) or isinstance(argvalue, float)) is False:
    #         raise TypeError(f"{argvalue} has to be int or float.")
    #
    #     # list that has the result of argcondition for each evento stored.
    #     conditions = self.condition(argcondition)
    #     # Ignore all False values, creating a list that stores each position where it is True
    #     positions = [_ for _ in range(len(conditions)) if (conditions[_] is True)]
    #
    #     # for _ in range(len(conditions)):
    #     #     if conditions[_]:
    #     #         positions.append(_)
    #
    #     with multiprocessing.Pool() as pool2:
    #         pool2.map(packager, positions)

    def getthefunctions(self, spacing, qpos):
        while not qpos.empty():
            try:
                pos = qpos.get()
                self.__q__.put((self.__lines[pos].updatetime, pos))
                time.sleep(spacing)
            except queue.Empty:
                break

        # for _ in range(len(self.__lines)):
        #     time.sleep(spacing)
        #     self.__q__.put((self.__lines[_].updatetime, _))
        return "Done Feeding"

    def updatetimes(self, **kwargs):
        """

            :param kwargs:
                'arg': How much time to alter.
                'cond': function condition to check which to alter.
            :return: """

        highest = 0
        qpos = queue.Queue()
        for _ in range(len(self.__lines)):
            qpos.put(_)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # start a future for a thread which sends work in through the queue
            futuretoevents = {executor.submit(self.getthefunctions, 0.05, qpos): "FEEDER DONE"}

            while futuretoevents:
                # check for status of the futures which are currently working
                done, notdone = concurrent.futures.wait(
                    futuretoevents, timeout=3,
                    return_when=concurrent.futures.FIRST_COMPLETED)

                # if there is incoming work, start a new future
                while not self.__q__.empty():

                    # fetch an event from the queue
                    splitthingy = self.__q__.get()
                    # neweventof = self.__q__.get()
                    neweventof = splitthingy[0]
                    newpos = splitthingy[1]

                    # Start the load operation and mark the future with its evento
                    futuretoevents[executor.submit(neweventof, kwargs["arg"], kwargs["condition"], newpos)] = f"{newpos}"

                # print(f"{len(done)}")
                # process any completed futures
                for future in done:
                    neweventof = futuretoevents[future]
                    try:
                        data = future.result(1)
                    except Exception as exc:
                        print("%r generated an exception: %s" % (neweventof, exc))
                    else:
                        if neweventof == "FEEDER DONE":
                            pass
                        #     print(data)
                        else:
                            if isinstance(data, int):
                                print(data)
                        #     if int(data) > highest:
                        #         highest = int(data)
                        #         print(highest)

                    # remove the now completed future
                    del futuretoevents[future]

    # def updatetimes(self, argvalue, argcondition=None):
    #     """ Add argvalue to the Timing of each event that satisfy argcondition.
    #
    #         :param argvalue: Integer, float. Can be negative values.
    #         :param argcondition: lambda or function that returns True or False. Will receive getstart() as arg.
    #         :return: self. """
    #     # self.__counter__ = 0
    #
    #     # def updatecapsule(argevent):
    #     #     if isinstance(argevent, Evento):
    #     #         raise TypeError(f"{argevent} must be an Evento instance.")
    #     #     argevent.updatetime(argvalue, argcondition)
    #     #     # print(self.__counter__)
    #     #     self.__counter__ += 1
    #
    #     # def updatecapsule(pos, fila):
    #     #     if isinstance(pos, int) is False:
    #     #         raise TypeError
    #     #     if pos < 0 or pos >= len(self.__lines):
    #     #         raise ValueError
    #     #     __value = Evento(self.__lines[pos].updatetime(argvalue, argcondition))
    #     #
    #     #     # double parenthesis because it's a tuple
    #     #     fila.put((__value, pos))
    #     #     # self.__lines[pos] = Evento(self.__lines[pos].updatetime(argvalue, argcondition))
    #     #
    #     # if True not in {isinstance(argvalue, _) for _ in [int, float]}:
    #     #     raise TypeError(f"{argvalue} must be Integer or float")
    #     #
    #     # eventos = Queue()
    #     # procs = JoinableQueue()
    #     # # counter = 0
    #     # for _ in range(len(self.__lines)):
    #     #     print(_)
    #     #     # if counter < os.cpu_count()*4:
    #     #     if procs.qsize() < os.cpu_count()*4:
    #     #         p = Process(target=updatecapsule, args=(_, eventos))
    #     #         # p.daemon = True
    #     #         p.start()
    #     #         procs.put(p)
    #     #     else:
    #     #         while procs.qsize() < os.cpu_count() * 2:
    #     #             procs.get().join()
    #
    #         # counter += 1
    #         # else:
    #         #     procs.join()
    #         #     # counter = 0
    #
    #         # if procs. > (os.cpu_count()*4):
    #         #     for p in procs:
    #         #         p.join()
    #         #     procs = []
    #     # procs.join()
    #
    #     while eventos.empty() is False:
    #         setar = eventos.get(False)
    #         print(f"({setar[1]}): {setar[0]}")
    #         self.setline(setar[0], setar[1])
    #         # setar = None
    #     # procs = []
    #     # with multiprocessing.Pool(8) as pool:
    #     #     pool.map(updatecapsule, self.__lines)

    def __repr__(self):
        """ Return Events section as a String.

            Used for saving. Called when using the String version of this object. f"{self}" i.e.

            :return: String."""

        saida = f"[Events]\n"
        if self.getformat() is not None:
            saida += f"{self.getformat()}"
        for _ in self.__lines:
            saida += f"{_}"
        return saida

    def __str__(self):
        """ Return unformatted string version of this object.

            Used for checking which values to edit.

            :return: String."""

        saida = f"[Events]\n"
        if self.getformat() is not None:
            saida += f"{self.getformat()}"
        for _ in range(len(self.__lines)):
            saida += f"({_}) - {self.__lines[_]}"
        return saida

    def getlen(self):
        """

        :return:
        """
        return len(self.__lines)

    @staticmethod
    def getalleventtypes():
        return Evento.getalleventtypes()

    def __checkline(self, argline):
        """ Checks if argline is a valid event. Returns it as Evento if true. Otherwise, return the same object.

            if format is not set, raise an assert error.

            :param argline: SimpleLine instance.
            :return: SimpleLine instance or Evento instance."""

        assert self.__formato is not None, f"Formato is not set."
        if isinstance(argline, SimpleLine) is False:
            raise TypeError(f"{argline} has to be a SimpleLine.")

        if argline.gettipo() is None:
            return argline

        # if the text before the first ":" is an event type
        if ((argline.gettipo()).strip()).lower() in self.getalleventtypes():
            # Create an event, set format, then set event type and values with readevent
            return (Evento().setformato(self.__formato.getformat())).readevent(argline)
        # Just store it as SimpleLine. Treating it as a comment
        return argline

    def readline(self, arg):
        """ Read a line and append a "SimpleLine" or an Evento to the list.

            If format is not set, only append "SimpleLine" instances.

            If it finds format, set format, then check previous lines for every valid Evento.

            If format is set, and line is a valid event, it will always append an "Evento" instance.

            :param arg: String or SimpleLine.
            :return: self."""

        def comparing(arg1, arg2):
            if arg1 is None:
                if arg2 is None:
                    return True
                return False
            if arg2 is None:
                return False
            if (isinstance(arg1, str) or isinstance(arg2, str)) is False:
                raise TypeError(f"{arg} must be a String")
            return ((arg1.strip()).lower()).startswith(arg2.lower())

        if (isinstance(arg, str) or isinstance(arg, SimpleLine)) is False:
            raise TypeError(f"{arg} must be a SimpleLine or String.")

        __value = SimpleLine(arg)

        if self.getformat() is None:
            # If it starts with:
            if comparing(__value.gettipo(), "format"):
                self.setformat(__value)
                # print(f"{type(self.getformat())}{self.getformat()}")
                replacement = []
                for _ in self.__lines:
                    # Will become Evento if valid.
                    __x__ = self.__checkline(_)
                    if isinstance(__x__, Evento):
                        # Replace all SimpleLine with Evento
                        replacement.append(__x__)

        # check if it starts with any of the valid event types
        if True in {comparing(__value.gettipo(), _) for _ in self.getalleventtypes()}:
            if self.getformat() is not None:
                __x__ = self.__checkline(__value)
                # print(f"__x__ = {__x__}          __value = {__value}")
                # print(f"__x__ = {__x__}          __value = {type(__value)}")
                # print(f"__x__ = {__x__}          type = {type(__x__)}")
                if isinstance(__x__, Evento):
                    self.__lines.append(self.__checkline(__value))
            else:
                self.__lines.append(__value)

        return self

    def getformat(self):
        """ Return Format.

            :return: Formato instance or None."""

        if self.__formato is None:
            return None
        return Formato(self.__formato)

    def setformat(self, arg):
        """ Set format.

            :param arg: String, SimpleLine instance or Formato instance.
            :return: self"""

        if isinstance(arg, SimpleLine) or isinstance(arg, str) or isinstance(arg, Formato):
            self.__formato = Formato(arg)
        else:
            raise TypeError(f"{arg} must be a SimpleLine, String, or Formato object.")
        return self

    def getlineall(self):
        """ Return all lines, "SimpleLine" instances and "Evento"s

            :return: list with "SimpleLine" instances and "Evento" instances."""

        if len(self.__lines) == 0:
            return []
        saida = []
        for _ in self.__lines:
            # If formato is None, it will never try to copy an Evento instance to the output
            if isinstance(_, SimpleLine) or isinstance(_, str) or (self.__formato is None):
                saida.append(SimpleLine(_))
            else:
                saida.append(Evento(_))
                # saida.append((Evento().setformato(self.__formato)).readevent(_))
        return saida

    def getlineevents(self):
        """ Return only Evento instances from the lines.

            :return: list with Evento instances."""

        return [Evento(x) for x in self.__lines if isinstance(x, Evento)]

    def clearinvalidlines(self):
        """ Loop through the list and clear all lines that aren't event lines.

            :return: self."""

        self.__lines = self.getlineevents()
        return self

    def setline(self, line, pos):
        """ Replace a line in position 'pos'.

            :param line: SimpleLine, String or Evento. Line to set.
            :param pos: Integer. Index position to set.
            :return: self."""

        if True not in {isinstance(line, _) for _ in [str, SimpleLine, Evento]}:
            raise TypeError(f"{line} has to be string, SimpleLine or Evento.")
        # if (isinstance(line, str) or isinstance(line, SimpleLine)) is False:
        #     raise TypeError(f"{line} has to be string or SimpleLine.")
        if isinstance(pos, int) is False:
            raise TypeError(f"{pos} has to be an Integer.")

        lista = self.getlineall()
        if len(lista) < pos:
            raise ValueError(f"There is no line in position {pos}.")

        if isinstance(line, Evento):
            if self.__formato is not None:
                __value = Evento(line)
                __value.setformato(self.__formato.getformat())
            else:
                __value = SimpleLine(f"{line}")
            self.__lines[pos] = __value
            return self

        __value = SimpleLine(line)
        if self.__formato is not None:
            # __checkline: Set it as event if valid, else set as SimpleLine
            self.__lines[pos] = self.__checkline(__value)
        else:
            self.__lines[pos] = __value
        return self

    def getline(self, pos):
        """ Return the line in position pos.

            :param pos: Integer. Index position of line.
            :return: SimpleLine or Evento instance.
            :raise ValueError: If there position is larger than the size stored."""

        if isinstance(pos, int) is False:
            raise TypeError(f"{pos} has to be an Integer.")

        # lista = self.getlineall()
        if len(self.__lines) <= pos:
            raise ValueError(f"There is no line in position {pos}.")

        return self.__lines[pos]
