from lc_demo.lc_ast import *
from lc_demo.lc import parser
from lc_demo.intrinsic_function import *
from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.matlab import MatlabLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

lc_completer = WordCompleter([
    'if', 'else', 'while', 'return','function'], ignore_case=True)

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

S_ = S

def prompt_continuation(width, line_number, is_soft_wrap):
    return '.' * width

session = PromptSession(lexer = PygmentsLexer(MatlabLexer))
text =""
while True:
    text = session.prompt('mi>>>> ', multiline=True,
       prompt_continuation = prompt_continuation, auto_suggest = AutoSuggestFromHistory())
    S_ = run_state(S_, text)

