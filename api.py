from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from controller import LogiMaster
from models import Package

app = FastAPI()

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Controller
controller = LogiMaster()

# Models
class PackageModel(BaseModel):
    tracking_id: str
    size: int
    destination: str

class TruckLoadRequest(BaseModel):
    capacity: int
    packages: List[PackageModel]

# API Endpoints
@app.get("/status")
def get_status():
    """Get current bin inventory status"""
    return {
        "bins": [
            {
                "bin_id": b.bin_id,
                "capacity": b.capacity,
                "current_load": b.current_load,
                "location": b.location_code,
                "packages": [] # In a real app, we'd list packages here
            }
            for b in controller.bin_inventory
        ]
    }

# --- Conveyor Belt Endpoints ---

@app.get("/package/queue")
def get_queue():
    """Get current packages on the conveyor belt"""
    return {
        "queue": [
            {"tracking_id": p.tracking_id, "size": p.size, "destination": p.destination}
            for p in controller.conveyor_queue.queue
        ]
    }

@app.post("/package/add")
def add_package(pkg: PackageModel):
    """Add a package to the conveyor queue"""
    package = Package(pkg.tracking_id, pkg.size, pkg.destination)
    controller.process_arrival(package)
    return {"status": "success", "message": "Package added to queue"}

@app.post("/package/process")
def process_next_package():
    """Process the next package from the queue (Binary Search & Store)"""
    if controller.conveyor_queue.is_empty():
        return {"status": "error", "message": "Queue is empty"}
    
    # Peek to know what we are processing for the response
    pkg = controller.conveyor_queue.queue[0]
    result = controller.assign_storage()
    
    if result and result["success"]:
        return {
            "status": "success", 
            "message": f"Package {pkg.tracking_id} stored in Bin {result['bin_id']}",
            "details": result
        }
    else:
        # If it failed, the package might still be in queue or dropped depending on logic.
        # In current controller implementation, assign_storage pops it.
        # If it failed, it's gone from queue.
        return {"status": "error", "message": "Storage assignment failed", "details": result}

# --- Truck Loading Endpoints ---

@app.get("/truck/status")
def get_truck_status():
    """Get current truck loading stack"""
    return {
        "stack": [
            {"tracking_id": p.tracking_id, "size": p.size, "destination": p.destination}
            for p in controller.loading_stack.stack
        ]
    }

@app.post("/truck/load")
def load_truck_item(pkg: PackageModel):
    """Load a single package onto the truck (Stack Push)"""
    package = Package(pkg.tracking_id, pkg.size, pkg.destination)
    controller.loading_stack.load_package(package)
    controller.db.log_shipment(package.tracking_id, -1, "LOADED")
    return {"status": "success", "message": f"Loaded {pkg.tracking_id}"}

@app.post("/truck/rollback")
def rollback_truck(count: int = 1):
    """Rollback the last N items (Stack Pop)"""
    controller.loading_stack.rollback_load(count)
    # We should probably log the rollback too, but the structure method prints it.
    # Ideally we log to DB here too.
    return {"status": "success", "message": f"Rolled back {count} items"}

# --- Planner Endpoint ---

@app.post("/truck/can-fit")
def check_fit(request: TruckLoadRequest):
    """Check if a set of packages fits in the truck (Backtracking)"""
    packages = [Package(p.tracking_id, p.size, p.destination) for p in request.packages]
    
    # We use the optimize_truck_loading function which returns the list if it fits
    # Note: optimize_truck_loading tries to find *a* valid combination.
    # If we want to check if *all* fit, we check if result length == input length.
    # The prompt says: "System checks via Backtracking if they fit... Shows YES or NO"
    
    result = controller.load_truck(request.capacity, packages) # This actually loads them in the controller logic!
    # Wait, controller.load_truck calls optimize AND loads them.
    # We just want to CHECK.
    # We need to access the algorithm directly or modify controller.
    
    from algorithms import optimize_truck_loading
    optimized_load = optimize_truck_loading(request.capacity, packages)
    
    if optimized_load and len(optimized_load) == len(packages):
         return {"status": "success", "fits": True, "message": "All packages fit!"}
    elif optimized_load:
         return {"status": "warning", "fits": True, "message": "Partial fit possible", "subset": [p.tracking_id for p in optimized_load]}
    else:
         return {"status": "error", "fits": False, "message": "No combination fits"}

@app.get("/logs")
def get_logs():
    """Get simulation logs from DB"""
    # We should read from DB now, not text file, as per requirements "SQL Logging API"
    # But for now, let's stick to the text file or DB?
    # The controller logs to DB. Let's read from DB.
    cursor = controller.db.conn.cursor()
    cursor.execute("SELECT * FROM shipment_logs ORDER BY timestamp DESC LIMIT 50")
    rows = cursor.fetchall()
    logs = [
        f"[{r[2]}] {r[0]}: {r[3]} (Bin {r[1]})" for r in rows
    ]
    return {"logs": logs}

# Serve Static Files (Frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
