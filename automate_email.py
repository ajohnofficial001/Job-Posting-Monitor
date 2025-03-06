import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# SMTP Server Configuration
smtp_server = "smtp.gmail.com"  
smtp_port = 587                 # TLS port
smtp_user = "jadeyemo004@gmail.com"   
smtp_password = "mkhb urih jmub kety"  #mkhb urih jmub kety  password 

# Email Details
from_email = smtp_user
to_email = "john.adeyemo@bulldogs.aamu.edu"
subject = "Test Email with CSV Attachments"
body = "Hello,\n\nPlease find the attached CSV files.\n\nBest regards,\nJohn"

# Attachments (CSV files)
file1 = "indeed_jobs.csv"
file2 = "linkedin_jobs.csv"


# Create Email
msg = MIMEMultipart()
msg["From"] = from_email
msg["To"] = to_email
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain"))

# Function to Attach Files
def attach_file(msg, filename):
    try:
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)
    except Exception as e:
        print(f"Error attaching {filename}: {e}")

# Attach CSV
attach_file(msg, file1)
attach_file(msg, file2)

# Send Email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(smtp_user, smtp_password)
    server.sendmail(from_email, to_email, msg.as_string())
    print("Email sent successfully with attachments!")
except Exception as e:
    print(f"Error sending email: {e}")
finally:
    server.quit()