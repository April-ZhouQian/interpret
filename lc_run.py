from cProfile import run
import re
from lc import parser
from lc_ast import *

def sub(S, x):
    return x[0]- x[1], S
def add(S, x):
    return x[0] + x[1], S
def div(S, x):
    return x[0] / x[1], S
def mul(S, x):
    return x[0] * x[1], S
def mod(S, x):
    return x[0] % x[1], S
def lt(S, x):
    return x[0] < x[1], S
def gt(S, x):
    return x[0] > x[1], S
def ge(S, x):
    return x[0] >= x[1], S
def le(S, x):
    return x[0] <= x[1], S
def eq(S, x):
    return x[0] == x[1], S
S = State(
    {"add": add, "sub": sub, "lt": lt, "gt": gt, "ge": ge, "le": le, "eq": eq, "div": div, "mul": mul, "mod": mod},
    is_returning = False
)
def run_code(source_code):
    ast = parser.parse(source_code)
    print("执行结果：", eval_lc(S, ast)[0])

def run_state(S, source_code):
    ast = parser.parse(source_code)
    r, S = eval_lc(S, ast)
    print("执行结果：", r)
    return S

run_code("""
{
func myfunc()
{
    y = add(1,2);
    return 7;
}
y = myfunc();
}
""")

run_code("9 * 4 /2 + 2")
run_code("""
if(lt(1,2))
{
    a = 3;
    b = 4;
    add(a,b);
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
    while(lt(a, 11))
    {
        a = add(a, 1);
        b = add(b, 1);
    }
}
"""
)
S_ = S
while True:
    S_ = run_state(S_, input("输入LC表达式> "))
