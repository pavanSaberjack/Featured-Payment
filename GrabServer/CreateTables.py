import sqlite3

import Secret

SERVER_DB = 'server_database.db'

def create_tables():
    conn = sqlite3.connect(SERVER_DB)
    print("Opened database successfully")

    conn.execute('CREATE TABLE users (user_id INTEGER PRIMARY KEY,\
                                      user_name TEXT, \
                                      user_phone INTEGER, \
                                      user_upi TEXT)')

    conn.execute('CREATE TABLE sellers (seller_id INTEGER PRIMARY KEY,\
                                        seller_name TEXT, \
                                        seller_upi TEXT)')

    conn.execute('CREATE TABLE transactions (sno INTEGER PRIMARY KEY,\
                                            transaction_id TEXT, \
                                             txn_date timestamp, \
                                             money REAL, \
                                             seller_id INTEGER, \
                                             user_id INTEGER, \
                                             state INTEGER)')

    conn.execute('CREATE TABLE confirm_seller (s_no INTEGER PRIMARY KEY,\
                                               transaction_id TEXT, \
                                               user_phone INTEGER, \
                                               otp TEXT)')

    conn.execute('CREATE TABLE confirm_payment (s_no INTEGER PRIMARY KEY,\
                                                seller_id INTEGER, \
                                                user_phone INTEGER, \
                                                transaction_id TEXT, \
                                                otp TEXT)')

    print("Table created successfully")
    conn.close()

def add_users():
    conn = sqlite3.connect(SERVER_DB)
    cursorObj = conn.cursor()
    cursorObj.execute('INSERT INTO users (user_name, user_phone, user_upi) \
                  VALUES ("Prasad", {}, "prasad.ok@sbi")'.format(Secret.PRASAD_NUMBER))
    cursorObj.execute('INSERT INTO users (user_name, user_phone, user_upi) \
                  VALUES ("Ram", {}, "ram@hdfc")'.format(Secret.RAM_NUMBER))
    print('Added users successfully')
    conn.commit()
    conn.close()

def add_sellers():
    conn = sqlite3.connect(SERVER_DB)
    cursorObj = conn.cursor()
    cursorObj.execute('INSERT INTO sellers (seller_name, seller_upi) \
                  VALUES ("Kislay", "kislay@hdfc")')
    cursorObj.execute('INSERT INTO sellers (seller_name, seller_upi) \
                  VALUES ("Pavan", "pavan@boi")')
    print('Added sellers successfully')
    conn.commit()
    conn.close()

def display_table(table_name):
    conn = sqlite3.connect(SERVER_DB)
    cursorObj = conn.cursor()
    cursorObj.execute('SELECT * from {}'.format(table_name))
    rows = cursorObj.fetchall()
    print('Rows in table:')
    for row in rows:
        print(row)
    conn.close()

def display_users():
    display_table('users')

def display_sellers():
    display_table('sellers')


if __name__ == '__main__':
    create_tables()
    add_users()
    add_sellers()
    display_users()
    display_sellers()
