import os
from openai import OpenAI
from pydantic import BaseModel


client = OpenAI()

class SentimentResponse(BaseModel):
    sentiment: str  #what sentiment is it? 3 options, positive, negative or neutral
    explanation: str

def analyze_sentiment(text):
    """
    Analyzes the sentiment of customer feedback.
    """
    prompt = f"""
    Analyze the following customer feedback and choose one of the following sentiment: 'positive', 'negative', or 'neutral'.
    
    Feedback: "{text}"
    
    Respond in JSON format with the keys: 'sentiment' and 'explanation'.
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a sentiment analysis assistant for a feeback system."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    import json
    result = json.loads(response.choices[0].message.content)
    return result

def generate_response(sentiment, customer_name):
    """
    Generates an appropriate response based on sentiment.
    """
    if sentiment == 'positive':
        return f"Hi {customer_name}! We're so glad you had a great experience. Would you mind sharing your feedback on Google? Here's the link: https://docs.google.com/forms/d/e/1FAIpQLSeiVvFtQE0JQiOnf2O5NWx9GZ1rDHyiv6N8b9REWmjXQWg7RA/viewform?usp=publish-editor"
    elif sentiment == 'negative':
        return f"Hi {customer_name}, we're very sorry to hear that. We've alerted our feedback team, and they will be calling you shortly to make things right. In the meantime, please use the discount code: HACKATHON for any future services"
    else:
        return f"Hi {customer_name}, thank you for your feedback! We're always looking to improve. Have a great day!"

if __name__ == "__main__":
    # Test
    test_feedback = "The service was amazing, the technician was very professional!"
    analysis = analyze_sentiment(test_feedback)
    print(f"Analysis: {analysis}")
    print(f"Response: {generate_response(analysis['sentiment'], 'John')}")
