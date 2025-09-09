import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

DB_FILE = "bank.db"

# ---------------- DATABASE HELPERS ---------------- #
def init_db():
    """Create database and initial accounts if not exist"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY,
        balance REAL NOT NULL
    )
    """)
    # Insert initial accounts if empty
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if cursor.fetchone()[0] == 0:
        initial_accounts = [
            (10001, 5000), (10002, 12000), (10003, 750),
            (10004, 30000), (10005, 1500), (10006, 9800),
            (10007, 450), (10008, 22000), (10009, 6700),
            (10010, 100000)
        ]
        cursor.executemany("INSERT INTO accounts (account_number, balance) VALUES (?, ?)", initial_accounts)
        conn.commit()
    conn.close()

def get_balance(acc):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM accounts WHERE account_number=?", (acc,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def update_balance(acc, new_balance):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET balance=? WHERE account_number=?", (new_balance, acc))
    conn.commit()
    conn.close()

def fetch_all_accounts():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT account_number, balance FROM accounts")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------------- BANK OPERATIONS ---------------- #
def update_table():
    """Refresh the accounts table"""
    for row in tree.get_children():
        tree.delete(row)
    for acc, bal in fetch_all_accounts():
        tree.insert('', 'end', values=(acc, bal))

def create_account():
    """Create a new bank account"""
    try:
        acc = int(acc_entry.get())
        initial = float(amount_entry.get())
        if get_balance(acc) is not None:
            messagebox.showerror("Error", "Account already exists!")
            return
        if initial < 1000:
            messagebox.showwarning("Warning", "Initial balance must be >= 1000")
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (account_number, balance) VALUES (?, ?)", (acc, initial))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Account {acc} created with Rs:{initial}")
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")

def deposit():
    """Deposit money into an account"""
    try:
        acc = int(acc_entry.get())
        amt = float(amount_entry.get())
        bal = get_balance(acc)
        if bal is None:
            messagebox.showerror("Error", "Account does not exist!")
            return
        update_balance(acc, bal + amt)
        messagebox.showinfo("Success", f"Deposited Rs:{amt}. New balance: Rs:{bal+amt}")
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")

def withdraw():
    """Withdraw money from an account"""
    try:
        acc = int(acc_entry.get())
        amt = float(amount_entry.get())
        bal = get_balance(acc)
        if bal is None:
            messagebox.showerror("Error", "Account does not exist!")
            return
        if bal < amt:
            messagebox.showerror("Error", "Insufficient balance!")
            return
        update_balance(acc, bal - amt)
        messagebox.showinfo("Success", f"Withdrawn Rs:{amt}. New balance: Rs:{bal-amt}")
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")

def check_balance():
    """Check the balance of an account"""
    try:
        acc = int(acc_entry.get())
        bal = get_balance(acc)
        if bal is None:
            messagebox.showerror("Error", "Account does not exist!")
            return
        messagebox.showinfo("Balance", f"Account {acc} balance: Rs:{bal}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")

def transfer():
    """Transfer money between accounts"""
    try:
        sender = int(sender_entry.get())
        recipient = int(recipient_entry.get())
        amt = float(amount_entry.get())
        sender_bal = get_balance(sender)
        recipient_bal = get_balance(recipient)
        if sender_bal is None or recipient_bal is None:
            messagebox.showerror("Error", "Sender or recipient account does not exist!")
            return
        if sender_bal < amt:
            messagebox.showerror("Error", "Insufficient balance in sender account!")
            return
        update_balance(sender, sender_bal - amt)
        update_balance(recipient, recipient_bal + amt)
        messagebox.showinfo("Success", f"Transferred Rs:{amt} from {sender} to {recipient}")
        update_table()
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers!")

# ---------------- PROFESSIONAL FUNCTIONS ---------------- #
def delete_account():
    """Delete an account"""
    try:
        acc = int(acc_entry.get())
        if get_balance(acc) is None:
            messagebox.showerror("Error", "Account does not exist!")
            return
        confirm = messagebox.askyesno("Confirm Delete", f"Delete account {acc}?")
        if confirm:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM accounts WHERE account_number=?", (acc,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", f"Account {acc} deleted.")
            update_table()
    except ValueError:
        messagebox.showerror("Error", "Enter valid account number!")

def search_account():
    """Search for an account by account number"""
    try:
        acc = int(acc_entry.get())
        bal = get_balance(acc)
        if bal is None:
            messagebox.showerror("Error", "Account does not exist!")
            return
        messagebox.showinfo("Search Result", f"Account {acc} balance: Rs:{bal}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid account number!")

