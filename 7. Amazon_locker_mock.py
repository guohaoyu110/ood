# definition of enumerations used in the Amazon Locker service
class LockerSize(enum.Enum):
    EXTRA_SMALL = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4
    EXTRA_LARGE = 5
    DOUBLE_EXTRA_LARGE = 6

class LockerState(enum.Enum):
    CLOSED = 1
    BOOKED = 2
    AVAILABLE = 3

class Item:
  def __init__(self, item_id, quantity):
    self.__item_id = item_id
    self.__quantity = quantity

class Order:
  def __init__(self, order_id, items, delivery_location):
    self.__order_id = order_id
    self.__items = items # List of items
    self.__delivery_location = delivery_location

 
class Package:
    def __init__(self, package_id, package_size, order):
        self.__package_id = package_id
        self.__package_size = package_size
        self.__order = order
 
    def pack():
        None

class LockerPackage(Package):
    def __init__(self, code_valid_days, locker_id, package_id, code, package_delivery_time, package_id, package_size, order):
        self.__code_valid_days = code_valid_days
        self.__locker_id = locker_id
        self.__package_id = package_id
        self.__code = code
        self.__package_delivery_time = package_delivery_time
        super().__init__(package_id, package_size, order)
 
    def is_valid_code():
        pass
   
    def verify_code(code):
        None


class Locker:
    def __init__(self, locker_id, locker_size, location_id, locker_state):
        self.__locker_id = locker_id
        self.__locker_size = locker_size
        self.location_id = location_id
        self.__locker_state = locker_state
 
    def add_package():
        None
    def remove_package():
        None
 
class LockerLocation:
    def __init__(self, name, lockers, longitude, latitude, open_time, close_time):
        self.__name = name
        self.__lockers = lockers # list of lockers
        self.__longitude = longitude
        self.__latitude = latitude
        self.__open_time = open_time
        self.__close_time = close_time


class __LockerService(object): # not important; good to have 
  __instances = None
 
  def __new__(cls):
    if cls.__instances is None:
        cls.__instances = super(__LockerService, cls).__new__(cls)
    return cls.__instances

class LockerService(metaclass=__LockerService):
    def __init__(self):
      self.__locations = {}

class Notification:
    def __init__(self, customer_id, order_id, locker_id, code):
        self.__customer_id = customer_id
        self.__order_id = order_id
        self.__locker_id = locker_id
        self.__code = code
   
    def send():
      pass



# Question : Design Goodreads.
# Users should be able to add books and friends.
# Users should be able to get a list of their books.
# Users should be able to get a list of their top books that their friends have read.
# Users should be able to get a list of top books that their network has read.

