from collections import deque
from typing import List, Optional
from models import Package

class ConveyorBelt:
    """FIFO Queue for incoming packages"""
    def __init__(self):
        self.queue = deque()

    def add_package(self, package: Package):
        self.queue.append(package)

    def get_next_package(self) -> Optional[Package]:
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self) -> bool:
        return len(self.queue) == 0

class LoadingDock:
    """LIFO Stack for truck loading with rollback capability"""
    def __init__(self):
        self.stack: List[Package] = []

    def load_package(self, package: Package):
        self.stack.append(package)
        print(f"Loaded package {package.tracking_id} onto truck.")

    def rollback_load(self, count: int = 1):
        """Simulate unloading items from the back (LIFO)"""
        for _ in range(count):
            if self.stack:
                removed = self.stack.pop()
                print(f"Rolled back: Unloaded package {removed.tracking_id}")
            else:
                print("Truck is empty, nothing to rollback.")

    def view_top(self) -> Optional[Package]:
        if self.stack:
            return self.stack[-1]
        return None
