from collections import deque
import heapq
import time
from enum import Enum

# 电梯状态定义
class State(Enum):
    IDLE = 1
    UP = 2
    DOWN = 3

# 请求来源：乘客在电梯内还是外部楼层发起请求
class RequestOrigin(Enum):
    INSIDE = 1
    OUTSIDE = 2

# 请求类，定义每次电梯的请求
class Request:
    def __init__(self, origin, origin_floor, destination_floor=None):
        self.origin = origin
        self.origin_floor = origin_floor
        self.destination_floor = destination_floor

    def __lt__(self, other):
        return self.destination_floor < other.destination_floor  # 用于优先队列排序

class Elevator:
    def __init__(self, current_floor=1):
        self.current_floor = current_floor  # 当前楼层
        self.state = State.IDLE  # 电梯初始状态
        self.up_queue = []  # 上行请求队列（最小堆）
        self.down_queue = []  # 下行请求队列（最小堆）

    # 打开电梯门
    def open_doors(self):
        print(f"Doors are OPEN on floor {self.current_floor}")

    # 关闭电梯门
    def close_doors(self):
        print(f"Doors are CLOSED")

    # 添加上行请求到队列
    def add_up_request(self, request):
        heapq.heappush(self.up_queue, request)

    # 添加下行请求到队列
    def add_down_request(self, request):
        heapq.heappush(self.down_queue, request)

    # 处理上行请求
    def process_up_requests(self):
        while self.up_queue:
            request = heapq.heappop(self.up_queue)
            self.move_to_floor(request.destination_floor)

    # 处理下行请求
    def process_down_requests(self):
        while self.down_queue:
            request = heapq.heappop(self.down_queue)
            self.move_to_floor(request.destination_floor)

    # 移动电梯到指定楼层
    def move_to_floor(self, floor):
        if self.current_floor != floor:
            print(f"Moving from floor {self.current_floor} to floor {floor}")
            time.sleep(1)  # 模拟移动时间
            self.current_floor = floor
            print(f"Arrived at floor {floor}")
        self.open_doors()
        time.sleep(1)  # 模拟开门时间
        self.close_doors()

    # 根据当前状态处理请求
    def operate(self):
        if self.up_queue or self.state == State.UP:
            print("Processing UP requests...")
            self.process_up_requests()
        if self.down_queue or self.state == State.DOWN:
            print("Processing DOWN requests...")
            self.process_down_requests()
        self.state = State.IDLE  # 所有请求处理完毕，恢复空闲状态
        print("Elevator is now IDLE.")

class Controller:
    def __init__(self):
        self.elevator = Elevator()

    # 添加上行请求
    def send_up_request(self, origin_floor, destination_floor):
        request = Request(RequestOrigin.OUTSIDE, origin_floor, destination_floor)
        self.elevator.add_up_request(request)

    # 添加下行请求
    def send_down_request(self, origin_floor, destination_floor):
        request = Request(RequestOrigin.OUTSIDE, origin_floor, destination_floor)
        self.elevator.add_down_request(request)

    # 开始处理所有请求
    def handle_requests(self):
        self.elevator.operate()

class Main:
    @staticmethod
    def main():
        controller = Controller()

        # 模拟一些上行和下行请求
        controller.send_up_request(1, 5)
        controller.send_down_request(4, 2)
        controller.send_up_request(3, 6)

        # 处理请求
        controller.handle_requests()

        print("New requests...")
        controller.send_up_request(1, 9)
        controller.send_down_request(5, 2)

        # 处理新的请求
        controller.handle_requests()

if __name__ == "__main__":
    Main.main()
