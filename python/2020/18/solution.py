import common

equations = common.read_file().splitlines()
digit_range = range(ord('0'), ord('9')+1)

import ast
import operator

def visit(expr, ops):
    if isinstance(expr, ast.BinOp):
        left = visit(expr.left, ops)
        right = visit(expr.right, ops)
        op = ops[type(expr.op)]
        return op(left, right)
    elif isinstance(expr, ast.Constant):
        return expr.value
    raise 'should not reach here'

def visit_str(expr_line, ops):
    expressions = ast.parse(expr_line)
    result = visit(expressions.body[0].value, ops)
    return result

# part 1
ops = {
    ast.Add: operator.add,
    ast.Sub: operator.mul
}
results = []
for eq in equations:
    line = eq.replace('*', '-')
    results.append(visit_str(line, ops))

print(sum(results))

# part 2
ops = {
    ast.Add: operator.mul,
    ast.Mult: operator.add
}
results = []
for eq in equations:
    line = eq.replace('+', '-').replace('*', '+').replace('-', '*')
    results.append(visit_str(line, ops))

print(sum(results))
