from flask import Flask, render_template, request, flash, redirect, url_for, current_app, send_from_directory
from flask_mail import Mail, Message
import re, os
from threading import Thread
from sheetsapi import Sheets

mail = Mail()

app = Flask(__name__)

app.secret_key = 'hey yarr'

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# 'MAIL_DEFAULT_SENDER' is the email of the sender
# replace ebsbcoordinator@iitbhilai.ac.in with the mail you want to send the notification of response from
app.config['MAIL_DEFAULT_SENDER'] = 'ebsbcoordinator@iitbhilai.ac.in'

# "MAIL_USERNAME" can be used same as 'MAIL_DEFAULT_SENDER'
# replace ebsbcoordinator@iitbhilai.ac.in with the mail you want to send the notification of response from
app.config["MAIL_USERNAME"] = 'ebsbcoordinator@iitbhilai.ac.in'

# "MAIL_PASSWORD" is the Password of the above email "MAIL_USERNAME"
# password of your mail provided
app.config["MAIL_PASSWORD"] = 'ebsb@iitbhilai1810'

# After you keep your mails in the following said places, follow this link
# https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html

mail = Mail(app)
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}([.]\w{2,3})*$'


@app.route("/", methods=['GET','POST'])
@app.route("/index", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg = request.form['message']
        if check(email):
            ''' To write to google sheets '''
            Sheets.createRow(name, email, msg)

            # follow this link to get the google sheets 've shared with you
            # https://docs.google.com/spreadsheets/d/1sgI5ASgksJjVIi2ZmP8_dqolSZrakKaddaJwt_oiWAM/edit#gid=0

            ''' To send email '''
            subject = "Mail sent from %s" % name

            # replace ebsbcoordinator@iitbhilai.ac.in with the mail you want to send the notification of response from
            to = 'ebsbcoordinator@iitbhilai.ac.in'
            send_email(to,subject,'email_temp.html',name,email,msg)

            subject2 = "Thank You"
            to2 = email
            send_email2(to2,subject2,'thanks.html',name)

            flash('Thanks for the Feedback.','success')
            return redirect(url_for('index'))
        else:
            flash('Please enter a valid email','danger')
            return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('index.html')


@app.route("/EBSB")
def EBSB():
    return render_template("EBSB.html")


@app.route("/Events")
def Events():
    return render_template("Events.html")


@app.route("/Team")
def Team():
    return render_template("Team.html")


def send_email1(msg):
    with app.app_context():
        mail.send(msg)


def check(email):
    if re.search(regex, email):
        return True
    else:
        return False


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


def send_async_email(app,msg):
       with app.app_context():
               mail.send(msg)


def send_email(to, subject, template, name, mail, message, **kwargs):
       msg = Message(subject, recipients=[to])
       msg.body = "Hello, this is {name} with my mail being <{mail}>.\nMy message for your team is: {message}".format(name=name,mail=mail,message=message)
       thr = Thread(target=send_async_email,args=[app,msg])
       thr.start()
       return thr


def send_email2(to, subject, template, name, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = 'Thank you {name}, for having your valuable time for us.\nNote: Replies to this email address are not ' \
               'monitored.\nFrom\nEBSB\nIIT Bhilai'.format(name=name)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


if __name__ == "__main__":
    app.run(debug=True)