def rich_accounts():
    """Show accounts with balance above a threshold"""
    try:
        threshold = simpledialog.askfloat("Threshold", "Show accounts with balance >= Rs:")
        if threshold is None:
            return
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT account_number, balance FROM accounts WHERE balance>=?", (threshold,))
        data = cursor.fetchall()
        conn.close()
        if not data:
            messagebox.showinfo("No Accounts", f"No accounts with balance >= Rs:{threshold}")
            return
        for row in tree.get_children():
            tree.delete(row)
        for acc, bal in data:
            tree.insert('', 'end', values=(acc, bal))
        messagebox.showinfo("Rich Accounts", f"Showing accounts with balance >= Rs:{threshold}")
    except ValueError:
        messagebox.showerror("Error", "Enter valid number!")

def reset_balances():
    """Reset all balances to Rs:1000"""
    confirm = messagebox.askyesno("Reset Balances", "Reset all balances to Rs:1000?")
    if confirm:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET balance=1000")
        conn.commit()
        conn.close()
        messagebox.showinfo("Reset Done", "All account balances reset to Rs:1000")
        update_table()

# ---------------- GUI SETUP ---------------- #
init_db()

root = tk.Tk()
root.title("🏦 Professional Bank App")
root.geometry("700x700")
root.configure(bg="#f0f0f0")

title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
btn_font = ("Helvetica", 12, "bold")

tk.Label(root, text="Welcome to Professional Bank", font=title_font, bg="#f0f0f0").pack(pady=10)

# Account Operations Frame
frame1 = tk.LabelFrame(root, text="Account Operations", padx=10, pady=10, font=label_font, bg="#e0e0e0")
frame1.pack(padx=10, pady=10, fill="x")

tk.Label(frame1, text="Account Number:", font=label_font, bg="#e0e0e0").grid(row=0, column=0, pady=5, sticky="w")
acc_entry = tk.Entry(frame1)
acc_entry.grid(row=0, column=1, pady=5)

tk.Label(frame1, text="Amount:", font=label_font, bg="#e0e0e0").grid(row=1, column=0, pady=5, sticky="w")
amount_entry = tk.Entry(frame1)
amount_entry.grid(row=1, column=1, pady=5)

tk.Button(frame1, text="Create Account", width=15, font=btn_font, bg="#4CAF50", fg="white", command=create_account).grid(row=2, column=0, pady=5)
tk.Button(frame1, text="Deposit", width=15, font=btn_font, bg="#2196F3", fg="white", command=deposit).grid(row=2, column=1, pady=5)
tk.Button(frame1, text="Withdraw", width=15, font=btn_font, bg="#FF5722", fg="white", command=withdraw).grid(row=3, column=0, pady=5)
tk.Button(frame1, text="Check Balance", width=15, font=btn_font, bg="#9C27B0", fg="white", command=check_balance).grid(row=3, column=1, pady=5)
tk.Button(frame1, text="Delete Account", width=15, font=btn_font, bg="#E91E63", fg="white", command=delete_account).grid(row=4, column=0, pady=5)
tk.Button(frame1, text="Search Account", width=15, font=btn_font, bg="#3F51B5", fg="white", command=search_account).grid(row=4, column=1, pady=5)
tk.Button(frame1, text="Rich Accounts", width=32, font=btn_font, bg="#00BCD4", fg="white", command=rich_accounts).grid(row=5, column=0, columnspan=2, pady=5)
tk.Button(frame1, text="Reset All Balances", width=32, font=btn_font, bg="#795548", fg="white", command=reset_balances).grid(row=6, column=0, columnspan=2, pady=5)

# Transfer Money Frame
frame2 = tk.LabelFrame(root, text="Transfer Money", padx=10, pady=10, font=label_font, bg="#e0e0e0")
frame2.pack(padx=10, pady=10, fill="x")

tk.Label(frame2, text="Sender Account:", font=label_font, bg="#e0e0e0").grid(row=0, column=0, pady=5, sticky="w")
sender_entry = tk.Entry(frame2)
sender_entry.grid(row=0, column=1, pady=5)

tk.Label(frame2, text="Recipient Account:", font=label_font, bg="#e0e0e0").grid(row=1, column=0, pady=5, sticky="w")
recipient_entry = tk.Entry(frame2)
recipient_entry.grid(row=1, column=1, pady=5)

tk.Button(frame2, text="Transfer", width=20, font=btn_font, bg="#FFC107", fg="black", command=transfer).grid(row=2, column=0, columnspan=2, pady=10)

# Accounts Table Frame
frame3 = tk.LabelFrame(root, text="All Accounts", padx=10, pady=10, font=label_font, bg="#e0e0e0")
frame3.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("Account Number", "Balance")
tree = ttk.Treeview(frame3, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center")
tree.pack(fill="both", expand=True)
update_table()

# Exit button
tk.Button(root, text="Exit", width=20, font=btn_font, bg="#B71C1C", fg="white", command=root.destroy).pack(pady=10)

root.mainloop()



