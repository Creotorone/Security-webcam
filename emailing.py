import smtplib
from email.message import EmailMessage
from login_creds import PASSWORD
from login_creds import SENDER
from login_creds import RECEIVER


PASSWORD = PASSWORD
SENDER = SENDER
RECEIVER = RECEIVER

def send_email(image_path):
    email_message = EmailMessage()
    email_message['Subject'] = "New image"
    email_message.set_content("Someone arrived")

    with open(image_path, "rb") as file:
        content = file.read()
        email_message.add_attachment(content, maintype="image", subtype="png")

        gmail = smtplib.SMTP("smtp.gmail.com", 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login(SENDER, PASSWORD)
        gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
        gmail.quit()


if __name__ == "__main__":
    send_email(image_path)



