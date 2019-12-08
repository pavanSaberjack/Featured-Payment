from flask import Flask, request
from Server import Server

app = Flask(__name__)
server = Server()


@app.route('/initiate_bank_payment', methods=['POST'])
def initate_bank_payment():
    money = float(request.form['money'])
    seller_id = int(request.form['seller_id'])
    user_id = int(request.form['user_id'])
    message = server.initiate_bank_request(seller_id, user_id, money)
    return message

@app.route('/confirm_bank_otp', methods=['POST'])
def confirm_bank_otp():
    otp = request.form['otp']
    user_phone = int(request.form['user_phone'])
    message = server.confirm_bank_otp(otp, user_phone)
    return message


if __name__ == '__main__':
   app.run(debug=True, port=6532)