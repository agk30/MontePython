import numpy
import direction_gen
import Inputs

class StartPoint:
    def __init__(self, inputs):

        start_point = numpy.zeros(3)

        start_point[0], start_point[1] = direction_gen.value()
        start_point = start_point*Inputs.valveRad
        start_point[2] = Inputs.valvePos
        self.value = start_point