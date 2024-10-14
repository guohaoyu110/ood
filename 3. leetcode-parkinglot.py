class ParkingSystem:

    def __init__(self, big: int, medium: int, small: int):
        # 直接存储各类型车位的数量
        self.big = big
        self.medium = medium
        self.small = small

    def addCar(self, carType: int) -> bool:
        """
        尝试停车，处理逻辑：
        - 大车优先停大车位，如果不行，返回 False
        - 中型车优先停中型车位，如果不行，小车位是否足够两小换一中
        - 小车优先停小车位，如果不行，中型或大车位是否可用
        """
        if carType == 1:  # 大车
            if self.big > 0:
                self.big -= 1
                return True
            elif self.small >= 4:  # 用 4 个小车位停 1 个大车
                self.small -= 4
                return True
            else:
                return False

        elif carType == 2:  # 中型车
            if self.medium > 0:
                self.medium -= 1
                return True
            elif self.small >= 2:  # 用 2 个小车位停 1 个中型车
                self.small -= 2
                return True
            else:
                return False

        elif carType == 3:  # 小车
            if self.small > 0:
                self.small -= 1
                return True
            elif self.medium > 0:  # 小车停中型车位
                self.medium -= 1
                return True
            elif self.big > 0:  # 小车停大车位
                self.big -= 1
                return True
            else:
                return False

# 示例使用：
parking_system = ParkingSystem(big=1, medium=1, small=4)

print(parking_system.addCar(1))  # True (1 big car parks in 1 big spot)
print(parking_system.addCar(3))  # True (1 small car parks in 1 small spot)
print(parking_system.addCar(2))  # True (1 medium car parks in medium spot)
print(parking_system.addCar(3))  # True (1 small car parks in 1 small spot)
print(parking_system.addCar(1))  # True (1 big car parks in 4 small spots)
print(parking_system.addCar(1))  # False (no more spots for big car)
