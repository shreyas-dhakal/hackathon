import os
from twilio.rest import Client

# Mocking communication for demo

def send_sms(to_number, message):
    """
    Sends an SMS using Twilio.
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')
    
    if account_sid and auth_token and from_number:
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message,
                from_=from_number,
                to=to_number
            )
            print(f"SMS sent to {to_number}: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending SMS: {e}")
            return False
    else:
        print(f"[MOCK SMS] To: {to_number} | Message: {message}")
        return True

def send_email(to_email, subject, body):
    """
    Sends an email using a mock approach.
    """
    # use smtplib or something in other time.
    print(f"[MOCK EMAIL] To: {to_email} | Subject: {subject} | Body: {body}")
    return True

def alert_owner(job_id, customer_name, feedback):
    """
    Alerts the business owner about a negative experience.
    """
    owner_email = "owner@business.com"
    subject = f"URGENT: Negative Feedback - Job #{job_id}"
    body = f"Customer {customer_name} left negative feedback: '{feedback}'. Please follow up immediately."
    send_email(owner_email, subject, body)
    print(f"Owner alerted for Job #{job_id}")
