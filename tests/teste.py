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
__version__ = "0.0.1"
__maintainer__ = "Lucas Alessandro do Carmo Lemos"
__email__ = "stiltztinkerstein@gmail.com"
__status__ = (["Prototype", "Development", "Production"])[2]

# import sys
# "from Dados.BasicStructure import BasicStructure"
#
# "from Dados.Script_Info.Script_Info import Script_Info"
# loadPath = r"""C:\Users\Clarund\Documents\Programming\Python\EditorSSA"""
# if loadPath in sys.path:
#     pass
# else:
#     sys.path.append(f"{loadPath}")

"""import EditorSSA

from Dados.V4Styles.V4Styles import V4Styles
"""
"""
from Dados.BasicStructure.SimpleLine.SimpleLine import SimpleLine
from Dados.Script_Info.Script_Info import Script_Info
"""
"""
def testandoSimpleLine():
    linha = SimpleLine(0,"Tipo","Nome")

    print(f"Posicao: {linha.getPosicao()}")
    print(f"Tipo: {linha.getTipo()}")
    print(f"Texto: {linha.getTexto()}")

    linha.setPosicao(2)
    linha.setTipo("NovoTipo")
    linha.setTexto("NovoTexto")

    
    print(f"Posicao: {linha.getPosicao()}")
    print(f"Tipo: {linha.getTipo()}")
    print(f"Texto: {linha.getTexto()}")
"""


def testandofloat():
    i = 0

    if isinstance(i, float):
        print("yes")
    else:
        print("no")

    """
    "teste de teste de integer"
    "print(type(i))"
    if(type(i)=="<class 'int'>"):
        print("yes")
    else:
        print("no")
    """
    "Teste de BasicStructure (deve ser alterado)"
    """
    print("Testando")
    parametrizando = ["teste1", "teste2", "teste3", "teste4"]
    valores = ["primeirotexto", "segundotexto", "terceiroTexto", "quartoTexto"]
    testeBasicStructure = BasicStructure.BasicStructure(parametrizando)
    for i in range(len(valores)):
        testeBasicStructure.adicionar(parametrizando[i],valores[i])
    for i in range(testeBasicStructure.getListaLen()):
        print("{}: {}".format(parametrizando[i],testeBasicStructure.getValor(parametrizando[i])))
    for i in range(10):
        print(testeBasicStructure.getValor("potato"))
    """

    """
    "Teste de Script_info"
    teste = ["primeiralinha", "segundalinha", "TerceiraLinha", "QuartaLinha"]
    novoInfo = Script_Info(teste)
    novoInfo.setLines(["potato", "potato", "potatoo"])
    testando = novoInfo.getLines()
    for i in testando:
        print(i)
    """


"""    

"testandoSimpleLine()"

def testeScript_Info():
    objeto = Script_Info()
    objeto.leitura(SimpleLine(0,"teste","testnado"))
    objeto.leitura(SimpleLine(1,"null","testnado"))
    objeto.leitura(SimpleLine(2,"cabbages","potato"))
    objeto.leitura(SimpleLine(3,"teste","ssss"))
    objeto.leitura(SimpleLine(4,"teste","pootis"))
    objeto.testando()

def testeString():
    x = "potato"
    y = str(x)
    print(y)


testeString()

"""


"""
a=1
print(type(a)==int)
assert type(a)==int, f"{a} should be int"

a=""
print(type(a)==str)
assert type(a)==str, f"{a} should be str"

a=0.1
print(type(a)==float)
assert type(a)==float, f"{a} should be float"

a=True
print(type(a)==bool)
assert type(a)==bool, f"{a} should be Bool"


"""
"""
print("1"==1)
print("sSsSsS".lower())"""


"x = V4Styles()"
"x.Format.teste()"

"""
if(type([])==list):
    print('yep')
"""

"""
class Testing():
    def __init__(self, a, b=None, c=None):
        if c is None:
            if b is None:
                print(f"a: {a}")
            else:
                print(f"a: {a}  b: {b}")
        else:
            print(f"a: {a}  b: {b}  c: {c}")


if __name__ == "__main__":
    Testing(1)
    Testing(1, 2)
    Testing(1, 2, 3)
"""

# if __name__ == "__main__":
#     S = [x**2 for x in range(10) if x > 5]
#     V = [2**i+b for *i, *b in (range(13))(range(10)) if i < 8]
#
#    print(S)
#    print(V)

# Using the generator pattern (an iterable)


class Firstn(object):
    def __init__(self, n):
        self.n = n
        self.num = 0

    def __iter__(self):
        return self

    # Python 3 compatibility
    def __next__(self):
        return self.next()

    def next(self):
        if self.num < self.n:
            cur, self.num = self.num, self.num+1
            return cur
        else:
            raise StopIteration()


def fib(maxvalue):
    a, b = 0, 1
    while 1:
        yield b
        a, b = b, a+b
        if b > maxvalue:
            return b


def testecount(lista):
    return lista.count(None)


if __name__ == "__main__":
    # sum_of_first_n = sum(Firstn(100))
    # print(sum_of_first_n)
    # for _ in Firstn(100):
    #     print(_)

    # for _ in fib(100000):
    #     print(_)
    """
    print(list(fib(500)))

    a = fib(500)
    for _ in range(20):
        try:
            print(a.__next__())
        except StopIteration:
            break
    """
    # try:
    #     int("ss")
    # except ValueError:
    #    print("ss")
    # print(testecount(["a", None, 2, None, [None, None, 3], None]))
    # raise ValueError("agaeygyaegyae")

    try:
        raise ValueError(f"wololooo")
    except ValueError as errag:
        print(errag.args[0])
        print(errag.args)
        print(errag.__dict__)
        print(errag.__cause__)
