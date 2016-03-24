class Shape:

    def __init__(self, name, shape, size, fill):
        size_dict = {'huge' : 6, 'very large' : 5, 'large' : 4, 'medium' : 3, 'small' : 2, 'very small' : 1}
        self.name = name
        self.shape = shape
        self.size = size_dict[size]
        self.fill = fill
        self.inside = []
        self.above = []
        self.left_of = []
        self.overlaps = []
        self.angle = 0
        self.alignment = 'center'

    # add to list of what shapes current one is inside of
    def add_inside(self, string):
        shape_list = string.split(",")
        for shape in shape_list:
            self.inside.append(shape)

    # add to list of what shapes current one is above
    def add_above(self, string):
        shape_list = string.split(",")
        for shape in shape_list:
            self.above.append(shape)

    # add to list of what shapes current one is above
    def add_left_of(self, string):
        shape_list = string.split(",")
        for shape in shape_list:
            self.left_of.append(shape)

    # add to list of what shapes current one is above
    def add_overlaps(self, string):
        shape_list = string.split(",")
        for shape in shape_list:
            self.overlaps.append(shape)


    def __str__(self):
        return 'Name: ' + str(self.name) + '\n' + \
               'Shape: ' + str(self.shape) + '\n' + \
               'Size: ' + str(self.size) + '\n' + \
               'Fill: ' + str(self.fill) + '\n'

