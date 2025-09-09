# 🏦 Professional Bank App (Tkinter + SQLite)

## Description
The **Professional Bank App** is a desktop banking application built using Python's **Tkinter** for the GUI and **SQLite** for data storage. It simulates a real-world banking system, allowing users to manage accounts, perform transactions, and view account details in a simple and interactive interface.

This app is ideal for beginners learning **Python GUI development** and **SQLite database management** while building a practical project.

---

## Features

### Account Management
- Create new accounts (minimum initial balance Rs:1000)
- Delete accounts
- Search for accounts

### Transactions
- Deposit money
- Withdraw money
- Transfer money between accounts

### Account Insights
- Check account balance
- View all accounts in a table
- Filter accounts by balance (Rich Accounts)

### Admin Utilities
- Reset all account balances to Rs:1000

### Data Persistence
- All account data is stored in a local SQLite database (`bank.db`)

---

## How to Run
1. Install **Python 3**: [Python Downloads](https://www.python.org/downloads/)  
2. Tkinter comes pre-installed. Test by running:
    ```python
    import tkinter
    ```
3. Save the script as `bank_app.py`.  
4. Open a terminal (or command prompt) and navigate to the folder containing `bank_app.py`.  
5. Run the app using the command:
    ```bash
    python bank_app.py
    ```
6. The GUI allows you to:
    - Create new accounts (minimum initial balance Rs:1000)
    - Deposit, Withdraw, Check balance
    - Transfer money between accounts
    - Delete accounts or search accounts
    - View all accounts and filter rich accounts
    - Reset all balances (useful for testing)

---

## Requirements
- Python 3.x  
- Tkinter (pre-installed with Python)  
- SQLite3 (built-in with Python)  

---

## Notes
- All data is stored in a local SQLite database file named `bank.db` in the same folder as the script.  
- The app is designed for **educational and demonstration purposes**; it is **not for real banking use**.
