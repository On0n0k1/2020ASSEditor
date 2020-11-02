# 2020ASSEditor
[(Table of Contents)](https://github.com/On0n0k1/2020ASSEditor#table-of-contents)

Editor for SubStation Alpha (.ass) format subtitle files. First main reason for this project is to add to my curriculum.
Second main reason is for it to be easy to expand and read. Third main reason is for it to be a good example to use for 
any python learner wanting to check on a larger project. Even with 4000 lines of code, most of what this code is doing 
is treating 'strings and numbers' in a useful way. It takes a large piece of text, splits into each of the individual 
useful pieces of data and store them to be modified however the user wants.

The number of lines doesn't get in the way in terms of understanding what it does. There are the 'macro' objects 
(ScriptInfo, V4Styles and Events), and the 'micro' objects that extend them. Each of these objects encompasses their own
scope. And only 'higher' objects have methods that interfere with the parts that they contain. I.E. V4Styles have a list
of Styles ("Estilo"), each style doesn't intefere with one another. But V4Styles have methods that may use or change 
each individual Style ("Estilo").

More tools for editing these values will be added later. There's no UI planned for this software at the moment. But 
there are expectations for adding multiprocessing and more practical methods for all the objects. As in: instead of 
checking element individually. Calling only one method to change all the elements we want to change. Developer Note: I'm 
delaying this until I can make an implementation that use the Ray multiprocessing framework.
 
Hopefully this readme will be useful in clearing every question the readers might have about the software.

## Table of Contents
* [Title](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)
* [How to use the code](https://github.com/On0n0k1/2020ASSEditor#how-to-use-the-code)
* [How it works](https://github.com/On0n0k1/2020ASSEditor#how-it-works)
* [How to contribute](https://github.com/On0n0k1/2020ASSEditor#how-to-contribute)
* [Why I will not completely finish this project](https://github.com/On0n0k1/2020ASSEditor#why-i-will-not-completely-finish-this-project)
* [License](https://github.com/On0n0k1/2020ASSEditor#license)
* [Developer Extra Note](https://github.com/On0n0k1/2020ASSEditor#developer-extra-note)
* [Latest addition](https://github.com/On0n0k1/2020ASSEditor#latest-addition)


## How to use the code
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

There's a 'download zip' bottom up there. But I prefer just using git instead.

- Install git
- Open command prompt
- Go to an empty folder that you want to copy using ls and cd
- Do:
- git clone https://github.com/On0n0k1/2020ASSEditor.git

## How it works
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

A .ass file is divided into 3 main sections:
* Script Info: File header and metadata
* V4+ Styles: Font and text styles that may be used by the subtitles
* Events: Every event that happens during the video. Include subtitles, but may also have other effects like pictures or
video. 

There is a folder for each one of these sections inside the folder 'Dados'. Each of these folders will also have the 
class definitions for the elements they may have.

Apart from these 3 main classes, there's one more with the name "SimpleLine". This object is intended to receive a 
String line and check if it is in the format "{Type}:{Text}". If it's not, Type will be None and Text will be the whole 
line. This class saves up a lot of code. And is used by the other classes when reading or saving the file.

V4Styles and Events both need a line named "Format: ". This line tells what each column stores. Currently, if the 
project read a Style or Event without reading "Format:", it will raise an exception. V4Styles doesn't have a limited 
number of columns, but Events will always have 10 columns. Last column in Events must always be Text, so that it can 
receive subsequent ',' as just part of it.

Couldn't find clear documentation on what each of the columns in Styles are for. So just reading Strings. Couldn't find 
clear documentation on what types of ScriptInfo headers may be read. So just reading Strings as well. Couldn't find 
clear documentation on Event effects like Karaoke. So it's basically an empty object that prints as "Karaoke". There is 
documentation on what commands we can add on Text, but implementing code for understanding each one individually will 
cost a few hundreds of code lines. So just reading an object that store a String.

Because of this, I ran into a wall after spending a reasonable amount of time writing a lot of code. Didn't want to 
throw everything away and start from scratch with another project. So I'm keeping this project here just to help people 
with understanding some of Python's core tools. Like my friends in my university.

There are some classes people may find interesting. I really recommend taking a look on the 'Timing' class. It is 
located in '\Dados\Events\Eventos\Timing.py'. It prints time in the format "H:MM:SS.CS". It can be turned into integer 
as centiseconds. It can be turned into float as seconds. It also supports operations with integers and float. As well as
comparisons with these values. The file can be compiled directly. And it will run several lines of assert operations to 
make sure that all the comparisons and operations will work properly.

To summarize. SubPackage will use ScriptInfo, V4Styles and Events. When it reads a file, it will distribute each piece 
of the text to it's children. For printing and saving, it will call it's children String formats too. Each object can be 
incremented with more tools without making the rest of the code less readable. Later I will add the JSON for each of the
objects below.

## How to contribute
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

Until I get a job in development, I intend to not take contributions for the time being. Just to make sure that the 
reader can see what I know in practice. As soon as I get a job and start getting more experience, I will allow others 
to support this code's development.

Nothing stops you from downloading this code and developing yourself. I just ask for credit in that case. My name is 
Lucas Alessandro do Carmo Lemos, and my github account name is On0n0k1. I'm very grateful for those who use and mention
the source.

## Why I will not completely finish this project
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

I thought that it would be a good idea to make an editor for subtitle files. All that I would need to do was check the 
documentation and tutorials on what it means and how it works. But unfortunately, on the little amount of docs I had 
access to, a lot of the details were missing. There are enough details for someone willing to open the file on a text 
editor and change it themselves. But there isn't enough to know what all of the effects do and how they work.

There isn't enough documentation about the metadata on the script info. There is open source software for dealing with 
these codes. But I don't think that it is worth the time and effort to go through everything when there are so many more
projects for me to do as well, which include REST APIs. This project would take a lot of work in order to be competitive
with the other available software out there. And I just want this to add to my curriculum.

## License
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

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


## Developer Extra Note
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

The individual parts of the code are working. But since the process is limited to a single core, It is annoying to wait 
for it through the CPU-intensive part of the process where it is going through all the subtitles checking and changing 
all the wanted elements. If it takes 0.5 seconds for each subtitle to be edited, a file with 600 lines would take 5 
minutes to finish. Which is unacceptable when the time can be divided by the number of CPU cores available on the 
system.

My computer has 8 cores. There are processors with 64 cores out already. There's no way to not use multiprocessing here
if it means pushing 300 seconds to 37.5 seconds or 4.68 seconds using the same code.

For Python, we can't simply multithread the program due to the Global Interlocking Cooldown (GIL). GIL forces only one 
processor to access an individual instance of the code at the time. In order to take the best of the CPU, multiple 
processes should be used instead.

At first I thought about using Python's Multiprocessing module. But the more I learned about the module, and the more I 
used it, more issues end up emerging. Here are the worst bottlenecks I found:

* Arguments for functions that are being used in multiprocessing must be picklable. Which makes code lose a lot of the 
traits that made Python so practical as a language. There's "duct tape" code to fix that though.

* In the current version docs (3.8.6) for multiprocessing, it is admitted that using fork "context and start" method 
may cause some issues. Good luck trying to find "what" errors may rise from using it. Fork is default for Unix systems.

* All Multiprocessing calls need to be "protected" inside an 'if \_\_name\_\_ == "\_\_main\_\_"' clause.

I wanted to create an iterator of methods that are eligible. Create a process that gets a function from this iterator.
Do the operation. Return the result. And another process assigns the result to the main objects. A single method that 
do all of this. But since it must be picklable. Generators, function objects, lambda objects and many other tools can't 
be used. If the main tools for Python are not available, why not just code with c++ instead?

From this I hope it is understandable that the code would be way too hard to read and use properly. Which is why I'm 
currently learning how to use Ray framework. Updates will come later.

## Latest addition
[(Back to the top)](https://github.com/On0n0k1/2020ASSEditor#2020asseditor)

Currently I'm creating an object for dealing with file management. It should be an object that selects a path for input 
and output folders when created. And it will handle file loading and saving for the user. At first, I was thinking about
letting it automatically generate an output file writing something like "{filename}{filenumber}" where {filenumber} is 
the lowest available number in that folder. Therefore writing in order as in "attempt1", "attempt2", "attempt3" and so 
on. For loading it was better to just use a file selector using Tkinter instead. So I'm currently reading the docs on 
how to use the module.
