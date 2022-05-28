import sqlite3
import random

def account_number_generator():
    global acct
    # use random.sample() then define a range of numbers ie range(), and pass the counts for the total numbers.
    integers = random.sample(range(10), 9)
    # using list comprehension to generate 9 random numbers.
    strings = [str(integer) for integer in integers]
    # using ''.join() to convert list back to string
    a = '2' + ''.join(strings)
    acct = int(a)
    return acct
global acct
account_number_generator()

# create() runs immediately app is launched, to create the db_file and table automatically.
def create():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT,fname text, lname text,username text UNIQUE,password text,acctnumber integer,balance integer)")
    conn.commit()
    conn.close()
create()


def insert(username, password, balance=1000):
    conn = sqlite3.connect('Banking.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO bank VALUES (NULL,?,?,?)", ((username, password, balance)))
    conn.commit()
    conn.close()
# insert('admin', 'password')
# insert('dking', 'cisco')


def view_balance():
    conn = sqlite3.connect('Banking.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bank')
    rows = cur.fetchall()
    conn.close()
    return rows
print('previous items in db are:', view_balance())


# executes when register button is clicked.
def registion_button(fname, lname, username, password, acctnumber=acct, balance=1000):
    conn = sqlite3.connect('banking.db')
    cur = conn.cursor()
    check = cur.execute('SELECT username, password FROM bank WHERE username=? AND password=?', (username, password))
    row = check.fetchone()
    if row:
        print('entry already exists..', row)
    else:
        check.execute("INSERT INTO bank VALUES (NULL,?,?,?,?,?,?)", (fname, lname, username, password, acctnumber, balance))
        print('registration successful..')
        conn.commit()
        conn.close()
registion_button('Nathan', 'Alabi', 'dking', 'dddd')
print('Current items in db are:', view_balance())


# executes when login button is clicked.
def login_button(username='hannah', password='dammy'):
    conn = sqlite3.connect('Banking.db')
    cur = conn.cursor()
    check = cur.execute('SELECT username, password FROM bank WHERE username=? AND password=?', (username, password))
    row = check.fetchone()
    if row:
        print('login check success..')
        check.execute('SELECT * FROM bank WHERE username=? AND password=?', (username, password))
        r = check.fetchone()
        # using indexing to list values from db.. ie r[0] is id, r[1] is f_name, r[2] is l_name, r[3] is balance.
        print(f'welcome {r[1]} {r[2]}, your acct balance is ${r[3]}')
    else:
        print('user does not exist, go and create an account!')
#login_button()


# for calculating withdrawals.
# i can draft out deposit from here also..
#wd = int(input('withdraw amount: '))
def withdraw_from_account(wd=30, username='dking'):
    conn = sqlite3.connect('Banking.db')
    cur = conn.cursor()
    global bal
    global new_balance
    bal = int(bal)
    new_balance = bal - wd
    # query for subtrating.
    cur.execute('UPDATE bank SET BALANCE=BALANCE - {} WHERE username=?'.format(wd), (username,))
    conn.commit()
    conn.close()
    print( f'u withdrew ${wd} new balance is now ${view_balance()}')
withdraw_from_account()
print(view_balance())