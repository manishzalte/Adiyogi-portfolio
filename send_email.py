from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

# Email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "rohitvijaymahajan1998@gmail.com"
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

def send_email(name, email, project_type, message):
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = SENDER_EMAIL  # Sending to yourself
        msg['Subject'] = f"New Project Proposal from {name}"

        # Create email body
        body = f"""
        New Project Proposal Details:
        
        Name: {name}
        Email: {email}
        Project Type: {project_type}
        
        Message:
        {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True, "Email sent successfully"
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False, str(e)

@app.route('/send-proposal', methods=['POST'])
def handle_proposal():
    try:
        data = request.get_json()
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        project_type = data.get('project_type')
        message = data.get('message')
        
        # Validate required fields
        if not all([name, email, project_type, message]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Send email
        success, message = send_email(name, email, project_type, message)
        
        if success:
            return jsonify({'message': 'Proposal sent successfully'}), 200
        else:
            return jsonify({'error': f'Failed to send email: {message}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not EMAIL_PASSWORD:
        print("Warning: EMAIL_PASSWORD environment variable is not set")
        print("Please set it using: export EMAIL_PASSWORD='your-app-password'")
    app.run(debug=True) 