
class Sort:

    def key(self, context):
        return None


class Alphabetical (Sort):

    @staticmethod
    def key(context):
        return context.name

    # my strategy:
    # understand the module
    # archetect the softrware
    # implamentation


class Unsorted:

    def __init__(self, ast_node, sorter):
        self.context = ast_node
        self.sorter = sorter
        self.grouping = [
            ast.alias,
            ast.Import,
            ast.ImportFrom,
            ast.ClassDef,
            ast.FunctionDef]
        self.mapper = Assign(self.sorter)

    def children(self):
        return self.context.body

    def sort(self):
        self.organize()
        self.context.body = self.get_sorted()

    def node_sorter(self, children):    
        s_nodes = {self.sorter.key(n): n for n in children}
        return [s_nodes[n] for n in sorted(s_nodes.keys())]


    def get_sorted(self):
        out = []
        for group_class in self.grouping:
            if group_class in self.groups:
                    out.extend(self.node_sorter(self.groups[group_class]))
        return out

    def organize(self):
        self.groups = {}
        for child in self.children():
            child_type = type(child)
            if child_type not in self.groups:
                self.groups[child_type] = []
            self.mapper.sort(child)
            self.groups[child_type].append(child)


class Assign:

    def __init__(self, sorter):
        self.sorter = sorter
        self.class_map = {ast.Import: Unsorted_Import, ast.ClassDef:Unsorted}

    def sort(self, ast_node):
        n_type = type(ast_node)
        if n_type in self.class_map:
            u = self.class_map[n_type](ast_node, self.sorter)
            u.sort()


class Unsorted_Import(Unsorted):

    def children(self):
        return self.context.names

    def sort(self):
        sorted_aliases = self.get_sorted()
        self.context.name = ",".join([a.name for a in sorted_aliases])
        self.context.names = sorted_aliases

    def get_sorted(self):
        return self.node_sorter(self.children())    

import ast
import codegen
import copy

expr = """

def bfoo():
    return 1

import zfoo, afoo,dfoo 

class ba():

    def foo():
       print("hello world")

import afoo

def afoo():
    return 2

class a1():

    def bfoo():
       print("hello world 2")

    def afoo():
       print("hello world 2")

"""
p = ast.parse(expr)

u = Unsorted(p, Alphabetical())
u.sort()

d = p
  # Replace function body with "return 42"

print(codegen.to_source(u.context))

# codegen.to_source(p.body[1])
