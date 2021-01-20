class Stack:
    """
    An object behaving like a data stack
    """

    def __init__(self, depth):
        self.depth = depth
        self.stack = []

    def push(self, value):
        if len(self.stack) < self.depth:
            self.stack.append(value)
            return True
        else:
            return False

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop(-1)
        else:
            return None

    def read(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None

    def flush(self):
        self.stack = []
