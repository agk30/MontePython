import numpy
import direction_gen

class StartPoint:
    def __init__(self, inputs):

        start_point = numpy.zeros(3)

        start_point[0], start_point[1] = direction_gen.disc_pick()
        start_point = start_point*inputs.valveRad
        start_point[2] = inputs.valvePos
        self.value = start_point