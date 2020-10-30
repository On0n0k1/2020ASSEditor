
    # I used a subtitle file generated by the website aegisub, which is 100x better than myne. Please consider 
    # supporting them. I'm only making this project to add to my curriculum. No intention of finishing
    # I wrote a lot more here yesterday. But accidentaly told git to pull instead of push what was written...

# 2020ASSEditor
Editor for SubStation Alpha (.ass) format subtitle files. First main reason for this project is to add to my curriculum.
Second main reason is for it to be easy to expand and read. Third main reason is for it to be a good example to use for 
anyone studying python that want to check on a larger project. Even with 4000 lines of code, most of what this code is 
doing is treating 'strings and numbers' in a useful way. It takes a large piece of text, splits into each of the 
individual useful pieces of data and store them to be modified however the user wants.

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

## How it works


## How to use the code


## Developer Note
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

* All Multiprocessing calls need to be "protected" inside an if _\__name_\__ == '_\__main_\__' clause.

* I wanted to create an iterator of methods that are eligible. Create a process that gets a function from this iterator.
 Do the operation. Return the result. And another process assigns the result to the main objects. A single method that 
 do all of this.

* But since it must be picklable. I have to create one method for each operation using multiprocessing.

* From this I hope I made my point that the code would be way too hard to read and use properly. Which is why I decided 
to learn how to use the ray framework. I'm still reading and practicing it today (10/28/20). Once I'm confident with it,
I will use it in "SubPackage".

