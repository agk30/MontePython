import numpy
import direction_gen

class StartPoint:
    def __init__(self, inputs):

        start_point = numpy.zeros(3)

        start_point[0], start_point[1] = direction_gen.value()
        start_point = start_point*float(inputs['experimental']['valveRad'])
        start_point[2] = float(inputs['experimental']['valvePos'])
        self.value = start_point