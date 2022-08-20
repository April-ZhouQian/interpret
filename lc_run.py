from cProfile import run
from lc import parser
from lc_ast import *

def lt(S,x):
    def lty(S, y):
        return x < y, S
    return lty, S
def sub(S, x):
    def suby(S, y):
        return x - y, S
    return suby, S
def add(S, x):
    def addx(S, y):
        return x + y, S
    return addx, S

S = State(
    {"add": add, "sub": sub, "lt": lt},
    is_returnning = False
)
def run_code(source_code):
    ast = parser.parse(source_code)
    print("执行结果：", eval_lc(S, ast)[0])

def run_state(S, source_code):
    ast = parser.parse(source_code)
    r, S = eval_lc(S, ast)
    print("执行结果：", r)
    return S

run_code("lt 1 2")
run_code("""
if(lt 1 2)
{
    a = 3;
    b = 4;
    add a b;
}
else
{
    a = 10;
}
"""
)

run_code("""
{
    a = 10;
    b = 1;
    while(lt a 11)
    {
        a = add a 1;
        b = add b 1;
    }
}
"""
)
run_code("sub 2 1")
run_code("a = 7")
run_code("""
{
f = func (x) {
    x = add x 1;
    return x;
    x = add x 6;
    x = add x 10;
};
f(1)
}
""")
S_ = S
while True:
    S_ = run_state(S_, input("输入LC表达式> "))
