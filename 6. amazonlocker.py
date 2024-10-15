import datetime
import uuid
from typing import List, Optional
from collections import defaultdict

# 数据结构定义
class LockerStatus:
    FREE = "FREE"
    BOOKED = "BOOKED"

class LockerSize:
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    XL = "XL"
    XXL = "XXL"

class Locker:
    def __init__(self, locker_id: str, size: str, status=LockerStatus.FREE):
        self.locker_id = locker_id
        self.size = size
        self.status = status

class LockerSystem:
    def __init__(self):
        # 所有锁柜以大小和状态分类存储
        self.lockers = defaultdict(list)
        self.codes = {}  # 用字典存储验证码 {locker_id: {"courier": code, "customer": code}}

    def add_locker(self, locker: Locker):
        self.lockers[locker.size].append(locker)

    def find_available_locker(self, size: str) -> Optional[Locker]:
        """按大小查找可用 Locker"""
        for locker in self.lockers[size]:
            if locker.status == LockerStatus.FREE:
                return locker
        return None

    def generate_codes(self, locker_id: str):
        """为 Locker 生成两个 6 位验证码"""
        courier_code = str(uuid.uuid4())[:6]
        customer_code = str(uuid.uuid4())[:6]
        self.codes[locker_id] = {
            "courier": courier_code,
            "customer": customer_code
        }
        print(f"Courier code: {courier_code}, Customer code: {customer_code}")

    def get_code(self, locker_id: str, role: str) -> Optional[str]:
        """获取某个 Locker 的验证码"""
        return self.codes.get(locker_id, {}).get(role)

    def release_locker(self, locker_id: str):
        """释放 Locker，并重置状态"""
        for lockers in self.lockers.values():
            for locker in lockers:
                if locker.locker_id == locker_id and locker.status == LockerStatus.BOOKED:
                    locker.status = LockerStatus.FREE
                    print(f"Locker {locker_id} is now free.")
                    self.codes.pop(locker_id, None)  # 移除验证码
                    return True
        return False

# 模拟支付服务
def process_payment(payment_status: bool) -> bool:
    return payment_status

# Locker 预订逻辑
def book_locker(locker_system: LockerSystem, size: str, payment_status: bool) -> Optional[str]:
    locker = locker_system.find_available_locker(size)
    if not locker:
        print("No locker available for the given size.")
        return None

    if not process_payment(payment_status):
        print("Payment failed. Locker not booked.")
        return None

    locker.status = LockerStatus.BOOKED
    print(f"Locker {locker.locker_id} booked successfully.")
    return locker.locker_id

# 超时处理逻辑
def handle_overdue_locker(locker_system: LockerSystem, locker_id: str, placed_time: datetime.datetime):
    """处理超过 3 天未取的物品"""
    if (datetime.datetime.now() - placed_time).days > 3:
        print(f"Item in locker {locker_id} has expired. Initiating refund process.")
        locker_system.release_locker(locker_id)  # 超时后释放 Locker

# 示例用法
if __name__ == "__main__":
    locker_system = LockerSystem()
    # 添加一些示例 Locker
    locker_system.add_locker(Locker("L1", LockerSize.SMALL))
    locker_system.add_locker(Locker("L2", LockerSize.MEDIUM))
    locker_system.add_locker(Locker("L3", LockerSize.LARGE))

    # 预订一个 Locker
    locker_id = book_locker(locker_system, LockerSize.SMALL, payment_status=True)
    if locker_id:
        locker_system.generate_codes(locker_id)

    # 获取用户的验证码
    print(f"Customer code: {locker_system.get_code(locker_id, 'customer')}")

    # 用户取出物品
    if locker_id:
        locker_system.release_locker(locker_id)

    # 模拟物品超时未取出
    handle_overdue_locker(locker_system, "L1", datetime.datetime.now() - datetime.timedelta(days=4))
