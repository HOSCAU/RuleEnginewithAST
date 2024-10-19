

class ASTNode:
    """Base class for AST nodes."""
    def evaluate(self):
        raise NotImplementedError("Must implement evaluate method.")


class NumberNode(ASTNode):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class AddNode(ASTNode):

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


def main():

    left_node = NumberNode(5)
    right_node = NumberNode(3)
    root_node = AddNode(left_node, right_node)

    # Evaluate the AST
    result = root_node.evaluate()

    # Print the result
    print(f"The result of the expression is: {result}")


if __name__ == "__main__":
    main()
