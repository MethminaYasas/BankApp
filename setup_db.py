import sqlite3

# Connect to database (creates file if it doesn't exist)
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create accounts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_number INTEGER PRIMARY KEY,
    balance REAL NOT NULL
)
""")

# Insert initial accounts if empty
cursor.execute("SELECT COUNT(*) FROM accounts")
if cursor.fetchone()[0] == 0:
    # More professional and varied accounts
    initial_accounts = [
        (10001, 5000.00),
        (10002, 12000.50),
        (10003, 750.75),
        (10004, 30000.00),
        (10005, 1500.25),
        (10006, 9800.00),
        (10007, 450.00),
        (10008, 22000.00),
        (10009, 6700.00),
        (10010, 100000.00)
    ]
    cursor.executemany("INSERT INTO accounts (account_number, balance) VALUES (?, ?)", initial_accounts)
    conn.commit()

conn.close()
print("Database created and ready with professional accounts!")
