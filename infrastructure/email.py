import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(receiver, header, message, file1, file2,
               host, sender, password, port, encrypt_type,
               name_file1, name_file2):
    try:
        subject = header
        body = message
        sender_email = sender
        receiver_email = receiver
        password = password

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Open PDF file in binary mode

        part = MIMEBase("application", "octet-stream")
        part.set_payload(file1)

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= " + name_file1
        )

        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(file2)

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part2)

        # Add header as key/value pair to attachment part
        part2.add_header(
            "Content-Disposition",
            f"attachment; filename= " + name_file2
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        message.attach(part2)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(host, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
        return {'message': 'email sent successfully'}

    except Exception as e:
        return {'error': str(e)}