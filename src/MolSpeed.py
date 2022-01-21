import Inputs
import speed_gen

class Speed:
    # type 1 for ingoing beam, 2 for MB model, 3 for IS model
    def __init__(self, type, *args):
        if type == 1:
            self.value = speed_gen.multi_gauss_speed(Inputs.gaussMeans, Inputs.gaussDevs, Inputs.gaussWeights, Inputs.gaussDist, Inputs.timeOffset)
        elif type == 2:
            self.value = speed_gen.mb_speed(Inputs.maxSpeed, Inputs.temp, Inputs.mass)
        elif type == 3:
            # get args and kwargs right here, take in ingoing speed and deflection angle pls
            for ar in args:
                ingoing_speed = ar
            self.value = speed_gen.soft_sphere_speed(Inputs.mass, Inputs.energyLoss, Inputs.surfaceMass, ingoing_speed, deflection_angle)
        else:
            print ("invalid speed-type number")