import speed_gen

class StartTime:
    def __init__(self, inputs):
        self.value = speed_gen.time_of_creation(inputs.pulseLength)