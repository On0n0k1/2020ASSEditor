#!/usr/bin/env python3
"""
Extends 2020ASSEditor. Contains all the Data that will be stored about the SSA file.

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

# Built-in/Generic Imports
import os
import multiprocessing
import queue
import time

# from concurrent.futures import ProcessPoolExecutor

# Own Modules
from Dados.ScriptInfo.ScriptInfo import ScriptInfo
from Dados.V4Styles.V4Styles import V4Styles
from Dados.Events.Events import Events
from Dados.SimpleLine.SimpleLine import SimpleLine
from Dados.Events.Evento.Timing import Timing

# Search for Epydoc, MIT LICENSE, Python Packages, PEP 0440 and RestructuredText


__author__ = "Lucas Alessandro do Carmo Lemos"
__copyright__ = "Copyright (C) 2020 Lucas Alessandro do Carmo Lemos"
__license__ = "MIT"
__credits__ = []
__version__ = "0.0.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[1]


PROCESSES = min(os.cpu_count() - 2, 1)


class SubPackage:
    def __init__(self):
        self.scriptinfo = ScriptInfo()
        self.v4styles = V4Styles()
        self.events = Events()
        # self.__defaulttitles__ = ("[Script Info]", "[V4+ Styles]", "[Events]")
        self.__defaulttitles__ = [f"{_}" for _ in SimpleLine().__defaulttitles__]
        self.__lowertitles__ = [f"{_}" for _ in SimpleLine().__lowertitles__]
        self.__readers__ = (self.scriptinfo.readline, self.v4styles.readline, self.events.readline)
        # __readerpos__ stores what index of __readers__ to use
        self.__readerpos__ = None
        # Used by the main processes
        self.tasklist = multiprocessing.Queue()
        # use by getthefunctions
        self.qpos = multiprocessing.Queue()
        # used by stackprocess
        self.qnum = multiprocessing.Queue()
        # store finished processes return values for printing
        self.done = multiprocessing.Queue()
        self.nworkers = 0

    def __repr__(self):
        """ Called when printing the formatted version of this object.

            Used for saving.

            :return: String."""
        return f"{self.scriptinfo!r}\n{self.v4styles!r}\n{self.events!r}\n"

    def loadfile(self, arg):
        """ Load an SSA text file into this object.

            :param arg: String. Local Address of file.
            :return: self."""

        if isinstance(arg, str) is False:
            raise TypeError(f"{arg} must be a file address (String).")
        try:
            with open(arg, "r") as f:
                # print("File Loaded")
                # counting = -1
                # saida = ""
                for _ in f:
                    # saida += _
                    # if SimpleLine(_) is not None:
                    #     if SimpleLine(_).gettipo() is None:
                    #         print(f"({SimpleLine(_)})")
                    #      else:
                    #          print(f"{SimpleLine(_)}")

                    __line = SimpleLine(_)
                    __linelower = f"{__line}".lower()
                    __checking__ = [__ in __linelower for __ in self.__lowertitles__]
                    if True in __checking__:
                        self.__readerpos__ = __checking__.index(True)
                    else:
                        if self.__readerpos__ is not None:
                            # Call the reading function for the current section
                            (self.__readers__[self.__readerpos__])(__line)

                #     if counting < 2:
                #         if self.__sections__[counting+1] in (_.strip()).lower():
                #             counting += 1
                #             # print(_)
                #     elif counting >= 0:
                #         __line = SimpleLine(_)
                #         (self.__readers__[counting])(__line)
                # # print(saida)
        except FileNotFoundError:
            raise ValueError(f"{arg} file could not be found.")
        return self

    def savefile(self, arg):
        """ Save file into location 'arg'.

            :param arg: String. File Path to save. Will not replace existing file.
            :return: True if Save was successful. False if file already exists."""

        if isinstance(arg, str) is False:
            raise TypeError(f"{arg} must be a file address (String).")
        try:
            with open(arg, "x") as f:
                f.write(f"{self!r}")
                return True
        except FileExistsError:
            return False

    # Not sure yet how to implement formatted strings with different results. Gonna study it more later
    def __str__(self):
        """ Unformatted string Version of the file. Used for checking what lines to edit.
            :return: String."""
        return f"{self.scriptinfo!s}\n{self.v4styles!s}\n{self.events!s}\n"

    # @staticmethod
    # def stepcounter(_, __max):
    #     """
    #         Generator that yields i incremented by the number of processes up to max.
    #         :param _: first value.
    #         :param __max: stop signal.
    #         :return: Integer. Will yield i, i + PROCESSES, i + PROCESSES * 2, ...
    #     """
    #     counting = _
    #     while counting < __max:
    #         yield counting
    #         counting += PROCESSES

    def stackprocess(self, **kwargs):
        """
            Process that will stack each call to getline from each event on the process queue
            :param kwargs: See below.
            :keyword arg:
            :keyword len:

            :return: True when finished."""

        # Number of the iteration of this process which will be called from 0 to PROCESSES.
        processnumber = self.qnum.get(block=True)

        counting = processnumber
        __max = kwargs["len"]
        for _ in range(counting, __max, PROCESSES):
            arguments = {"arg": kwargs["arg"], "condition": kwargs["condition"]}
            self.tasklist.put({"target": self.getthefunctions, "kwargs": arguments})

        # for _ in self.stepcounter(processnumber, self.events.getlen()):
        #     arguments = {"arg": kwargs["arg"], "condition": kwargs["condition"]}
        #     self.tasklist.put({"target": self.getthefunctions, "kwargs": arguments})

        # Send message for the 'done' queue telling this is done
        self.done.put({"stack": True, "value": processnumber}, block=True)
        return True

    def getthefunctions(self, **kwargs):
        """

            :param kwargs:
            :keyword arg: How many centiseconds will be altered when condition is True.
            :keyword condition: Function that returns True or False receiving 2 arguments.
            :return:
            """
        # qpos = kwargs['qpos'].get()

        try:
            pos = self.qpos.get(block=True, timeout=0.2)
            arguments = (kwargs["arg"], kwargs["condition"], pos)

            self.tasklist.put({"target": self.events.getline(pos).updatetime, "kwargs": arguments})
        except queue.Empty:
            return False
        return True

    def procworker(self):
        """
            Process unique for a single CPU core.

            Process the tasks queue until it's empty.

            :return: True when done."""

        done = False
        while False in {_.empty() for _ in [self.tasklist, self.qpos, self.qnum]}:
            try:
                getthing = self.tasklist.get(timeout=1.0)
                newprocess = getthing["target"](getthing["kwargs"])
                self.done.put({"stack": False, "value": newprocess}, block=True)
                # Giving a small delay for other processes to maybe fill the queue again before ending

                for _ in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
                    if False not in {_.empty() for _ in [self.tasklist, self.qpos, self.qnum]}:
                        time.sleep(0.02)
                    else:
                        break
            except queue.Empty:
                done = True
        return done

    def cleanerworker(self):
        """
            checks through
            :return:
        """
        def drain(q):
            returnlist = []
            while True:
                try:
                    returnlist.append(q.get_nowait())
                except queue.Empty:
                    break
            return returnlist

        while False in {_.empty() for _ in [self.tasklist, self.qpos, self.qnum]}:
            for _ in drain(self.done):
                if _["stack"]:
                    self.nworkers -= 1
                    print(f"Workers = {self.nworkers}")
                else:
                    print(f"{_['value']}")
            for _ in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
                if False not in {_.empty() for _ in [self.tasklist, self.qpos, self.qnum]}:
                    time.sleep(0.02)
                else:
                    break

    def taskdistributor(self, conditions, arg):

        keyargs = {
            "arg": arg,
            "condition": conditions,
            "len": self.events.getlen()
        }

        plist = multiprocessing.JoinableQueue()
        for _ in range(PROCESSES):
            self.tasklist.put({"target": self.stackprocess, "kwargs": keyargs})
        for _ in range(PROCESSES):
            newprocess = multiprocessing.Process(target=self.procworker)
            newprocess.start()
            plist.put(newprocess)
        newprocess = multiprocessing.Process(target=self.cleanerworker())
        newprocess.start()
        plist.put(newprocess)
        plist.join()

        return self


