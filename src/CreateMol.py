import MolDirection
import MolSpeed
import MolStartPoint
import MolStartTime

class Molecule:
    def __init__(self, inputs, scatter_type, speed_type, **kwargs):
        self.speed = MolSpeed.Speed(inputs, speed_type, **kwargs)
        self.direction = MolDirection.Direction(inputs, scatter_type)
        self.start_point = MolStartPoint.StartPoint(inputs)
        self.start_time = MolStartTime.StartTime(inputs)