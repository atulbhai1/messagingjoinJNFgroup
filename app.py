import email, smtplib, ssl, sys
PROVIDERS = {
    "AT&T": {"sms": "txt.att.net", "mms": "mms.att.net", "mms_support": True},
    "Boost Mobile": {
        "sms": "sms.myboostmobile.com",
        "mms": "myboostmobile.com",
        "mms_support": True,
    },
    "C-Spire": {"sms": "cspire1.com", "mms_support": False},
    "Cricket Wireless": {
        "sms": "sms.cricketwireless.net ",
        "mms": "mms.cricketwireless.net",
        "mms_support": True,
    },
    "Consumer Cellular": {"sms": "mailmymobile.net", "mms_support": False},
    "Google Project Fi": {"sms": "msg.fi.google.com", "mms_support": True},
    "Metro PCS": {"sms": "mymetropcs.com", "mms_support": True},
    "Mint Mobile": {"sms": "mailmymobile.net", "mms_support": False},
    "Page Plus": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
    "Republic Wireless": {
        "sms": "text.republicwireless.com",
        "mms_support": False,
    },
    "Sprint": {
        "sms": "messaging.sprintpcs.com",
        "mms": "pm.sprint.com",
        "mms_support": True,
    },
    "Straight Talk": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
    "T-Mobile": {"sms": "tmomail.net", "mms_support": True},
    "Ting": {"sms": "message.ting.com", "mms_support": False},
    "Tracfone": {"sms": "", "mms": "mmst5.tracfone.com", "mms_support": True},
    "U.S. Cellular": {
        "sms": "email.uscc.net",
        "mms": "mms.uscc.net",
        "mms_support": True,
    },
    "Verizon": {"sms": "vtext.com", "mms": "vzwpix.com", "mms_support": True},
    "Virgin Mobile": {
        "sms": "vmobl.com",
        "mms": "vmpix.com",
        "mms_support": True,
    },
    "Xfinity Mobile": {
        "sms": "vtext.com",
        "mms": "mypixmessages.com",
        "mms_support": True,
    },
}
global number, provider, sender_credentials
def send_sms_via_email(number:str, message:str, provider:str, sender_credentials:tuple, subject:str="A person wants to join the JNF group!"):
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"
    print(email_message)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, email_password)
    server.sendmail(sender_email, receiver_email, email_message)
number = "5514270386"
provider = "Verizon"
sender_credentials = ("nitin.srinivasan@gmail.com", "xoskxonzlrfpbdxh")
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = '17bb05ad203765f49322692652f2bf6d761bf939885c0fc6'
@app.route('/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        contact = request.form['contact']
        print(fname, lname, contact)
        if not fname:
            flash('First Name is required')
        elif not lname:
            flash('Last Name Is Required')
        elif not contact:
            flash('Your Imessage-available Contact Is Required')
        else:
            message = f"{fname} {lname} wants to join JNF with {contact}"
            if len(message) > 160:
                flash("Sorry, please try to shorten your name and email to less than 135 characters.")
            else:
                send_sms_via_email(number=number, message=message, provider=provider, sender_credentials=sender_credentials)
                return redirect(url_for('success'))
    return render_template('signup.html')

# noinspection PyRedundantParentheses
@app.route('/success', methods=['GET'])
def success():
    return render_template('success.html')