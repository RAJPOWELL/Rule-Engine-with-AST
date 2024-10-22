# models/ast.py
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left       # left child (Node)
        self.right = right     # right child (Node)
        self.value = value     # value for operands

# Function to create a rule's AST from a string like "age > 30 AND department = 'Sales'"
def create_rule(rule_string):
    # For simplicity, we'll mock parsing logic here
    # You can expand this using a parser like pyparsing for a complete solution
    if rule_string == "age > 30 AND department = 'Sales'":
        return Node("AND", 
                    Node("operand", value="age > 30"),
                    Node("operand", value="department = 'Sales'"))
    return None

# Function to evaluate a rule against user data
def evaluate_rule(node, data):
    if node.type == "operand":
        # Simulate condition checking based on node value
        if node.value == "age > 30":
            return data['age'] > 30
        elif node.value == "department = 'Sales'":
            return data['department'] == 'Sales'
    elif node.type == "operator":
        if node.value == "AND":
            return evaluate_rule(node.left, data) and evaluate_rule(node.right, data)
        elif node.value == "OR":
            return evaluate_rule(node.left, data) or evaluate_rule(node.right, data)
    return False
