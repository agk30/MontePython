import speed_gen
import direction_gen
import numpy

class Speed:
    # type 1 for ingoing beam, 2 for MB model, 3 for IS model
    def __init__(self, type, inputs, *args):
        if type == 1:
            self.value = speed_gen.multi_gauss_speed(float(inputs['math parameters']['gaussMeans']), float(inputs['math parameters']['gaussDevs']),
                                                     float(inputs['math parameters']['gaussWeights']), float(inputs['math parameters']['gaussDist']),
                                                     float(inputs['math parameters']['timeOffset']))
        elif type == 2:
            self.value = speed_gen.mb_speed(inputs['math parameters']['maxSpeed'], inputs['math parameters']['temp'], inputs['math parameters']['mass'])
        elif type == 3:
            # get args and kwargs right here, take in ingoing speed and deflection angle pls
            for ar in args:
                ingoing_speed = ar
            self.value = speed_gen.soft_sphere_speed(float(inputs['math parameters']['mass']), float(inputs['math parameters']['energyLoss']),
                                                     float(inputs['math parameters']['surfaceMass']), ingoing_speed, deflection_angle)
        else:
            print ("invalid speed-type number")

class Direction:
    def __init__(self, type, inputs):
        if type == 1:
            self.value = direction_gen.ingoing_direction(float(inputs['experimental']['valveRad']), float(inputs['experimental']['valvePos']),
                                                         float(inputs['experimental']['skimRad']), float(inputs['experimental']['skimPos']),
                                                         float(inputs['experimental']['colRad']), float(inputs['experimental']['colPos']))
        elif type == 2:
            self.value = direction_gen.cosine_distribution(int(inputs['math parameters']['cosinePower']))
        else:
            print ("invalid direction-type number")

class StartPoint:
    def __init__(self, inputs):

        start_point = numpy.zeros(3)

        start_point[0], start_point[1] = direction_gen.value()
        start_point = start_point*float(inputs['experimental']['valveRad'])
        start_point[2] = float(inputs['experimental']['valvePos'])
        self.value = start_point

class StartTime:
    def __init__(self, inputs):
        self.value = speed_gen.time_of_creation(float(inputs['experimental']['pulseLength']))

class Molecule:
    def __init__(self, scatter_type, speed_type, inputs):
        self.speed = Speed(speed_type, inputs)
        self.direction = Direction(scatter_type, inputs)
        self.start_point = StartPoint(inputs)
        self.start_time = StartTime(inputs)