import ast
import inspect

# https://stackoverflow.com/a/31197273
def get_decorators(cls):
    target = cls
    decorators = {}

    def visit_FunctionDef(node):
        decorators[node.name] = []
        for n in node.decorator_list:
            name = ""
            if isinstance(n, ast.Call):
                name = n.func.attr if isinstance(n.func, ast.Attribute) else n.func.id
            else:
                name = n.attr if isinstance(n, ast.Attribute) else n.id

            decorators[node.name].append(name)

    node_iter = ast.NodeVisitor()
    node_iter.visit_FunctionDef = visit_FunctionDef
    node_iter.visit(ast.parse(inspect.getsource(target)))
    return decorators


def is_builtin(annotation):
    return (
        annotation.__module__ is None
        or annotation.__module__ == str.__class__.__module__
    )


def is_primitive(t, prim_list=set({str, int, float, bool, object})):
    return t in prim_list


def is_union(t):
    return type(t) is type(Union)


# https://stackoverflow.com/a/2020083
def full_name(annotation):
    module = annotation.__module__
    if is_builtin(annotation):
        return annotation.__name__  # Avoid reporting __builtin__
    else:
        return module + "." + annotation.__name__


if __name__ == "__main__":
    from orangegraph.graph_functions import dpath

    print(get_decorators(dpath))
