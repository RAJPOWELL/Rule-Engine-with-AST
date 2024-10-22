from models import Node

def parse_rule(rule_string):
    try:
        # Split the rule string into parts (simple tokenizer)
        rule_parts = rule_string.replace('(', '').replace(')', '').split()
        stack = []
        key = None
        operand = None

        for part in rule_parts:
            if part in ['AND', 'OR']:
                # Logical operator: pop two nodes from the stack and create an operator node
                right = stack.pop()
                left = stack.pop()
                stack.append(Node('operator', part, left, right))
            elif part in ['>', '<', '=', '>=', '<=']:
                operand = part  # Set the comparison operator
            elif part.isdigit():  # If it's a number
                # Numeric comparison
                stack.append(Node('operand', (key, operand, int(part))))
            elif part.startswith("'") and part.endswith("'"):
                # String comparison (e.g., 'Sales')
                stack.append(Node('operand', (key, operand, part.strip("'"))))
            else:
                # Assume it's a key (like 'age' or 'department')
                key = part

        if len(stack) != 1:
            raise ValueError("Invalid rule structure")

        return stack[0]  # Return the root node (AST)
    except Exception as e:
        raise ValueError(f"Error parsing rule: {str(e)}")
