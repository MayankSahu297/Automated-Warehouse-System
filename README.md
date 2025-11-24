# LogisTech: Automated Warehouse Management System

![LogisTech Banner]
<img width="302" height="69" alt="Screenshot 2025-11-24 132101" src="https://github.com/user-attachments/assets/34766829-0554-4b99-9e7b-eed1edd1c9e6" />

🌐 Live Demo

👉 Deployed Link: https://logistech-prime.onrender.com/

## Project Description

LogisTech is a full-stack Automated Warehouse Orchestration System that simulates real-world warehouse operations. It manages incoming packages, finds optimal storage bins using Binary Search, loads trucks using Stack logic, and validates fragile shipments through Backtracking.
A centralized Singleton Controller powers the entire workflow, while SQL audit logs ensure complete traceability of every operation.

## 📑 Table of Contents
1. [Features](#-features)
2. [System Architecture](#-system-architecture)
3. [Algorithms Implemented](#-algorithms-implemented)
4. [Tech Stack](#-tech-stack)
5. [Database Schema](#-database-schema)
6. [Installation Steps](#-installation--setup-instructions)
7. [How to Run](#-how-to-run)
8. [API Endpoints](#-api-endpoints)
9. [UI Screenshots](#-ui-screenshots)
10. [Future Enhancements](#-future-enhancements)
11. [License](#-license)

## 🚀 Features

### 📦 Package Ingestion (Queue – FIFO)
- Add new packages to conveyor belt
- Processes items in arrival order (First-In, First-Out)

### 🗄️ Smart Storage Allocation (Binary Search)
- Bins are sorted by capacity
- Finds the **best-fitting bin** in $O(\log N)$ time
- Prevents storage inefficiency and item damage

### 🚚 Truck Loading Simulator (Stack – LIFO)
- Load packages in **LIFO** (Last-In, First-Out) order
- **Rollback mechanism** to unload items if the wrong package is loaded

### 🔍 Shipment Planner (Backtracking)
- Validates fragile package combinations
- Checks if a specific set of bundles fits inside the truck capacity

### 🧠 Singleton Warehouse Controller
- Centralized decision-making
- Prevents race conditions by ensuring only one controller instance exists

### 🗃 SQL Audit Logging
- Logs every storage, loading, and rollback event
- Ensures traceability after server restart

## 🏗 System Architecture

The system follows a centralized "Control Tower" architecture where the **WarehouseController (Singleton)** coordinates all operations.

```
┌─────────────────────────────────────────────────────────────┐
│                         USER / WEB UI                        │
│                    (HTML + CSS + JavaScript)                 │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Requests
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│                    (REST API Endpoints)                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LogisTech Controller (Singleton)                │
│                  Centralized Orchestration                   │
└─┬───────────┬────────────┬──────────────┬──────────────────┘
  │           │            │              │
  ▼           ▼            ▼              ▼
┌──────┐  ┌──────┐  ┌──────────┐  ┌─────────────┐
│Queue │  │Stack │  │Binary    │  │Backtracking │
│(FIFO)│  │(LIFO)│  │Search    │  │Planner      │
└──┬───┘  └──┬───┘  └────┬─────┘  └──────┬──────┘
   │         │           │                │
   └─────────┴───────────┴────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  SQLite Database     │
              │  (Audit Logs + Bins) │
              └──────────────────────┘
```

**Explanation:**
- **Frontend ↔ Backend ↔ Database** are loosely coupled for scalability.
- The **Controller** acts as the brain, managing the state of the Queue, Stack, and Inventory.

## 🧮 Algorithms Implemented

### A. Binary Search (Best-Fit Storage Bin)
- **Why:** To efficiently find the smallest bin that fits a package among thousands of bins.
- **Complexity:** $O(\log N)$
- **Logic:** Bins are sorted by capacity. The algorithm finds the first bin where `bin.capacity >= package.size`.

### B. Stack (Truck Loading Simulator)
- **Why:** Trucks are loaded from back to front. To remove an item deep inside, you must remove items in front of it first.
- **Logic:** Uses **LIFO** (Last-In, First-Out).
- **Rollback:** Supports popping the last $N$ items to correct loading errors.

### C. Queue (Conveyor Belt)
- **Why:** Packages arrive sequentially and must be processed in order.
- **Logic:** Uses **FIFO** (First-In, First-Out).

### D. Backtracking (Shipment Planner)
- **Why:** To determine if a specific combination of packages (e.g., fragile bundles) can fit into the remaining truck space.
- **Logic:** Recursively tries to fit packages. If a path leads to overflow, it **backtracks** and tries the next combination.

## 🛠 Tech Stack

### Frontend
- **HTML5, CSS3, JavaScript** (Vanilla, Responsive Design)
- **Google Fonts** (Outfit)

### Backend
- **Python 3.x**
- **FastAPI** (High-performance web framework)
- **Singleton Pattern** for Controller

### Algorithms
- Binary Search
- Stack / Queue Data Structures
- Backtracking Algorithm

### Database
- **MySQL** (Relational Database Management System)

### 🗄 Database Schema

The system uses a relational database to ensure data persistence.

### 📄 `shipment_logs`
| Column | Type | Description |
| :--- | :--- | :--- |
| `id` | INT | Primary Key (Auto Increment) |
| `tracking_id` | VARCHAR | Unique Package ID |
| `bin_id` | INT | ID of the bin (or -1 for Truck) |
| `timestamp` | DATETIME | Time of operation |
| `status` | VARCHAR | STORED, LOADED, ROLLBACK, etc. |

### 📦 `bins`
| Column | Type | Description |
| :--- | :--- | :--- |
| `bin_id` | INT | Unique Bin ID (Auto Increment) |
| `capacity` | INT | Volume capacity |
| `location_code` | VARCHAR | Physical location (e.g., A1, B2) |

## 📥 Installation & Setup Instructions

### 1. Clone Project
```bash
git clone https://github.com/yourusername/logistech.git
cd logistech
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Note: Requires `fastapi`, `uvicorn`, `mysql-connector-python`, `python-dotenv`)*

### 3. Configure Database
Create a `.env` file in the root directory with your MySQL credentials:
```ini
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=warehouse
```
*Ensure your MySQL server is running and accessible.*

### 4. Run Application
```bash
uvicorn api:app --reload
```

### 4. Open in Browser
Go to: `http://127.0.0.1:8000`

## 🔌 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/status` | Get current bin inventory |
| `POST` | `/package/add` | Add package to conveyor queue |
| `GET` | `/package/queue` | View current queue |
| `POST` | `/package/process` | Process next item (Binary Search) |
| `POST` | `/truck/load` | Load item onto truck (Stack) |
| `POST` | `/truck/rollback` | Remove last N items |
| `POST` | `/truck/can-fit` | Check fit (Backtracking) |
| `GET` | `/logs` | View audit logs |

## 📸 UI Screenshots

> *Placeholders for actual screenshots*

### Dashboard Overview
![Dashboard]<img width="1918" height="874" alt="Screenshot 2025-11-24 131830" src="https://github.com/user-attachments/assets/ce0656c6-ad9b-4e3f-9a07-2aa6a8e660b9" />


### Conveyor & Inventory
![Inventory]
<img width="368" height="213" alt="Screenshot 2025-11-24 131900" src="https://github.com/user-attachments/assets/95bf74d6-c677-4799-869e-3537cda99165" />
<img width="1112" height="199" alt="Screenshot 2025-11-24 131907" src="https://github.com/user-attachments/assets/ade5a51d-c105-422e-beee-8cf318c3526d" />

## 🔮 Future Enhancements

- **Real-time Updates:** Implement WebSockets for instant dashboard updates without polling.
- **IoT Integration:** Connect with RFID scanners for automated package tracking.
- **ML Optimization:** Use Machine Learning to predict package sizes and optimize bin layout.
- **Multi-Warehouse:** Scale the system to manage multiple warehouse locations.
- **User Auth:** Add Admin/Staff roles for security.

## 📜 License
MIT License
