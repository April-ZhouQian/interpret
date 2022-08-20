# Generated from lark-action.


from lc_ast import *
def append(lst, element):
    lst.append(element)
    return lst

if '_get_location' not in globals(): 
    def _get_location(token):
        return (token.line, token.column)

if '_get_value' not in globals(): 
    def _get_value(token):
        return token.value


from lc_raw import Transformer, Lark_StandAlone, Tree
class lc_Transformer(Transformer):

    def start_0(self, __args):
        return  __args[1-1]
    def lc_0(self, __args):
        return  Call(__args[1-1], __args[2-1])
    def lc_1(self, __args):
        return  __args[1-1]
    def stmts_0(self, __args):
        return  [__args[1-1]]
    def stmts_1(self, __args):
        return  append(__args[1-1], __args[2-1])
    def atom_0(self, __args):
        return  Var(__args[1-1].value)
    def atom_1(self, __args):
        return  NumberVal(eval(__args[1-1].value))
    def atom_2(self, __args):
        return  BoolVal(True)
    def atom_3(self, __args):
        return  BoolVal(False)
    def atom_4(self, __args):
        return  Func(__args[3-1].value, Block(__args[6-1]))
    def atom_5(self, __args):
        return StringVal(eval(__args[1-1].value))
    def atom_6(self, __args):
        return  __args[2-1]
    def atom_7(self, __args):
        return AssignVal(__args[1-1].value, __args[3-1])
    def atom_8(self, __args):
        return  Block(__args[2-1])
    def atom_9(self, __args):
        return  IfBlock(__args[3-1], Block(__args[6-1]), Block([]))
    def atom_10(self, __args):
        return  IfBlock(__args[3-1], Block(__args[6-1]), __args[10-1])
    def atom_11(self, __args):
        return  WhileBlock(__args[3-1], Block(__args[6-1]))
    def atom_12(self, __args):
        return  ReturnBlock(__args[2-1])
    def atom_13(self, __args):
        return  NamedFunc(__args[2-1].value, __args[4-1].value, Block(__args[7-1]))


parser = Lark_StandAlone(transformer=lc_Transformer())
