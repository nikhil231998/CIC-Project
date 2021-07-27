import smtplib
import email.utils
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import json

# Replace sender@example.com with your "From" address.
# This address must be verified.
SENDER = 'awscic2021@gmail.com'
SENDERNAME = 'Australia Post'
SENDERPASSWORD = 'AwsCIC2021'
SMTP_SERVER = "imap.gmail.com"

# Replace recipient@example.com with a "To" address. If your account
# is still in the sandbox, this address must be verified.
RECIPIENT  = 'nikhilsharma23198@gmail.com'

# Replace smtp_username with your Amazon SES SMTP user name.
USERNAME_SMTP = "AKIAY3LKA7OHSKM3B7A2"

# Replace smtp_password with your Amazon SES SMTP password.
PASSWORD_SMTP = "BG9eHMRgtjRz94lGxYhpaLAycqNKud/OKdpHv3QoPZf7"

# (Optional) the name of a configuration set to use for this message.
# If you comment out this line, you also need to remove or comment out
# the "X-SES-CONFIGURATION-SET:" header below.
CONFIGURATION_SET = "TrackEmailConfigurationSet"

# If you're using Amazon SES in an AWS Region other than US West (Oregon),
# replace email-smtp.us-west-2.amazonaws.com with the Amazon SES SMTP
# endpoint in the appropriate region.
HOST = "email-smtp.ap-southeast-2.amazonaws.com"
PORT = 587

# The subject line of the email.
SUBJECT = 'Parcel Received'

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("You have received a parcel from australia post\r\n"
            )

# The HTML body of the email.
BODY_HTML = """<html>
<head></head>
<body>
  <h1>You have received a parcel from australia post</h1>
  <p>Click 
    <a href='https://www.python.org/'>here</a>
    to track your order</p>
</body>
</html>
            """

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = SUBJECT
msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
msg['To'] = RECIPIENT
# Comment or delete the next line if you are not using a configuration set
msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(BODY_TEXT, 'plain')
part2 = MIMEText(BODY_HTML, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Try to send the message.
try:
    server = smtplib.SMTP(HOST, PORT)
    server.ehlo()
    server.starttls()
    #stmplib docs recommend calling ehlo() before & after starttls()
    server.ehlo()
    server.login(USERNAME_SMTP, PASSWORD_SMTP)
    # server.sendmail(SENDER, RECIPIENT, msg.as_string())
    server.close()
# Display an error message if something goes wrong.
except Exception as e:
    print ("Error: ", e)
else:
    print ("Email sent!")

list = []

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(SENDER,SENDERPASSWORD)
        mail.select('inbox')

        data = mail.search(None, 'ALL')
        mail_ids = data[1]
        id_list = mail_ids[0].split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id,first_email_id-1, -1):
            data = mail.fetch(str(i), '(RFC822)' )
            for response_part in data:
                arr = response_part[0]
                if isinstance(arr, tuple):
                    msg = email.message_from_string(str(arr[1],'utf-8'))
                    msgFinal = msg.get_payload(None, True)
                    dataTest = msgFinal.decode('utf-8')
                    data = json.loads(dataTest)
                    msgFinal_message = json.loads(data['Message'])
                    msgFinal_mail = msgFinal_message['mail']
                    timestamp = msgFinal_mail['timestamp']
                    mail_id = msgFinal_mail['destination'][0]
                    list.append((timestamp, mail_id))

    except Exception as e:
        traceback.print_exc()
        print(str(e))

read_email_from_gmail()

for i in list:
    print(i[0])
    print(i[1])