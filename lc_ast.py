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
class Return:
    body: LC

if typing.TYPE_CHECKING:
    LC = Var | Call | NumberVal | BoolVal | StringVal | AssignVal | Block | NamedFunc | IfBlock | WhileBlock | Return # type: ignore
else:
    LC = (Var, Call, NumberVal, BoolVal, StringVal, AssignVal, Block, NamedFunc, IfBlock, WhileBlock, Return)

@dataclass
class State:
    scope:typing.Dict[str, typing.Any]
    is_returning: bool

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
    elif isinstance(syntactic_structure, NamedFunc):
        def rf(S_star: State, r_star):
            arg = syntactic_structure.arg
            S1 = State({**S.scope, arg: r_star}, S.is_returning)
            r1 = None
            r1, S1 = eval_lc(S1, syntactic_structure.body)
            return r1, S_star
        name = syntactic_structure.name
        if name != '':
            S = State({**S.scope, name: rf}, S.is_returning)
        return rf, S
    elif isinstance(syntactic_structure, AssignVal):
        value = eval_lc(S, syntactic_structure.value)[0]
        S_New = State({**S.scope, syntactic_structure.var: value}, S.is_returning)
        return value, S_New
    elif isinstance(syntactic_structure, Block):
        r = None
        for item in syntactic_structure.body:
            if S.is_returning == False:
                r, S = eval_lc(S, item)
            else:
                break
        return r, S
    elif isinstance(syntactic_structure, IfBlock):
        r, S = eval_lc(S, syntactic_structure.cond)
        r1 = None
        if r:
            r1, S = eval_lc(S, syntactic_structure.body)
        else:
            r1, S = eval_lc(S, syntactic_structure.else_body)
        return r1, S
    elif isinstance(syntactic_structure, WhileBlock):
        r1 = None
        r, S = eval_lc(S,syntactic_structure.cond)
        while(r):
            r1, S = eval_lc(S, syntactic_structure.body)
            r, S = eval_lc(S, syntactic_structure.cond)
        return r1, S
    elif isinstance(syntactic_structure, Return):
        r, S = eval_lc(S, syntactic_structure.body)
        S_New = State({**S.scope}, True)
        return r, S_New
    if typing.TYPE_CHECKING:
        typing_extensions.assert_never(syntactic_structure)
    else:
        raise TypeError(syntactic_structure)