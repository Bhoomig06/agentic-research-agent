
from app.tools.calculator import calculate

expressions = [
    "85 * 0.9",
    "(8 + 9 + 7) / 3",
    "100 - 25"
]

for expression in expressions:
    result = calculate(expression)

    if result["success"]:
        print("Expression:", expression)
        print("Result:", result["result"])
    else:
        print("Error:", result["error"])

    print("-" * 40)
