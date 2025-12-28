import ast
from typing import Tuple, List

class CodeValidator:
    def __init__(self):
        self.allowed_imports = [
            'matplotlib', 'numpy', 'pygame', 'turtle', 'math', 'random', 'time', 'sys'
        ]
        self.forbidden_functions = ['exec', 'eval', 'open', '__import__', 'os.system', 'subprocess']

    def validate_syntax(self, code: str) -> Tuple[bool, str]:
        try:
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, str(e)

    def validate_safety(self, code: str) -> Tuple[bool, List[str]]:
        errors = []
        tree = ast.parse(code)
        
        for node in ast.walk(tree):
            # Check imports
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in (node.names if isinstance(node, ast.Import) else [node.module]):
                    name = alias.name if isinstance(node, ast.Import) else alias
                    if name and not any(name.startswith(pkg) for pkg in self.allowed_imports):
                        errors.append(f"Import non autorisé : {name}")
            
            # Check forbidden functions
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in self.forbidden_functions:
                    errors.append(f"Fonction interdite : {node.func.id}")
                elif isinstance(node.func, ast.Attribute):
                    full_name = f"{getattr(node.func.value, 'id', '')}.{node.func.attr}"
                    if full_name in self.forbidden_functions:
                        errors.append(f"Fonction interdite : {full_name}")

        return len(errors) == 0, errors

validator = CodeValidator()
