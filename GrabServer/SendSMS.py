import Secret

from twilio.rest import Client

def service(message, to_phone_no):
    client = Client(Secret.TWILLIO_SID, Secret.TWILLIO_AUTH_TOKEN)
    to_phone = '+91' + str(to_phone_no)
    print('TOOOOOOOOOOOOOOOOO: ', to_phone)
    message = client.messages.create(
        to=to_phone,
        # from_='+919663269499',
        from_="+13038350658",
        body=message)
    print('SMS Message SENT: ', message.sid)