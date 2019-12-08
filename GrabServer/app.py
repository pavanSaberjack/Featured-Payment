from flask import Flask, request
from Server import Server

app = Flask(__name__)
server = Server()

@app.route('/initiate_payment', methods=['POST'])
def initate_payment():
    print(request.form)
    money = float(request.form['money'])
    seller_id = int(request.form['seller_id'])
    user_phone = int(request.form['user_phone'])
    message = server.merchant_initiate_payment(money, seller_id, user_phone)
    return message

@app.route('/confirm_seller', methods=['POST'])
def confirm_seller():
    otp = request.form['otp']
    user_phone = int(request.form['user_phone'])
    message = server.confirm_merchant_otp(otp, user_phone)
    return message

@app.route('/confirm_bank_otp', methods=['POST'])
def confirm_bank_otp():
    otp = request.form['otp']
    user_phone = int(request.form['user_phone'])
    message = server.confirm_bank_otp(otp, user_phone)
    return message

@app.route('/merchant_confirm_transaction', methods=['POST'])
def merchant_confirm_transaction():
    otp = request.form['otp']
    user_phone = int(request.form['user_phone'])
    seller_id = int(request.form['seller_id'])
    message = server.merchant_confirm_transaction(otp, user_phone, seller_id)
    return message


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3679)
    app.run(host='0.0.0.0', port=8080, debug=True)