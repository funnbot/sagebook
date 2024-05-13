from sage.matrix.matrix_rational_dense import Matrix_rational_dense
from sage.structure.element import Element
from sage.modules.vector_rational_dense import Vector_rational_dense
from sage.all import matrix, vector, SR
from sage.repl.rich_output import get_display_manager
from sage.repl.rich_output.pretty_print import pretty_print
from sage.repl.rich_output.output_basic import OutputAsciiArt
from sage.modules.free_module_element import FreeModuleElement, is_FreeModuleElement
from sage.misc.latex import latex, LatexExpr
from sage.rings.ring import Ring
from sage.matrix.matrix_generic_dense import Matrix_generic_dense

import inspect
from pprint import pprint
from pprint import PrettyPrinter

cfg_ring: Ring = SR


def vec(*entries: Element) -> FreeModuleElement:
    return vector(cfg_ring, entries)


def mat(*entries: list[Element]) -> Matrix_generic_dense:
    return matrix(cfg_ring, entries)

def diag(*entries: Element) -> Matrix_generic_dense:
    return matrix.diagonal(cfg_ring, entries, sparse=False)

def project(v: FreeModuleElement, basis: list[FreeModuleElement]) -> FreeModuleElement:
    result = v.parent().zero()
    for b in basis:
        assert(is_FreeModuleElement(b))
        assert(b.parent() == v.parent())
        c = v.dot_product(b) / b.dot_product(b)
        result = result + c * b
    return result


def set_ring(ring: Ring):
    global cfg_ring
    cfg_ring = ring


def p(*args: any):
    def convert(a: any) -> LatexExpr | str:
        if isinstance(a, str):
            return a
        elif is_FreeModuleElement(a):
            return latex(a.column())
        elif isinstance(a, list):
            return (r"\left( {} \right)").format(
                " , ".join(
                    [str(convert(v)) for v in a]))
        elif isinstance(a, tuple):
            return "".join([str(convert(v)) for v in a])
        else:
            return latex(a)
    ltx = LatexExpr((" ").join([str(convert(v)) for v in args]))
    pretty_print(ltx)


def set_display(pref: str):
    dm = get_display_manager()
    dm.preferences.text = pref


def type_tree(val: any):
    pprint(inspect.getclasstree(inspect.getmro(type(val)), unique=True),
           compact=True, )