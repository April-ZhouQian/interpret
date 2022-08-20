from __future__ import annotations
from dataclasses import dataclass
from numbers import Number
import typing
import typing_extensions

@dataclass(frozen=True)
class Call:
    func: LC
    arg: LC

@dataclass(frozen=True)
class Func:
    name: str
    body: Block

@dataclass(frozen=True)
class NamedFunc:
    name: str
    arg: str
    body: Block

@dataclass(frozen=True)
class Var:
    name: str

@dataclass(frozen=True)
class BoolVal:
    value: bool

@dataclass(frozen=True)
class NumberVal:
    value: Number

@dataclass(frozen=True)
class StringVal:
    value: str

@dataclass(frozen=True)
class AssignVal:
    var: str
    value: LC

@dataclass(frozen=True)
class Block:
    body:list[LC]

@dataclass(frozen=True)
class IfBlock:
    cond: LC
    body: Block
    else_body: Block

@dataclass(frozen=True)
class WhileBlock:
    cond: LC
    body: Block

@dataclass(frozen=True)
class ReturnBlock:
    body: LC

if typing.TYPE_CHECKING:
    LC = Var | Func | Call | NumberVal | BoolVal | StringVal | AssignVal | Block | NamedFunc | IfBlock | WhileBlock | ReturnBlock # type: ignore
else:
    LC = (Var, Func, Call, NumberVal, BoolVal, StringVal, AssignVal, Block, NamedFunc, IfBlock, WhileBlock, ReturnBlock)

@dataclass
class State:
    scope:typing.Dict[str, typing.Any]
    is_returnning: bool = False

def eval_lc(S: State, syntactic_structure: LC) -> tuple[typing.Any, State]:
    if isinstance(syntactic_structure, Var):
        return S.scope[syntactic_structure.name], S
    elif isinstance(syntactic_structure,BoolVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, StringVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, NumberVal):
        return syntactic_structure.value, S
    elif isinstance(syntactic_structure, Call):
        rf, S1 = eval_lc(S, syntactic_structure.func)
        r1, S2 = eval_lc(S1, syntactic_structure.arg)
        r2, S3 = rf(S2, r1)
        return r2, S3
    elif isinstance(syntactic_structure,Func):
        def rf(S_star: State, r_star):
            a = syntactic_structure.name
            S1 = State({**S.scope, a: r_star})
            r1 = None
            r1, S1 = eval_lc(S1, syntactic_structure.body)
            return r1, S_star
        return rf, S
    elif isinstance(syntactic_structure, AssignVal):
        value = eval_lc(S, syntactic_structure.value)[0]
        S_New = State({**S.scope, syntactic_structure.var: value})
        return value, S_New
    elif isinstance(syntactic_structure, Block):
        r = None
        for item in syntactic_structure.body:
            if S.is_returnning == False:
                r, S = eval_lc(S, item)
            else:
                break
        return r, S
    elif isinstance(syntactic_structure, NamedFunc):
        def rf(S_star: State, r_star):
            arg = syntactic_structure.arg
            S1 = State({**S.scope, arg: r_star})
            r1 = None
            r1, S1 = eval_lc(S1, item)
            return r1, S_star
        name = syntactic_structure.name
        S = State({**S.scope, name: rf})
        return rf, S
    elif isinstance(syntactic_structure, IfBlock):
        r = eval_lc(S,syntactic_structure.cond)[0]
        r1 = None
        if r:
            r1, S = eval_lc(S, syntactic_structure.body)
        else:
            r1, S = eval_lc(S, syntactic_structure.else_body)
        return r1, S
    elif isinstance(syntactic_structure, WhileBlock):
        r = None
        while(eval_lc(S,syntactic_structure.cond)[0]):
            r, S = eval_lc(S, syntactic_structure.body)
        return r, S
    elif isinstance(syntactic_structure, ReturnBlock):
        r, S = eval_lc(S, syntactic_structure.body)
        S.is_returnning = True
        return r, S
    if typing.TYPE_CHECKING:
        typing_extensions.assert_never(syntactic_structure)
    else:
        raise TypeError(syntactic_structure)