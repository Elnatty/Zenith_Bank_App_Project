from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import sqlite3
import random
import time

root = Tk()
root.title('Zenith Bank Mobile by DKING')
root.geometry('800x405')
root.iconbitmap('images_and_icon/computer.ico')
root.configure(bd=3)


# account number generator.
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


# 0 ---------->>> SQLITE3 functions
# create() runs immediately app is launched, to create the db_file and table automatically.
def create():
    conn = sqlite3.connect('banking.db')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS bank (id INTEGER PRIMARY KEY AUTOINCREMENT,fname text, lname text,username text UNIQUE,password text,acctnumber integer,balance integer)")
    conn.commit()
    conn.close()
create()


def view_balance():
    conn = sqlite3.connect('banking.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM bank')
    rows = cur.fetchall()
    conn.close()
    return rows
print(f'current users: {view_balance()}')


def registration_sql(fname, lname, username, password, acctnumber=acct, balance=1000):
    conn = sqlite3.connect('banking.db')
    cur = conn.cursor()
    check = cur.execute('SELECT username, password FROM bank WHERE username=? AND password=?', (username, password))
    row_reg = check.fetchone()
    if row_reg:
        register_info.grid_forget()
        register_info_check = Label(register_tab)
        register_info_check.grid(row=5, column=0, columnspan=2)
        register_info_check.configure(text='entry already exists..')
    else:
        check.execute("INSERT INTO bank VALUES (NULL,?,?,?,?,?,?)",
                      (fname, lname, username, password, acctnumber, balance))
        print('registration successful..')
        conn.commit()
        # conn.close()


# for dev option.
def dev_option():
    # wipes page_2_frame_label
    page_2_frame_label.pack_forget()
    # brings up page_5_frame_label
    page_5_frame_label.pack()
    # page_5 ui design.
    frame_for_dev_option.grid(row=0, column=0, pady=25)
    # dev_option label
    dev_option_label_page_5.grid(row=0, column=0)
    # dev option button
    dev_option_button_back.grid(row=1, column=0)
    print(info)


# logout function.
def logout():
    page_2_frame_label.pack_forget()
    page_1_frame_label.pack()
    f_name_register_entry.delete(0, END)
    l_name_register_entry.delete(0, END)
    username_register_entry.delete(0, END)
    password_register_entry.delete(0, END)
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    register_info.configure(text='')
    login_info.configure(text='')


# deposit_money main function
def deposit_money(deposit_amt, username):
    try:
        conn = sqlite3.connect('banking.db')
        cur = conn.cursor()
        if (len(deposit_amount.get()) == 0 or len(deposit_password.get()) == 0):
            deposit_status_page_4.configure(text='')
            deposit_status_page_4.configure(text='enter required entries..')
            print('enter required entries..')
        else:
            if username != un_for_check:
                print('dont use another person username man!')
                deposit_status_page_4.configure(text='')
                deposit_status_page_4.configure(text='wrong username..')
            else:
                # to handle negative inputs
                if int(deposit_amt) <= 0:
                    deposit_status_page_4.configure(text='')
                    deposit_status_page_4.configure(text='deposit error...')
                else:
                    cur.execute('UPDATE bank SET BALANCE=BALANCE + {} WHERE username=?'.format(deposit_amt), (username,))
                    usrbal = cur.execute('SELECT balance from bank WHERE username=?', (username,))
                    global usr
                    usr = usrbal.fetchone()
                    usr = str(usr[0])
                    conn.commit()
                    conn.close()
                    print(f'u deposited ${deposit_amt} new balance is ${usr}')
                    deposit_status_page_4.configure(text='')
                    deposit_status_page_4.configure(
                        text='deposit of ${} success,\nnew balance is ${}'.format(deposit_amt, usr))
                    deposit_amt.format('')
                    # errors to handle
                    # TypeError--username not exist.
    except (TypeError, ValueError, sqlite3.OperationalError) as e:
        print('wrong username..')
        deposit_status_page_4.configure(text='')
        deposit_status_page_4.configure(text='error..')



