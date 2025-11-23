from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Package:
    tracking_id: str
    size: int
    destination: str

class StorageUnit(ABC):
    @abstractmethod
    def occupy_space(self, amount: int):
        pass

    @abstractmethod
    def free_space(self, amount: int):
        pass

class StorageBin(StorageUnit):
    def __init__(self, bin_id: int, capacity: int, location_code: str):
        self.bin_id = bin_id
        self.capacity = capacity
        self.location_code = location_code
        self.current_load = 0

    def occupy_space(self, amount: int):
        if self.current_load + amount > self.capacity:
            raise ValueError("Bin capacity exceeded")
        self.current_load += amount

    def free_space(self, amount: int):
        if self.current_load - amount < 0:
            raise ValueError("Cannot free more space than occupied")
        self.current_load -= amount

    def __lt__(self, other):
        # Critical for Binary Search: sort by capacity
        return self.capacity < other.capacity

    def __repr__(self):
        return f"StorageBin(id={self.bin_id}, capacity={self.capacity}, load={self.current_load})"
