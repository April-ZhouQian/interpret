from lc_demo.lc_ast import *
from lc_demo.lc import parser
from lc_demo.intrinsic_function import *
import wisepy2
from prompt_toolkit import prompt
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.matlab import MatlabLexer
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

lc_completer = WordCompleter(
    ["if", "else", "while", "return", "function", "exit"], ignore_case=True
)
S = State(
    {
        "or": logic_or,
        "and": logic_and,
        "not": logic_not,
        "add": add,
        "sub": sub,
        "lt": lt,
        "gt": gt,
        "ge": ge,
        "le": le,
        "eq": eq,
        "div": div,
        "mul": mul,
        "mod": mod,
        "printf": printf,
        'exit': exit
    },
    is_returning=False,
)

@wisepy2.wise
def mi(*filenames: str):
    if not filenames:
        repl(S)
        return
    for filename in filenames:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
        ast = parser.parse(source_code)
        eval_lc(S, ast)


def prompt_continuation(width, line_number, is_soft_wrap):
    return "." * width


def run_state(S, source_code):
    ast = parser.parse(source_code)
    r, S = eval_lc(S, ast)
    print("执行结果：", r)
    return S

def repl(S: State):
    session = PromptSession(lexer=PygmentsLexer(MatlabLexer), completer=lc_completer)
    text = ""
    while True:
        text = session.prompt(
            "mi> ",
            multiline=True,
            prompt_continuation=prompt_continuation,
            auto_suggest=AutoSuggestFromHistory(),
        )
        S= run_state(S, text)


