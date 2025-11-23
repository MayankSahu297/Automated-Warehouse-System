from typing import List, Optional
from models import StorageBin, Package
import bisect

def find_best_fit_bin(bins: List[StorageBin], package_size: int) -> Optional[StorageBin]:
    """
    Uses Binary Search to find the smallest bin that fits the package.
    Assumes 'bins' is sorted by capacity.
    """
    # We want to find the first bin such that bin.capacity >= package_size
    # Since we can't use a custom key with bisect_left directly on objects in older python versions easily without a key wrapper,
    # but here we can assume Python 3.10+ or just use a helper list of capacities if needed.
    # However, let's implement the binary search manually to be explicit and robust and avoid overhead of creating key lists.
    
    low = 0
    high = len(bins) - 1
    best_fit_index = -1

    while low <= high:
        mid = (low + high) // 2
        if bins[mid].capacity >= package_size:
            best_fit_index = mid
            high = mid - 1  # Try to find a smaller valid bin in the left half
        else:
            low = mid + 1   # Bin is too small, look in the right half

    if best_fit_index != -1:
        return bins[best_fit_index]
    return None

def optimize_truck_loading(truck_capacity: int, packages: List[Package]) -> Optional[List[Package]]:
    """
    Uses Backtracking to find a subset of packages that fits into the truck.
    Returns the list of packages if a valid combination is found, else None.
    This is a variation of the Subset Sum problem / Knapsack.
    For this specific requirement: "if they don't fit, backtrack".
    We will try to fit as many as possible or a specific set. 
    Let's interpret the requirement: "calculate if a specific set of packages can fit... if not backtrack".
    Actually, the prompt says: "Recursively try to fit Package A... If truck overflows, Backtrack... try skipping to Package C".
    This implies finding *any* valid combination that maximizes usage or just fits a sequence?
    Let's implement a standard backtracking to find a combination that fits.
    """
    
    valid_combination = []
    
    def backtrack(start_index, current_load, current_path):
        if current_load <= truck_capacity:
            # We found a valid state. We can keep trying to add more, 
            # or if we have a specific target (like "all fragile bundles"), we check that.
            # For this generic "optimize" function, let's try to fit as many as possible?
            # Or simply return the first valid combination that is "maximal" in some sense?
            # Let's stick to the prompt's logic: Try A, then B. If fail, remove B, try C.
            
            # If we are at the end of the list, or just want to return this valid path:
            if start_index == len(packages):
                return list(current_path)
            
            # Try adding the next package
            pkg = packages[start_index]
            if current_load + pkg.size <= truck_capacity:
                current_path.append(pkg)
                result = backtrack(start_index + 1, current_load + pkg.size, current_path)
                if result: return result
                current_path.pop() # Backtrack
            
            # Skip the current package and try the next one
            return backtrack(start_index + 1, current_load, current_path)
            
        return None

    # To make it interesting, let's try to fit as many items as possible from the start
    # The prompt describes a specific flow: Try A, then B...
    return backtrack(0, 0, [])
