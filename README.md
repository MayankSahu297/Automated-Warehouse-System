# LogisTech: Automated Warehouse Management System

![LogisTech Banner](https://placehold.co/1200x300/1e293b/3b82f6?text=LogisTech+Automated+Warehouse+System)

## Project Description

**LogisTech** is a full-stack Automated Warehouse Orchestration System that manages incoming packages, finds optimal storage bins using **Binary Search**, loads trucks using **Stack** logic, and validates fragile bundle shipments using **Backtracking**.

The entire system is powered by a **Singleton** controller and backed by **SQL-based audit logs** to ensure full traceability.

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

```mermaid
graph TD
    User[User / Web UI] -->|HTTP Requests| API[FastAPI Backend]
    API -->|Calls| Controller[LogisTech Controller (Singleton)]
    Controller -->|FIFO| Queue[Conveyor Belt]
    Controller -->|Binary Search| Inventory[Bin Inventory]
    Controller -->|Backtracking| Planner[Shipment Planner]
    Controller -->|LIFO| Stack[Truck Loading Dock]
    Controller -->|Persist| DB[(MySQL Database)]
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
![Dashboard](https://placehold.co/600x400/1e293b/3b82f6?text=Dashboard+Screenshot)

### Conveyor & Inventory
![Inventory](https://placehold.co/600x400/1e293b/3b82f6?text=Inventory+View)

## 🔮 Future Enhancements

- **Real-time Updates:** Implement WebSockets for instant dashboard updates without polling.
- **IoT Integration:** Connect with RFID scanners for automated package tracking.
- **ML Optimization:** Use Machine Learning to predict package sizes and optimize bin layout.
- **Multi-Warehouse:** Scale the system to manage multiple warehouse locations.
- **User Auth:** Add Admin/Staff roles for security.

## 📜 License
MIT License