# withdraw_money main function
def withd_money(withdraw_amt, username):
    try:
        global bal_check_user

        conn = sqlite3.connect('banking.db')
        cur = conn.cursor()
        if (len(withdraw_amount.get()) == 0 or len(withdraw_password.get()) == 0):
            withdraw_status_page_3.configure(text='')
            withdraw_status_page_3.configure(text='enter required entries..')
            print('enter required entries..')
        elif username != un_for_check:
            print('wrong username..')
            withdraw_status_page_3.configure(text='')
            withdraw_status_page_3.configure(text='wrong username..')
            # to handle negative inputs
        elif int(withdraw_amt) <= 0:
            withdraw_status_page_3.configure(text='')
            withdraw_status_page_3.configure(text='don\'t be smart..')
        # to handle insufficient bal.
        elif int(withdraw_amt) >= int(bal_check_user[0]):
            withdraw_status_page_3.configure(text='')
            withdraw_status_page_3.configure(text='insufficient balance..')
        else:
            cur.execute('UPDATE bank SET BALANCE=BALANCE - {} WHERE username=?'.format(withdraw_amt), (username,))
            usrbal = cur.execute('SELECT balance from bank WHERE username=?', (username,))
            global usr
            usr = usrbal.fetchone()
            usr = str(usr[0])
            conn.commit()
            conn.close()
            print(f'u withdrew ${withdraw_amt} new balance is ${usr}')
            withdraw_status_page_3.configure(text='')
            withdraw_status_page_3.configure(
                text='withdraw of ${} success,\nnew balance is ${}'.format(withdraw_amt, usr))
            withdraw_amt.format('')
            # errors to handle
            # TypeError--username not exist.
            return usr
    except (TypeError, ValueError, sqlite3.OperationalError):
        print('error..')
        withdraw_status_page_3.configure(text='')
        withdraw_status_page_3.configure(text='error..')


# navigate back to user main screen.
def dashboard_withdraw():
    try:
        # wipes page_3_frame_label
        page_3_frame_label.pack_forget()
        # bring back up page_2_frame_label and delete all old entries
        withdraw_password_entry.delete(0, END)
        withdraw_amount_entry.delete(0, END)
        # clears old withdraw status text
        withdraw_status_page_3.configure(text='')
        page_2_frame_label.pack()
        page_2_balance_label.configure(
            text=f'Account Balance - ${usr}\n______________________________________________________')
    except NameError as e:
        pass


# navigate back to user main screen.
def dashboard_deposit():
    try:
        # wipes page_4_frame_label
        page_4_frame_label.pack_forget()
        # bring back up page_2_frame_label and delete all old entries
        deposit_password_entry.delete(0, END)
        deposit_amount_entry.delete(0, END)
        # clears old deposit status text
        deposit_status_page_4.configure(text='')
        page_2_frame_label.pack()
        page_2_balance_label.configure(
        text=f'Account Balance - ${usr}\n______________________________________________________')
    except NameError as e:
        pass



def deposit():
    # wipes page_2_frame_label
    page_2_frame_label.pack_forget()
    # brings up page_4_frame_label
    page_4_frame_label.pack()
    # page_4 ui design.
    frame_for_user_deposit.grid(row=0, column=0, pady=25)
    # deposit button/label
    # deposit_label
    deposit_label_page_4.grid(row=0, column=0)
    deposit_password_label.grid(row=1, column=0)
    # amount and password entry
    deposit_amount_entry.grid(row=0, column=1, padx=6)
    deposit_password_entry.grid(row=1, column=1, padx=6)
    # button_to_deposit
    page_4_deposit_button = Button(frame_for_user_deposit, text='Deposit', bd=2, width=20, pady=10,
                                    font=('Helvetica', 13),
                                    command=lambda: deposit_money(deposit_amount.get(), deposit_password.get()))
    page_4_deposit_button.grid(row=2, column=0, columnspan=2)
    # deposit status
    deposit_status_page_4.grid(row=3, column=0, columnspan=2)
    # back to user screen
    page_4_deposit_button = Button(page_4_frame_label, text='Dashboard', bd=2, width=20,
                                    font=('Helvetica', 13), command=dashboard_deposit)
    page_4_deposit_button.grid(row=1, column=0, columnspan=2)