if __name__ == "__main__":
    # def condtest(a=None, b=None):
    #
    #     if a is not None:
    #         if True not in {isinstance(a, _) for _ in {int, float, Timing}}:
    #             raise TypeError(f"{a} must be an Integer, Floating or Timing instance.")
    #
    #     if b is not None:
    #         if True not in {isinstance(b, _) for _ in {int, float, Timing}}:
    #             raise TypeError(f"{b} must be an Integer, Floating or Timing instance.")
    #
    #     if a == b:
    #         f"{a} == {b} no valid intervals to acquire"
    #     argmin = a
    #     argmax = b
    #
    #     def cond(value):
    #         xmin = argmin
    #         xmax = argmax
    #
    #         # test1 operation between value and xmin
    #         # test2 operation between value and xmax
    #         # returned value will be (test1) and (test2)
    #
    #         if (xmin is None) and (xmax is None):
    #             raise ValueError(f"Both arguments are empty.")
    #         if xmin is None:
    #             test1 = True
    #         else:
    #             test1 = value > xmin
    #         if xmax is None:
    #             test2 = True
    #         else:
    #             test2 = value < xmax
    #
    #         return test1 and test2
    #
    #     return cond

    x = SubPackage()
    x.loadfile(r"/media/clarund/Videos/[Beatrice-Raws] Jormungand [BDRip 1920x1080 x264 FLAC]/[Beatrice-Raws] "
               + r"Jormungand 01 [BDRip 1920x1080 x264 FLAC].ass")
    # print(x)
    # print(x.scriptinfo)
    # print(x.v4styles)
    # print(f"\n\n[Events]\n{x.events.getformat()}\n")
    # eventos = x.events.getlineall()
    # for _ in range(len(eventos)):
    #     print(f"({_}){type(eventos[_])}")
    # for _ in range(6, 431):
    #     print(f"{_}")
    #     __line__ = x.events.getline(_)
    #     try:
    #         __time1__ = __line__.getstart() - 1400
    #     except Timingnegativeerror as e:
    #         print(f"Negative Timing at {_} (start)")
    #         __time1__ = Timing(0)
    #     try:
    #         __time2__ = __line__.getend() - 1400
    #     except Timingnegativeerror as e:
    #         print(f"Negative Timing at {_} (end)")
    #         __time2__ = Timing(0)
    #
    #     __line__.setstart(__time1__)
    #     __line__.setend(__time2__)
    #     x.events.setline(f"{__line__}", _)

    # x.events.updatetimes(testing, 15)
    # cond1 = lambda __x__: ((__x__ > Timing([0, 2, 44, 0])) and (__x__ < Timing([0, 12, 25, 0])))
    # for _ in range(x.events.getlen()):
    #     print(_)
    #     x.events.setline(x.events.getline(_).updatetime(-1420, cond1), _)
    # dolines(x, [-1420, cond1])

    # cond2 = lambda __x__: __x__ > Timing([0, 12, 20, 0])
    # for _ in range(x.events.getlen()):
    #     print(_)
    #     x.events.setline(x.events.getline(_).updatetime(-2900, cond2), _)

    # dolines(x, [-2900, cond2])
    # cond2 = lambda __x__: __x__ > Timing([0, 12, 40, 0])
    # x.events.updatetimes(-1500, lambda __x__: ((__x__ > Timing([0, 2, 44, 0])) and (__x__ < Timing([0, 12, 25, 0]))))
    # x.events.updatetimes(-2900, lambda __x__: __x__ > Timing([0, 12, 25, 0]))

    # for _ in x.events.getlen():
    #     print(_)
    x.taskdistributor(conditions=(Timing([0, 2, 44, 0]), Timing([0, 12, 25, 0])), arg=-1420)
    x.taskdistributor(conditions=(None, Timing([0, 12, 20, 0])), arg=-2900)
    # x.events.updatetimes(arg=-1420, condition=cond1)
    # x.events.updatetimes(arg=-2900, condition=cond2)
    print(f"{x}")
    # print("x.scriptinfo")

    if x.savefile(r"/media/clarund/Videos/[Beatrice-Raws] Jormungand [BDRip 1920x1080 x264 FLAC]/Whatan.ass"):
        print("Saved")
    else:
        print("File already exists")

    # print(f"{x.scriptinfo}")
