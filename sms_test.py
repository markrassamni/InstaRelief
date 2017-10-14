from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import pyrebase


# test
message_body = " "
locations = ['location', 'safe place']
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

    # If text is from app, else from user seeking help
    msg_size = len(msg_breakdown)
    if msg_size == 7: # Check if user altered the message
        data = {"address":  msg_breakdown[0], "city": msg_breakdown[1], "state": msg_breakdown[2], "zip": msg_breakdown[3], "country":  msg_breakdown[4], "numPeople":  msg_breakdown[5], "disaster":  msg_breakdown[6]}
        db.child("texts").child(number).push(data)
        msg = resp.message("Thank you for sharing your information. Here is a map with details"
                     " including dangers around you and where to find help! Please refer to our app"
                     " for any other information needed! -InstaRelief")

        for cities in db.child('Images').get().each():
                for url in cities.val():
                    if url == 'url':
                        img = cities.val()['url']
        msg.media(img)
    else:
        resp.message("We are sorry, we cannot process your information at this time. Please try"
                     " resubmitting without altering the output text. -InstaRelief")

        # safe_location = "Peterson, NY"
        # direction_image = "https://debonair-shame-6855.twil.io/assets/test%20image.jpg"
        #
        # if any(i in message_body for i in locations):
        #     msg = resp.message("You can go to " + safe_location + " for safety!")
        #     msg.media(direction_image)
        # else:
        #     resp.message("Zombies are coming, RUN!")

    return str(resp)

if __name__ == "__main__":

    app.run(debug=True)
