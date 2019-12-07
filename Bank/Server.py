import sqlite3
import time
import random

import Secret
import SendSMS

SERVER_DB = 'bank_database.db'
FAILURE = 'failure'
SUCCESS = 'success'

class Server:
    def __init__(self):
        pass

    def get_seller_details(self, seller_id):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from sellers where seller_id == {}'.format(seller_id))
            seller_data = cursorObj.fetchall()
        if len(seller_data) != 1:
            return None
        return seller_data[0]

    def get_user_details(self, user_id):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from users where user_id == {}'.format(user_id))
            user_data = cursorObj.fetchall()
        if len(user_data) != 1:
            return None
        return user_data[0]

    def get_user_details_with_phone_no(self, phone_no):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from users where user_phone == {}'.format(phone_no))
            user_data = cursorObj.fetchall()
        if len(user_data) != 1:
            return None
        return user_data[0]

    def initiate_bank_request(self, seller_id, user_id, money):
        seller = self.get_seller_details(seller_id)
        if seller is None:
            return {'status': FAILURE, 'message': 'No seller exists'}
        user = self.get_user_details(user_id)
        if user is None:
            return {'status': FAILURE, 'message': 'No user exists'}

        # Create transaction entry
        txn_date = int(time.time())
        transaction_id = str(txn_date)
        state = 1
        values_str = '"{}", {}, {}, {}, {}, {}'.format(transaction_id, txn_date, money,
                                                       seller['seller_id'], user['user_id'], state)
        otp = ':06d'.format(random.randint(0, 999999))
        otp = '222222'  # DELETE
        user_phone = user['user_phone']
        with sqlite3.connect(SERVER_DB) as conn:
            cursorObj = conn.cursor()
            cursorObj.execute('INSERT INTO transactions (transaction_id, txn_date, money, seller_id, user_id, \
                                        state) VALUES ({})'.format(values_str))
            cursorObj.execute('INSERT INTO confirm_payment (transaction_id, user_phone, otp) VALUES ("{}", \
                                        {}, "{}")'.format(transaction_id, user_phone, otp))
            conn.commit()

        message_to_user = '{} is requesting {} Rs. SMS {} to {} to confirm your request'.format(
            seller['seller_name'], money, otp, Secret.BANK_CONFIRM_NUMBER)
        SendSMS.service(message_to_user, user_phone)

        return {'status': SUCCESS, 'message': 'ok'}

    def confirm_bank_otp(self, otp, user_phone):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from confirm_payment where user_phone == {}'.format(user_phone))
            user_data = cursorObj.fetchall()

            if len(user_data) == 0:
                return {'status': FAILURE, 'message': 'No bank has requested payment'}
            transaction_data = max(user_data, key=lambda x: x['transaction_id'])
            if transaction_data['otp'] != otp:
                return {'status': FAILURE, 'message': 'OTP has failed'}

            transaction_id = transaction_data['transaction_id']
            cursorObj.execute('DELETE FROM confirm_payment WHERE transaction_id == "{}"'.format(transaction_id))
            conn.commit()

            cursorObj.execute('SELECT * FROM transactions WHERE transaction_id == "{}"'.format(transaction_id))
            rows = cursorObj.fetchall()
            if len(rows) != 1:
                return {'status': FAILURE, 'message': 'Transaction is missing'}
            transaction = rows[0]

            cursorObj.execute('SELECT * from users where user_id == {}'.format(transaction['user_id']))
            user_data = cursorObj.fetchall()
            if len(user_data) != 1:
                return {'status': FAILURE, 'message': 'User doesnt have account in bank'}
            user_data = user_data[0]

            if user_data['balance'] < transaction['money']:
                return {'status': FAILURE, 'message': 'Insufficient balance'}

            balance = user_data['balance'] - transaction['money']
            cursorObj.execute('UPDATE users SET balance={} where user_id == {}'.format(balance, user_data['user_id']))
            cursorObj.execute('UPDATE transactions SET state=2 where transaction_id == "{}"'.format(transaction_id))
            conn.commit()

        return {'status': SUCCESS, 'message': 'Ok'}
