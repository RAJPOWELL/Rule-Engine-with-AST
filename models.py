class Node:
    def __init__(self, node_type, value, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def to_dict(self):
        return {
            "node_type": self.node_type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


    def __repr__(self):
        return f"Node({self.node_type}, {self.value}, {self.left}, {self.right})"

def eval_ast(node, data):
    if node.node_type == 'operand':
        key, op, val = node.value
        if op == '>':
            return data.get(key, 0) > val
        elif op == '<':
            return data.get(key, 0) < val
        elif op == '=':
            return data.get(key, None) == val
    elif node.node_type == 'operator':
        left_result = eval_ast(node.left, data)
        right_result = eval_ast(node.right, data)
        if node.value == 'AND':
            return left_result and right_result
        elif node.value == 'OR':
            return left_result or right_result
    return False
