import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ReportEmail:
    """
    The class used for sending out the report email. Used to create the mail client, build an
    email message using a premade HTML string, and send it. 
    """

    def __init__(self, sender_email, password, recipients, subject):
        """
        Initialize all fields necessary for sending the emails.

        Args:
            sender_email (str): The gmail client's full email address
            password (str): The app password from the gmail client
            recipients ([str]): The list of recipient for the email
            subject (str): The subject line for the email
        """
        self.sender_email = sender_email
        self.password = password

        self.recipients = recipients

        self.subject = subject

    def create_message(self, html):
        """
        Builds out the actual email object by completing these steps:
        1. Populate out the subject, sender, and recipient
        2. Take the full html string that will be send in the email and add it to the message
        
        The message is a MIMEMultipart object to allow for future expansion to the report's content

        Args:
            html (str): A complete HTML string that will be displayed in the email
        """
        self.message = MIMEMultipart("alternative")

        self.message["Subject"] = self.subject
        self.message["From"] = self.sender_email
        self.message["To"] = ", ".join(self.recipients)

        # Turn these into plain/html MIMEText objects
        htmlMessage = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        self.message.attach(htmlMessage)

    def send_message(self):
        """
        Send the completed message object to the predefined recipients. Must be called after 
        create_message, unless the message object will not exist, and the script will fail
        """
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                self.sender_email, self.recipients, self.message.as_string()
        )