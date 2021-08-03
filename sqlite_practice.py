import sqlite3

db = sqlite3.connect(':memory:') # use in-memory database
cur = db.cursor() # Create cursor object to run queries

# Create Customer table, a parent table
queryCreateCustomer = '''
CREATE TABLE IF NOT EXISTS customer (
    customer_id integer PRIMARY KEY,
    name varchar(255),
    age integer,
    gender varchar(255) 
)
'''

cur.execute(queryCreateCustomer)

# Create Transactions table
queryCreateTransactions = '''
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id integer PRIMARY KEY,
    customer_id integer,
    transaction_date date,
    item varchar(255),
    amount float,
    CONSTRAINT customer_id
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
)
'''

cur.execute(queryCreateTransactions)

# Insert records into Customer table
queryInsertCustomer = '''
INSERT INTO customer(name, age, gender)
VALUES ('Tan Xay Yin', 29, 'F'),
('Robert Pickford', 43, 'M'),
('Ibrahim Mahmud', 37, 'M')
'''
cur.execute(queryInsertCustomer)

# Insert records into Transactions table
queryInsertTransactions = '''
INSERT INTO transactions(customer_id, transaction_date, item, amount)
VALUES (1, '2021-03-03', 'xbox', 700),
(1, '2021-06-01', 'morris fan', 120),
(2, '2021-04-05', 'xbox', 680),
(2, '2021-05-01', 'adidas shoes', 89),
(2, '2021-07-04', 'adidas shoes', 94),
(3, '2021-01-01', 'adidas shoes', 124),
(3, '2021-04-08', 'philips tv', 940)
'''
cur.execute(queryInsertTransactions)

# Aggregation
# Find total amount spent by customer
queryTotalAmount = '''
SELECT customer.customer_id, SUM(transactions.amount) AS total_amount
FROM customer AS customer
LEFT JOIN transactions AS transactions
ON (customer.customer_id = transactions.customer_id)
GROUP BY customer.customer_id
ORDER BY total_amount DESC
'''
cur.execute(queryTotalAmount)
print(cur.fetchall())

# Window functions
# Find amount growth day by day by customer
queryAmountGrowth = '''
SELECT a.*, (a.amount - a.previous_amount)/a.previous_amount AS amount_growth
FROM
(
SELECT customer.customer_id, transactions.transaction_date, transactions.amount, 
COALESCE(LAG(transactions.amount) OVER (PARTITION BY customer.customer_id ORDER BY transactions.transaction_id ASC), 0) AS previous_amount
FROM customer AS customer
LEFT JOIN transactions AS transactions
ON (customer.customer_id = transactions.customer_id)
) AS a
'''
cur.execute(queryAmountGrowth)
print(cur.fetchall())

# Find daily sales growth
queryDailyGrowth = '''
SELECT a.*, (a.sales - COALESCE(LAG(sales) OVER (ORDER BY a.transaction_date ASC), 0))/COALESCE(LAG(sales) OVER (ORDER BY a.transaction_date ASC), 1)
FROM
(
SELECT transactions.transaction_date, SUM(transactions.amount) AS sales
FROM transactions AS transactions
GROUP BY transactions.transaction_date
) AS a
'''
cur.execute(queryDailyGrowth)
print(cur.fetchall())
