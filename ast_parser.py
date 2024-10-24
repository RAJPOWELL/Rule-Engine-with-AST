# ast_parser.py
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right
    
    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }

def create_rule(rule_string):
    def tokenize(s):
        tokens = []
        current = ''
        i = 0
        while i < len(s):
            if s[i] in '()':
                if current:
                    tokens.append(current.strip())
                tokens.append(s[i])
                current = ''
            elif s[i] in ['>', '<', '=']:
                if current:
                    tokens.append(current.strip())
                current = s[i]
                if i + 1 < len(s) and s[i + 1] == '=':
                    current += s[i + 1]
                    i += 1
                tokens.append(current)
                current = ''
            else:
                current += s[i]
            i += 1
        if current:
            tokens.append(current.strip())
        return tokens

    def parse_tokens(tokens):
        def parse_expression():
            if tokens[0] == '(':
                tokens.pop(0)  # Remove opening parenthesis
                left = parse_expression()
                op = tokens.pop(0)  # AND/OR
                right = parse_expression()
                tokens.pop(0)  # Remove closing parenthesis
                return Node('operator', op, left, right)
            else:
                field = tokens.pop(0)
                op = tokens.pop(0)
                value = tokens.pop(0)
                # Try to convert numeric values
                try:
                    if '.' in value:
                        value = float(value.strip("'"))
                    else:
                        value = int(value.strip("'"))
                except ValueError:
                    value = value.strip("'")
                return Node('operand', {'field': field, 'op': op, 'value': value})

        return parse_expression()

    tokens = tokenize(rule_string)
    ast = parse_tokens(tokens)
    return ast.to_dict()

def combine_rules(rules):
    if not rules:
        return None
    if len(rules) == 1:
        return rules[0]
    
    # Combine rules with AND operator
    combined = {
        'type': 'operator',
        'value': 'AND',
        'left': rules[0],
        'right': combine_rules(rules[1:])
    }
    return combined

def evaluate_rule(ast, data):
    def convert_value(value):
        """Convert value to appropriate type for comparison"""
        if isinstance(value, (int, float)):
            return value
        try:
            if '.' in str(value):
                return float(value)
            return int(value)
        except (ValueError, TypeError):
            return str(value)

    def evaluate_node(node):
        if node['type'] == 'operator':
            left_result = evaluate_node(node['left'])
            right_result = evaluate_node(node['right'])
            
            if node['value'] == 'AND':
                return left_result and right_result
            elif node['value'] == 'OR':
                return left_result or right_result
        
        elif node['type'] == 'operand':
            field = node['value']['field']
            op = node['value']['op']
            expected_value = node['value']['value']
            
            if field not in data:
                return False
            
            # Convert both values to the same type for comparison
            actual_value = convert_value(data[field])
            expected_value = convert_value(expected_value)
            
            # Ensure both values are of the same type
            if type(actual_value) != type(expected_value):
                if isinstance(actual_value, (int, float)) and isinstance(expected_value, (int, float)):
                    # Convert both to float for numeric comparisons
                    actual_value = float(actual_value)
                    expected_value = float(expected_value)
                else:
                    # Convert both to strings for string comparisons
                    actual_value = str(actual_value)
                    expected_value = str(expected_value)
            
            if op == '>':
                return actual_value > expected_value
            elif op == '<':
                return actual_value < expected_value
            elif op == '=':
                return actual_value == expected_value
            elif op == '>=':
                return actual_value >= expected_value
            elif op == '<=':
                return actual_value <= expected_value
            
        return False
    
    try:
        return evaluate_node(ast)
    except Exception as e:
        print(f"Error evaluating rule: {str(e)}")
        return False