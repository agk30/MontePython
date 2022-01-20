import speed_gen
import direction_gen
import numpy

class Speed:
    # type 1 for ingoing beam, 2 for MB model, 3 for IS model
    def __init__(self, type, inputs, *args):
        if type == 1:
            self.value = speed_gen.multi_gauss_speed(inputs['gaussMeans'], inputs['gaussDevs'], inputs['gaussWeights'], inputs['gaussDist'], inputs['timeOffset'])
        elif type == 2:
            self.value = speed_gen.mb_speed(inputs['maxSpeed'], inputs['temp'], inputs['mass'])
        elif type == 3:
            # get args and kwargs right here, take in ingoing speed and deflection angle pls
            for ar in args:
                ingoing_speed = ar
            self.value = speed_gen.soft_sphere_speed(inputs['mass'], inputs['energyLoss'], inputs['surfaceMass'], ingoing_speed, deflection_angle)
        else:
            print ("invalid speed-type number")

class Direction:
    def __init__(self, type, inputs):
        if type == 1:
            self.value = direction_gen.ingoing_direction(inputs['valveRad'], inputs['valvePos'], inputs['skimRad'], inputs['skimPos'], inputs['colRad'], inputs['colPos'])
        elif type == 2:
            self.value = direction_gen.cosine_distribution(inputs['cosinePower'])
        else:
            print ("invalid direction-type number")

class StartPoint:
    def __init__(self, inputs):

        start_point = numpy.zeros(3)

        start_point[0], start_point[1] = direction_gen.value()
        start_point = start_point*inputs['valveRad']
        start_point[2] = inputs['valvePos']
        self.value = start_point

class StartTime:
    def __init__(self):
        self.value = speed_gen.time_of_creation(inputs['pulseLength'])  

class Molecule:
    def __init__(self, type, inputs):
        self.speed = Speed(type, inputs)
        self.direction = Direction(type, inputs)
        self.start_point = StartPoint(type, inputs)
        self.start_time = StartTime(type, inputs)