
import ast
import operator


# Only allow safe mathematical operations
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_math(node):
    if isinstance(node, ast.Expression):
        return evaluate_math(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = evaluate_math(node.left)
        right = evaluate_math(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")

        result = OPERATORS[type(node.op)](left, right)

        if abs(result) > 1e12:
            raise ValueError("Result is too large.")

        return result

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](
            evaluate_math(node.operand)
        )

    raise ValueError("Unsupported mathematical expression.")


def calculate(expression: str) -> dict:
    """
    Safely evaluate basic mathematical expressions.
    """

    print(f"\n[CALCULATOR] Calculating: {expression}")

    try:
        tree = ast.parse(expression, mode="eval")
        result = evaluate_math(tree)

        print(f"[CALCULATOR] Result: {result}")

        return {
            "success": True,
            "expression": expression,
            "result": result,
            "error": None
        }

    except (ValueError, TypeError, ZeroDivisionError, SyntaxError) as error:
        print(f"[CALCULATOR ERROR] {error}")

        return {
            "success": False,
            "expression": expression,
            "result": None,
            "error": str(error)
        }
