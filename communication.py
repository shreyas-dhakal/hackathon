import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, subject, body):
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        print("[MOCK EMAIL] Missing credentials")
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print(f"Email sent to {to_email}")
        return True

    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_sms(phone_number, message):
    """
    Send SMS message (mock implementation).
    In production, you would integrate with Twilio or similar service.
    """
    print(f"[MOCK SMS] Message sent to {phone_number}: {message}")
    return True

def alert_owner(job_id, customer_name, feedback):
    """
    Alert the business owner about negative feedback.
    """
    owner_email = os.environ.get("SENDER_EMAIL")
    if owner_email:
        subject = f"[URGENT] Negative Feedback - Job #{job_id}"
        body = f"Customer {customer_name} left negative feedback:\n\n{feedback}"
        send_email(owner_email, subject, body)
    else:
        print(f"[ALERT] Could not notify owner - no email configured")
