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

# import sys
# loadPath = r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA"""

# if r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA""" in sys.path:
#     pass
# else:
#    sys.path.append(r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA""")
# """ How to setup EditorSSA as source root for importing in Pycharm:
#     Go to:
#
#         File -> Settings
#
#         Select
#         Build, Execution, Deployment -> Console -> Python Console
#
#             Make sure that "Add source roots to PYTHONPATH" is marked.
#
#     Right click "EditorSSA" In the Project window, left of the screen, go to "Mark directory as", then "Mark as
#     sources root".
#
#     Last Note: I forgot which to use, so I set both EditorSSA and Dados as sources root. If things go south. Try that.
#
#     """


from Dados.Events.Evento.Timing import Timing

if __name__ == "__main__":
    for _ in range(0, 5):
        print(Timing([_]))
        print(Timing([_, 0]))
        print(Timing([_ + 2, 0, _]))
        print(Timing([_, _ + 1, _ + 2, _ + 10]))
        print("---")
