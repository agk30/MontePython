import direction_gen

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