from flask import Flask, request
from Server import Server

app = Flask(__name__)
server = Server()

@app.route('/initiate_payment', methods=['POST'])
def initate_payment():
    money = float(request.form['money'])
    seller_id = int(request.form['seller_id'])
    user_phone = int(request.form['user_phone'])
    message = server.merchant_initiate_payment(money, seller_id, user_phone)
    return message

if __name__ == '__main__':
   app.run(debug=True)