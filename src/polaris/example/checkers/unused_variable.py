import ast
from polaris.base.base_linter import BaseChecker, Offense, Severity

SEVERITY = Severity.WARNING

class _UnusedVarInScopeChecker(BaseChecker):

    def __init__(self, offense_code: str):
        self._name_nodes:       dict[str,ast.Name]  = {}
        self._unused_var_names: dict[str,bool]      = {}
        super().__init__(offense_code)

    def reset(self):
        self._name_nodes:       dict[str,ast.Name]  = {}
        self._unused_var_names: dict[str,bool]      = {}
        super().reset()    

    def visit_Name(self, node: ast.Name):
        var_name = node.id 

        if isinstance(node.ctx, ast.Store):
            # var not seen before, we add
            if var_name not in self._name_nodes.keys():
                self._name_nodes[var_name] = node 

            # var not in unused names, we add
            if var_name not in self._unused_var_names.keys():
                self._unused_var_names[var_name] = True

        else:
             # var was seen and is used somewhere else
             self._unused_var_names[var_name] = False

class UnusedVarChecker(BaseChecker):

    def __init__(self,offense_code):
        self._current_scope = ""
        super().__init__(offense_code)

    def reset(self):
        self._current_scope = ""
        super().reset()

    def check_unused_vars(self, node: ast.AST):
        visitor = _UnusedVarInScopeChecker(self.offense_code)
        visitor.visit(node)

        for name, is_unused in visitor._unused_var_names.items():
            if is_unused:
                visitor._name_nodes[name] = node
                offense = Offense(
                    node        = node,
                    message     = f"variable {name} is not used within its {self._current_scope} scope",
                    severity    = SEVERITY
                )
                self.offenses.add(offense)


    def visit_Module(self, node: ast.Module):
        self._current_scope = "module"

        if not hasattr(node, "lineno"):
            node.lineno     = 0

        if not hasattr(node, "end_lineno"):
            node.end_lineno = 0

        self.check_unused_vars(node)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._current_scope = "function"
        self.check_unused_vars(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        self._current_scope = "class"
        self.check_unused_vars(node)
        self.generic_visit(node)