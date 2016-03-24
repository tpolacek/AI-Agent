class Figure:

    def __init__(self):
        self.shapes = []

    # adds a new shape to the figure
    def add_shape(self, shape):
        self.shapes.append(shape)

    # declares a string representation of a shape (for inside/above/left-of/overlaps lists) as the actual shape object
    def str_to_shape(self):
        dict = {}
        for x in self.shapes:
            dict[x.name] = x

        for shape in self.shapes:
            new_list = []
            for ref in shape.inside:
                new_list.append(dict[ref])
            shape.inside = new_list

        for shape in self.shapes:
            new_list = []
            for ref in shape.above:
                new_list.append(dict[ref])
            shape.above = new_list

        for shape in self.shapes:
            new_list = []
            for ref in shape.left_of:
                new_list.append(dict[ref])
            shape.left_of = new_list

        for shape in self.shapes:
            new_list = []
            for ref in shape.overlaps:
                new_list.append(dict[ref])
            shape.overlaps = new_list

    # will sort the list of shape objects by their size
    def sorter(self):
        self.shapes.sort(key=lambda x: x.size, reverse=True)


