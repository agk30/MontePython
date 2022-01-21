import direction_gen
import Inputs

class Direction:
    def __init__(self, type, inputs):
        if type == 1:
            self.value = direction_gen.ingoing_direction(Inputs.valveRad, Inputs.valvePos, Inputs.skimRad, Inputs.skimPos, Inputs.colRad, Inputs.colPos)
        elif type == 2:
            self.value = direction_gen.cosine_distribution(Inputs.cosinePower)
        else:
            print ("invalid direction-type number")