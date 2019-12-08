import sqlite3
import random
import time
import requests

import SendSMS
import Secret

SERVER_DB = 'server_database.db'
FAILURE = 'failure'
SUCCESS = 'success'

BANK_URL = 'http://localhost:6532'

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
        otp = '111111'  # DELETE
        with sqlite3.connect(SERVER_DB) as conn:
            cursorObj = conn.cursor()
            cursorObj.execute('INSERT INTO transactions (transaction_id, txn_date, money, seller_id, user_id, \
                                state) VALUES ({})'.format(values_str))
            cursorObj.execute('INSERT INTO confirm_seller (transaction_id, user_phone, otp) VALUES ("{}", \
                                {}, "{}")'.format(transaction_id, user_phone, otp))
            conn.commit()


        message_to_user = '{} is requesting {} Rs. SMS {} to {} to confirm your request'.format(
                            seller['seller_name'], money, otp, Secret.GRAB_CONFIRM_NUMBER)
        SendSMS.service(message_to_user, user_phone)

        return {'status': SUCCESS, 'message': 'ok'}

    def confirm_merchant_otp(self, otp, user_phone):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()
            cursorObj.execute('SELECT * from confirm_seller where user_phone == {}'.format(user_phone))
            user_data = cursorObj.fetchall()

            if len(user_data) == 0:
                return {'status': FAILURE, 'message': 'No seller has requested payment'}
            transaction_data = max(user_data, key=lambda x:x['transaction_id'])
            if transaction_data['otp'] != otp:
                return {'status': FAILURE, 'message': 'OTP has failed'}

            transaction_id = transaction_data['transaction_id']
            cursorObj.execute('DELETE FROM confirm_seller WHERE transaction_id == "{}"'.format(transaction_id))
            conn.commit()

            cursorObj.execute('SELECT * FROM transactions WHERE transaction_id == "{}"'.format(transaction_id))
            rows = cursorObj.fetchall()
            if len(rows) != 1:
                return {'status': FAILURE, 'message': 'Transaction is missing'}

            cursorObj.execute('UPDATE transactions SET state=1 where transaction_id == "{}"'.format(transaction_id))
            conn.commit()

        transaction = rows[0]
        bank_url = BANK_URL + '/initiate_bank_payment'
        body = {'money': transaction['money'], 'seller_id': transaction['seller_id'],
                'user_id': transaction['user_id']}

        response = requests.post(bank_url, data=body)
        return response.json()

    def confirm_bank_otp(self, otp, user_phone):
        bank_url = BANK_URL + '/confirm_bank_otp'
        body = {'otp': otp, 'user_phone': user_phone}
        response = requests.post(bank_url, data=body).json()

        if response['status'] == FAILURE:
            return response

        user_data = self.get_user_details_with_phone_no(user_phone)
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()

            cursorObj.execute('SELECT * FROM transactions WHERE user_id == {}'.format(user_data['user_id']))
            rows = cursorObj.fetchall()
            if len(rows) == 0:
                return {'status': FAILURE, 'message': 'Transaction is missing'}
            transaction = max(rows, key=lambda x: x['txn_date'])

            cursorObj.execute('UPDATE transactions SET state=2 where '
                              'transaction_id == "{}"'.format(transaction['transaction_id']))

            otp = '{:06d}'.format(random.randint(1, 999999))
            otp = '333333'     # DELETE
            cursorObj.execute('INSERT INTO confirm_payment (seller_id, transaction_id, user_phone, otp) '
                              'VALUES ({}, "{}", {}, "{}")'.format(transaction['seller_id'],
                                                                   transaction['transaction_id'],
                                                                   user_phone, otp))
            conn.commit()

        sms = 'You have successfully performed transaction. Say the number {} to the seller'.format(otp)
        SendSMS.service(sms, user_phone)

        return {'status': SUCCESS, 'message': 'Ok'}

    def merchant_confirm_transaction(self, otp, user_phone, seller_id):
        with sqlite3.connect(SERVER_DB) as conn:
            conn.row_factory = sqlite3.Row
            cursorObj = conn.cursor()

            cursorObj.execute('SELECT * FROM confirm_payment WHERE seller_id == {} AND '
                              'user_phone == {} AND otp == "{}"'.format(seller_id, user_phone, otp))
            rows = cursorObj.fetchall()
            if len(rows) == 0:
                return {'status': FAILURE, 'message': 'No transaction has happened'}
            rows = max(rows, key=lambda x: x['s_no'])

            cursorObj.execute('DELETE FROM confirm_payment WHERE s_no == {}'.format(rows['s_no']))
            conn.commit()

        return {'status': SUCCESS, 'message': 'Ok'}