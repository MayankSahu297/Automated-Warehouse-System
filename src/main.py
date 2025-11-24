from controller import LogiMaster
from models import Package
from database import Database

def setup_dummy_data():
    """Populate DB with some initial bins for the demo"""
    db = Database()
    cursor = db.conn.cursor()
    # Clear existing for fresh run
    cursor.execute("DELETE FROM bins")
    
    # Insert bins of various sizes
    bins = [
        (1, 5, 'A1'),
        (2, 10, 'A2'),
        (3, 15, 'B1'),
        (4, 50, 'B2'),
        (5, 100, 'C1')
    ]
    cursor.executemany("INSERT INTO bins (bin_id, capacity, location_code) VALUES (%s, %s, %s)", bins)
    db.conn.commit()
    db.close()

def main():
    print("=== LogisTech System Startup ===")
    setup_dummy_data()
    
    # Initialize Controller (Singleton)
    controller = LogiMaster()
    
    # Verify Singleton
    controller2 = LogiMaster()
    if controller is controller2:
        print("Singleton Verification: PASSED")
    else:
        print("Singleton Verification: FAILED")

    print("\n--- Ingestion & Storage (Binary Search) ---")
    # Create some packages
    pkgs = [
        Package("PKG001", 12, "New York"), # Should go to size 15
        Package("PKG002", 4, "Boston"),    # Should go to size 5
        Package("PKG003", 55, "Chicago"),  # Should go to size 100
        Package("PKG004", 200, "Miami")    # Should fail
    ]

    for p in pkgs:
        controller.process_arrival(p)
        controller.assign_storage()

    print("\n--- Truck Loading (Backtracking & Stack) ---")
    # Truck loading scenario
    truck_pkgs = [
        Package("SHIP001", 30, "LA"),
        Package("SHIP002", 40, "SF"),
        Package("SHIP003", 20, "Seattle"),
        Package("SHIP004", 50, "Austin")
    ]
    
    # Truck capacity 100
    # 30+40+20 = 90 (Fits)
    # 30+40+50 = 120 (Too big)
    # The backtracking should find a combination that fits.
    controller.load_truck(100, truck_pkgs)

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    main()
