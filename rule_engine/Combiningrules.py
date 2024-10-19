import re


class Node:
    """Represents a node in the AST."""

    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.left = left  # Left child (for binary operators)
        self.right = right  # Right child (for binary operators)
        self.value = value  # Value for leaf nodes

    def __repr__(self):
        return f"Node(type={self.node_type}, value={self.value})"


def parse_rule_to_ast(rule):
    """Parses a simple rule into an AST node."""

    # Regular expression to match a comparison rule
    pattern = r"(\w+)\s*(>=|<=|>|<|==|!=)\s*(\d+)"
    match = re.match(pattern, rule.strip())

    if not match:
        raise ValueError(f"Invalid rule format: {rule}")

    variable, operator, value = match.groups()

    # Create nodes for the variable and value
    operand_node = Node("operand", value={variable: int(value)})
    operator_node = Node("operator", left=operand_node, right=None, value=operator)

    return operator_node


def combine_rules(rules):
    """Combines multiple rules into a single AST node using OR logic."""

    if not rules:
        raise ValueError("No rules provided to combine.")

    # Convert the first rule to an AST node
    combined = parse_rule_to_ast(rules[0])

    for rule in rules[1:]:
        # For each additional rule, create a new OR operation
        new_rule_ast = parse_rule_to_ast(rule)
        combined = Node("operator", left=combined, right=new_rule_ast, value="OR")

    return combined


# Example usage
if __name__ == "__main__":
    rules_list = ["age > 30", "income < 50000"]
    combined_ast = combine_rules(rules_list)
    print(combined_ast)

