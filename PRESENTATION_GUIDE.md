# Presentation & Interview Guide: Inventory Management System

This guide is designed to help you confidently present this project during placement interviews. It breaks down the system architecture, core codebase structures, database design, and likely questions an interviewer might ask.

---

## 1. Project Overview & Pitch

### The Pitch
> "I built/refactored a **monolithic Inventory Management System** using Django. The system tracks parts (components), coordinates physical stock locations, manages supplier companies, and processes purchase orders. I simplified the architecture to prioritize ease of deployment, utilizing SQLite for quick local setups and scripting a single-command entry point (`run.py`) to handle database setup, asset preparation, and superuser generation out of the box."

### Key Constraints Solved
* **Zero-Config Deployment**: Handled complex environment configuration programmatically so the app runs immediately using `python3 run.py`.
* **Lightweight Footprint**: Disabled enterprise overhead (like plug-ins, heavy background worker setups, and native report printing libraries) to make it suitable for local developer environments.

---

## 2. Core Architecture & Modules

The project follows the standard **Django Model-View-Template (MVT)** pattern:

```
[Client/Browser] <---> [Django URLs] <---> [Views/API] <---> [Models/Database]
```

Here are the 5 core apps you need to explain:

1. **`part/` (Parts Catalog)**
   - *Purpose*: Defines what items exist in the catalog. Includes categories and Bills of Materials (BOM) to represent assemblies (parts made of other parts).
   - *Key File*: `part/models.py` defines `Part`, `PartCategory`, and `BomItem`.
2. **`stock/` (Stock Tracking)**
   - *Purpose*: Tracks the physical location and quantity of the parts defined in `part/`.
   - *Key File*: `stock/models.py` defines `StockItem` and `StockLocation`.
3. **`company/` (Suppliers & Manufacturers)**
   - *Purpose*: Tracks third-party entities who manufacture or supply parts.
   - *Key File*: `company/models.py` defines `Company` and `SupplierPart`.
4. **`order/` (Purchase Orders)**
   - *Purpose*: Manages purchasing parts from suppliers.
   - *Key File*: `order/models.py` defines `PurchaseOrder` and `PurchaseOrderLineItem`.
5. **`users/` (Authentication & Control)**
   - *Purpose*: Manages admin accounts and user permissions.

---

## 3. Database Relationships (ERD Concepts)

Be prepared to explain how the models relate to each other:

* **Many-to-One (ForeignKey)**: A `StockItem` links to a `Part` (one part can have many physical stock items in different places).
* **Self-Referential ForeignKey (Adjacency List)**: `PartCategory` and `StockLocation` both use self-referential relationships to create hierarchical structures (e.g., a Location can have parent/child Locations, like "Warehouse A -> Shelf 3 -> Bin 2").
* **Many-to-Many**: A `Part` relates to other parts via `BomItem` (establishing which components build an assembly).

---

## 4. Key Interview Questions & Answers

### Q1: Why did you choose a monolithic Django architecture over Microservices?
* **Answer**: "For an inventory management system of this scale, a monolith keeps database transactions ACID-compliant and makes deployment straightforward. Microservices introduce complex network overhead, eventual consistency problems, and distributed transaction challenges (like the Saga pattern) which are unnecessary for this business domain."

### Q2: How do you handle performance optimization when fetching large amounts of inventory data?
* **Answer**: "Django's ORM is lazy by default, which can lead to the $N+1$ query problem when accessing related foreign key fields (e.g., accessing `item.part.name` for 100 stock items). I resolve this by using `.select_related()` for ForeignKey relationships (SQL `JOIN`) and `.prefetch_related()` for many-to-many or reverse relationships to batch-fetch records in a single query."

### Q3: How are migrations managed in this project?
* **Answer**: "Django manages schema changes through migration files. When a model's structure is updated, we run `python manage.py makemigrations` to generate step-by-step SQL conversion scripts, and `python manage.py migrate` to apply them. In the startup script, this is automated to ensure the SQLite schema is always up to date."

### Q4: What database constraints are in place to prevent corrupt inventory data?
* **Answer**: "We enforce integrity at both the application level and the database level:
  1. `unique_together` constraints (e.g., a Part SKU must be unique).
  2. Cascade behaviors: using `models.PROTECT` or `models.SET_NULL` for critical associations (like preventing a `Part` deletion if active `StockItem` records exist) to avoid orphaned records."

---

## 5. Walkthrough Demo Steps

When demonstrating this project to an evaluator, follow this flow:

1. **Start the server**: Run `python3 run.py` in the terminal to show the automated setup.
2. **Access Admin**: Go to `http://127.0.0.1:8000/admin` and log in using `admin / admin123`.
3. **Show Core Flows**:
   - Create a new **Part Category** (e.g., "Electronics") and add a **Part** (e.g., "Resistor 10k").
   - Create a **Stock Location** (e.g., "Main Warehouse") and place 50 units of the "Resistor 10k" into it.
   - Show how the stock counts update dynamically.
