import MolDirection
import MolSpeed
import MolStartPoint
import MolStartTime

class Molecule:
    def __init__(self, scatter_type, speed_type, inputs):
        self.speed = MolSpeed.Speed(speed_type, inputs)
        self.direction = MolDirection.Direction(scatter_type, inputs)
        self.start_point = MolStartPoint.StartPoint(inputs)
        self.start_time = MolStartTime.StartTime(inputs)