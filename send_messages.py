import requests
import time

def send_messages(image_url):
    """
    Sends a message with an image URL to a specified notification service.

    Parameters:
        image_url (str): The URL of the image to include in the message.
    """
    # Unique identifier for the notification service
    id = 't0yPSmH'
    
    # Construct the message text with the provided image URL
    message_text = f"Today's exercise and rehabilitation status: {image_url}"
    print(f"Sending message: {message_text}")
    
    # Timestamp for the message to avoid duplicate issues or for logging
    timestamp = str(time.time())
    
    # Desired response format for the request
    response_format = 'json'
    
    # Endpoint URL for the notification service
    request_url = "http://miaotixing.com/trigger?"
    
    # HTTP headers to mimic a web browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'
    }
    
    # Data payload for the POST request
    payload = {
        'id': id,
        'text': message_text,
        'ts': timestamp,
        'type': response_format
    }
    
    # Making the HTTP POST request to send the message
    try:
        response = requests.post(request_url, params=payload, headers=headers)
        print(f"Message sent successfully: {response.text}")
    except requests.RequestException as e:
        print(f"Failed to send message: {str(e)}")

# Example usage of the function
if __name__ == "__main__":
    image_url = "http://example.com/path/to/image.jpg"
    send_messages(image_url)
