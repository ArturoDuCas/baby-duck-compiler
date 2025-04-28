class Node(tuple):
    """Simple immutable AST node: (name, [children])."""

    __slots__ = ()

    def __new__(cls, name, children=None):
        if children is None:
            children = []
        return super().__new__(cls, (name, list(children)))

    # Helpers
    @property
    def name(self):
        return self[0]

    @property
    def children(self):
        return self[1]

    def __repr__(self):
        return f"{self.name}({', '.join(map(repr, self.children))})"