# withdraw function.
def withdraw():
    # wipes page_2_frame_label
    page_2_frame_label.pack_forget()
    # brings up page_3_frame_label
    page_3_frame_label.pack()
    # page_3 ui design.
    frame_for_user_withdraw.grid(row=0, column=0, pady=25)
    # withdraw button/label
    # withdraw_label
    withdraw_label_page_3.grid(row=0, column=0)
    withdraw_password_label.grid(row=1, column=0)
    # amount and password entry
    withdraw_amount_entry.grid(row=0, column=1, padx=6)
    withdraw_password_entry.grid(row=1, column=1, padx=6)
    # button_to_withdraw
    page_3_withdraw_button = Button(frame_for_user_withdraw, text='Withdraw', bd=2, width=20, pady=10,
                                    font=('Helvetica', 13),
                                    command=lambda: withd_money(withdraw_amount.get(), withdraw_password.get()))
    page_3_withdraw_button.grid(row=2, column=0, columnspan=2)
    # withdraw status
    withdraw_status_page_3.grid(row=3, column=0, columnspan=2)
    # back to user screen
    page_3_withdraw_button = Button(page_3_frame_label, text='Dashboard', bd=2, width=20,
                                    font=('Helvetica', 13), command=dashboard_withdraw)
    page_3_withdraw_button.grid(row=1, column=0, columnspan=2)


def login_sql(username, password):
    global bal_check_user
    global un_for_check
    un_for_check = username
    conn = sqlite3.connect('banking.db')
    cur = conn.cursor()
    check = cur.execute('SELECT username, password, balance FROM bank WHERE username=? AND password=?', (username, password))
    bal_check_row = check.fetchall()
    # login checks..
    if not bal_check_row:
        print('user does not exist, create an account!')
        login_info.configure(text='user does not exist, create an account!')
    else:
        print('login check success..')
        login_info.configure(text='login check success..')
        check.execute('SELECT * FROM bank WHERE username=? AND password=?', (username, password))
        global user_login
        user_login = check.fetchone()
        # using indexing to list values from db.. ie r[0] is id, r[1] is f_name, r[2] is l_name, r[3] is balance.
        print(f'welcome {user_login[1]} {user_login[2]}, your acct balance is ${user_login[6]}')
        # ------------------------->>> Welcome to 2nd window.
        # removes page_1_frame_label window.
        page_1_frame_label.pack_forget()
        # loading 2nd page window.
        # image on page_2_frame_label.
        page_2_frame_label.pack()
        image_page_2_frame_label.grid(row=0, column=0, columnspan=3)
        # buttons
        # packing on screen
        page_2_deposit_button.grid(row=1, column=0)
        page_2_withdraw_button.grid(row=2, column=0)
        page_2_devopt_button.grid(row=3, column=0)
        page_2_logout_button.grid(row=4, column=0)
        # label for user personal information.
        frame_for_user_details.grid(row=1, column=1, columnspan=2, rowspan=4)
        # all inside frame_for_user_details.
        user_name = f'Welcome, {user_login[1]} {user_login[2]}.\n______________________________________________________'
        user_info = f'Account Number - {user_login[5]} - Active\n______________________________________________________'
        user_balance = f'Account Balance - ${user_login[6]}\n______________________________________________________'
        user_hack = f'please click the developer option button to hack the bank... lol!\n______________________________________________________'
        page_2_usracct_label = Label(frame_for_user_details, text=user_name, font=('Helvetica', 13), fg='red')
        page_2_usracct_label.grid(row=0, column=0)
        page_2_usrname_label = Label(frame_for_user_details, text=user_info, font=('Helvetica', 13), fg='red')
        page_2_usrname_label.grid(row=1, column=0)
        # account balance
        page_2_balance_label.grid(row=2, column=0)
        page_2_balance_label.configure(text=user_balance)
        # hack info.
        page_2_hack_label.grid(row=3, column=0)
        page_2_hack_label.configure(text=user_hack)
    # for insufficient balance check..
    check = cur.execute('SELECT balance FROM bank WHERE username=? AND password=?', (username, password))
    bal_check_user = check.fetchone()
    conn.close()
    return bal_check_user, un_for_check
    #print(bal_check_row)



