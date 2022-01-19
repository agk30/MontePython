import speed_gen

class Speed:
    def __init__(self, type, inputs):
        if type == 1:
            self.value = speed_gen.ingoing()
        elif type == 2:
            self.value = speed_gen.mb_speed(inputs['maxSpeed'], inputs['temp'], inputs['mass'])
        elif type == 3:
            self.value = speed_gen.soft_sphere()
        else:
            print ("invalid type number")

class Direction:
    def __init__(self):
        pass

class StartPoint:
    def __init__(self):
        pass

class StartTime:
    def __init__(self):
        pass  

class Molecule:
    def __init__(self, type, inputs):
        self.speed = Speed(type, inputs)
        #self.direction = Direction(type)
        #self.start_point = StartPoint(type)
        #self.start_time = StartTime(type)

inputs = {
    "maxSpeed": 1000,
    "temp": 298,
    "mass": 2.8240519E-26,
}

mol = Molecule(1, inputs)

print (mol.speed.value)