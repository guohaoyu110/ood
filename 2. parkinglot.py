# define a few classes: Vehicle: (inherited class: large medium small )
# driver class: pay 
# parking system class: parking gargage
from abc import ABC, abstractmethod
from enum import Enum
class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
# status can also be enum 
class ParkingSpotType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
class Vehicle(ABC):
    def __init__(self, size: VehicleSize, license_plate: str):
        self._size = size
        self._license_plate = license_plate
    def get_size(self):
        return self._size
    def get_license_plate(self):
        return self._license_plate
    @abstractmethod
    def get_parking_fee(self, hours):
        pass 
class SmallCar(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(VehicleSize.SMALL, license_plate)
    def get_parking_fee(self, hours):
        return hours * 10 
class MediumCar(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(VehicleSize.MEDIUM, license_plate)
    def get_parking_fee(self, hours):
        return hours * 5
class LargeCar(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(VehicleSize.LARGE, license_plate)
    def get_parking_fee(self, hours):
        return hours * 3

class ParkingSpot:
    def __init__(self, spot_type: ParkingSpotType):
        self._spot_type = spot_type
        self._is_occupied = False
        self._vehicle = None
    def can_fit_vehicle(self, vehicle: Vehicle):
        if self._spot_type == ParkingSpotType.LARGE:
            return True  # Large spots can fit any vehicle
        elif self._spot_type == ParkingSpotType.MEDIUM:
            return vehicle.get_size() in [VehicleSize.MEDIUM, VehicleSize.SMALL]
        elif self._spot_type == ParkingSpotType.SMALL:
            return vehicle.get_size() == VehicleSize.SMALL
    def park(self, vehicle: Vehicle):
        if self.can_fit_vehicle(vehicle) and not self._is_occupied:
            self._vehicle = vehicle
            self._is_occupied = True
            return True
        return False
    def remove_vehicle(self):
        self._is_occupied = False
        self._vehicle = None
    def is_occupied(self):
        return self._is_occupied

class Driver:
    def __init__(self, id, vehicle):
        self._id = id
        self._vehicle = vehicle
        self._payment_due = 0
    def get_vehicle(self):
        return self._vehicle
    def get_id(self):
        return self._id
    def charge(self, amount):
        self._payment_due += amount
    def get_payment_due(self):
        return self._payment_due


class ParkingFloor:
    def __init__(self, spots):
        # `spots` is a list of ParkingSpot objects
        self._spots = spots
        self._vehicle_map = {}
    def park_vehicle(self, vehicle: Vehicle):
        for spot in self._spots:
            if not spot.is_occupied() and spot.can_fit_vehicle(vehicle):
                spot.park(vehicle)
                self._vehicle_map[vehicle.get_license_plate()] = spot
                return True
        return False
    def remove_vehicle(self, vehicle: Vehicle):
        license_plate = vehicle.get_license_plate()
        if license_plate in self._vehicle_map:
            spot = self._vehicle_map[license_plate]
            spot.remove_vehicle()
            del self._vehicle_map[license_plate]
            return True
        return False
    
class ParkingGarage:
    def __init__(self, floors):
        self._floors = floors  # `floors` is a list of ParkingFloor objects
    def park_vehicle(self, vehicle: Vehicle):
        for floor in self._floors:
            if floor.park_vehicle(vehicle):
                return True
        return False
    def remove_vehicle(self, vehicle: Vehicle):
        for floor in self._floors:
            if floor.remove_vehicle(vehicle):
                return True
        return False
import datetime
import math
class ParkingSystem:
    def __init__(self, parkingGarage, hourlyRate):
        self._parkingGarage = parkingGarage
        self._hourlyRate = hourlyRate
        self._timeParked = {}  # map driverId to time that they parked
    def park_vehicle(self, driver):
        currentHour = datetime.datetime.now().hour
        isParked = self._parkingGarage.park_vehicle(driver.get_vehicle())
        if isParked:
            self._timeParked[driver.get_id()] = currentHour
        return isParked
    
    def remove_vehicle(self, driver):
        if driver.get_id() not in self._timeParked:
            return False
        currentHour = datetime.datetime.now().hour
        timeParked = math.ceil(currentHour - self._timeParked[driver.get_id()])
        driver.charge(timeParked * self._hourlyRate)
        del self._timeParked[driver.get_id()]
        return self._parkingGarage.remove_vehicle(driver.get_vehicle())

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> None:
        """Centralized contract for processing payment.
           This method must be overridden by subclasses.
        """
        pass
class CreditCardPayment(PaymentProcessor):
    def __init__(self, card_number: str, expiration_date: str, cvv: str):
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv

    def process_payment(self, amount: float) -> None:
        # Simulate processing a credit card payment
        print(f"Processing credit card payment of ${amount}")
        print(f"Using card number {self.card_number}, expiration date {self.expiration_date}, CVV {self.cvv}")
        # Here would be the actual logic to communicate with a payment gateway
        print("Credit card payment successful.")

class PayPalPayment(PaymentProcessor):
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
    def process_payment(self, amount: float) -> None:
        # Simulate processing a PayPal payment
        print(f"Processing PayPal payment of ${amount}")
        print(f"Using PayPal account {self.email}")
        # Here would be the actual logic to authenticate and process the payment
        print("PayPal payment successful.")

    
# Creating parking spots for a floor (2 small, 1 medium, 1 large)
floor1 = ParkingFloor([ParkingSpot(ParkingSpotType.SMALL), ParkingSpot(ParkingSpotType.SMALL),
                      ParkingSpot(ParkingSpotType.MEDIUM), ParkingSpot(ParkingSpotType.LARGE)])
# Creating parking garage with multiple floors
parkingGarage = ParkingGarage([floor1])
# Initialize the Parking System with hourly rate
parkingSystem = ParkingSystem(parkingGarage, 5)
# Drivers with vehicles of various types and sizes
driver1 = Driver(1, SmallCar("ABC123"))  # Small car
driver2 = Driver(2, MediumCar("XYZ789"))  # Medium car
driver3 = Driver(3, LargeCar("TRK456"))  # Large truck
# Parking vehicles
print(parkingSystem.park_vehicle(driver1))  # True (fits in a small spot)
print(parkingSystem.park_vehicle(driver2))  # True (fits in a medium spot)
print(parkingSystem.park_vehicle(driver3))  # True (fits in a large spot)
# Removing vehicles and calculating the charges
print(parkingSystem.remove_vehicle(driver1))  # True
print(parkingSystem.remove_vehicle(driver2))  # True
print(parkingSystem.remove_vehicle(driver3))  # True
