from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import pyrebase

message_body = " "
location = ['location', 'safe place']
number = None
safe_location = None
direction_image = None
app = Flask(__name__)

config = {
  "apiKey": "AIzaSyAFjbldaX_ZJw_yOLahlYJNFtlBbxP8hTg",
  "authDomain": "ngcode-9f40c.firebaseapp.com",
  "databaseURL": "https://ngcode-9f40c.firebaseio.com",
  "storageBucket": "ngcode-9f40c.appspot.com"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# Your Account SID from twilio.com/console
account_sid = "ACa1a69fdd06f6ad6e6c6078f9a5c0a929"
# Your Auth Token from twilio.com/console
auth_token  = "910a102592cf2e0145863c3b1e5242a9"

client = Client(account_sid, auth_token)
#
# message = client.messages.create(
#     to="+18582126620",
#     from_="+16193045612",
#     body="Alert: Zombies Incoming!")
#
# print(message.sid)

def sms():
    num = request.form['From']
    msg = request.form['Body']
    return num, msg

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming texts with a simple text message."""
    # Start our TwiML response
    number, message_body = sms()
    resp = MessagingResponse()
    msg_breakdown = message_body.split("//")
    data = {"address":  msg_breakdown[0], "city": msg_breakdown[1], "state": msg_breakdown[2], "zip": msg_breakdown[3], "country":  msg_breakdown[4], "numPeople":  msg_breakdown[5], "disaster":  msg_breakdown[6]}
    db.child("texts").child(number).push(data)
    safe_location = "Peterson, NY"
    direction_image = "https://debonair-shame-6855.twil.io/assets/test%20image.jpg"

    if "location" in message_body:
        msg = resp.message("You can go to " + safe_location + " for safety!")
        msg.media(direction_image)
    else:
        resp.message("Zombies are coming, RUN!")

    return str(resp)

if __name__ == "__main__":

    app.run(debug=True)
