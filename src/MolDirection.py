import direction_gen

class Direction:
    def __init__(self, inputs, type):
        if type == 1:
            self.value = direction_gen.ingoing_direction(inputs.valveRad, inputs.valvePos, inputs.skimRad, inputs.skimPos, inputs.colRad, inputs.colPos)
        elif type == 2:
            self.value = direction_gen.cosine_distribution(inputs.cosinePower)
        else:
            print ("MolDirection error: invalid direction-type number")