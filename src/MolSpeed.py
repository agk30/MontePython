import speed_gen

class Speed:
    # type 1 for ingoing beam, 2 for MB model, 3 for IS model
    def __init__(self, inputs, type, **kwargs):
        if type == 1:
            self.value = speed_gen.multi_gauss_speed(inputs.gaussMeans, inputs.gaussDevs, inputs.gaussWeights, inputs.gaussDist, inputs.timeOffset)
        elif type == 2:
            self.value = speed_gen.mb_speed(inputs.maxSpeed, inputs.temp, inputs.mass)
        elif type == 3:
            # get args and kwargs right here, take in ingoing speed and deflection angle pls

            for key, value in kwargs.items():
                if key == "ingoing_speed":
                    ingoing_speed = value
                    inspeed = True
                elif key == "deflection_angle":
                    deflection_angle = value
                    defangle = True

            if not (inspeed and defangle):
                print ("Soft sphere calculation failed: improper ingoing speed and/or deflection angle arguments")

            self.value = speed_gen.soft_sphere_speed(inputs.mass, inputs.energyLoss, inputs.surfaceMass, ingoing_speed, deflection_angle)
        else:
            print ("invalid speed-type number")