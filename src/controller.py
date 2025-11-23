from typing import List
from models import StorageBin, Package
from structures import ConveyorBelt, LoadingDock
from database import Database
from algorithms import find_best_fit_bin, optimize_truck_loading

class LogiMaster:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogiMaster, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.bin_inventory: List[StorageBin] = []
        self.conveyor_queue = ConveyorBelt()
        self.loading_stack = LoadingDock()
        self.db = Database()
        self._initialized = True
        self.load_inventory()

    def load_inventory(self):
        """Load bins from DB and sort them for Binary Search"""
        rows = self.db.load_bins()
        self.bin_inventory = [StorageBin(r[0], r[1], r[2]) for r in rows]
        self.bin_inventory.sort() # Critical for Binary Search

    def process_arrival(self, package: Package):
        """Ingest a package onto the conveyor belt"""
        print(f"Package {package.tracking_id} arrived (Size: {package.size}).")
        self.conveyor_queue.add_package(package)

    def assign_storage(self):
        """Process next package from queue and find best bin"""
        package = self.conveyor_queue.get_next_package()
        if not package:
            return {"success": False, "reason": "No packages on conveyor"}

        best_bin = find_best_fit_bin(self.bin_inventory, package.size)
        
        if best_bin:
            try:
                best_bin.occupy_space(package.size)
                print(f"Assigned Package {package.tracking_id} to Bin {best_bin.bin_id} (Capacity: {best_bin.capacity}).")
                self.db.log_shipment(package.tracking_id, best_bin.bin_id, "STORED")
                return {
                    "success": True,
                    "package_id": package.tracking_id,
                    "bin_id": best_bin.bin_id,
                    "bin_capacity": best_bin.capacity,
                    "bin_location": best_bin.location_code
                }
            except Exception as e:
                print(f"Error assigning storage: {e}")
                return {"success": False, "reason": str(e)}
        else:
            print(f"No suitable bin found for Package {package.tracking_id} (Size: {package.size}).")
            return {
                "success": False,
                "reason": "No suitable bin found",
                "package_size": package.size
            }

    def load_truck(self, truck_capacity: int, packages_to_load: List[Package]):
        """Attempt to load a set of packages using backtracking"""
        print(f"Attempting to load truck (Capacity: {truck_capacity})...")
        optimized_load = optimize_truck_loading(truck_capacity, packages_to_load)
        
        if optimized_load:
            print("Optimal load found. Loading truck...")
            loaded_info = []
            try:
                for pkg in optimized_load:
                    self.loading_stack.load_package(pkg)
                    self.db.log_shipment(pkg.tracking_id, -1, "LOADED") # -1 for truck
                    loaded_info.append({"id": pkg.tracking_id, "size": pkg.size, "dest": pkg.destination})
                
                return {
                    "success": True,
                    "loaded_packages": loaded_info,
                    "count": len(loaded_info)
                }
            except Exception as e:
                print(f"Error during loading: {e}. Rolling back...")
                self.loading_stack.rollback_load(len(optimized_load))
                return {"success": False, "reason": str(e)}
        else:
            print("Could not find a valid combination to load.")
            return {"success": False, "reason": "No valid combination found"}