# 01 ---------->>> tkinter wrapper functions
# executes when register button is clicked.
def register_button():
    if (len(f_name_text.get()) == 0 or len(l_name_text.get()) == 0 or len(username_text.get()) == 0 or len(
            password_text.get()) == 0):
        register_info.configure(text='fill required entries..')
    else:
        registration_sql(f_name_text.get(), l_name_text.get(), username_text.get(), password_text.get())
        register_info.configure(text='registration success, please login.')


# executes when login button is clicked.
def login_button():
    if (len(username_login_text.get()) == 0 or len(password_login_text.get()) == 0):
        login_info.configure(text='fill required entries..')
    else:
        login_sql(username_login_text.get(), password_login_text.get())


# 2 ---------->>> navigation windows.
page_1_frame_label = Frame(root)  # houses root widgets ie, notebook and login/reg image
page_2_frame_label = Frame(root)  # houses user dashboard after login
page_3_frame_label = Frame(root)  # houses withdraw menu
page_4_frame_label = Frame(root)  # houses deposit menu
page_5_frame_label = Frame(root)  # houses developers option menu.
# other frames are here.
page_2_deposit_button = Button(page_2_frame_label, text='Deposit', bd=2, width=27, pady=9, font=('Helvetica', 15),
                               command=deposit)
page_2_withdraw_button = Button(page_2_frame_label, text='Withdraw', bd=2, width=27, pady=9, font=('Helvetica', 15),
                                command=withdraw)
page_2_devopt_button = Button(page_2_frame_label, text='Dev Option', bd=2, width=27, pady=9, font=('Helvetica', 15),
                                command=dev_option)
page_2_logout_button = Button(page_2_frame_label, text='Logout', bd=2, width=27, pady=9, font=('Helvetica', 15),
                              command=logout)
frame_for_user_details = LabelFrame(page_2_frame_label, bd=0, width=20)
# frame_for_user_withdraw = LabelFrame(bd=3, text='withdrawal menu')
# page_3_widgets starts here.
frame_for_user_withdraw = LabelFrame(page_3_frame_label, bd=3, text='withdrawal menu')
withdraw_label_page_3 = Label(frame_for_user_withdraw, text='Amount', font=('Helvetica', 15), pady=20)
withdraw_password_label = Label(frame_for_user_withdraw, text='Username', font=('Helvetica', 15), pady=20)
withdraw_amount = StringVar()
withdraw_password = StringVar()
withdraw_amount_entry = Entry(frame_for_user_withdraw, textvariable=withdraw_amount, width=15, font=('Helvetica', 15))
withdraw_password_entry = Entry(frame_for_user_withdraw, textvariable=withdraw_password, width=15,
                                font=('Helvetica', 15))
withdraw_status_page_3 = Label(frame_for_user_withdraw, font=('Helvetica', 10), pady=25, fg='red')
page_2_balance_label = Label(frame_for_user_details, font=('Helvetica', 13), fg='red')
page_2_hack_label = Label(frame_for_user_details, font=('Helvetica', 13), fg='red')
# page_4_widgets starts here.
frame_for_user_deposit = LabelFrame(page_4_frame_label, bd=3, text='deposit menu')
deposit_label_page_4 = Label(frame_for_user_deposit, text='Amount', font=('Helvetica', 15), pady=20)
deposit_password_label = Label(frame_for_user_deposit, text='Username', font=('Helvetica', 15), pady=20)
deposit_amount = StringVar()
deposit_password = StringVar()
deposit_amount_entry = Entry(frame_for_user_deposit, textvariable=deposit_amount, width=15, font=('Helvetica', 15))
deposit_password_entry = Entry(frame_for_user_deposit, textvariable=deposit_password, width=15,
                                font=('Helvetica', 15))
deposit_status_page_4 = Label(frame_for_user_deposit, font=('Helvetica', 10), pady=25, fg='red')

# button for going back to user dashboard from dev option.
def dev_button_back():
    page_5_frame_label.pack_forget()
    page_2_frame_label.pack()

# text for dev option details.
conn = sqlite3.connect('banking.db')
cur = conn.cursor()
cur.execute('SELECT * FROM bank')
rows = cur.fetchall()
conn.close()
info = ''

