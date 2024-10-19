from fastapi import FastAPI
from pydantic import BaseModel
import ast
import operator as op

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Rule Engine API!"}

class RuleEvaluationRequest(BaseModel):
    rule: str
    context: dict

# Supported operators for evaluation
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    ast.And: op.and_,
    ast.Or: op.or_,
}

def evaluate_ast(node, context):
    """Evaluate AST nodes recursively with the given context."""
    if isinstance(node, ast.Expression):
        return evaluate_ast(node.body, context)
    elif isinstance(node, ast.BinOp):  # Binary operations (e.g. 2 + 3)
        left = evaluate_ast(node.left, context)
        right = evaluate_ast(node.right, context)
        return operators[type(node.op)](left, right)
    elif isinstance(node, ast.Compare):  # Comparisons (e.g. x > 10)
        left = evaluate_ast(node.left, context)
        right = evaluate_ast(node.comparators[0], context)
        return operators[type(node.ops[0])](left, right)
    elif isinstance(node, ast.Name):  # Variable (e.g. x)
        return context[node.id]
    elif isinstance(node, ast.Constant):  # Constant values (e.g. 10)
        return node.value
    elif isinstance(node, ast.BoolOp):  # Boolean operations (e.g. x and y)
        values = [evaluate_ast(value, context) for value in node.values]
        return all(values) if isinstance(node.op, ast.And) else any(values)
    else:
        raise TypeError(f"Unsupported AST node: {type(node).__name__}")

@app.post("/evaluate/")
async def evaluate_rule(request: RuleEvaluationRequest):
    rule = request.rule
    context = request.context

    # Parse the rule into an AST
    try:
        tree = ast.parse(rule, mode='eval')
        # Evaluate the AST using the context
        result = evaluate_ast(tree, context)
        return {"eligible": result}
    except Exception as e:
        return {"error": str(e)}
