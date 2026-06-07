# 🏨 Hotel Management System

A desktop **Hotel Management System** built with **Python (Tkinter)** and **MySQL**, enhanced with **AI/ML features** — sentiment analysis on guest reviews and automatic customer segmentation, plus an analytics dashboard, real‑time room availability, and PDF invoice generation.

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Screenshots / Modules](#-modules-overview)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Database Setup](#-database-setup)
- [Running the App](#-running-the-app)
- [Configuration](#-configuration)
- [AI / ML Features Explained](#-ai--ml-features-explained)
- [Default Login](#-default-login)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)

---

## ✨ Features

### Core
- 🔐 **Login / Register** with security‑question based password reset.
- 👤 **Customer management** — add, update, delete, search guest records.
- 🛏️ **Room inventory** — manage room number, floor and room type.
- 📅 **Room booking** with **calendar date pickers** (no more manual date typing).
- 🧑‍💼 **Staff details** management.

### Smart Booking
- ✅ **Real room availability** — only shows rooms that are *not already booked* for the selected dates.
- 🚫 **Double‑booking prevention** + check‑out‑after‑check‑in validation.
- 🔖 **Booking status** tracking (Checked‑in / Checked‑out / Cancelled).
- 🧾 **PDF invoice generation** — auto‑formatted bills saved to `main/invoices/`.

### Analytics & AI/ML
- 📊 **Dashboard** — live cards (occupancy, today's check‑ins/outs, revenue, customers) and charts.
- 💬 **Review Sentiment Analysis** — classifies guest feedback as Positive / Negative / Neutral using **VADER** (no model training needed).
- 🧠 **Customer Segmentation** — automatically groups guests into **Budget / Frequent / Premium** using **KMeans** clustering (unsupervised, no training step).

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| GUI | Tkinter, tkcalendar |
| Database | MySQL |
| Imaging | Pillow |
| PDF | fpdf2 |
| Charts | Matplotlib |
| Sentiment | vaderSentiment |
| Clustering | scikit-learn |

---

## 🧩 Modules Overview

| Module | File | Description |
|--------|------|-------------|
| Login / Reset | [`main/main.py`](main/main.py) | Authentication, forgot‑password flow |
| Register | [`main/register.py`](main/register.py) | New user sign‑up |
| Dashboard | [`main/hotel.py`](main/hotel.py) | Main menu / navigation hub |
| Customer | [`main/customer.py`](main/customer.py) | Guest CRUD + search |
| Room Booking | [`main/room.py`](main/room.py) | Availability, booking, billing, PDF invoice |
| Room Details | [`main/details.py`](main/details.py) | Room inventory management |
| Staff | [`main/staffdetails.py`](main/staffdetails.py) | Staff records |
| Analytics | [`main/dashboard.py`](main/dashboard.py) | KPI cards + charts |
| Reviews (AI) | [`main/reviews.py`](main/reviews.py) | Review entry + sentiment analysis |
| Segmentation (AI) | [`main/customer_segmentation.py`](main/customer_segmentation.py) | KMeans customer grouping |
| DB Helper | [`main/db.py`](main/db.py) | Central connection + schema setup |

---

## 📁 Project Structure

```
hotel management system/
├── README.md
├── requirements.txt
├── hotel images/                 # UI images, logos, backgrounds
└── main/
    ├── main.py                   # Entry point (Login window)
    ├── register.py               # Registration
    ├── hotel.py                  # Main menu
    ├── customer.py               # Customer module
    ├── room.py                   # Room booking + invoices
    ├── details.py                # Room inventory
    ├── staffdetails.py           # Staff module
    ├── dashboard.py              # Analytics dashboard
    ├── reviews.py                # Review sentiment analysis (AI)
    ├── customer_segmentation.py  # KMeans segmentation (AI)
    ├── db.py                     # Shared DB helper
    └── invoices/                 # Auto-generated PDF invoices
```

---

## ✅ Prerequisites

- **Python 3.10 or newer**
- **MySQL Server** running locally (or reachable)
- **pip** (comes with Python)

---

## ⚙️ Installation & Setup

```powershell
# 1. Clone or download the project, then open the folder
cd "hotel management system"

# 2. (Recommended) create a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

> **requirements.txt** includes: `mysql-connector-python`, `Pillow`, `tkcalendar`, `fpdf2`, `matplotlib`, `vaderSentiment`, `scikit-learn`.

---

## 🗄 Database Setup

1. Start MySQL and create the database:

```sql
CREATE DATABASE hotel_management_system;
USE hotel_management_system;
```

2. Create the core tables:

```sql
CREATE TABLE register (
    FirstName  VARCHAR(50),
    LastName   VARCHAR(50),
    Contact    VARCHAR(20),
    Email      VARCHAR(100) PRIMARY KEY,
    SecurityQ  VARCHAR(100),
    SecurityA  VARCHAR(100),
    Password   VARCHAR(100)
);

CREATE TABLE customer (
    `Ref no.`     VARCHAR(20),
    Name          VARCHAR(100),
    `Father name` VARCHAR(100),
    Gender        VARCHAR(20),
    Post          VARCHAR(20),
    Mobile        VARCHAR(20),
    Email         VARCHAR(100),
    Nationality   VARCHAR(50),
    `Id proof`    VARCHAR(50),
    `Id number`   VARCHAR(50),
    Address       VARCHAR(255)
);

CREATE TABLE details (
    `Room No.`   VARCHAR(20) PRIMARY KEY,
    `Floor`      VARCHAR(20),
    `Room Type`  VARCHAR(50)
);

CREATE TABLE room (
    `Customer Contact` VARCHAR(20),
    `Checkin date`     VARCHAR(20),
    `Checkout date`    VARCHAR(20),
    `Room Type`        VARCHAR(50),
    `Room No`          VARCHAR(20),
    Meal               VARCHAR(50),
    `No Of Days`       VARCHAR(20)
);

CREATE TABLE employee (
    emp_id      VARCHAR(20),
    Name        VARCHAR(100),
    Job         VARCHAR(50),
    Department  VARCHAR(50),
    DOJ         VARCHAR(20),
    Mobile      VARCHAR(20),
    Email       VARCHAR(100),
    Shift       VARCHAR(50),
    Address     VARCHAR(255),
    Salary      VARCHAR(20)
);
```

> 💡 The `room.Status` column and the `reviews` table are **created automatically** by the app on first run (see [`main/db.py`](main/db.py)). You do not need to create them manually.

---

## ▶️ Running the App

```powershell
cd main
python main.py
```

The **Login** window opens first. After logging in (or registering), the **main menu** gives access to all modules.

---

## 🔧 Configuration

Database credentials are centralised in [`main/db.py`](main/db.py) and can be overridden with **environment variables** (so you don't hard‑code passwords):

| Variable | Default | Purpose |
|----------|---------|---------|
| `HMS_DB_HOST` | `localhost` | MySQL host |
| `HMS_DB_USER` | `root` | MySQL user |
| `HMS_DB_PASSWORD` | *(set yours)* | MySQL password |
| `HMS_DB_NAME` | `hotel_management_system` | Database name |

Example (PowerShell):

```powershell
$env:HMS_DB_PASSWORD = "your_password"
python main.py
```

---

## 🤖 AI / ML Features Explained

### 💬 Review Sentiment Analysis ([`reviews.py`](main/reviews.py))
- Uses **VADER**, a rule‑based sentiment model 
- Each review's *compound score* maps to a label:
  - `score ≥ 0.05` → **Positive**
  - `score ≤ -0.05` → **Negative**
  - otherwise → **Neutral**
- Reviews + sentiment are stored in the auto‑created `reviews` table, with filtering and a summary breakdown. Sentiment also feeds the dashboard.

### 🧠 Customer Segmentation ([`customer_segmentation.py`](main/customer_segmentation.py))
- **Unsupervised KMeans clustering** — also **no training phase**. It groups whatever customers currently exist, on demand.
- Features per customer: number of bookings, total nights, total spend.
- Clusters are auto‑named by behaviour:
  - Highest average spend → **Premium**
  - Most bookings → **Frequent**
  - Remaining → **Budget**
- Just add customers/bookings and click **Run Segmentation** to regroup instantly.

---

## 🔑 Default Login

There is no seeded admin account. **Register a new user** from the login screen first, then log in with those credentials.

---

## 🧰 Troubleshooting

| Problem | Fix |
|---------|-----|
| `Access denied for user 'root'` | Set the correct password via `HMS_DB_PASSWORD` or in [`main/db.py`](main/db.py). |
| `Unknown database 'hotel_management_system'` | Run the `CREATE DATABASE` step. |
| `No module named 'tkcalendar' / 'fpdf' / 'sklearn'` | Run `pip install -r requirements.txt`. |
| Images not loading | The image paths are absolute (`D:\hotel management system\...`). Update them if your project lives elsewhere. |
| Dashboard/segmentation empty | Add some customers and bookings first — the analytics need data. |

---

## 🗺 Roadmap

- [ ] Password hashing (bcrypt) instead of plain text
- [ ] Role‑based access (Admin / Receptionist)
- [ ] Configurable pricing & tax (move out of code)
- [ ] CSV / Excel export
- [ ] Occupancy & revenue forecasting
- [ ] Relative image paths for portability

---

> Built with Python • Tkinter • MySQL • scikit‑learn • VADER

