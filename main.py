import database
import agent
import communication

def process_job_completion(customer_name, contact, job_type):
    """
    Step 1: Job is completed, send initial follow-up.
    """
    job_id = database.add_job(customer_name, contact, job_type)
    print(f"--- Job #{job_id} Completed for {customer_name} ---")
    
    initial_message = f"Hi {customer_name}, thanks for choosing us for your {job_type}! How was your experience? Please reply with your feedback."
    
    if "@" in contact:
        communication.send_email(contact, "How did we do?", initial_message)
    else:
        communication.send_sms(contact, initial_message)
    
    return job_id

def handle_customer_reply(job_id, feedback):
    """
    Step 2: Customer replies, analyze and route.
    """
    print(f"--- Handling Reply for Job #{job_id} ---")
    
    # Analyze sentiment
    analysis = agent.analyze_sentiment(feedback)
    sentiment = analysis['sentiment']
    
    # Update database
    database.update_feedback(job_id, feedback, sentiment)
    
    # Get customer info
    import sqlite3
    conn = sqlite3.connect('reputation.db')
    cursor = conn.cursor()
    cursor.execute('SELECT customer_name, customer_contact FROM jobs WHERE id = ?', (job_id,))
    customer_name, contact = cursor.fetchone()
    conn.close()
    
    # Generate and send response
    response_text = agent.generate_response(sentiment, customer_name)
    
    if "@" in contact:
        communication.send_email(contact, "Re: Your Feedback", response_text)
    else:
        communication.send_sms(contact, response_text)
        
    # If negative, alert owner
    if sentiment == 'negative':
        communication.alert_owner(job_id, customer_name, feedback)
        
    print(f"Action taken for {sentiment} sentiment.")

if __name__ == "__main__":
    # Initialize DB
    database.init_db()
    
    # Scenario 1: Positive Experience
    job_id_1 = process_job_completion("Alice Smith", "alice@example.com", "House Cleaning")
    handle_customer_reply(job_id_1, "The house looks amazing! Thank you so much.")
    
    print("\n" + "="*30 + "\n")
    
    # Scenario 2: Negative Experience
    job_id_2 = process_job_completion("Bob Jones", "+15551234567", "Plumbing Repair")
    handle_customer_reply(job_id_2, "The sink is still leaking and the plumber was late.")
