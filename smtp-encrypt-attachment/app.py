# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from virtru_tdf3_python import Client, Policy, EncryptFileParam, LogLevel,Protocol

# SMTP Variables
smtp_from_address = "sender@example.com"
smtp_to_address = "to.recipient@domain.com"

# Virtru Variables
virtru_appid = "appid"
virtru_owner = "sender@example.com"

# File Variables
file_name_tdf = "helloworld.txt.tdf3.html"
file_path_plain="/tmp/helloworld.txt"
file_path_tdf="/tmp/helloworld.txt.tdf3.html"


# Virtru Encryption
client = Client(owner=virtru_owner, app_id=virtru_appid)
policy = Policy()
policy.share_with_users([smtp_to_address])
param = EncryptFileParam(in_file_path=file_path_plain,
                         out_file_path=file_path_tdf)
param.set_policy(policy)
client.encrypt_file(encrypt_file_param=param)

# Email
msg = MIMEMultipart()
msg['From'] = smtp_from_address
msg['To'] = smtp_to_address
msg['Subject'] = "Test Email"
body = "Message Body"
msg.attach(MIMEText(body, 'plain'))
attachment = open(file_name_tdf, "rb")
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
attachment_disposition = "attachment; filename= {}".format(file_name_tdf)
p.add_header('Content-Disposition', attachment_disposition)
msg.attach(p)
s = smtplib.SMTP('smtp-relay.gmail.com', 587)
s.starttls()
text = msg.as_string()
s.sendmail(smtp_from_address, smtp_to_address, text)
s.quit()
