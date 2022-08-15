class Vehicle:
    def __init__(self):
        self.name = "Vehicle"


class WaterVehicle(Vehicle):
    def __init__(self):
        super().__init__()
        self.name = "WaterVehicle"


class Boat(WaterVehicle):
    def __init__(self):
        super().__init__()
        self.name = "Boat"


class LandVehicle(Vehicle):
    def __init__(self):
        super().__init__()
        self.name = "LandVehicle"


class Car(LandVehicle):
    def __init__(self):
        super().__init__()
        self.name = "Car"


class CarBoat(Car, Boat):
    def __init__(self):
        super().__init__()
        self.name = "CarBoat"
