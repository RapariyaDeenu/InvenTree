# Inventory Management System

A simplified, beginner-friendly Inventory Management System built on Django, optimized for college students, learning, and job interview demonstrations.

This project was simplified from the open-source InvenTree project to focus on core inventory features: Parts, Stock, Companies, Orders, and Users.

## Features Included
- **Part Tracking**: Manage catalog items, BOM (Bill of Materials), and part categories.
- **Stock Control**: Track physical stock items and their locations.
- **Company Management**: Keep records of suppliers and manufacturers.
- **Purchase Orders**: Basic order workflow tracking.
- **User Authentication**: Default admin control.

## Quick Start (Under 5 Minutes)

You can run this project with a single command! The startup script handles database migrations, collects static assets, automatically creates a default administrator account, and starts the development server.

### Prerequisites
Make sure you have Python 3 installed.

### Setup and Start

From the root directory of the project, run:
```bash
python3 run.py
```

*Note: The script automatically activates the pre-configured virtual environment under `src/backend/venv`.*

### Access the Application
- **URL**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Admin Credentials**:
  - **Username**: `admin`
  - **Password**: `admin123`

---

## Technical Details (For Interviews)
- **Framework**: Django (Monolithic backend architecture)
- **Database**: SQLite3 (Local storage, zero configuration required)
- **Primary Apps**:
  - `part/`: Manages part definitions and categories.
  - `stock/`: Manages physical stock and tracking locations.
  - `company/`: Manages manufacturer and supplier records.
  - `order/`: Manages purchase orders.
  - `users/`: Handles user logins and permissions.

For detailed guidelines on how to present this project during a placement interview, see [PRESENTATION_GUIDE.md](PRESENTATION_GUIDE.md).
