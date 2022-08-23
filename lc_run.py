from cProfile import run
import re
from lc import parser
from lc_ast import *
from intrinsic_function import *

S = State(
    {"or": logic_or, "and": logic_and, "not": logic_not, "add": add, "sub": sub, "lt": lt, "gt": gt, "ge": ge, "le": le, "eq": eq, "div": div, "mul": mul, "mod": mod},
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
    1 + 2 && 2
}
""")

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
