# Stock Analyzer Platform

Stock Analyzer is a simulated trading and investment analysis web platform. It features user authentication, a simulated live-ticking market (using Geometric Brownian Motion), real-time portfolio tracking, virtual trading (buying/selling), and historical charts with indicators (SMA, EMA, RSI, MACD).

---

## 🛠️ Tech Stack & Features

- **Backend**: Python Flask & Flask-SQLAlchemy.
- **Database**: Local SQLite database out-of-the-box (fallback) or MySQL database (fully compatible schema provided).
- **Frontend**: Responsive custom HTML & premium Vanilla CSS styling (dark mode, glassmorphic accents, custom micro-animations).
- **Charting**: Interactive line and doughnut charts using Chart.js.
- **Simulation**: Geometric Brownian Motion for live market fluctuation + technical indicators calculation (SMA, EMA, RSI, MACD) in real-time.

---

## 📂 Project Directory Structure

```text
stock_analyzer/
├── app.py                      # Main entrypoint, routing & API handlers
├── database.py                 # SQLAlchemy DB models & user authentication
├── simulator.py                # Live market engine & technical indicator calculator
├── requirements.txt            # Python dependencies list
├── schema.sql                  # MySQL schema definition script
├── README.md                   # Installation & Setup documentation
├── static/
│   ├── css/
│   │   └── style.css           # Custom dark theme styles
│   └── js/
│       ├── app.js              # Real-time data updating & core behaviors
│       └── charts.js           # Chart.js graphing configurations
└── templates/
    ├── base.html               # Shared layout structure with live ticker
    ├── login.html              # Authenticate or Register screen
    ├── dashboard.html          # Net Worth summary & asset allocation
    ├── market.html             # Chart analysis, technical metrics & place orders
    └── transactions.html       # Historical execution logs
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install the Python dependencies:
```bash
pip install -r requirements.txt
```

### 2. Running the Application (SQLite Out-of-the-Box)
By default, the application runs with an automatic SQLite fallback. This means it creates a local file named `stock_analyzer.db` in the root folder and runs immediately without any database setup!

Run the app:
```bash
python3 app.py
```
Open [http://localhost:5000](http://localhost:5000) in your web browser.

---

## 🛢️ Connecting to MySQL

If you wish to run the project using a local or remote **MySQL** instance, follow these steps:

### 1. Create the Database & Tables
Log in to your MySQL terminal and run the DDL schema script:
```bash
mysql -u your_username -p < schema.sql
```
*Alternatively, you can copy the contents of `schema.sql` and run them inside your favorite SQL client (e.g. MySQL Workbench, DBeaver).*

### 2. Configure Environment Variable
Set the `DATABASE_URL` environment variable before running the Flask application. Use the `pymysql` driver (which is already configured in the dependencies):

```bash
export DATABASE_URL="mysql+pymysql://your_mysql_username:your_mysql_password@localhost/stock_analyzer"
```

### 3. Run the App
Now run the app normally:
```bash
python3 app.py
```
Flask will automatically pick up the MySQL connection string and use it to authenticate users and persist trades.
