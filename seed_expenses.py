import sqlite3
import random
from datetime import datetime, timedelta
from database.db import get_db

def seed_expenses(user_id, count, months):
    categories = {
        'Food': {'range': (50, 800), 'weight': 30, 'desc': ['Morning Latte', 'Lunch Special', 'Dinner with Friends', 'Grocery Store', 'Street Food', 'Quick Snack']},
        'Transport': {'range': (20, 500), 'weight': 20, 'desc': ['Uber Ride', 'Auto Rickshaw', 'Petrol Fill', 'Metro Fare', 'Bus Pass']},
        'Bills': {'range': (200, 3000), 'weight': 10, 'desc': ['Electricity Bill', 'Water Bill', 'Internet Bill', 'Mobile Recharge', 'Gas Bill']},
        'Health': {'range': (100, 2000), 'weight': 5, 'desc': ['Pharmacy', 'Dental Checkup', 'General Physician', 'Eye Care']},
        'Entertainment': {'range': (100, 1500), 'weight': 5, 'desc': ['Movie Ticket', 'Gaming Zone', 'Streaming Service', 'Book Store', 'Concert Ticket']},
        'Shopping': {'range': (200, 5000), 'weight': 15, 'desc': ['New Shirt', 'Shoes', 'Home Decor', 'Gadget Accessory', 'Electronic Item']},
        'Other': {'range': (50, 1000), 'weight': 10, 'desc': ['Gift', 'Stationery', 'Misc Expense', 'Charity', 'Donation']},
    }

    category_names = list(categories.keys())
    weights = [categories[c]['weight'] for c in category_names]
    
    expenses = []
    start_date = datetime.now() - timedelta(days=months * 30)
    end_date = datetime.now()

    for _ in range(count):
        cat_name = random.choices(category_names, weights=weights)[0]
        cat_info = categories[cat_name]
        amount = random.randint(*cat_info['range'])
        description = random.choice(cat_info['desc'])
        
        days_offset = random.randint(0, (end_date - start_date).days)
        date_str = (start_date + timedelta(days=days_offset)).strftime('%Y-%m-%d')
        
        expenses.append((user_id, amount, cat_name, date_str, description))

    try:
        with get_db() as conn:
            conn.execute('BEGIN TRANSACTION')
            conn.executemany(
                'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                expenses
            )
            conn.commit()
            
            sample = conn.execute(
                'SELECT date, category, description, amount FROM expenses WHERE user_id = ? ORDER BY date DESC LIMIT 5',
                (user_id,)
            ).fetchall()
            
            return {
                "count": len(expenses),
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "sample": sample
            }
    except sqlite3.Error as e:
        print(f"Error during insertion: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python seed_expenses.py <user_id> <count> <months>")
        sys.exit(1)
    
    try:
        uid = int(sys.argv[1])
        cnt = int(sys.argv[2])
        mth = int(sys.argv[3])
    except ValueError:
        print("Error: User ID, count, and months must be integers.")
        sys.exit(1)
    
    with get_db() as conn:
        user = conn.execute('SELECT id FROM users WHERE id = ?', (uid,)).fetchone()
        if not user:
            print(f"No user found with id {uid}.")
            sys.exit(1)
            
    result = seed_expenses(uid, cnt, mth)
    if result:
        print(f"Inserted {result['count']} expenses.")
        print(f"Date range: {result['start_date']} to {result['end_date']}")
        print("\nSample Records:")
        for row in result['sample']:
            print(f"{row['date']} | {row['category']} | {row['description']} | ₹{row['amount']}")
    else:
        print("Seeding failed.")
