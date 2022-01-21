import speed_gen

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