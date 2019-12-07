import sqlite3
import random
import time

import SendSMS
import Secret

SERVER_DB = 'server_database.db'
FAILURE = 'failure'
SUCCESS = 'success'

class Server:
    def __init__(self):
        self.conn = sqlite3.connect(SERVER_DB)
        self.cursorObj = self.conn.cursor()

    def get_seller_details(self, seller_id):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from sellers where seller_id == {}'.format(seller_id))
            seller_data = cursorObj.fetchall()
        if len(seller_data) != 1:
            return None
        return seller_data[0]

    def get_user_details_with_phone_no(self, phone_no):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from users where user_phone == {}'.format(phone_no))
            user_data = cursorObj.fetchall()
        if len(user_data) != 1:
            return None
        return user_data[0]

    def get_user_details(self, user_id):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from users where user_id == {}'.format(user_id))
            user_data = cursorObj.fetchall()
        if len(user_data) != 1:
            return None
        return user_data[0]

    def merchant_initiate_payment(self, money, seller_id, user_phone):
        seller = self.get_seller_details(seller_id)
        if seller is None:
            return {'status': FAILURE, 'message': 'No seller exists'}
        user = self.get_user_details_with_phone_no(user_phone)
        if user is None:
            return {'status': FAILURE, 'message': 'No user exists'}

        # Create transaction entry
        txn_date = int(time.time())
        transaction_id = str(txn_date)
        state = 0
        values_str = '"{}", {}, {}, {}, {}, {}'.format(transaction_id, txn_date, money,
                                                     seller['seller_id'], user['user_id'], state)
        otp = ':06d'.format(random.randint(0, 999999))
        with sqlite3.connect(SERVER_DB) as conn:
            cursorObj = conn.cursor()
            cursorObj.execute('INSERT INTO transactions (transaction_id, txn_date, money, seller_id, user_id, \
                                state) VALUES ({})'.format(values_str))
            cursorObj.execute('INSERT INTO confirm_seller (transaction_id, otp) VALUES ("{}", \
                                "{}")'.format(transaction_id, otp))
            conn.commit()


        message_to_user = '{} is requesting {} Rs. SMS {} to {} to confirm your request'.format(
                            seller['seller_name'], money, otp, Secret.GRAB_CONFIRM_NUMBER)
        SendSMS.service(message_to_user, user_phone)

        return {'status': SUCCESS, 'message': 'ok'}