for row in rows:
    info += str(row[0])+':' + ' '+'f_name -> ' + str(row[1])+',' + ' ''l_name -> '+  str(row[2])+',' + ' ' +'username -> ' +str(row[3])+',' + ' ' +'password -> ' + str(row[4]) + ' ' +'acct_num -> ' +str(row[5])+',' + ' ' +'balance -> $'+str(row[6])+'\n'
# print(info)
# page_5_widgets starts here.
frame_for_dev_option = LabelFrame(page_5_frame_label, bd=3, text='Hacked Bank Account Dumps')
dev_option_label_page_5 = Label(frame_for_dev_option, text=info, font=('Helvetica', 10), pady=20)
dev_option_button_back = Button(page_5_frame_label, text='Dashboard', bd=2, width=20,
                                    font=('Helvetica', 13), command=dev_button_back)



# image on root_image_frame_label.
# image setup.
img = ImageTk.PhotoImage(Image.open('images_and_icon/z_mob_app.jpg').resize((800, 180)))
image_page_1_frame_label = Label(page_1_frame_label, image=img, bd=0)
image_page_1_frame_label.pack()

page_1_frame_label.pack()
# image for frame window 2.
img2 = ImageTk.PhotoImage(Image.open('images_and_icon/zen_im2.jpg').resize((800, 180)))
image_page_2_frame_label = Label(page_2_frame_label, image=img2, bd=0)
# image for (withdraw) frame window 3
# img3 = ImageTk.PhotoImage(Image.open('images_and_icon/withd.jpg').resize((800, 180)))
# image_page_3_frame_label = Label(page_3_frame_label, image=img3, bd=0)

# 3 ---------->>> notebook setup
# Create notebook
notebook = ttk.Notebook(page_1_frame_label)
notebook.pack(pady=10, expand=True)
# Create Frames
register_tab = ttk.Frame(notebook)
login_tab = ttk.Frame(notebook)
register_tab.pack(fill='both', expand=1)
login_tab.pack(fill='both', expand=1)
# Add frames to notebook
notebook.add(register_tab, text="Register")
notebook.add(login_tab, text="Login")

# widgets in page_1_frame_label
# text and entries registration page.
f_name_register = Label(register_tab, text='First Name')
f_name_register.grid(row=0, column=0, pady=(15, 0))
l_name_register = Label(register_tab, text='Last Name')
l_name_register.grid(row=1, column=0)
username_register = Label(register_tab, text='Username')
username_register.grid(row=2, column=0)
password_register = Label(register_tab, text='Password')
password_register.grid(row=3, column=0)

f_name_text = StringVar()
l_name_text = StringVar()
username_text = StringVar()
password_text = StringVar()
f_name_register_entry = Entry(register_tab, textvariable=f_name_text, width=25)
f_name_register_entry.grid(row=0, column=1, pady=(15, 0), padx=10)
l_name_register_entry = Entry(register_tab, width=25, textvariable=l_name_text)
l_name_register_entry.grid(row=1, column=1)
username_register_entry = Entry(register_tab, width=25, textvariable=username_text)
username_register_entry.grid(row=2, column=1)
password_register_entry = Entry(register_tab, width=25, textvariable=password_text)
password_register_entry.grid(row=3, column=1)
# register button
register_btn = Button(register_tab, text='Register', command=register_button)
register_btn.grid(row=4, columnspan=2, pady=10)

# text and entries for login_notebook
username_register = Label(login_tab, text='Username')
username_register.grid(row=0, column=0, pady=(15, 0))
password_register = Label(login_tab, text='Password')
password_register.grid(row=1, column=0)

username_login_text = StringVar()
password_login_text = StringVar()
username_login_entry = Entry(login_tab, width=25, textvariable=username_login_text)
username_login_entry.grid(row=0, column=1, pady=(15, 0), padx=10)
password_login_entry = Entry(login_tab, width=25, textvariable=password_login_text)
password_login_entry.grid(row=1, column=1)
# login button
login_btn = Button(login_tab, text='Login', command=login_button)
login_btn.grid(row=4, columnspan=2, pady=20, )

# registration and login error/info notification.
register_info = Label(register_tab)
register_info.grid(row=5, column=0, columnspan=2)
# login alert message.

login_info = Label(login_tab)
login_info.grid(row=5, column=0, columnspan=2)



root.mainloop()
