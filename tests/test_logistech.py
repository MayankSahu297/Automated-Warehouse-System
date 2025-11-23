import unittest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from controller import LogiMaster
from models import Package
from database import Database

class TestLogisTech(unittest.TestCase):
    def setUp(self):
        # Reset Singleton for testing purposes (Hack for testing)
        LogiMaster._instance = None
        
        # Setup clean DB
        self.db_name = "test_logistech.db"
        if os.path.exists(self.db_name):
            os.remove(self.db_name)
            
        # Initialize Controller with test DB
        # We need to patch the database init in controller or just use the default and clean it?
        # The controller uses "logistech.db" by default. Let's just use the main one but clean it.
        # Or better, let's modify the controller to accept a db_name, but for now let's stick to the existing code
        # and just clean the bins table.
        
        self.controller = LogiMaster()
        
        # Clear data
        conn = self.controller.db.conn
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bins")
        cursor.execute("DELETE FROM shipment_logs")
        conn.commit()
        
        # Setup bins
        bins = [
            (1, 5, 'A1'),
            (2, 10, 'A2'),
            (3, 15, 'B1'),
            (4, 50, 'B2'),
            (5, 100, 'C1')
        ]
        cursor.executemany("INSERT INTO bins (bin_id, capacity, location_code) VALUES (?, ?, ?)", bins)
        conn.commit()
        
        # Reload inventory
        self.controller.load_inventory()

    def test_singleton_pattern(self):
        """Check if two instances are the same object"""
        c1 = LogiMaster()
        c2 = LogiMaster()
        self.assertIs(c1, c2, "Singleton pattern failed: Instances are different")

    def test_binary_search_best_fit(self):
        """Verify Binary Search finds the optimal bin"""
        # Size 12 should go to 15 (Bin 3)
        pkg = Package("TEST001", 12, "NYC")
        self.controller.process_arrival(pkg)
        result = self.controller.assign_storage()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["bin_capacity"], 15)
        self.assertEqual(result["bin_id"], 3)

        # Size 4 should go to 5 (Bin 1)
        pkg2 = Package("TEST002", 4, "BOS")
        self.controller.process_arrival(pkg2)
        result2 = self.controller.assign_storage()
        self.assertEqual(result2["bin_capacity"], 5)

        # Size 200 should fail
        pkg3 = Package("TEST003", 200, "MIA")
        self.controller.process_arrival(pkg3)
        result3 = self.controller.assign_storage()
        self.assertFalse(result3["success"])
        self.assertEqual(result3["reason"], "No suitable bin found")

    def test_backtracking_loader(self):
        """Verify Backtracking finds a valid combination"""
        packages = [
            Package("P1", 30, "A"),
            Package("P2", 40, "B"),
            Package("P3", 20, "C"),
            Package("P4", 50, "D")
        ]
        # Truck 100. 30+40+20 = 90. 30+40+50 = 120 (Fail).
        # So it should load P1, P2, P3.
        
        result = self.controller.load_truck(100, packages)
        self.assertTrue(result["success"])
        loaded_ids = [p["id"] for p in result["loaded_packages"]]
        self.assertIn("P1", loaded_ids)
        self.assertIn("P2", loaded_ids)
        self.assertIn("P3", loaded_ids)
        self.assertNotIn("P4", loaded_ids)

    def test_impossible_shipment(self):
        """Verify Backtracking handles impossible cases"""
        packages = [Package("Big", 200, "X")]
        result = self.controller.load_truck(100, packages)
        self.assertFalse(result["success"])

    def test_sql_persistence(self):
        """Verify actions are logged to SQL"""
        pkg = Package("SQLTEST", 10, "DB")
        self.controller.process_arrival(pkg)
        self.controller.assign_storage()
        
        cursor = self.controller.db.conn.cursor()
        cursor.execute("SELECT * FROM shipment_logs WHERE tracking_id='SQLTEST'")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[3], "STORED") # Status

if __name__ == '__main__':
    unittest.main()
